from Tkinter import *

class Application(Frame):

    objectList = []
    currentPrevious = None
    currentChild = None



    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):

        self.parent.title = "Chunk editor"
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1, minsize=200)
        self.columnconfigure(3)
        self.columnconfigure(4)

        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Chunk")
        lbl.grid(sticky=W, pady=4, padx=5)


        self.textareaPrevious = Text(self)
        self.textareaPrevious.config(bg="black", fg="white", insertbackground="white")
        self.textareaPrevious.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)


        self.textarea = Text(self)
        self.textarea.grid(row=5, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)


        #LISTBOX
        self.lb = Listbox(self)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.config(command=self.lb.yview)
        scrollbar.grid(column=3, row=2, rowspan=3,sticky=N+S)

        self.lb.config(yscrollcommand=scrollbar.set, width=50, selectmode=EXTENDED)
        self.lb.grid(row=2, rowspan=3, column=2,columnspan=1, sticky=N+E+S+W)
        for i in self.objectList:

            self.lb.insert(END, i["child"].text)

        #bind slot
        self.lb.bind("<<ListboxSelect>>", self.onSelect)


        hbtn = Button(self, text=" Save ", command=self.saveChildModifications)
        hbtn.grid(row=5, column=3, padx=5, sticky=N+E+S)

        obtn = Button(self, text="Combine", command=self.combineChildren)
        obtn.grid(row=5, column=2,sticky=N+E+S)


    def saveChildModifications(self):
        #take the child at question:
        self.currentChild["child"].text = self.textarea.get(1.0, END)
        self.currentChild["child"].attrib["checked"] = "True"
        print self.currentChild["child"].text

    def combineChildren(self):
        newtxt = self.textareaPrevious.get(1.0, END).strip('\n') + " " + self.textarea.get(1.0, END).strip('\n')
        self.currentChild["child"].text = newtxt
        self.currentChild["child"].attrib["combined"] = "True"
        self.xmldocument.remove(self.currentPrevious)
        print self.currentChild["child"].text


    def onSelect(self, val):

        #set text of this child to textfield
        sender = val.widget         #get sender of the event
        idx = sender.curselection() #get index of selection
        value = self.objectList[idx[0]]["child"].text #sender.get(idx)     #get actual value of selection
        self.currentChild = self.objectList[idx[0]]
        self.textarea.delete(1.0, END)
        self.textarea.insert(INSERT,value)

        #find previous child's text
        self.currentPrevious = self.currentChild["child"].getprevious()
        print self.currentPrevious.text
        self.textareaPrevious.delete(1.0, END)

        self.textareaPrevious.insert(INSERT,self.currentPrevious.text)


    def __init__(self, objectList, xmldocument, master=None):
        Frame.__init__(self, master)
        self.objectList = objectList
        self.xmldocument = xmldocument
        self.parent = master
        self.createWidgets()

    def say(self):
        print "asdfsadsa"


def startGUI(objectList, xmldocument):
    root = Tk()
    root.geometry("800x800+300+100")
    app = Application(objectList,xmldocument, master=root)
    app.mainloop()
    #root.destroy()