#coding=utf-8
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import queue
import logics

cmds=queue.Queue()
cellSize=32
paused=False

tk=Tk()
tk.title('Digging Treasure')
tk.resizable(False,False)

def cmd(value):
    cmds.put(value)

def pause():
    global paused
    paused=not paused
    pausebtn.state(['pressed' if paused else '!pressed'])
    pausebtn['text']='Resume' if paused else 'Pause'

f=Frame(tk)
f.grid(row=0,column=0,sticky='we')
f.columnconfigure(2,weight=1)

hpbar=Progressbar(f,orient=HORIZONTAL,length=100,value=100,maximum=100,mode='determinate')
hpbar.grid(row=0,column=0)
Label(f,text='Life').grid(row=0,column=1)
Label(f).grid(row=0,column=2,sticky='we')
Label(f,text='Money').grid(row=0,column=3)
moneybar=Progressbar(f,orient=HORIZONTAL,length=80,value=0,maximum=1,mode='determinate')
moneybar.grid(row=0,column=4)

canvas=Canvas(tk,width=10*cellSize,height=10*cellSize,bg='#770055')
canvas.grid(row=1,column=0,sticky='nswe')

infof=Frame(tk)
infof.grid(row=2,column=0,sticky='we')
infof.columnconfigure(1,weight=1)

pausebtn=Button(infof,text='Pause',width=8,command=pause)
pausebtn.grid(row=0,column=0)

Label(infof).grid(row=0,column=1,sticky='we')
Button(infof,text='Instructions',width=8,command=lambda:messagebox.showinfo('Instructions','instructions')).grid(row=0,column=2)
Button(infof,text='About',width=8,command=lambda:messagebox.showinfo('About','about')).grid(row=0,column=3)

tk.bind_all('<Left>',lambda *_:cmd(logics.Command.left))
tk.bind_all('<Right>',lambda *_:cmd(logics.Command.right))
tk.bind_all('<Up>',lambda *_:cmd(logics.Command.next))
tk.bind_all('<Down>',lambda *_:cmd(logics.Command.down))

mainloop()
