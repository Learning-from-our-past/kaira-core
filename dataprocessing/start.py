from qtgui.mainWindow import start as startApp
import subprocess


def start_mongodb():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(['mongodb/bin/mongod', '--dbpath', "mongodb/data/db"], startupinfo=startupinfo)



mongo = start_mongodb()
startApp(mongo)