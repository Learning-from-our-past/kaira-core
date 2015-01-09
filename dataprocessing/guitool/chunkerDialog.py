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


from Tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkFileDialog
import re

class Example(Frame):

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

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.onOpen()


    def onOpen(self):

        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            #self.txt.insert(END, text)
            self.chunkTextFile(text, fl)

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read().decode('utf8')
        return text

    def chunkTextFile(self, text, filename):
        #remove <>& characters
        text = re.sub(r"(?:<|>|&)", r"", text)

        #tag stuff:
        text = re.sub(ur"(?:\W|\d){1,5}((?!(?:AAL|SPOIK|AUL|AKE|AKM|AKL|APT|AKK|AOK|AUK|AAUK|EKM|ELK|ETP|FFB|HRUP|HTK|HKI|HRE|HRR|HKKK|IPA|IPE|IPK|IIK|JBK|JKL|JKV|KEK|KHK|KKK|KAL|KKP|KLP|KTA|KOK|KTR|KTP|KTV|LKV|LLP|LRE|LVK|OKH|OKL|OKM|OKW|PIM|PPK|PPP|PLL|PTK|PYS|PYP|RAUL|RJR|RKJ|RKK|RTR|RUK|RVP|RVL|SKK|URR|VKM|MKL|MSK|MKUL|MLL|MTK|KTK|PBH|NPOR|RUL|SAK|SLL|RTVL|IPAK|SDP|SKL|SUL|STS|SNL|SML|SMP|SNS|SKP|KVL|SVR|SVJ|SVUL|SVML|STKL|SPR|SRL|SLR|SKDL|SUL|STL|KOP|SEL|SOP|SOL|SAL|SOK|STTK|SPL|SKT|TVO|TVK|TUL|TTPS|SKTL|OTK|USA|VPK|VVL|VVP|VII|SHL|IIKT|KORPR|VVL|EKIII|STIK|XXX)\b)[A-ZÄ-Öln-]{3,})\b", ur"\n</PERSON>\n\n<PERSON>\1", text)
        text = "<DATA>\n<PERSON>\n" + text + "</PERSON>\n</DATA>"

        newfilename = filename[0:len(filename)-3]
        newfilename = newfilename + "xml"
        f = open(newfilename, "w")
        f.write(text.encode('utf8'))
        f.close()


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()