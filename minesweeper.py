"""This module provides the Minesweeper game logic and interactions between game objects.
It contains main() function which is responsible for running the Minesweeper game."""

import tkinter as tk
from level import Level
from info_board import InfoBoard
from grid import Grid


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Minesweeper')
        self.geometry('+600+200')
        self.resizable(False, False)
        self.level = Level()

        self.draw_window()
        self.info_board.restart_btn['command'] = self.destroy_game
        self.generate_menu()

    def draw_window(self):
        self.grid = Grid(height=self.level.height, width=self.level.width, q_mines=self.level.q_mines,
                         cell_size=self.level.cell_size)
        self.info_board = InfoBoard(self.grid)
        self.info_board.restart_btn['command'] = self.destroy_game
        self.info_board.pack(fill=tk.BOTH)
        self.grid.pack()

    def generate_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.level_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.level_menu.add_command(label='Beginner', command=self.change_level_beginner)
        self.level_menu.add_command(label='Intermediate', command=self.change_level_medium)
        self.level_menu.add_command(label='Expert', command=self.change_level_expert)
        self.menu_bar.add_cascade(label='Level', menu=self.level_menu)

    def change_level_beginner(self):
        self.level.set_beginner()
        self.destroy_game()

    def change_level_medium(self):
        self.level.set_intermediate()
        self.destroy_game()

    def change_level_expert(self):
        self.level.set_expert()
        self.destroy_game()

    def destroy_game(self):
        self.grid.destroy()
        self.info_board.destroy()
        self.draw_window()


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
