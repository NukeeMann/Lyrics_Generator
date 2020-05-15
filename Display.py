from tkinter import *
from tkinter.messagebox import *
from os import listdir
from tkinter.filedialog import askopenfilename
import shutil
import os
import ntpath

class Window:


    def __init__(self, x, y, managerRef):
        root=Tk()
        root.title("Lyrics Generator v2.3")
        self.x = 0
        self.managerRef = managerRef
        self.y = 0
        self.canvas = Canvas(root, width=x, height=y)
        self.b1 = Button(self.canvas, text="Description", font=9, command=self.displayDescrition, height =6, width = 30)
        self.b1.place(relx=0.5, rely=0.048)
        self.b2 = Button(self.canvas, text="Your Database", font=9, command=self.database,height =6, width = 30)
        self.b2.place(relx=0.5, rely=0.35)
        self.b3 = Button(self.canvas, text="Generate Lyrics", font=9, command=self.generateLyrics,height =6, width = 30)
        self.b3.place(relx=0.5, rely=0.65)
        img = PhotoImage(file="rapbot.ppm")
        self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.pack()
        root.mainloop()

    def displayDescrition(self):
        showinfo("Description", "TODO Welcome in Lyrics Generator, application which can create the best song u can even imagine!")

    def database(self):
        popup = Tk()
        popup.title("Lyrics Generator v2.3")
        self.canvas = Canvas(popup, width=400, height=525)
        self.b = Button(self.canvas, text="Add new", font=14, command=self.fileManagment, bg="green",height =2, width = 25)
        self.b.pack()
        iter=2
        for f in listdir('database/Yours/'):
            if '.txt' in f:
                self.b = Button(self.canvas, text=f, font=14, command=lambda f=f: self.readFile(f), height =2, width = 25)
                self.b.pack()
                iter+=1
        self.canvas.pack()

    def readFile(self,name):
        f = open('database/Yours/' + name , 'r', encoding="utf8")
        showinfo(name,f.read())


    def generateLyrics(self):
        popup = Tk()
        popup.title("Lyrics Generator v2.3")
        label = Label(popup, text="Choose the artist", font=15,height =2, width = 25)
        label.pack()
        self.canvas = Canvas(popup, width=200, height=225)
        self.b = Button(self.canvas, text="Eminem", font=14, command=lambda: self.createSongByArtist('Eminem',popup),height =2, width = 25)
        self.b.pack()
        self.b = Button(self.canvas, text="2pac", font=14, command=lambda: self.createSongByArtist('2pac',popup),height =2, width = 25)
        self.b.pack()
        self.b = Button(self.canvas, text="50 cent", font=14, command=lambda: self.createSongByArtist('50cent',popup),height =2, width = 25)
        self.b.pack()
        self.b = Button(self.canvas, text="Yours", font=14, command=lambda: self.chooseTheSong(popup),height =2, width = 25)
        self.b.pack()
        self.canvas.pack()

    def createSongByArtist(self,name,popup):
        self.managerRef.createByArtist(name)
        popup.destroy()


    def chooseTheSong(self,prevPopup):
        popup = Tk()
        popup.title("Lyrics Generator v2.3")
        label = Label(popup, text="Choose the songs", font=15)
        label.pack()
        vars =[]
        iter=0
        self.canvas = Canvas(popup, width=400, height=525)
        for f in listdir('database/Yours/'):
            if '.txt' in f:
                vars.append(StringVar())
                self.b = Checkbutton(popup, text=f, variable=vars[iter], command=lambda f=f, vars=vars, iter=iter: self.toggle(vars[iter],f))
                self.b.pack()
                iter+=1
        self.canvas.pack()
        self.b1 = Button(self.canvas, text="Submit", font=14, command=lambda: self.addToList(vars,popup, prevPopup))
        self.b1.pack()

    def toggle(self, var, name):
        if var.get() == '':
            var.set(name)
        else:
            var.set('')
        return

    def addToList(self, vars, popup, prevPopup):
        songList = []
        for i in range(0, len(vars)):
            if not vars[i].get() == '':
                songList.append(vars[i].get())
        if not songList:
            showerror(title="Error", message="Choose song!")
            return
        self.managerRef.createBySong(songList)
        popup.destroy()
        prevPopup.destroy()

    def displayText(self, text):
        showinfo(text)

    def fileManagment(self):
        showinfo("Lyrics Generator", "Choose text file")
        text = askopenfilename()
        if not text:
            return
        if not '.txt' in text:
            showerror(title="Error", message="It's not a .txt file!")
            return
        newPath = shutil.copy(text, 'database/Yours')
        showinfo("Lyrics Generator", "Choose phonetic file")
        phon = askopenfilename()
        if not phon:
            os.remove('database/Yours/' + self.path_leaf(text))
            return
        if not '.txt' in phon:
            os.remove('database/Yours/' + self.path_leaf(text))
            showerror(title="Error", message="It's not a .txt file!")
            return
        if not 'PHON_'+ self.path_leaf(text) in phon:
            os.remove('database/Yours/' + self.path_leaf(text))
            showerror(title="Error", message="The name of file is incorrect. It has to have the same name as text file and starts with 'PHON'")
            return
        newPath = shutil.copy(phon, 'database/Yours/phonetics')

    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

class WindowText:
    def __init__(self,artist, text):
        showinfo(artist,text)