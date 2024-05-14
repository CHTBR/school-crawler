from drawing_functions import Drawing_functions

from tkinter import *
from random import *
import os


# Constants declarations
DIRECTIONS = ['north', 'east', 'south', 'west']
FILL_GRID = N+S+E+W
CELL_DESIGNATIONS = {
    'wall' : 0,
    'floor' : 1,
    'door' : 2,
    'question' : 3,
    'game-end' : 4
}
CD = CELL_DESIGNATIONS # Shorter name for use in code

# Global variables declarations
player_name = 'char1'


# Exception for breaking out of loops
class Loop_Break_Exception(Exception):
    def __init__(self):
        pass


# Class with methods used by a lot of other classes
class General_methods():
    def set_up_window(self, title: str, win_width: int, win_height: int, window=None):
        if window == None:
            window = self
        window.geometry('%dx%d+%d+%d'%(win_width, win_height, (self.winfo_screenwidth()-win_width)//2, (self.winfo_screenheight()-win_height)//2))
        window.configure(bg='white')
        window.title(title)
        window.resizable(width=False, height=False)

    def return_configured_grid(self, frame: Frame, row_num: int, col_num: int, row_w=1, col_w=1):
        for i in range(row_num):
            frame.rowconfigure(i, weight=row_w, uniform='rows')
        for i in range(col_num):
            frame.columnconfigure(i, weight=col_w, uniform='cols')
        return frame


# Creates a window asking for the player's name
class Player_login(Tk, General_methods):
    def __init__(self):
        super().__init__()
        self.set_up_window('Login', 400, 400)
        frame = Frame(self, background='white')
        frame = self.return_configured_grid(frame, 3, 2)
        frame = self.return_added_widgets(frame)
        frame.place(relx=.5, rely=.5, anchor=CENTER)

    def return_added_widgets(self, frame):
        Label(frame, text='Userame: ', background='white').grid(row=0, column=0, sticky=FILL_GRID)
        player_name = StringVar()
        Entry(frame, textvariable=player_name).grid(row=0, column=1, sticky=FILL_GRID)
        Label(frame, text='Password: ', background='white').grid(row=1, column=0, sticky=FILL_GRID)
        player_password = StringVar()
        Entry(frame, textvariable=player_password).grid(row=1, column=1, sticky=FILL_GRID)
        Button(frame, text='CONFIRM', command=lambda: self.check_if_login_valid(player_name, player_password)).grid(row=2, column=0, columnspan=2, sticky=FILL_GRID)
        return frame

    def check_if_login_valid(self, name, password):
        if name.get() == '' or password.get() == '':
            return
        with open('assets/login.txt', 'r') as logins_file:
            all_logins = logins_file.readlines()
        temp = []
        for login in all_logins:
            temp.append(login
                        .strip()
                        .split(';'))
        all_logins = temp
        for login in all_logins:
            if name.get() == login[0]:
                if password.get() == login[1]:
                    self.create_main_menu(name)
                    return
                return
        self.confirm_new_login(name, password)
        
    def confirm_new_login(self, name, password):
        confirm_window = Toplevel()
        self.set_up_window('Confirm New Login', 400, 200, confirm_window)
        Label(confirm_window, text='Confirm new login as:\nName: ' + name.get() + '\nPassword: ' + password.get(), background='white').pack(side=TOP)
        Button(confirm_window, text='Yes', command=lambda: (confirm_window.destroy(), self.create_new_login(name, password), self.create_main_menu(name))).place(relx=.25, rely=.75, anchor=CENTER)
        Button(confirm_window, text='No', command=lambda: confirm_window.destroy()).place(relx=.75, rely=.75, anchor=CENTER)
        confirm_window.grab_set()

    def create_new_login(self, name, password):
        with open('assets/login.txt', 'a') as logins_file:
            logins_file.write(name.get() + ';' + password.get() + '\n')

    def create_main_menu(self, name): # Set global player_name as name
        global player_name
        player_name = name.get()
        self.destroy()
        Main_screen()

     
# Creates the main menu screen
class Main_screen(Tk, General_methods):
    def __init__(self):
        super().__init__()
        self.set_up_window('Title screen', 600, 600)
        Label(self, text='Welcome ' + player_name, bg='white').place(relx=.5, y=20, anchor=CENTER)
        frame = Frame(self, bg='white')
        frame = self.return_configured_grid(frame, 4, 1)
        frame = self.return_added_widgets(frame)
        frame.place(relx=.5, rely=.5, anchor=CENTER)
    
    def return_configured_grid(self, frame: Frame, row_num: int, col_num: int, row_w=1, col_w=1):
        for i in range(row_num):
            frame.rowconfigure(i, weight=row_w, uniform='rows')
        for i in range(col_num):
            frame.columnconfigure(i, weight=col_w, uniform='cols')
        return frame
    
    def return_added_widgets(self, frame: Frame):
        Button(frame, text='START', command=lambda: self.choose_category(self.start_game)).grid(row=0, column=0, sticky=FILL_GRID)
        Button(frame, text='LEADERBOARDS', command=lambda: self.choose_category(self.show_leaderboard)).grid(row=1, column=0, sticky=FILL_GRID)
        Button(frame, text='CREDITS', command=self.show_credits).grid(row=2, column=0, sticky=FILL_GRID)
        Button(frame, text='LOG OUT', command=self.create_player_login).grid(row=3, column=0, sticky=FILL_GRID)
        return frame
    
    def choose_category(self, function):
        self.leaderboard_list_window = Toplevel()
        self.set_up_window('Category', 500, 500, self.leaderboard_list_window)
        self.leaderboard_list_window = self.return_configured_grid(self.leaderboard_list_window, 3, 1, 0)
        Button(self.leaderboard_list_window, text='Biology', command=lambda: function('biology')).grid(row=0, column=0, sticky=FILL_GRID)
        Button(self.leaderboard_list_window, text='Chemistry', command=lambda: function('chemistry')).grid(row=1, column=0, sticky=FILL_GRID)
        Button(self.leaderboard_list_window, text='Physics', command=lambda: function('physics')).grid(row=2, column=0, sticky=FILL_GRID)
        self.leaderboard_list_window.grab_set()

    def show_leaderboard(self, category: str):
        for widget in self.leaderboard_list_window.winfo_children():
            widget.destroy()
        self.leaderboard_list_window = self.return_configured_grid(self.leaderboard_list_window, 12, 2)
        list_header_lbl = Label(self.leaderboard_list_window, text=category.capitalize(), borderwidth=2, relief='solid').grid(row=0, column=0, columnspan=2, sticky=FILL_GRID)
        leaderboard_list = self.return_leaderboard_list(category)
        for i in range(10):
            player_name_lbl = Label(self.leaderboard_list_window, text=str(leaderboard_list[i][0]), borderwidth=1, relief='solid').grid(row=i+1, column=0, sticky=FILL_GRID)
            player_score_lbl = Label(self.leaderboard_list_window, text=str(leaderboard_list[i][1]), borderwidth=1, relief='solid').grid(row=i+1, column=1, sticky=FILL_GRID)
        return_button = Button(self.leaderboard_list_window, text='BACK', command=lambda: [self.leaderboard_list_window.destroy(), self.choose_category(self.show_leaderboard)]).grid(row=11, column=0, columnspan=2, sticky=FILL_GRID)

    def return_leaderboard_list(self, category: str):
        with open(os.path.join('assets', category, 'leaderboard.txt')) as leaderboard:
            leaderboard_list = leaderboard.readlines()
        temp = []
        for entry in leaderboard_list:
            temp.append(entry
                        .strip()
                        .split(';'))
        leaderboard_list = temp
        return leaderboard_list

    def show_credits(self):
        credits_window = Toplevel()
        self.set_up_window('Credits', 500, 500, credits_window)
        Label(credits_window, background='white',
              text=
'''
Everything
Filip Popelka
''').pack(side=TOP)
        credits_window.grab_set()

    def create_player_login(self):
        self.destroy()
        Player_login()

    def start_game(self, category):
        self.destroy()
        game_manager = Game_manager(category)
        Player_controler(game_manager)


# Creates the game map and creates a window displaying what the player sees
class Game_manager(Tk, General_methods, Drawing_functions):
    def __init__(self, category):
        super().__init__()
        self.category = category
        self.get_images()
        self.set_up_window('Dungeon', 600, 600)
        self.set_up_cvs()
        self.player = Player_controler
        self.question_count = 0
        self.question_text = StringVar()
        self.map = self.create_map()
        for a in range(len(self.map)):
            for b in range(len(self.map[a])):
                if self.map[a][b] == 3:
                    self.question_count += 1
        self.question_text.set('Questions: ' + str(self.question_count))
        self.score = 5002
        self.score_text = StringVar()
        self.refresh_variables()
        self.set_up_ui()
        
    def get_images(self):
        self.img = PhotoImage(file='assets/tmp.png', width=200, height=200)
        self.big_img = PhotoImage(file='assets/tmp_big.png', width=400, height=400)

    def create_map(self):
        '''
        Function for creating a game map

        Creates a grid in the form of a double layered list with the same number of rows and columns and the length of it's sides depending on the difficulty setting.
        Creates a path through said grid from the spawn to the boss.
        Creates branches from that path and puts enemies at their ends.
        '''

        grid = self.return_square_grid(25)
        while True:
            tmp_grid = self.return_map(grid)
            for x in range(len(tmp_grid)):
                if CD['question'] in tmp_grid[x]:
                    return tmp_grid

    def return_square_grid(self, length_of_side: int):
        grid=[]
        for i in range(length_of_side):
            grid.append([])
        for a in range(length_of_side):
            for b in range(length_of_side):
                grid[a].append(CD['wall'])
        return grid

    def return_map(self, grid):
        size = len(grid)-1
        start_cell = [size-4, size//2] # Start for the pathfinder
        # Creates the boss room
        boss_room_y = randint(2, size-2) 
        for a, b in zip((1, 2, 3), (CD['game-end'], CD['door'], CD['floor'])):
            if b == CD['door']:
                self.door_coords = [a, boss_room_y]
            grid[a][boss_room_y] = b
        goal_cell = [4, boss_room_y] # Goal for the pathfinder
        path = [start_cell, goal_cell] # A list containing the goal points for the pathfinder

        # Creates target cells for the path finder other than the end cell
        for row in range((size-6)//4):
            path.insert(-1, [size-(randint(0, 1)+5+4*row), randint(1, size-1)])
            
        while len(path) != 1:
            distance_to_target = path[0][0]-path[1][0]+abs(path[0][1]-path[1][1]) # Calculates the distance from the current position to the target cell
            path_branch_point = -1
            if distance_to_target > 2: #  Determines the point in the path where there will be a branch if the distance is more than 2
                path_branch_point = randint(1, distance_to_target)
            while True:
                grid[path[0][0]][path[0][1]] = 1
                distance_to_target = path[0][0]-path[1][0]+abs(path[0][1]-path[1][1]) # Updates distance to target point
                if distance_to_target == path_branch_point:
                    self.create_path_branch(path[0], grid)
                    path_branch_point = -1
                    if distance_to_target > 2: #  Determines the point in the path where there will be a branch if the distance is more than 2
                        path_branch_point = randint(1, distance_to_target)
                if path[0][0] > path[1][0]: # If the x coordinate is bigger than the target decrease the x coordinate
                    path[0][0] -= 1
                elif path[0][1] > path[1][1]: # If the y coordinate is bigger than the target decrease the y coordinate  
                    path[0][1] -= 1
                elif path[0][1] < path[1][1]: # If the y coordinate is amller than the target increase the y coordinate  
                    path[0][1] += 1
                elif path[0][0] == path[1][0] and path[0][1] == path[1][1]: # If you've reached the target point pop it from the list and break out of the loop
                    path.pop(0)
                    break
        # Creates the starting point for the player and sets their coordinates
        grid[size-1][size//2] = CD['floor']
        self.player.x = size-1
        self.player.y = size//2
        # Creates the starting room
        for x in (-4, -3):
            for y in (-1, 0, 1):
                grid[x][size//2+y] = CD['floor']
        return grid

    def create_path_branch(self, starting_cell: list, grid: list):
        size = len(grid)-1
        direction = choice(DIRECTIONS)
        try:
            current_cell_x = starting_cell[0]
            current_cell_y = starting_cell[1]
            next_cell_x = current_cell_x
            next_cell_y = current_cell_y
            for counter in range(4): # Branch can be extended at most 3 times
                tmp_direction = choice(DIRECTIONS)
                while (DIRECTIONS.index(tmp_direction)+2)%4 == DIRECTIONS.index(direction): # If new direction is opposite of current
                    tmp_direction = choice(DIRECTIONS)
                direction = tmp_direction
                for counter in range(2): # Each part of the branch is at most 2 cells long
                    match direction: # Find the next cell for each direction
                        case 'north':
                            next_cell_x = current_cell_x-1
                        case 'east':
                            next_cell_y = current_cell_y+1
                        case 'south':
                            next_cell_x = current_cell_x+1
                        case 'west':
                            next_cell_y = current_cell_y-1
                    if next_cell_x in (0, size) or next_cell_y in (0, size): # If the next cell is on the edge of the map create an enemy and end branch
                        grid[current_cell_x][current_cell_y] = CD['question']
                        raise Loop_Break_Exception
                    # If there's a door or the boss anywhere around the next cell create an enemy and end branch
                    for x in (-1, 0, 1):
                        for y in (-1, 0, 1):
                            if grid[next_cell_x+x][next_cell_y+y] in (2, 4): 
                                grid[current_cell_x][current_cell_y] = CD['question']
                                raise Loop_Break_Exception
                    current_cell_x = next_cell_x
                    current_cell_y = next_cell_y
                    grid[current_cell_x][current_cell_y] = CD['floor']              
            grid[current_cell_x][current_cell_y] = CD['question']
        except Loop_Break_Exception:
            pass

    def set_up_ui(self):
        Label(self, textvariable=self.score_text, background='black', font='Helvetica 30', foreground='yellow').place(x=300, y=30, anchor=CENTER)
        Label(self, textvariable=self.question_text, background='black', font='Helvetica 30', foreground='yellow').place(x=300, y=70, anchor=CENTER)

    def refresh_variables(self):
        if self.score <= 0:
            self.score = 0
        else:
            self.score -= 2
        self.score_text.set('Score: ' + str(self.score))
        if True: # TEST self.question_count == 0:
            self.map[self.door_coords[0]][self.door_coords[1]] = CD['floor']
        self.after(200, self.refresh_variables)
    
    def set_up_cvs(self):
        self.cvs = Canvas(self, bg='black')
        self.cvs.pack(fill='both', expand=True)

    # Finds the coordinates of the cells in the players view
    def draw_view(self, player_x, player_y, player_direction):
        self.cvs.delete('all')
        self.floor()
        self.whiteout()
        match player_direction:
            case 'north':
                self.evaluate_front_cells_north_south(player_x, player_y, forward=-1, left=-1, right=1)
            case 'east':
                self.evaluate_front_cells_east_west(player_x, player_y, forward=1, left=-1, right=1)
            case 'south':
                self.evaluate_front_cells_north_south(player_x, player_y, forward=1, left=1, right=-1)
            case 'west':
                self.evaluate_front_cells_east_west(player_x, player_y, forward=-1, left=1, right=-1)
        self.cvs.update()
        
    # Checks what kind of cell is at the given coordinates and draws a part of the player's view based on it and the keyword specifying it's place in the view
    def evaluate_cell(self, cell_num, keyword):
        match cell_num:
            case 0: # Wall
                self.wall(keyword)
            case 2: # Floor
                self.door(keyword)
            case 3: # Enemy
                self.image(keyword)      

    def evaluate_front_cells_north_south(self, player_x: int, player_y: int, forward: int, left: int, right: int):
        if self.map[player_x+forward][player_y] in (1, 3, 4):
            self.evaluate_cell(self.map[player_x+2*forward][player_y], '2Forward')
            self.evaluate_cell(self.map[player_x+2*forward][player_y+left], 'Left2Forward')
            self.evaluate_cell(self.map[player_x+2*forward][player_y+right], 'Right2Forward')
            self.evaluate_cell(self.map[player_x+forward][player_y+left], 'LeftForward')
            self.evaluate_cell(self.map[player_x+forward][player_y+right], 'RightForward')
        self.evaluate_cell(self.map[player_x+forward][player_y], 'Forward')
        self.evaluate_cell(self.map[player_x][player_y+left], 'Left')
        self.evaluate_cell(self.map[player_x][player_y+right], 'Right')

    def evaluate_front_cells_east_west(self, player_x: int, player_y: int, forward: int, left: int, right: int):
        if self.map[player_x][player_y+forward] in (1, 3, 4):
            self.evaluate_cell(self.map[player_x][player_y+2*forward], '2Forward')
            self.evaluate_cell(self.map[player_x+left][player_y+2*forward], 'Left2Forward')
            self.evaluate_cell(self.map[player_x+right][player_y+2*forward], 'Right2Forward')
            self.evaluate_cell(self.map[player_x+left][player_y+forward], 'LeftForward')
            self.evaluate_cell(self.map[player_x+right][player_y+forward], 'RightForward')
        self.evaluate_cell(self.map[player_x][player_y+forward], 'Forward')
        self.evaluate_cell(self.map[player_x+left][player_y], 'Left')
        self.evaluate_cell(self.map[player_x+right][player_y], 'Right')

    def show_question_menu(self):
        self.cvs.destroy()
        self.question_count -= 1
        self.question_text.set('Questions: ' + str(self.question_count))
        question = self.return_question()
        self.rowconfigure(0, weight=4)
        for i in range(2):
            self.rowconfigure(i+1, weight=1)
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform='cols')
        Label(text=question.question).grid(row=0, column=0, columnspan=2, sticky=FILL_GRID)
        answers = question.incorrect_answers
        answers.append(question.correct_answer)
        shuffle(answers); shuffle(answers); shuffle(answers)
        commands = []
        for i in range(4):
            if answers[i] == question.correct_answer:
                commands.append(self.correct_answer)
            else:
                commands.append(self.incorrect_answer)
        
        for current_answer, current_command, row_num, col_num in zip(answers, commands, (2, 1, 2, 1), (0, 0, 1, 1)):
            Button(text=current_answer, command=current_command).grid(row=row_num, column=col_num, sticky=FILL_GRID)

    def return_question(self):
        with open(os.path.join('assets', self.category, 'questions.txt'), 'r') as questions_file:
            all_questions = questions_file.readlines()
        current_question = choice(all_questions)
        current_question = (current_question
                            .strip()
                            .split(';'))
        return Question(current_question[0], current_question[1], current_question[2:])
    
    def correct_answer(self):
        self.score += 300
        self.repair_map_view()

    def incorrect_answer(self):
        self.repair_map_view()

    def repair_map_view(self):
        for child in self.winfo_children():
            child.destroy()
        self.set_up_cvs()
        self.map[self.player.x][self.player.y] = CD['floor']
        self.player.bind_keyboard()
        self.player.draw_view()
        self.set_up_ui()


# Stores information about the player, binds keyboard inputs
class Player_controler():
    def __init__(self, game_manager: Game_manager):
        global player_name
        self.name = player_name
        # Initiating a game_manager variable and giving it the Player_controler instance
        self.game_manager = game_manager
        self.game_manager.player = self
        # Player position defaults
        self.direction = 'north'
        # Draw first screen + bind keys to functions
        self.draw_view()
        self.bind_keyboard()
        
    # Binds keyboard inputs to their respective commands
    def bind_keyboard(self):
        self.game_manager.bind_all('w', self.move_forward)
        self.game_manager.bind_all('a', self.turn_left)
        self.game_manager.bind_all('d', self.turn_right)
        self.game_manager.bind_all('<Up>', self.move_forward)
        self.game_manager.bind_all('<Left>', self.turn_left)
        self.game_manager.bind_all('<Right>', self.turn_right)
    
    def unbind_keyboard(self):
        self.game_manager.unbind_all('w')
        self.game_manager.unbind_all('a')
        self.game_manager.unbind_all('d')
        self.game_manager.unbind_all('<Up>')
        self.game_manager.unbind_all('<Left>')
        self.game_manager.unbind_all('<Right>')

    # Gives arguments to the cell_managers dwaw_view method
    def draw_view(self):
        self.game_manager.draw_view(self.x, self.y, self.direction)

    # Manages the players movement forward - 'W' key input
    def move_forward(self, bind):
        match self.direction:
            case 'north':
                if self.game_manager.map[self.x-1][self.y] == CD['floor']:
                    self.x-=1
                elif self.game_manager.map[self.x-1][self.y] == CD['question']:
                    self.game_manager.map[self.x-1][self.y] = CD['floor']
                    self.unbind_keyboard()
                    self.game_manager.show_question_menu()
                    return
                elif self.game_manager.map[self.x-1][self.y] == CD['game-end']:
                    self.game_manager.destroy()
                    Game_win(self.game_manager.score, self.game_manager.category)
                    return
            case 'east':
                if self.game_manager.map[self.x][self.y+1] == CD['floor']:
                    self.y+=1
                elif self.game_manager.map[self.x][self.y+1] == CD['question']:
                    self.game_manager.map[self.x][self.y+1]= CD['floor']
                    self.unbind_keyboard()
                    self.game_manager.show_question_menu()
                    return
                elif self.game_manager.map[self.x][self.y+1] == CD['game-end']:
                    self.game_manager.destroy()
                    Game_win(self.game_manager.score, self.game_manager.category)
                    return
            case 'south':
                if self.game_manager.map[self.x+1][self.y] == CD['floor']:
                    self.x+=1
                elif self.game_manager.map[self.x+1][self.y] == CD['question']:
                    self.game_manager.map[self.x+1][self.y] = CD['floor']
                    self.unbind_keyboard()
                    self.game_manager.show_question_menu()
                    return
                elif self.game_manager.map[self.x+1][self.y] == CD['game-end']:
                    self.game_manager.destroy()
                    Game_win(self.game_manager.score, self.game_manager.category)
                    return
            case 'west':
                if self.game_manager.map[self.x][self.y-1] == CD['floor']:
                    self.y-=1
                elif self.game_manager.map[self.x][self.y-1] == CD['question']:
                    self.game_manager.map[self.x][self.y-1] = CD['floor']
                    self.unbind_keyboard()
                    self.game_manager.show_question_menu()
                    return
                elif self.game_manager.map[self.x][self.y-1] == CD['game-end']:
                    self.game_manager.destroy()
                    Game_win(self.game_manager.score, self.game_manager.category)
                    return
        self.draw_view()

    # Manages the players 'D' key input
    def turn_right(self, bind):
        if DIRECTIONS.index(self.direction) < 3:
            self.direction = DIRECTIONS[DIRECTIONS.index(self.direction) + 1]
        else:
            self.direction = DIRECTIONS[0]
        self.draw_view()

    # Manages the players 'A' key input
    def turn_left(self, bind):
        if DIRECTIONS.index(self.direction) > 0:
            self.direction = DIRECTIONS[DIRECTIONS.index(self.direction)-1]
        else:
            self.direction = DIRECTIONS[3]
        self.draw_view()


class Question():
    def __init__(self, question: str, correct_answer: str, incorrect_answers: list):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers


# Tells the player they have won and returns to the Main_screen
class Game_win(Tk, General_methods):
    def __init__(self, score: int, category: str):
        self.score = score
        self.category = category
        self.leaderboard_result_message = ''
        self.compare_score_with_leaderboard()
        super().__init__()
        self.set_up_window('YOU WON', 600, 600)
        Label(text='GAME WIN', background='white', foreground='gold', font=('', 50, 'bold')).place(relx=.5, rely=.1, anchor=CENTER)
        Label(text='You won with a score of %d.' % score, background='white', font=('', 15)).place(relx=.5, rely=.25, anchor=CENTER)
        Label(text=self.leaderboard_result_message, background='white', font=('', 15)).place(relx=.5, rely=.30, anchor=CENTER)
        Button(text='MENU', font=('', 15), command=lambda: (self.destroy(), Main_screen())).place(relx=.5, rely=.60, anchor=CENTER)
        Button(text='PLAY AGAIN', font=('', 15), command=self.start_game).place(relx=.5, rely=.67, anchor=CENTER)
    
    def compare_score_with_leaderboard(self):
        global player_name
        leaderboard_list = self.return_leaderboard_list(self.category)
        for entry in leaderboard_list:
            if entry[0] == player_name:
                if int(entry[1]) < self.score:
                    leaderboard_list.remove(entry)
                else:
                    self.leaderboard_result_message = 'You didn\'t beat your previous score of ' + entry[1]
                break
        if self.leaderboard_result_message == '':
            for entry in leaderboard_list:
                if self.score > int(entry[1]):
                    leaderboard_list.insert(leaderboard_list.index(entry), [player_name, self.score])
                    self.leaderboard_result_message = 'You\'ve placed %d. on the leaderboard' % (leaderboard_list.index(entry))
                    break
        if self.leaderboard_result_message == '':
            self.leaderboard_result_message = 'You didn\'t place on the leaderboard'
        self.rewrite_leaderboard(self.category, leaderboard_list)
        
    def rewrite_leaderboard(self, category, leaderboard_list):
        with open(os.path.join('assets', category, 'leaderboard.txt'), 'w') as leaderboard:
            for i in range(10):
                leaderboard.write(str(leaderboard_list[i][0]) + ';' + str(leaderboard_list[i][1]) + '\n')
        
    def return_leaderboard_list(self, category: str):
        with open(os.path.join('assets', category, 'leaderboard.txt'), 'r') as leaderboard:
            leaderboard_list = leaderboard.readlines()
        temp = []
        for entry in leaderboard_list:
            temp.append(entry
                        .strip()
                        .split(';'))
        leaderboard_list = temp
        return leaderboard_list
    
    def start_game(self):
        self.destroy()
        game_manager = Game_manager(self.category)
        Player_controler(game_manager)


if __name__ == '__main__':
    # Start of the program
    ''' TEST
    char_login = Char_login()
    char_login.mainloop()
    '''
    main_screen = Game_win(0, 'biology')
    main_screen.mainloop()