#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we show how to
use the Listbox widget.

author: Jan Bodar
last modified: December 2010
website: www.zetcode.com
"""



from ttk import Frame, Label, Style, Button
from Tkinter import Tk, BOTH, Listbox, StringVar, END
import guitool.combineTool as CombineTool

class Application(Frame):

    callback = None
    errorList = {}
    xmlroot = None
    currentSelection = None
    def __init__(self, parent, errorlist, xmlroot, callback):
        Frame.__init__(self, parent)
        self.errorList = errorlist
        self.xmlroot = xmlroot
        self.callback = callback
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.master.protocol("WM_DELETE_WINDOW", self.closeHandler)
        self.parent.title("Listbox")

        self.pack(fill=BOTH, expand=1)


        lb = Listbox(self)
        lb.config(width=150, height=15)
        for key, value in self.errorList.iteritems():
            lb.insert(END, (str(key) + " " + str(len(value))))

        lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.place(x=20, y=20)

        okb = Button(self, text="OK", command=self.gotoEdit)
        okb.place(x=20, y = 300)

    def gotoEdit(self):
        print "Start tool..."
        self.master.withdraw()
        CombineTool.startGUI(self.currentSelection, self.xmlroot, self.callbackEdit)
        print "back"



    def callbackEdit(self):
        self.master.deiconify()

    def onSelect(self, val):

        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        value = value.partition(' ')[0]
        self.currentSelection = self.errorList[value]
        print self.currentSelection

    def closeHandler(self):
        print "close groupselection"
        self.quit()
        self.master.destroy()
        self.callback(self.xmlroot)

def startGUI(errorList, xmlroot, callback):
    root = Tk()
    ex = Application(root, errorList, xmlroot, callback)
    root.geometry("500x500+300+300")
    root.mainloop()

    #root.destroy()