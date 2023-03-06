"""level.py module was created to set the difficulty level of the game. After selecting particular option, the level
is saved to a file, so after rerunning the program difficulty level is the same as it was recently selected"""


class Level:
    def __init__(self):
        self.cell_size = 20
        with open('level.txt', 'r') as file:
            # Read the entire file content and store it in a variable
            file_content = file.read()
        if file_content == 'beginner' or file_content == '':
            self.set_beginner()
        elif file_content == 'intermediate':
            self.set_intermediate()
        elif file_content == 'expert':
            self.set_expert()

    def set_beginner(self):
        self.width = 9
        self.height = 9
        self.q_mines = 10
        self.level = 0
        with open('level.txt', mode='w', encoding='utf-8') as file:
            file.write('beginner')
    def set_intermediate(self):
        self.width = 16
        self.height = 16
        self.q_mines = 40
        self.level = 1
        with open('level.txt', mode='w', encoding='utf-8') as file:
            file.write('intermediate')
    def set_expert(self):
        self.width = 30
        self.height = 16
        self.q_mines = 99
        self.level = 2
        with open('level.txt', mode='w', encoding='utf-8') as file:
            file.write('expert')