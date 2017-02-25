from qtgui.mainWindow import start as startApp
import os
import subprocess


def start_mongodb():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(['mongodb/bin/mongod', '--dbpath', "mongodb/data/db"], startupinfo=startupinfo)


if 'DEVELOPMENT' in os.environ:
    mongo = None
else:
    mongo = start_mongodb()
startApp(mongo)