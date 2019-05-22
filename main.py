# coding=utf-8
import os
import queue
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import logics
import main_menu

lang = 'Eng'
english = ['Eng', 'Digging Treasure', 'Resume', 'Pause', 'Instructions', 'About']
russian = ['Рус', 'Спрятанные сокровища', 'Продолжать', 'Пауза', 'Инструкция', 'О проекте']

game = logics.Game()
main_menu.main_menu(game.player)

tk = Tk()
tk.title('Digging Treasure')
tk.resizable(False, False)

cmds = queue.Queue()
cellSize = 32
borderSize = 10
tickTime = .4
initLevel = 1
paused = False
moneyBarText = StringVar()
hudText = StringVar()

dg = [[None for x in range(logics.GX)] for y in range(logics.GY)]
onscreen = [[None for x in range(logics.GX)] for y in range(logics.GY)]
material = {
    logics.Elem.chunk[0]: PhotoImage(file='gifes/chunk1.gif'),
    logics.Elem.chunk[1]: PhotoImage(file='gifes/chunk2.gif'),
    logics.Elem.chunk[2]: PhotoImage(file='gifes/chunk3.gif'),
    logics.Elem.dirt: PhotoImage(file='gifes/dirt.gif'),
    logics.Elem.evildirt: PhotoImage(file='gifes/dirt.gif'),
    logics.Elem.empty: PhotoImage(file='gifes/empty.gif'),
    logics.Elem.fire: PhotoImage(file='gifes/fire.gif'),
    logics.Elem.heart: PhotoImage(file='gifes/heart.gif'),
}
player = {
    'LeftNormal': PhotoImage(file='gifes/playerL.gif'),
    'RightNormal': PhotoImage(file='gifes/playerR.gif'),
    'LeftHurt': PhotoImage(file='gifes/playerHurtL.gif'),
    'RightHurt': PhotoImage(file='gifes/playerHurtR.gif'),
}


def change_language(language):
    langbtn.config(text=language[0])
    tk.title(language[1])
    pausebtn.config(text=(language[2] if paused else language[3]))
    instructionbtn.config(text=language[4])
    aboutbtn.config(text=language[5])


def cmd(value):
    cmds.put(value)


def show_hud(msg):
    hudText.set(' %s ' % msg)
    hud.grid(row=1, column=0)
    time.sleep(2)
    hud.grid_forget()


def pause():
    global paused
    paused = not paused
    pausebtn.state(['pressed' if paused else '!pressed'])
    pausebtn['text'] = 'Resume' if paused else 'Pause'


def game_controller():
    init_level(initLevel)
    while True:
        if paused:
            time.sleep(.1)
            continue
        try:
            try:
                if not game.player.command:
                    x = cmds.get_nowait()
                    game.player.command = x
            except queue.Empty:
                game.player.command = ''
            game.tick()
            tick_routine()
            time.sleep(tickTime)
        except logics.GameOver:
            show_hud('You lost')
            show_hud('Your level: %d' % game.level)
            game.player.add_total_score(moneybar['value'])
            main_menu.insert_or_update_result(game.player.name, game.player.total_score)
            init_level(initLevel)
            show_hud('level %d：$ %d' % (game.level, game.goal))
        except logics.YouWin:
            show_hud('You won')
            init_level(game.level + 1)
            show_hud('level %d：$ %d' % (game.level, game.goal))


def tick_routine(redraw=False):
    def get_player_img():
        return player[('Left' if game.player.left else 'Right') + ('Hurt' if game.player.life_restore else 'Normal')]

    for y in range(logics.GY):
        for x in range(logics.GX):
            if redraw or game.g[y][x] is not onscreen[y][x] or game.g[y][x] == logics.Elem.player:
                onscreen[y][x] = game.g[y][x]
                if dg[y][x]:
                    canvas.delete(dg[y][x])
                if game.g[y][x] == logics.Elem.player:
                    dg[y][x] = canvas.create_image(x * cellSize, y * cellSize, anchor='nw', image=get_player_img())
                else:
                    dg[y][x] = canvas.create_image(x * cellSize, y * cellSize, anchor='nw',
                                                   image=material[game.g[y][x]])

    moneyBarText.set('$ %d / %d' % (game.cur, game.goal))
    moneybar['value'] = game.cur
    hpbar['value'] = game.player.life
    canvas.yview_moveto((borderSize + game.player.y - 3.5) / (logics.GY + 2 * borderSize))
    canvas.xview_moveto((borderSize + game.player.x - 4.5) / (logics.GX + 2 * borderSize))


def init_level(level):
    global dg
    global onscreen
    dg = [[None for x in range(logics.GX)] for y in range(logics.GY)]
    onscreen = [[None for x in range(logics.GX)] for y in range(logics.GY)]
    canvas.delete('all')
    if level != initLevel:
        game.player.add_total_score(moneybar['maximum'])
    game.init_level(level)
    canvas['scrollregion'] = (-borderSize * cellSize, -borderSize * cellSize, (borderSize + logics.GX) * cellSize,
                              (borderSize + logics.GY) * cellSize)
    moneybar['value'] = 0
    moneybar['maximum'] = game.goal
    tick_routine(redraw=True)


def end_game(tk):
    game.player.add_total_score(moneybar['value'])
    main_menu.insert_or_update_result(game.player.name, game.player.total_score)
    tk.destroy()
    os.abort()


f = Frame(tk)
f.grid(row=0, column=0, sticky='we')
f.columnconfigure(2, weight=1)

hpbar = Progressbar(f, orient=HORIZONTAL, length=100, value=100, maximum=100, mode='determinate')
hpbar.grid(row=0, column=0)
Label(f, text='Life').grid(row=0, column=1)
Label(f).grid(row=0, column=2, sticky='we')
moneybar = Progressbar(f, orient=HORIZONTAL, length=80, value=0, maximum=1, mode='determinate')
Label(f, textvariable=moneyBarText).grid(row=0, column=3)
moneybar.grid(row=0, column=4)

canvas = Canvas(tk, width=10 * cellSize, height=10 * cellSize, bg='#770055')
canvas.grid(row=1, column=0, sticky='nswe')
hud = Label(tk, textvariable=hudText, background='#000055', foreground='#ffffff')

infof = Frame(tk)
infof.grid(row=2, column=0, sticky='we')
infof.columnconfigure(1, weight=1)

pausebtn = Button(infof, text='Pause', width=8, command=pause)
pausebtn.grid(row=0, column=0)
langbtn = Button(infof, text='Eng', width=8, command=lambda: change_language(russian if lang == 'Eng' else english))
langbtn.grid(row=0, column=1)

Label(infof).grid(row=0, column=1, sticky='we')
instructionbtn = Button(infof, text='Instructions', width=12,
                        command=lambda: messagebox.showinfo('Instructions', 'This is DigTreasure game:\n' \
                                                            + '1) To complete the level you have to score as much money as you can see in the right top corner\n' \
                                                            + '2) Fire is your emeny\n' \
                                                            + '3) To increase your health use aid kid\n' \
                                                            + '4) Use Right and Left button to navigate and Down button to dig\n' \
                                                            + 'Good luck and have fun!\n'))
instructionbtn.grid(row=0, column=2)

aboutbtn = Button(infof, text='About', width=8,
                  command=lambda: messagebox.showinfo('About', 'This game was created by:\n' \
                                                      + 'johnkim7\n vmmnnn \n name570\n for fun and as a project for python course'))
aboutbtn.grid(row=0, column=3)

tk.bind_all('<Left>', lambda *_: cmd(logics.Command.left))
tk.bind_all('<Right>', lambda *_: cmd(logics.Command.right))
tk.bind_all('<Up>', lambda *_: cmd(logics.Command.next))
tk.bind_all('<Down>', lambda *_: cmd(logics.Command.down))
tk.after(0, lambda *_: threading.Thread(target=game_controller).start())

tk.protocol('WM_DELETE_WINDOW', lambda: end_game(tk))

mainloop()
