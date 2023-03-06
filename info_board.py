"""Module which provides the info_board frame which displays information such as: number of remaining flags,
restart button and timer"""
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk


class InfoBoard(ttk.Frame):
    def __init__(self, grid_instance):
        super().__init__(relief='sunken')

        self.grid_instance = grid_instance

        options = {'padx': 5, 'pady': 5}

        # access flag count from the grid
        self.grid_columnconfigure([0, 1, 2], weight=1)

        # Create the flag label displaying the count
        self.counter = tk.Label(self)
        self.counter.grid(row=0, column=0, sticky='w', **options)
        self._update_frame()

        # Load the smiley image
        self.smiley_face = Image.open('smiley_face.png')
        self.smiley_face = self.smiley_face.resize((30, 30))
        self.smile = ImageTk.PhotoImage(self.smiley_face)
        # Load the dead face image
        self.dead_face = Image.open('dead_face.png')
        self.dead_face = self.dead_face.resize((30, 30))
        self.dead = ImageTk.PhotoImage(self.dead_face)
        # Load the winning face image
        self.winning_face = Image.open('winning_face.png')
        self.winning_face = self.winning_face.resize((30, 30))
        self.win = ImageTk.PhotoImage(self.winning_face)

        # Create restart button
        self.restart_btn = tk.Button(self, image=self.smile, width=30, height=30)
        self.restart_btn.grid(column=1, row=0, **options)

        self.restart = False
        # self.restart_btn.bind('<Button-1>', self.restart_the_game)

        # Create time label
        self.seconds = -1
        self.time_lbl = tk.Label(self, text=str(self.seconds).zfill(3))
        self.time_lbl.grid(row=0, column=2, sticky='e', **options)
        self._update_timer()

    # Function that check if the value of counter was updated every 0.1 second
    def _update_frame(self):
        self.counter.config(text=str(self.grid_instance.count).zfill(3))
        # Change the face expression if the player loses
        if self.grid_instance.is_loser:
            self.restart_btn.config(image=self.dead)
        elif self.grid_instance.is_winner:
            self.restart_btn.config(image=self.win)
        try:
            self.after(100, self._update_frame)
        except NameError as e:
            print('error')

    def _update_timer(self):
        self.seconds += 1
        self.time_lbl.config(text=str(self.seconds).zfill(3))
        if self.grid_instance.is_loser:
            return
        elif self.grid_instance.is_winner:
            return
        self.after(1000, self._update_timer)