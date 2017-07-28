# -*- coding:utf-8 -*-

import os, os.path, sys
from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
from tkFileDialog import *
import json

# the path of images and json file to load, and where to save the json file with chinese annotation
picdir = ''
jsondir= ''
json_save_name = 'captions_with_chn.json'

# The interface to load the path of images and json file
class Selectpath():
    def __init__(self, root):
        self.topframe = Frame(root, borderwidth=2, relief=GROOVE)
        self.topframe.pack(padx=2, pady=2)

        self.piclabel = Label(self.topframe, text='图片路径:')
        self.piclabel.grid(row=0, column=0, padx=4, pady=4)

        self.picdir_text = StringVar()
        self.picdir_text.set('')
        self.picentry = Entry(self.topframe, textvariable=self.picdir_text, width=30)
        self.picentry.grid(row=0, column=1, columnspan=2, padx=4, pady=4)

        self.picbutton = Button(self.topframe, text='浏览', command=self.getpicdir, width=6)
        self.picbutton.grid(row=0, column=3, padx=4, pady=4)

        self.jsonlabel = Label(self.topframe, text='JSON路径:')
        self.jsonlabel.grid(row=1, column=0, padx=4, pady=4)

        self.jsondir_text = StringVar()
        self.jsondir_text.set('')
        self.jsonentry = Entry(self.topframe, textvariable=self.jsondir_text, width=30)
        self.jsonentry.grid(row=1, column=1, columnspan=2, padx=4, pady=4)

        self.jsonbutton = Button(self.topframe, text='浏览', command=self.getjsondir, width=6)
        self.jsonbutton.grid(row=1, column=3, padx=4, pady=4)

        self.enter = Button(self.topframe, text='确定', command=self.getdirs, width=6)
        self.enter.grid(row=2, column=1, padx=4, pady=4)
        self.cancel = Button(self.topframe, text='取消', command=root.quit, width=6)
        self.cancel.grid(row=2, column=2, padx=4, pady=4)
    
    # get the path of images through the Load button
    # and put it into the Image Path entry
    def getpicdir(self):
        global picdir
        picdir = askdirectory()
        if picdir:
            self.picdir_text.set(picdir)
            self.picentry['textvariable'] = self.picdir_text

    # get the path of json file through the Load button
    # and put it into the JSON Path entry
    def getjsondir(self):
        global jsondir
        ftypes = (('JSON Files', '*.json'),
                ('All Files', '*'))
        jsondir = askopenfilename(filetypes=ftypes)
        if jsondir:
            self.jsondir_text.set(jsondir)
            self.jsonentry['textvariable'] = self.jsondir_text
    
    # get picdir and jsondir
    # if not exists, then pop-up a warning window
    def getdirs(self):
        global picdir, jsondir
        picdir = self.picentry.get()
        jsondir = self.jsonentry.get()
        if os.path.exists(picdir) and os.path.exists(jsondir):
            Anno(self.topframe)
        else:
            win = Toplevel(self.topframe)
            Label(win, text="文件路径不存在!").pack()


# The interface to annotate the images with Chinese sentences.
class Anno():
    def __init__(self, root):
        global picdir, jsondir
        self.anno = Toplevel(root)
        
        # left frame: the list of images
        self.leftframe = Frame(self.anno, borderwidth=2, relief=GROOVE)
    	self.leftframe.grid(row=0, column=0, rowspan=3, padx=2, pady=2)
        self.leftscrbar = Scrollbar(self.leftframe, orient=VERTICAL)
        self.listbox = Listbox(self.leftframe, yscrollcommand=self.leftscrbar.set, width=30, height=45)
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.leftscrbar.pack(side=LEFT, fill=Y)
        self.pl = []
        self.getpiclist()
        for pic in self.pl:
            self.listbox.insert(END, pic)

        # if there has been a file named json_save_name, load it
        # else load the jsondir
        if os.path.exists(json_save_name):
            self.jl = json.load(open(json_save_name, 'r'))
        else:
            self.jl = json.load(open(jsondir, 'r'))
            for i, it in enumerate(self.jl):
                self.jl[i]['chn'] = ['','','','','']
            

        self.cur_imgname = ''
    	self.cur_jl_index = -1
	self.cur_pl_index = 0

        self.leftscrbar.config(command=self.listbox.yview)

        # middle frame: current image
	self.midframe = Frame(self.anno, borderwidth=2, relief=GROOVE)
	self.midframe.grid(row=0, column=1, rowspan=3, padx=2, pady=2)
        self.img = ImageTk.PhotoImage(file=picdir+os.path.sep+self.pl[0])
        self.imglabel = Label(self.midframe, image=self.img)
        self.imglabel.pack(side=LEFT, fill=BOTH)
	
        # top right: EN annotations loading from json file
	self.rightframe1 = Frame(self.anno, borderwidth=2, relief=GROOVE)
	self.rightframe1.grid(row=0, column=2, padx=2, pady=2)
        self.origin_anno = ['1. 请在左侧列表选中文件后单击Enter键进行切换              ', '2. 请在左侧列表选中文件后单击Enter键进行切换              ', '3. 请在左侧列表选中文件后单击Enter键进行切换              ', '4. 请在左侧列表选中文件后单击Enter键进行切换              ', '5. 请在左侧列表选中文件后单击Enter键进行切换              ']

        self.origin_label1 = Label(self.rightframe1, text=self.origin_anno[0], wraplength=500, justify=LEFT)
        self.origin_label1.pack(side=TOP, anchor=W, padx=10, pady=8)
        self.origin_label2 = Label(self.rightframe1, text=self.origin_anno[1], wraplength=500, justify=LEFT)
        self.origin_label2.pack(side=TOP, anchor=W, padx=10, pady=8)
        self.origin_label3 = Label(self.rightframe1, text=self.origin_anno[2], wraplength=500, justify=LEFT)
        self.origin_label3.pack(side=TOP, anchor=W, padx=10, pady=8)
        self.origin_label4 = Label(self.rightframe1, text=self.origin_anno[3], wraplength=500, justify=LEFT)
        self.origin_label4.pack(side=TOP, anchor=W, padx=10, pady=8)
        self.origin_label5 = Label(self.rightframe1, text=self.origin_anno[4], wraplength=500, justify=LEFT)
        self.origin_label5.pack(side=TOP, anchor=W, padx=10, pady=8)
        
        # middle right: entries to type Chinese sentences into
	self.rightframe2 = Frame(self.anno, borderwidth=2, relief=GROOVE)
	self.rightframe2.grid(row=1, column=2, padx=2, pady=2)
        
        self.chn_anno1 = StringVar()
        self.chn_anno2 = StringVar()
        self.chn_anno3 = StringVar()
        self.chn_anno4 = StringVar()
        self.chn_anno5 = StringVar()
        
        self.chn_label1 = Label(self.rightframe2, text='1. ')
        self.chn_label1.grid(row=0, column=0, padx=10, pady=5)
	self.chn_entry1 = Entry(self.rightframe2, width=50)
	self.chn_entry1.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        self.chn_label2 = Label(self.rightframe2, text='2. ')
        self.chn_label2.grid(row=1, column=0, padx=10, pady=5)
    	self.chn_entry2 = Entry(self.rightframe2, width=50)
	self.chn_entry2.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

        self.chn_label3 = Label(self.rightframe2, text='3. ')
	self.chn_label3.grid(row=2, column=0, padx=10, pady=5)
	self.chn_entry3 = Entry(self.rightframe2, width=50)
	self.chn_entry3.grid(row=2, column=1, columnspan=4, padx=5, pady=5)

        self.chn_label4 = Label(self.rightframe2, text='4. ')
	self.chn_label4.grid(row=3, column=0, padx=10, pady=5)        
	self.chn_entry4 = Entry(self.rightframe2, width=50)
        self.chn_entry4.grid(row=3, column=1, columnspan=4, padx=5, pady=5)

    	self.chn_label5 = Label(self.rightframe2, text='5. ')
	self.chn_label5.grid(row=4, column=0, padx=10, pady=5)
	self.chn_entry5 = Entry(self.rightframe2, width=50)
	self.chn_entry5.grid(row=4, column=1, columnspan=4, padx=5, pady=5)

        self.chn_save_button = Button(self.rightframe2, text='保 存', command=self.chn_save, width=8)
        self.chn_save_button.grid(row=5, column=0,columnspan=5, padx=5, pady=5)

        
        # buttom right: buttons of Last and Next
        self.rightframe3 = Frame(self.anno, borderwidth=2, relief=GROOVE)
        self.rightframe3.grid(row=2, column=2, padx=2, pady=2)
        self.lastbutton = Button(self.rightframe3, text='上一个', command=self.last_img, width =10)
        self.lastbutton.grid(row=0, column=0, padx=10, pady=10)
        self.nextbutton = Button(self.rightframe3, text='下一个', command=self.next_img, width =10)
        self.nextbutton.grid(row=0, column=1, padx=10, pady=10)

        self.listbox.bind('<Return>', self.show_img_and_text)

    # load piclist from picdir
    def getpiclist(self):
        global picdir
        ls = os.listdir(picdir)
        for f in ls:
            if os.path.splitext(f)[1] == '.jpg':
                self.pl.append(f)
        #self.pl.sort(key=lambda x:int(x[:-4]))
    
    # 
    def show_img_and_text(self, event):
        global picdir, jsondir
        self.cur_imgname = event.widget.get(ACTIVE)
        for index, it in enumerate(self.pl):
            if it == self.cur_imgname:
                self.cur_pl_index = index
                break
        fl = picdir+os.path.sep+self.cur_imgname
        self.img = ImageTk.PhotoImage(file=fl)
        self.imglabel.config(image=self.img)
        for index, it in enumerate(self.jl):
            if it['file_name'] == self.cur_imgname:
                self.origin_anno[0] = '1. ' + it['captions'][0]
                self.origin_anno[1] = '2. ' + it['captions'][1]
                self.origin_anno[2] = '3. ' + it['captions'][2]
                self.origin_anno[3] = '4. ' + it['captions'][3]
                self.origin_anno[4] = '5. ' + it['captions'][4]
                self.chn_anno1.set(it['chn'][0])
                self.chn_anno2.set(it['chn'][1])
                self.chn_anno3.set(it['chn'][2])
                self.chn_anno4.set(it['chn'][3])
                self.chn_anno5.set(it['chn'][4])
                self.cur_jl_index = index
                break
        self.origin_label1['text'] = self.origin_anno[0]
        self.origin_label2['text'] = self.origin_anno[1]
        self.origin_label3['text'] = self.origin_anno[2]
        self.origin_label4['text'] = self.origin_anno[3]
        self.origin_label5['text'] = self.origin_anno[4]
        
        self.chn_entry1['textvariable'] = self.chn_anno1
        self.chn_entry2['textvariable'] = self.chn_anno2
        self.chn_entry3['textvariable'] = self.chn_anno3
        self.chn_entry4['textvariable'] = self.chn_anno4
        self.chn_entry5['textvariable'] = self.chn_anno5

    
    def chn_save(self):
        global json_save_name
	self.chn_anno1.set(self.chn_entry1.get())
	self.chn_anno2.set(self.chn_entry2.get())
	self.chn_anno3.set(self.chn_entry3.get())
	self.chn_anno4.set(self.chn_entry4.get())
	self.chn_anno5.set(self.chn_entry5.get())
        if self.cur_jl_index >= 0:
            self.jl[self.cur_jl_index]['chn'][0] = self.chn_anno1.get()
            self.jl[self.cur_jl_index]['chn'][1] = self.chn_anno2.get()
            self.jl[self.cur_jl_index]['chn'][2] = self.chn_anno3.get()
            self.jl[self.cur_jl_index]['chn'][3] = self.chn_anno4.get()
            self.jl[self.cur_jl_index]['chn'][4] = self.chn_anno5.get()
            json_save = open(json_save_name, 'w')
            json_save.write(json.dumps(self.jl))
            json_save.close()

    def last_img(self):
	global picdir, jsondir
	if self.cur_pl_index >=1:
            self.cur_pl_index = self.cur_pl_index - 1
	self.listbox.selection_set(self.cur_pl_index,self.cur_pl_index)
        self.cur_imgname = self.pl[self.cur_pl_index]
        fl = picdir+os.path.sep+self.cur_imgname
        self.img = ImageTk.PhotoImage(file=fl)
        self.imglabel.config(image=self.img)
        for index, it in enumerate(self.jl):
            if it['file_name'] == self.cur_imgname:
                self.origin_anno[0] = '1. ' + it['captions'][0]
                self.origin_anno[1] = '2. ' + it['captions'][1]
                self.origin_anno[2] = '3. ' + it['captions'][2]
                self.origin_anno[3] = '4. ' + it['captions'][3]
                self.origin_anno[4] = '5. ' + it['captions'][4]
                self.chn_anno1.set(it['chn'][0])
                self.chn_anno2.set(it['chn'][1])
                self.chn_anno3.set(it['chn'][2])
                self.chn_anno4.set(it['chn'][3])
                self.chn_anno5.set(it['chn'][4])
                self.cur_jl_index = index
                break
        self.origin_label1['text'] = self.origin_anno[0]
        self.origin_label2['text'] = self.origin_anno[1]
        self.origin_label3['text'] = self.origin_anno[2]
        self.origin_label4['text'] = self.origin_anno[3]
        self.origin_label5['text'] = self.origin_anno[4]

        self.chn_entry1['textvariable'] = self.chn_anno1
        self.chn_entry2['textvariable'] = self.chn_anno2
        self.chn_entry3['textvariable'] = self.chn_anno3
        self.chn_entry4['textvariable'] = self.chn_anno4
        self.chn_entry5['textvariable'] = self.chn_anno5

    def next_img(self):
	global picdir, jsondir
	if self.cur_pl_index < len(self.pl) - 1:
            self.cur_pl_index = self.cur_pl_index + 1
	self.listbox.selection_set(self.cur_pl_index, self.cur_pl_index)
        self.cur_imgname = self.pl[self.cur_pl_index]
        fl = picdir+os.path.sep+self.cur_imgname
        self.img = ImageTk.PhotoImage(file=fl)
        self.imglabel.config(image=self.img)
        for index, it in enumerate(self.jl):
            if it['file_name'] == self.cur_imgname:
                self.origin_anno[0] = '1. ' + it['captions'][0]
                self.origin_anno[1] = '2. ' + it['captions'][1]
                self.origin_anno[2] = '3. ' + it['captions'][2]
                self.origin_anno[3] = '4. ' + it['captions'][3]
                self.origin_anno[4] = '5. ' + it['captions'][4]
                self.chn_anno1.set(it['chn'][0])
                self.chn_anno2.set(it['chn'][1])
                self.chn_anno3.set(it['chn'][2])
                self.chn_anno4.set(it['chn'][3])
                self.chn_anno5.set(it['chn'][4])
                self.cur_jl_index = index
                break
        self.origin_label1['text'] = self.origin_anno[0]
        self.origin_label2['text'] = self.origin_anno[1]
        self.origin_label3['text'] = self.origin_anno[2]
        self.origin_label4['text'] = self.origin_anno[3]
        self.origin_label5['text'] = self.origin_anno[4]

        self.chn_entry1['textvariable'] = self.chn_anno1
        self.chn_entry2['textvariable'] = self.chn_anno2
        self.chn_entry3['textvariable'] = self.chn_anno3
        self.chn_entry4['textvariable'] = self.chn_anno4
        self.chn_entry5['textvariable'] = self.chn_anno5

def main():
    global picdir, jsondir
    root = Tk()
    root.title('Image Caption中文数据集标注程序')
    root.resizable(0,0)

    sp = Selectpath(root)

    root.mainloop()
    
if __name__ == '__main__':
    main()

