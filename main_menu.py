import operator
from tkinter import *
from tkinter import messagebox

lang = 'Eng'
english = ['Eng', 'Menu', 'Please, input your name:', 'Welcome to Digging Treasure game!', 'New Game', 'View top',
           'Top 10 best players', 'Invalid name', 'Name must be entered']
russian = ['Рус', 'Меню', 'Please, input your name:', 'Добро пожаловать в игру спрятанные сокровища!', 'Новая игра',
           'Посмотреть лучших', 'Топ 10 лучших игроков', 'Неверное имя', 'Имя должно быть введено']


def main_menu(player):
    root = Tk()
    root.title("Menu")

    frame_image = Frame(root)
    frame_image.grid(row=0, column=0, rowspan=8)

    background_image = PhotoImage(master=root, file='gifes/brick.png')
    label = Label(frame_image)
    label["image"] = background_image
    label.grid(row=0, column=0, sticky=E + W + S + N)

    frame_input = Frame(frame_image)
    frame_input.grid(row=0, column=0, rowspan=3)
    name = StringVar()
    name_entry = Entry(frame_input, textvariable=name)
    name_label = Label(frame_input, text='Please, input your name:', font=("Helvetica", 10), bg="brown", fg="white")
    label = Label(frame_input, text='Welcome to Digging Treasure game!', font=("Helvetica", 11, "bold italic"),
                  bg="brown", fg="white")
    name_entry.grid(row=2, column=0, sticky=E + W + S + N)
    name_label.grid(row=1, column=0, sticky=E + W + S + N)
    label.grid(row=0, column=0, sticky=E + W + S + N)

    button_frame = Frame(frame_image)
    button_frame.grid(row=3, column=0, columnspan=1)

    new_game_button = Button(button_frame, text='New Game', width=8, bg="green", font=("Helvetica", 8, "bold italic"),
                             fg="white",
                             command=lambda: new_game(root, name.get(), russian if lang == 'Eng' else english))
    new_game_button.grid(row=0, column=0)

    view_top_button = Button(button_frame, text='View top', width=8, bg="blue", font=("Helvetica", 8, "italic"),
                             fg="white", command=lambda: load_top_from_file(russian if lang == 'Eng' else english))
    view_top_button.grid(row=0, column=1)

    lang_button = Button(button_frame, text='Eng', width=8, bg="red", font=("Helvetica", 8, "italic"), fg="white",
                         command=lambda: change_language(russian if lang == 'Eng' else english))
    lang_button.grid(row=0, column=2)

    root.protocol('WM_DELETE_WINDOW', lambda: exit_menu(root))
    root.mainloop()
    player.set_name(name.get())


def change_language(language):
    lang_button.config(text=language[0])
    root.title(language[1])
    name_label.config(text=language[2])
    label.config(text=language[3])
    new_game_button.title(language[4])
    view_top_button.config(text=language[5])


def new_game(root, name, language):
    if name == "":
        messagebox.showinfo(language[7], language[8])
    else:
        root.destroy()
    return


def exit_menu(root):
    root.destroy()
    exit(0)


def load_top_from_file(language):
    top_players = {}
    file = open("scoreboard.txt", 'r')
    for line in file:
        if line != "\n":
            a = line.split(',')
            name = a[0]
            score = int(a[1])
            top_players[name] = score

    file.close()

    top = Tk()
    top.title(language[6])
    top.geometry("600x300")

    frame = Frame(top)
    frame.grid(row=0, column=0)

    background_image = PhotoImage(master=frame, file='gifes/cup.png')
    label = Label(frame)
    label["image"] = background_image
    label.grid(row=0, column=0, sticky=E + W + S + N)

    frame_text = Frame(top)
    frame_text.grid(row=0, column=1)

    for i in range(1, 11):
        if not (top_players):
            break
        curr_player_score = max(iter(top_players.items()), key=operator.itemgetter(1))
        label = Label(frame_text, text=curr_player_score[0], fg="green", font="Helvetica")
        label.grid(row=i, column=0)
        label = Label(frame_text, text=curr_player_score[1], fg="red", font="Helvetica")
        label.grid(row=i, column=1)
        del top_players[curr_player_score[0]]

    top.mainloop()


def insert_or_update_result(name, score):
    top_players = {}
    file = open("scoreboard.txt", 'r')
    for line in file:
        if line != "\n":
            a = line.split(',')
            top_players[a[0]] = int(a[1])
    file.close()
    if name in top_players.keys():
        if (top_players[name] < score):
            top_players[name] = score
    else:
        top_players[name] = score
    file = open("scoreboard.txt", 'w')
    for i in top_players:
        file.write(i + ',' + str(top_players[i]) + '\n')
    file.close()
