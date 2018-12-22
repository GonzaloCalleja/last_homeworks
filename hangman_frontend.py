from tkinter import *
from os import path
from PIL import ImageTk, Image
import hangman_backend


class HangmanGUI(object):

    def __init__(self):

        # GENERAL SCREEN SETTINGS

        self.tk = Tk(screenName="Hangman")

        self.bgcolor = "grey"
        self.tk.title("Poker")
        self.tk.geometry("900x400")

        self.frame = Frame(master=self.tk, bg=self.bgcolor)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=BOTH, expand=1)

        self.general_frame = Frame(master=self.frame, bg=self.bgcolor, height=90)
        self.general_frame.pack(fill=X)

        self.label = Label(self.general_frame, text="Hangman Game", bg=self.bgcolor, fg="white")
        self.label.place(x=300, y=20)
        self.label.config(font=("Courier", 30))

        # Game Settings
        self.word_images = []
        self.letters = []
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.max_errors = 6
        self.bk = hangman_backend.Backend()

        # Loading Images
        self.load_images()
        self.load_letters()
        im = Image.open(path.join(self.img_dir, "_BlankTile.png"))
        im = im.resize((35, 35), Image.ANTIALIAS)
        im1 = ImageTk.PhotoImage(im)
        self.blank_image = im1

        # Screens GUI
        self.start_screen_gui()
        self.game_screen_gui()

        self.tk.mainloop()

    def start_screen_gui(self):
        self.start_game_frame = Frame(master=self.frame, bg=self.bgcolor)
        self.start_game_frame.pack(fill=BOTH, expand=1)

        self.frame_one = Frame(master=self.start_game_frame, bg=self.bgcolor)
        self.frame_one.place(x=835, y=50, anchor="ne")

        self.listbox = Listbox(master=self.frame_one, height=10, width=40, font=("Times New Roman", 15))
        self.listbox.grid(row=0, column=0, rowspan=8, columnspan=2)

        self.scroll = Scrollbar(master=self.frame_one)
        self.scroll.grid(row=0, column=1, rowspan=8, sticky="nse")
        self.scroll.configure(command=self.listbox.yview)

        # Add the buttons
        self.play_btn = Button(master=self.start_game_frame, text="Play", width=10, font=("Courier", 15),
                               command=lambda: self.play())
        self.play_btn.place(x=50, y=30, anchor="nw")

        self.info_adding = Label(master=self.start_game_frame, text="Add a word to the Game:", bg=self.bgcolor,
                                 font=("Courier", 10))
        self.info_adding.place(x=30, y=100, anchor="nw")

        self.add_word_btn = Button(master=self.start_game_frame, text="Submit", width=10, font=("Courier", 10),
                                   command=lambda: self.add_word())
        self.add_word_btn.place(x=275, y=130, anchor="nw")

        self.name_text = StringVar()
        self.entry_word = Entry(master=self.start_game_frame, textvariable=self.name_text, font=("Courier", 15))
        self.entry_word.place(x=30, y=130, anchor="nw")

        self.invalid_word = Label(self.start_game_frame, text="Invalid word", bg="white", fg="red", font=("Courier", 8))

        self.score_info = Frame(master=self.start_game_frame, borderwidth=1, bg=self.bgcolor, height=100, width=150,
                                relief=GROOVE)
        self.score_info.place(x=80, y=190, anchor="nw")

        self.scoreboard_label = Label(master=self.start_game_frame, text="Scoreboard:", bg=self.bgcolor,
                                      font=("Courier", 10))
        self.scoreboard_label.place(x=50, y=180, anchor="nw")

        self.wins = Label(self.score_info, text="Wins: " + str(self.bk.get_win()), bg=self.bgcolor, fg="green",
                          font=("Times New Roman", 15))
        self.wins.place(x=20, y=15, anchor="nw")

        self.loss = Label(self.score_info, text="Loses " + str(self.bk.get_lost()), bg=self.bgcolor, fg="red",
                          font=("Times New Roman", 15))
        self.loss.place(x=22, y=50, anchor="nw")

        self.view_games_btn = Button(master=self.start_game_frame, text="View Games", width=10, font=("Courier", 15),
                                     command=lambda: self.view_games())
        self.view_games_btn.grid(row=2, column=0)
        self.view_games_btn.place(x=600, y=0, anchor="ne")

        self.view_words_btn = Button(master=self.start_game_frame, text="View Words", width=10, font=("Courier", 15),
                                     command=lambda: self.view_words())
        self.view_words_btn.place(x=800, y=0, anchor="ne")

    def game_screen_gui(self):
        self.game_frame = Frame(master=self.frame, bg=self.bgcolor)

        self.letter_frame = Frame(master=self.game_frame, bg=self.bgcolor)

        self.image_canvas = Canvas(master=self.game_frame, bg="green", highlightthickness=0, height=250, width=250)
        self.image_canvas.place(x=620, y=20)

        self.frame_solution = Frame(master=self.game_frame, bg="darkgray", width=600, height=60)
        self.frame_solution.place(x=10, y=20, anchor="nw")

        for i in range(len(self.alphabet)):
            self.letters.append(Button(master=self.letter_frame, image=self.letter_images[i], relief="flat"))
            if i < len(self.alphabet) // 2:
                self.letters[i].grid(row=0, column=i + 1)
            else:
                self.letters[i].grid(row=1, column=i + 1 - (len(self.alphabet) // 2))

        self.restart_btn = Button(master=self.game_frame, text="Play Again", font=("Courier", 20),
                                  command=lambda: self.play())
        self.restart_btn.place(x=370, y=230, anchor="n")

        self.restart_btn = Button(master=self.game_frame, text="Back", font=("Courier", 20),
                                  command=lambda: self.back())
        self.restart_btn.place(x=150, y=230, anchor="n")

        self.win_label = Label(self.game_frame, text="You Won!!", bg=self.bgcolor, fg="green",
                               font=("Times New Roman", 40))
        self.loose_label = Label(self.game_frame, text="You Lost!!", bg=self.bgcolor, fg="red",
                                 font=("Times New Roman", 40))

        self.score_frame = Frame(master=self.game_frame, bg=self.bgcolor)
        self.victories = Label(self.score_frame, text="Wins: " + str(self.bk.get_win()), bg=self.bgcolor, fg="green",
                               font=("Times New Roman", 15))
        self.victories.pack(fill=X, expand=1)

        self.loses = Label(self.score_frame, text="Loses " + str(self.bk.get_lost()), bg=self.bgcolor, fg="red",
                           font=("Times New Roman", 15))
        self.loses.pack(fill=X, expand=1)

    def load_images(self):

        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")

        self.size = 500, 500
        self.images = []

        for i in range(self.max_errors):
            im = Image.open(path.join(self.img_dir, str(i+1)+".gif"))
            # im.thumbnail(self.size)
            im = im.resize((250, 250), Image.ANTIALIAS)
            im1 = ImageTk.PhotoImage(im)
            self.images.append(im1)

    def load_letters(self):

        self.size = 20, 20
        self.letter_images = []
        for i in range(26):
            im = Image.open(path.join(self.img_dir, self.alphabet[i] +".png"))
            # im.thumbnail(self.size)
            im = im.resize((35, 35), Image.ANTIALIAS)
            im1 = ImageTk.PhotoImage(im)
            self.letter_images.append(im1)

    def select(self, index):

        guessed = False

        for i, letter in enumerate(self.solution):
            if letter == self.alphabet[index]:
                temp = list(self.hidden)
                temp[i] = letter
                self.hidden = "".join(temp)

                self.word_images[i].config(image=self.letter_images[self.alphabet.index(letter)])

                guessed = True

        self.letters[index].config(bg="dim gray", command=lambda: i)

        if not guessed:
            self.errors += 1
            self.image_canvas.create_image(0, 0, image=self.images[self.errors - 1], anchor='nw')
            if self.max_errors <= self.errors:
                self.lose()

        if "".join(self.hidden.split()) == self.solution:
            self.win()

    def back(self):
        self.game_frame.pack_forget()
        self.start_game_frame.pack(fill=BOTH, expand=1)

    def play(self):

        # Changing from screen
        self.start_game_frame.pack_forget()
        self.game_frame.pack(fill=BOTH, expand=1)
        self.win_label.place_forget()
        self.loose_label.place_forget()
        self.score_frame.place_forget()
        self.letter_frame.place(x=550, y=120, anchor="ne")
        self.frame_solution.config(bg="darkgray")

        # Clering all variables
        self.solution = self.bk.get_random_word()
        print(self.solution)
        self.hidden = ""
        self.errors = 0
        if self.word_images:
            for image in self.word_images:
                image.place_forget()
        self.word_images = []
        self.image_canvas.create_image(0, 0, image=self.images[self.errors], anchor='nw')
        for i, letter in enumerate(list(self.solution)):

            self.hidden += "_"
            self.word_images.append(Label(master=self.frame_solution, image=self.blank_image))
            # Long words don't fit otherwise
            if len(self.solution) > 13:
                self.word_images[i].place(x=10 + i * 35, y=10, anchor="nw")
            else:
                self.word_images[i].place(x=10 + i*45, y=10, anchor="nw")

        for i in range(len(self.alphabet)):
            self.letters[i].config(bg="gray90", command=lambda i=i: self.select(i))

    def win(self):
        self.frame_solution.config(bg="green")
        self.bk.add_game(self.bk.get_word_id(self.solution), self.errors, True)
        self.letter_frame.place_forget()

        self.win_label.place(x=70, y=100, anchor="nw")
        self.victories.config(text="Wins: " + str(self.bk.get_win()))
        self.score_frame.place(x= 340, y =115, anchor="nw")

    def lose(self):
        self.frame_solution.config(bg="red")
        self.bk.add_game(self.bk.get_word_id(self.solution), self.errors, False)
        self.letter_frame.place_forget()

        self.loose_label.place(x=70, y=100, anchor="nw")
        self.victories.config(text="Loses: " + str(self.bk.get_lost()))
        self.score_frame.place(x=340, y=115, anchor="nw")

    def view_games(self):
        self.listbox.delete(0, END)
        rows = self.bk.view_all_games()
        for line in rows:
            result = "Lost"
            if line[3]:
                result = "Won"

            txt = "{:*>4d}   Word: {:<15s} Tries: {:1d}   ".format(line[0], self.bk.get_word(line[1]), line[2])
            txt += result
            self.listbox.insert(END, txt)

    def view_words(self):
        self.listbox.delete(0, END)
        rows = self.bk.view_all_words()
        for line in rows:
            txt = "{:*>4d}  {}".format(line[0], line[1])
            self.listbox.insert(END, txt)

    def add_word(self):
        word = self.name_text.get().lower()
        for letter in word:
            if not "a" <= letter <= "z":
                self.invalid_word.place(x=160, y=133, anchor="nw")
                break
        else:
            self.bk.add_word(word)
            self.invalid_word.grid_forget()


if __name__ == "__main__":
    g = HangmanGUI()

# ORIGINAL VERSION - WITHOUT GUI
# solution = input("Choose a word: ")
# hidden = ""
# errors = ""
# max_errors = 5
# for letter in solution:
#     hidden += "_ "
#
# while hidden != solution and len(errors) < max_errors:
#
#     if len(errors) > 0:
#         print("\nWrong letters you have tried: ", end="")
#         for letter in errors:
#             print(letter, end=" ")
#
#     print("\nWord to find: ", end="")
#     for letter in hidden:
#         print(letter, end=" ")
#
#     attempt = input("\nTry a letter: ") + " "
#     found = False
#
#     if attempt in hidden or attempt in errors:
#         print("\nYou already tried with ", attempt)
#         continue
#
#     for i, letter in enumerate(solution):
#         if letter == attempt:
#             temp = list(hidden)
#             temp[i] = letter
#             hidden = "".join(temp)
#             found = True
#
#     if found:
#         print("Congrats! The letter is in the word")
#     else:
#         errors += attempt
#         print("Sorry wrong letter, you have", max_errors-len(errors),"errors left")
#
# if len(errors) == max_errors:
#     print("\nYou lost!")
# else:
#     print("\nYou won!")