from tkinter import *

class popupWindow(object):
    def __init__(self, master, msg = "Prompt: "):
        top=self.top=Toplevel(master)
        self.l=Label(top,text=msg)
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()