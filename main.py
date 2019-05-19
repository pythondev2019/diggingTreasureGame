#coding=utf-8
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import queue
import logics
import threading

tk=Tk()
tk.title('Digging Treasure')
tk.resizable(False,False)


descriptionText='Nokia\'s classic game in python3 with tkinter.'
aboutText='This is the project for python3 course of faculty of computational mathematics and cybernetics of Lomonosov Moscow State University.'
cmds=queue.Queue()
cellSize=32
borderSize=10
tickTime=.4
initLevel=1
paused=False
moneyBarText = StringVar()
hudText = StringVar()

dg=[[None for x in range(logics.GX)] for y in range(logics.GY)]
onscreen=[[None for x in range(logics.GX)] for y in range(logics.GY)]
material={
    logics.Elem.chunk[0]: PhotoImage(file='gifes/chunk1.gif'),
    logics.Elem.chunk[1]: PhotoImage(file='gifes/chunk2.gif'),
    logics.Elem.chunk[2]: PhotoImage(file='gifes/chunk3.gif'),
    logics.Elem.dirt: PhotoImage(file='gifes/dirt.gif'),
    logics.Elem.evildirt: PhotoImage(file='gifes/dirt.gif'),
    logics.Elem.empty: PhotoImage(file='gifes/empty.gif'),
    logics.Elem.fire: PhotoImage(file='gifes/fire.gif'),
    logics.Elem.heart: PhotoImage(file='gifes/heart.gif'),
}
player={
    'LeftNormal':PhotoImage(file='gifes/playerL.gif'),
    'RightNormal':PhotoImage(file='gifes/playerR.gif'),
    'LeftHurt':PhotoImage(file='gifes/playerHurtL.gif'),
    'RightHurt':PhotoImage(file='gifes/playerHurtR.gif'),
}

def cmd(value):
    cmds.put(value)

def show_hud(msg):
    hudText.set(' %s '%msg)
    hud.grid(row=1,column=0)
    time.sleep(2)
    hud.grid_forget()

def pause():
    global paused
    paused = not paused
    pausebtn.state(['pressed' if paused else '!pressed'])
    pausebtn['text']='Resume' if paused else 'Pause'

def game_controller():
    init_level(initLevel)
    show_hud('Level %d：$ %d'%(game.level,game.goal))
    while True:
        if paused:
            time.sleep(.1)
            continue
        try:
            try:
                if not game.player.command:
                    x=cmds.get_nowait()
                    game.player.command=x
            except queue.Empty:
                game.player.command=''
            game.tick()
            tick_routine()
            time.sleep(tickTime)
        except logics.GameOver:
            show_hud('You lost')
            show_hud('Your level: %d'%game.level)
            init_level(initLevel)
            show_hud('level %d：$ %d'%(game.level,game.goal))
        except logics.YouWin:
            show_hud('You won')
            init_level(game.level+1)
            show_hud('level %d：$ %d'%(game.level,game.goal))

def tick_routine(redraw=False):
    def get_player_img():
        return player[('Left' if game.player.left else 'Right')+('Hurt' if game.player.life_restore else 'Normal')]
    
    for y in range(logics.GY):
        for x in range(logics.GX):
            if redraw or game.g[y][x] is not onscreen[y][x] or game.g[y][x]==logics.Elem.player:
                onscreen[y][x]=game.g[y][x]
                if dg[y][x]:
                    canvas.delete(dg[y][x])
                if game.g[y][x]==logics.Elem.player:
                    dg[y][x]=canvas.create_image(x*SZ,y*SZ,anchor='nw',image=get_player_img())
                else:
                    dg[y][x]=canvas.create_image(x*SZ,y*SZ,anchor='nw',image=material[game.g[y][x]])

    tk.title('Digging treasure [ level %d ]'%game.level)
    moneyBarText.set('$ %d / %d'%(game.cur,game.goal))
    moneybar['value']=game.cur
    hpbar['value']=game.player.life
    canvas.yview_moveto((BORDER+game.player.y-3.5)/(logics.GY+2*BORDER))
    canvas.xview_moveto((BORDER+game.player.x-4.5)/(logics.GX+2*BORDER))

def init_level(level):
    global dg
    global onscreen
    dg=[[None for x in range(logics.GX)] for y in range(logics.GY)]
    onscreen=[[None for x in range(logics.GX)] for y in range(logics.GY)]
    canvas.delete('all')
    game.init_level(level)
    canvas['scrollregion']=(-BORDER*SZ,-BORDER*SZ,(BORDER+logics.GX)*SZ,(BORDER+logics.GY)*SZ)
    moneybar['value']=0
    moneybar['maximum']=game.goal
    tick_routine(redraw=True)

f=Frame(tk)
f.grid(row=0,column=0,sticky='we')
f.columnconfigure(2,weight=1)

hpbar=Progressbar(f,orient=HORIZONTAL,length=100,value=100,maximum=100,mode='determinate')
hpbar.grid(row=0,column=0)
Label(f,text='Life').grid(row=0,column=1)
Label(f).grid(row=0,column=2,sticky='we')
moneybar=Progressbar(f,orient=HORIZONTAL,length=80,value=0,maximum=1,mode='determinate')
Label(f,textvariable = moneyBarText).grid(row=0,column=3)
moneybar.grid(row=0,column=4)

canvas=Canvas(tk,width=10*cellSize,height=10*cellSize,bg='#770055')
canvas.grid(row=1,column=0,sticky='nswe')

infof=Frame(tk)
infof.grid(row=2,column=0,sticky='we')
infof.columnconfigure(1,weight=1)

pausebtn=Button(infof,text = 'Pause',width = 8,command = pause)
pausebtn.grid(row = 0,column = 0)

Label(infof).grid(row = 0,column = 1,sticky = 'we')
Button(infof,text = 'Instructions',width = 12,command = lambda:messagebox.showinfo('Instructions','instructions')).grid(row = 0,column = 2)
Button(infof,text = 'About',width = 8,command = lambda:messagebox.showinfo('About','about')).grid(row=0,column=3)

tk.bind_all('<Left>',lambda *_:cmd(logics.Command.left))
tk.bind_all('<Right>',lambda *_:cmd(logics.Command.right))
tk.bind_all('<Up>',lambda *_:cmd(logics.Command.next))
tk.bind_all('<Down>',lambda *_:cmd(logics.Command.down))
tk.after(0,lambda *_:threading.Thread(target=game_controller).start())

mainloop()
