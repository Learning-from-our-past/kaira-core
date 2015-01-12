#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this program, we use the
tkFileDialog to select a file from
a filesystem.

author: Jan Bodar
last modified: January 2011
website: www.zetcode.com
"""


from Tkinter import Frame, Tk, BOTH, Text, Menu, END, Label
import tkFileDialog
from Tkinter import *
import Tkinter, time, threading
import re
import processData
import guitool.groupSelection as GUITool



class Example(Frame):

    file = ""
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.label = Label(self, text="Select XML-file to load.")
        self.label.pack()

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.onOpen()


    def onOpen(self):
        ftypes = [('Xml files', '*.xml'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            #self.master.destroy()
            self.label.config(text="Loading and analyzing. Results will be saved in CSV and problematic entries shown. Please wait...")

            #load the file and run analysis on different thread
            done = []
            def call():
                result = processData.startProcess(fl[0:len(fl)-4], self.endLoading)
                done.append(result)
            thread = threading.Thread(target = call)
            thread.start() # start parallel computation
            while thread.is_alive():
                # code while computing
                self.update()
                time.sleep(0.001)

            #fire up the fixing tool:
            ###############################################################
            print "Start error fix tool..."
            self.file = done[0]["file"]
            self.master.withdraw()
            GUITool.startGUI(done[0]["errors"], done[0]["root"], self.saveresults)

            self.label["text"] = "Changes saved to the file " + self.file

            print "muutokset loppu"


    def saveresults(self, root):
        self.master.deiconify()
        processData.saveModificationsToFile(self.file, root)

    def endLoading(self):
        self.master.destroy()

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read().decode('utf8')
        return text


def main():

    root = Tk()
    ex = Example(root)
    #root.geometry("300x250+300+300")
    root.mainloop()



if __name__ == '__main__':
    main()
