import tkinter as tk
from pathlib import Path
import random
from numpy import array_equal, copy, zeros, any

_GRID_SIZE = 4


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_iconbitmap('2048.ico')
        self.title("2048")
        self.minsize(272, 350)
        self.tab = []
        self.old_tab = []
        self.random_color = random.randrange(16777215)

        # Score frame
        self.score_frame = tk.Frame(self)
        self.score_frame.pack()

        # Score label
        self.score = 0
        self.old_score = 0
        self.score_text = tk.StringVar()
        self.score_text.set('Score\n' + str(self.score))
        self.score_label = tk.Label(self.score_frame, textvariable=self.score_text, font=("Arial", 16),
                                    width=11, borderwidth=1, relief="ridge")
        self.score_label.pack(side=tk.LEFT)

        # Best score label
        self.best = 0
        try:
            self.best = int(Path('score.txt').read_text())
        except FileNotFoundError:
            pass
        self.best_text = tk.StringVar()
        self.best_text.set('Best\n' + str(self.best))
        self.best_label = tk.Label(self.score_frame, textvariable=self.best_text, font=("Arial", 16),
                                   width=11, borderwidth=1, relief="ridge")
        self.best_label.pack(side=tk.RIGHT)

        # Button frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        # Restart button
        restart_button = tk.Button(self.button_frame, text="Restart", command=self.restart, font=("Arial", 10),
                                   width=16, borderwidth=1, relief="ridge")
        restart_button.pack(side=tk.LEFT)
        # Undo button
        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo, font=("Arial", 10),
                                     width=16, borderwidth=1, relief="ridge", state=tk.DISABLED)
        self.undo_button.pack(side=tk.RIGHT)

        # Game grid
        self.grid = tk.Frame(self)
        self.grid.pack()

        # You win label
        self.win_label = tk.Label(self, text="You win!", font=("Arial", 16))
        self.win_label.pack_forget()
        # Continue button
        self.continue_button = tk.Button(self, text="Continue", command=self.continue_game, font=("Arial", 10),
                                         width=33, borderwidth=1, relief="ridge")
        self.continue_button.pack_forget()
        # Game over label
        self.defeat_label = tk.Label(self, text="Game over!", font=("Arial", 16))
        self.defeat_label.pack_forget()

        self.start()

    def start(self):
        self.tab = zeros((_GRID_SIZE, _GRID_SIZE), dtype=int)
        self.old_tab = zeros((_GRID_SIZE, _GRID_SIZE), dtype=int)

        self.score = 0
        self.old_score = 0
        self.update_score()

        self.random_tile()
        self.random_tile()

        self.bind_key()

    def random_tile(self):
        random_row = random.randrange(_GRID_SIZE)
        random_column = random.randrange(_GRID_SIZE)

        while self.tab[random_row][random_column] != 0:
            random_row = random.randrange(_GRID_SIZE)
            random_column = random.randrange(_GRID_SIZE)

        if random.randrange(10) < 8:
            self.tab[random_row][random_column] = 2  # 8% chance
        else:
            self.tab[random_row][random_column] = 4  # 2% chance
        self.display_tab()

    def bind_key(self):
        self.bind("<Up>", lambda e: self.key_up_pressed())
        self.bind("<Down>", lambda e: self.key_down_pressed())
        self.bind("<Right>", lambda e: self.key_right_pressed())
        self.bind("<Left>", lambda e: self.key_left_pressed())

    def unbind_key(self):
        self.unbind("<Up>")
        self.unbind("<Down>")
        self.unbind("<Right>")
        self.unbind("<Left>")

    def restart(self):
        self.random_color = random.randrange(16777215)
        self.start()
        # You win label
        self.win_label.destroy()
        self.win_label = tk.Label(self, text="You win!", font=("Arial", 16))
        # Continue button
        self.continue_button.destroy()
        self.continue_button = tk.Button(self, text="Continue", command=self.continue_game, font=("Arial", 10),
                                         width=33, borderwidth=1, relief="ridge")
        # Game over label
        self.defeat_label.destroy()
        self.defeat_label = tk.Label(self, text="Game over!", font=("Arial", 16))
        self.undo_button['state'] = tk.DISABLED

    def undo(self):
        if any(self.old_tab) and not array_equal(self.tab, self.old_tab):
            self.tab = self.old_tab.copy()
            self.display_tab()
            self.score = self.old_score
            self.score_text.set('Score\n' + str(self.score))
            self.undo_button['state'] = tk.DISABLED

    def continue_game(self):
        self.win_label.destroy()
        self.continue_button.destroy()
        self.bind_key()
        self.undo_button['state'] = tk.NORMAL

    def update_score(self):
        self.score_text.set('Score\n' + str(self.score))
        if self.best < self.score:
            self.best = self.score
            self.best_text.set('Best\n' + str(self.best))
            Path('score.txt').write_text(str(self.best))

    def display_tab(self):
        for label in self.grid.winfo_children():
            label.destroy()
        for x in range(_GRID_SIZE):
            for y in range(_GRID_SIZE):
                if self.tab[x][y] == 0:
                    label = tk.Label(self.grid, text=None, font=("Arial", 20),
                                     width=4, height=2, borderwidth=1, relief="ridge")
                elif self.tab[x][y] % 2 != 0:
                    self.tab[x][y] += 1
                    label = tk.Label(self.grid, text=self.tab[x][y], font=("Arial", 20),
                                     width=4, height=2, borderwidth=1, relief="ridge", underline=0)
                else:
                    label = tk.Label(self.grid, text=self.tab[x][y], font=("Arial", 20),
                                     width=4, height=2, borderwidth=1, relief="ridge")
                # Colors
                if self.tab[x][y] != 0:
                    label.config(bg="#" + '{0:06X}'.format(self.tab[x][y] * 20 + self.random_color))
                label.grid(row=x, column=y)

    def update_tab(self):
        self.undo_button['state'] = tk.NORMAL
        defeat = 1
        for x in range(_GRID_SIZE):
            for y in range(_GRID_SIZE):
                if self.win_label.winfo_exists():
                    # check win
                    if self.tab[x][y] == 2048:
                        self.win_label.pack()
                        self.continue_button.pack()
                        self.unbind_key()
                        self.undo_button['state'] = tk.DISABLED
                # defeat
                if self.tab[x][y] == 0:
                    defeat = 0
                else:
                    # check x
                    if 0 <= x < _GRID_SIZE - 1:
                        if self.tab[x][y] == self.tab[x + 1][y]:
                            defeat = 0
                    # check y
                    if 0 <= y < _GRID_SIZE - 1:
                        if self.tab[x][y] == self.tab[x][y + 1]:
                            defeat = 0
        if defeat == 1:
            self.defeat_label.pack()
            self.unbind_key()
            self.undo_button['state'] = tk.DISABLED

    def move_up(self):
        move = 0
        self.old_tab = copy(self.tab)
        self.old_score = self.score
        for row in range(_GRID_SIZE):
            for column in range(_GRID_SIZE):
                # merge
                if self.tab[column][row] != 0:
                    i = 1
                    while column + i < _GRID_SIZE and self.tab[column + i][row] != self.tab[column][row] \
                            and self.tab[column + i][row] == 0:
                        i += 1
                    if column + i < _GRID_SIZE and self.tab[column + i][row] == self.tab[column][row]:
                        self.tab[column][row] *= 2
                        self.score += self.tab[column][row]
                        self.update_score()
                        self.tab[column][row] -= 1
                        self.tab[column + i][row] = 0
                        move = 1
                # move
                if self.tab[column][row] != 0 and column != 0:
                    i = 0
                    while i < _GRID_SIZE and self.tab[i][row] != 0:
                        i += 1
                    if i < column and self.tab[i][row] == 0:
                        self.tab[i][row] = self.tab[column][row]
                        self.tab[column][row] = 0
                        move = 1
        return move

    def move_down(self):
        move = 0
        self.old_tab = copy(self.tab)
        self.old_score = self.score
        for row in range(_GRID_SIZE - 1, -1, -1):
            for column in range(_GRID_SIZE - 1, -1, -1):
                # merge
                if self.tab[column][row] != 0:
                    i = 1
                    while i < _GRID_SIZE and self.tab[column - i][row] != self.tab[column][row] \
                            and self.tab[column - i][row] == 0:
                        i += 1
                    if i <= column and self.tab[column - i][row] == self.tab[column][row]:
                        self.tab[column][row] *= 2
                        self.score += self.tab[column][row]
                        self.update_score()
                        self.tab[column][row] -= 1
                        self.tab[column - i][row] = 0
                        move = 1
                # move
                if self.tab[column][row] != 0 and column != _GRID_SIZE - 1:
                    i = _GRID_SIZE - 1
                    while i >= 0 and self.tab[i][row] != 0:
                        i -= 1
                    if i > column and self.tab[i][row] == 0:
                        self.tab[i][row] = self.tab[column][row]
                        self.tab[column][row] = 0
                        move = 1
        return move

    def move_right(self):
        move = 0
        self.old_tab = copy(self.tab)
        self.old_score = self.score
        for row in range(_GRID_SIZE - 1, -1, -1):
            for column in range(_GRID_SIZE - 1, -1, -1):
                # merge
                if self.tab[column][row] != 0:
                    i = 1
                    while i < _GRID_SIZE and self.tab[column][row - i] != self.tab[column][row] \
                            and self.tab[column][row - i] == 0:
                        i += 1
                    if i <= row and self.tab[column][row - i] == self.tab[column][row]:
                        self.tab[column][row] *= 2
                        self.score += self.tab[column][row]
                        self.update_score()
                        self.tab[column][row] -= 1
                        self.tab[column][row - i] = 0
                        move = 1
                # move
                if self.tab[column][row] != 0 and row != _GRID_SIZE - 1:
                    i = _GRID_SIZE - 1
                    while i >= 0 and self.tab[column][i] != 0:
                        i -= 1
                    if i > row and self.tab[column][i] == 0:
                        self.tab[column][i] = self.tab[column][row]
                        self.tab[column][row] = 0
                        move = 1
        return move

    def move_left(self):
        move = 0
        self.old_tab = copy(self.tab)
        self.old_score = self.score
        for row in range(_GRID_SIZE):
            for column in range(_GRID_SIZE):
                # merge
                if self.tab[column][row] != 0:
                    i = 1
                    while row + i < _GRID_SIZE and self.tab[column][row + i] != self.tab[column][row] \
                            and self.tab[column][row + i] == 0:
                        i += 1
                    if row + i < _GRID_SIZE and self.tab[column][row + i] == self.tab[column][row]:
                        self.tab[column][row] *= 2
                        self.score += self.tab[column][row]
                        self.update_score()
                        self.tab[column][row] -= 1
                        self.tab[column][row + i] = 0
                        move = 1
                # move
                if self.tab[column][row] != 0 and row != 0:
                    i = 0
                    while i < _GRID_SIZE and self.tab[column][i] != 0:
                        i += 1
                    if i < row and self.tab[column][i] == 0:
                        self.tab[column][i] = self.tab[column][row]
                        self.tab[column][row] = 0
                        move = 1
        return move

    def key_up_pressed(self):
        if self.move_up() == 1:
            self.random_tile()
            self.update_tab()

    def key_down_pressed(self):
        if self.move_down() == 1:
            self.random_tile()
            self.update_tab()

    def key_right_pressed(self):
        if self.move_right() == 1:
            self.random_tile()
            self.update_tab()

    def key_left_pressed(self):
        if self.move_left() == 1:
            self.random_tile()
            self.update_tab()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
