"""grid.py module is responsible for creating grid object, which generateds game interface."""

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import random


class Grid(ttk.Frame):
    def __init__(self, width, height, q_mines, cell_size):
        super().__init__(relief='sunken')

        self.width = width
        self.height = height
        self.q_mines = q_mines
        self.cell_size = cell_size
        self.count = q_mines
        # Load the mine image
        self.mine_image = Image.open('mine.png')
        self.mine_image = self.mine_image.resize((24, 18))
        self.mine = ImageTk.PhotoImage(self.mine_image)

        # Load the flag image
        self.flag_image = Image.open('flag.png')
        self.flag_image = self.flag_image.resize((20, 20))
        self.flag = ImageTk.PhotoImage(self.flag_image)

        # Load cross out mine
        self.crossed_mine_image = Image.open('crossed_mine.png')
        self.crossed_mine_image = self.crossed_mine_image.resize((20, 20))
        self.crossed_mine = ImageTk.PhotoImage(self.crossed_mine_image)

        # Load mine with red background
        self.red_mine_image = Image.open('red_mine.png')
        self.red_mine_image = self.red_mine_image.resize((20, 20))
        self.red_mine = ImageTk.PhotoImage(self.red_mine_image)
        #
        self.buttons = {}
        self.canvas = {}
        self.visited = set()
        self._create_widgets()
        self._locate_bombs()
        self._locate_hint_markups()
        self.is_winner = False
        self.is_loser = False

    def _create_widgets(self):
        # Create unique buttons and grid
        for x in range(self.width):
            for y in range(self.height):
                # Create canvas
                self.canvas[(x, y)] = tk.Canvas(self, width=self.cell_size + 3, height=self.cell_size + 3)
                x0 = self.width * 20
                y0 = self.height * 20
                x1 = x0 + 20
                y1 = y0 + 20
                self.canvas[(x, y)].create_rectangle(x0, y0, x1, y1)
                self.canvas[(x, y)].grid(column=x, row=y, sticky='nsew')
                # Create button
                self.buttons[(x, y)] = tk.Button(self, image='', width=2, height=1)
                # bind the button with specific mouse clicks
                self.buttons[(x, y)].bind('<Button-3>', lambda event, x=x, y=y: self.on_right_press(event, x, y))
                self.buttons[(x, y)].bind('<Button-1>',
                                          lambda event, x=x, y=y: self.on_left_press(event, x, y, self.visited))
                self.buttons[(x, y)].grid(column=x, row=y, sticky='nsew')

    def _locate_bombs(self):
        b = list(self.canvas.keys())
        random.shuffle(b)
        mine_locations = []
        for _ in range(self.q_mines):
            loc = b.pop()
            mine_locations.append(loc)
            # put a mine at specific location
            self.canvas[loc].create_image(12, 13, image=self.mine, tags='mine')

    def _locate_hint_markups(self):
        # Iterate through all the canvas locations to figure out what to put on each field
        for key in self.canvas.keys():
            mine_item = self.canvas[key].find_withtag('mine')
            # If canvas has 'image' tags it means there is a mine
            if mine_item:
                continue
            # find out if there are some Q_mines around
            else:
                x, y = key
                # Check all locations around position (x, y)
                locations_around = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                                    (x - 1, y), (x + 1, y),
                                    (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
                # Count all mine occurrences around position (x, y)
                count = 0
                for loc in locations_around:
                    # Exclude all the locations which are out of the board
                    if loc not in list(self.canvas.keys()):
                        continue
                    # Add to a count if there is a mine
                    elif self.canvas[loc].find_withtag('mine'):
                        count += 1
                # Give the number of Q_mines around that field
                if count != 0:
                    bold_font = ("Helvetica", 12, "bold")
                    text_item = self.canvas[key].create_text(12, 12, text=str(count), tags='text')
                    if count == 1:
                        self.canvas[key].itemconfig(text_item, fill="blue", font=bold_font)
                    elif count == 2:
                        self.canvas[key].itemconfig(text_item, fill="green", font=bold_font)
                    elif count == 3:
                        self.canvas[key].itemconfig(text_item, fill="red", font=bold_font)
                    elif count == 4:
                        self.canvas[key].itemconfig(text_item, fill="#0e0031", font=bold_font)
                    elif count == 6:
                        self.canvas[key].itemconfig(text_item, fill='#00cccc', font=bold_font)

    def on_right_press(self, event, x, y):
        # Check if there is a flag mark on the button an 'lock'
        if self.buttons[(x, y)].cget('image') == "":
            self.count -= 1
            self.buttons[(x, y)].configure(image=self.flag, width=20, height=20)
            self.buttons[(x, y)].unbind('<Button-1>')
        else:
            self.count += 1
            self.buttons[(x, y)].configure(image='', width=2, height=1)
            self.buttons[(x, y)].bind('<Button-1>',
                                      lambda event,
                                             x=x,
                                             y=y: self.on_left_press(event, x, y, self.visited))

        # Check winning conditions
        if len(self.visited) == self.width * self.height - self.q_mines and self.count == 0:
            self.is_winner = True
            print('Winner')
            return

    # Method which process the action after lest-mouse-press
    def on_left_press(self, event, x, y, visited):

        self.buttons[(x, y)].destroy()

        # Check if there is a mine under the button. If so lock all remaining buttons.
        if self.canvas[(x, y)].find_withtag('mine'):
            self.canvas[(x, y)].create_image(12, 13, image=self.red_mine)
            self.is_loser = True
            for location, button in self.buttons.items():
                if not button.winfo_exists():
                    continue
                elif self.canvas[location].find_withtag('mine'):
                    button.destroy()
                elif button.cget('image') and not self.canvas[location].find_withtag('mine'):
                    button.destroy()
                    self.canvas[location].create_image(12, 13, image=self.crossed_mine)
                else:
                    button.config(state='disabled')
                    button.unbind('<Button-1>')
                    button.unbind('<Button-3>')
            return
        # if the field was visited or there is some image return
        if (x, y) in self.visited or self.canvas[(x, y)].find_withtag('mine'):
            return

        # Mark the current cell as visited
        self.visited.add((x, y))
        print(len(self.visited))
        # Check winning conditions:
        if len(self.visited) == self.width * self.height - self.q_mines and self.count == 0:
            self.is_winner = True
            print('Winner')
            return
        # Check if the location is 'empty field' - no text nor image
        if not (self.canvas[(x, y)].find_withtag('text') or self.canvas[(x, y)].find_withtag('mine')):
            # Now scan the fields around that empty field
            for location in [(x - 1, y), (x, y - 1),
                             (x + 1, y), (x, y + 1),
                             (x - 1, y - 1), (x + 1, y - 1),
                             (x - 1, y + 1), (x + 1, y + 1)]:

                # Check if location is on the grid
                x, y = location
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Check if that location is a button
                    if self.buttons[(x, y)] is not None:
                        # If it is text or empty field destroy that button
                        if not self.canvas[location].find_withtag('mine'):
                            self.on_left_press(event, x, y, visited)
