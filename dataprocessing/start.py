from qtgui.mainWindow import start as startApp
import subprocess

def start_mongodb():
    subprocess.Popen(['mongodb/bin/mongod', '--dbpath', "mongodb/data/db"])


start_mongodb()
startApp()