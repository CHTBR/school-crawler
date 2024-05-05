from tkinter import *
from random import *
import os

# Constants declarations
DIRECTIONS = ['north', 'east', 'south', 'west']
FILL_GRID = N+S+E+W
WALL_COLOR = choice(('#FF9C07', '#FFA8F9', '#90AF90'))
DOOR_OUTLIER_COLOR = '#404040'
DOOR_WOOD_COLOR = '#853411'
CELL_DESIGNATIONS = {
    'wall' : 0,
    'floor' : 1,
    'door' : 2,
    'enemy' : 3,
    'boss' : 4
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


# Methods used to draw the players vision
class Draw_methods():
    # Draws the edge of player's vision
    def whiteout(self):
        self.cvs.create_rectangle(
            0, 200,
            600, 400,
            width=0, fill='white'
        )

    def floor(self):
        self.cvs.create_rectangle(
            0, 300,
            600, 600,
            width=0, fill='#93D1C9'
        )

    def side_walls(self, base):
        self.cvs.create_rectangle(
                abs(base-600), 100,
                abs(base-500), 500,
                width=0, fill=WALL_COLOR
            )

    def wall(self, keyword):
        match keyword:
            case 'Forward':
                self.cvs.create_rectangle(
                    0, 100,
                    600, 500,
                    width=0, fill=WALL_COLOR
                )
            case '2Forward':
                self.cvs.create_rectangle(
                    100, 200,
                    500, 400,
                    width=0, fill=WALL_COLOR
                )

            case keyword if keyword in ('Right', 'Left'):
                if keyword == 'Left':
                    base = 600
                else:
                    base = 0
                
                self.cvs.create_polygon(
                    abs(base-600), 0,
                    abs(base-500), 100,
                    abs(base-500), 500,
                    abs(base-600), 600,
                    width=0, fill=WALL_COLOR
                )
            
            case keyword if keyword in ('RightForward', 'LeftForward'):
                if 'Left' in keyword:
                    base = 600
                else:
                    base = 0

                self.side_walls(base)

                self.cvs.create_polygon(
                    abs(base-500), 100,
                    abs(base-400), 200,
                    abs(base-400), 400,
                    abs(base-500), 500,
                    width=0, fill=WALL_COLOR
                )

            case keyword if keyword in ('Right2Forward', 'Left2Forward'):
                if 'Left' in keyword:
                    base = 600
                else:
                    base = 0
                
                self.cvs.create_rectangle(
                    abs(base-600), 200,
                    abs(base-400), 400,
                    width=0, fill=WALL_COLOR
                )
    
    def door(self, keyword):
        match keyword:
            case 'Forward':
                self.side_walls(600)
                self.side_walls(0)

                self.cvs.create_rectangle(
                    100, 100,
                    500, 500,
                    width=0, fill=WALL_COLOR
                )
                self.cvs.create_rectangle(
                    167, 204,
                    433, 500,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_oval(
                    167, 113,
                    433, 294,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_rectangle(
                    174, 209,
                    427, 500,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_oval(
                    174, 120,
                    427, 298,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_rectangle(
                    297, 119,
                    303, 500,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )

            case '2Forward':
                self.cvs.create_rectangle(
                    200, 200,
                    400, 400,
                    width=0, fill=WALL_COLOR
                )
                self.cvs.create_rectangle(
                    234, 251,
                    367, 400,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_oval(
                    234, 206,
                    367, 297,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_rectangle(
                    237, 254,
                    364, 400,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_oval(
                    237, 209,
                    364, 299,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_rectangle(
                    299, 209,
                    302, 400,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )


            case keyword if keyword in ('Right', 'Left'):
                if keyword == 'Left':
                    base = 600
                else:
                    base = 0

                self.cvs.create_polygon(
                    abs(base-600), 0,
                    abs(base-500), 100,
                    abs(base-500), 500,
                    abs(base-600), 600,
                    width=0, fill=WALL_COLOR
                )
                self.cvs.create_polygon(
                    abs(base-580), 185.41,
                    abs(base-580), 580,
                    abs(base-516), 516,
                    abs(base-516), 233.5,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_oval(
                    abs(base-581), 88,
                    abs(base-516), 341,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )
                self.cvs.create_polygon(
                    abs(base-575), 189,
                    abs(base-575), 575,
                    abs(base-519), 519,
                    abs(base-519), 231,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_oval(
                    abs(base-576), 100,
                    abs(base-519), 353,
                    width=0, fill=DOOR_WOOD_COLOR
                )
                self.cvs.create_polygon(
                    abs(base-548), 548,
                    abs(base-548), 97,
                    abs(base-545), 97,
                    abs(base-545), 545,
                    width=0, fill=DOOR_OUTLIER_COLOR
                )

    def image(self, keyword):
        match keyword:
            case keyword if 'Left' in keyword:
                if '2Forward' in keyword:
                    self.cvs.create_image(50, 300, anchor=CENTER, image=self.img)
                elif 'Forward' in keyword:
                    self.cvs.create_image(-75, 300, anchor=CENTER, image=self.big_img)
                else:
                    self.cvs.create_image(-25, 300, anchor=CENTER, image=self.big_img)
            case keyword if 'Right' in keyword:
                if '2Forward' in keyword:
                    self.cvs.create_image(550, 300, anchor=CENTER, image=self.img)
                elif 'Forward' in keyword:
                    self.cvs.create_image(675, 300, anchor=CENTER, image=self.big_img)
                else:
                    self.cvs.create_image(625, 300, anchor=CENTER, image=self.big_img)
            case _:
                if '2Forward' == keyword:
                    self.cvs.create_image(300, 300, anchor=CENTER, image=self.img)
                else:
                    self.cvs.create_image(300, 300, anchor=CENTER, image=self.big_img)


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
        Button(frame, text='START', command=self.start_game).grid(row=0, column=0, sticky=FILL_GRID)
        Button(frame, text='LEADERBOARDS', command=self.choose_leaderboard).grid(row=1, column=0, sticky=FILL_GRID)
        Button(frame, text='CREDITS', command=self.show_credits).grid(row=2, column=0, sticky=FILL_GRID)
        Button(frame, text='LOG OUT', command=self.create_player_login).grid(row=3, column=0, sticky=FILL_GRID)
        return frame
    
    def choose_leaderboard(self):
        self.leaderboard_list_window = Toplevel()
        self.set_up_window('Leaderboards', 500, 500, self.leaderboard_list_window)
        self.leaderboard_list_window = self.return_configured_grid(self.leaderboard_list_window, 3, 1, 0)
        Button(self.leaderboard_list_window, text='Biology', command=lambda: self.show_leaderboard('biology')).grid(row=0, column=0, sticky=FILL_GRID)
        Button(self.leaderboard_list_window, text='Chemistry', command=lambda: self.show_leaderboard('chemistry')).grid(row=1, column=0, sticky=FILL_GRID)
        Button(self.leaderboard_list_window, text='Physics', command=lambda: self.show_leaderboard('physics')).grid(row=2, column=0, sticky=FILL_GRID)
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
        return_button = Button(self.leaderboard_list_window, text='BACK', command=lambda: [self.leaderboard_list_window.destroy(), self.choose_leaderboard()]).grid(row=11, column=0, columnspan=2, sticky=FILL_GRID)

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

    def start_game(self):
        self.destroy()
        game_manager = Cell_manager()
        Player_controler(game_manager)


# Creates the game map and creates a window displaying what the player sees
class Cell_manager(Tk, General_methods, Draw_methods):
    def __init__(self):
        super().__init__()
        self.get_images()
        self.set_up_window('Dungeon', 600, 600)
        self.cvs = Canvas(self, bg='black')
        self.cvs.pack(fill='both', expand=True)
        self.player = Player_controler

        ''' TEST while I don't generate enemies on the map
        has_enemy = False
        while not has_enemy: # Checks whether there are any enemies on the map, if not (happens only about 15 times in a thousand and is too hard to fix) generates a new one
            self.create_map(difficulty)
            has_enemy = False
            for x in range(len(self.map)):
                if 3 in self.map[x]:
                    has_enemy = True
        '''
        self.create_map()

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
        self.map = self.return_map(grid)        

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

        # Creates the starting point for the player and sets their coordinates
        grid[size-1][size//2] = 1
        self.player.x = size-1
        self.player.y = size//2
        # Creates the starting room
        for x in (-4, -3):
            for y in (-1, 0, 1):
                grid[x][size//2+y] = CD['floor']
        start_cell = [size-4, size//2] # Start for the pathfinder
        # Creates the boss room
        boss_room_y = randint(2, size-2) 
        for a, b in zip((1, 2, 3), (CD['boss'], CD['door'], CD['floor'])):
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
                if path[0][0] > path[1][0]: # If the x coordinate is bigger than the target decrease the x coordinate
                    path[0][0] -= 1
                elif path[0][1] > path[1][1]: # If the y coordinate is bigger than the target decrease the y coordinate  
                    path[0][1] -= 1
                elif path[0][1] < path[1][1]: # If the y coordinate is amller than the target increase the y coordinate  
                    path[0][1] += 1
                elif path[0][0] == path[1][0] and path[0][1] == path[1][1]: # If you've reached the target point pop it from the list and break out of the loop
                    path.pop(0)
                    break
        return grid

    def create_path_branch(self, starting_cell: list, grid: list):
        size = len(grid)-1
        try:
            current_cell_x = starting_cell[0]
            current_cell_y = starting_cell[1]
            next_cell_x = current_cell_x
            next_cell_y = current_cell_y
            for counter in range(5): # Branch can be extended at most 3 times
                direction = choice(DIRECTIONS)
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
                        grid[current_cell_x][current_cell_y] = CD['enemy']
                        raise Loop_Break_Exception
                    # If there's a door or the boss anywhere around the next cell create an enemy and end branch
                    for x in (-1, 0, 1):
                        for y in (-1, 0, 1):
                            if grid[next_cell_x+x][next_cell_y+y] in (2, 3, 4): 
                                grid[current_cell_x][current_cell_y] = CD['enemy']
                                raise Loop_Break_Exception
                    current_cell_x = next_cell_x
                    current_cell_y = next_cell_y
                    grid[current_cell_x][current_cell_y] = CD['floor']              
                grid[current_cell_x][current_cell_y] = CD['enemy']
        except Loop_Break_Exception:
            pass

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


# Stores information about the player, binds keyboard inputs
class Player_controler():
    def __init__(self, cell_manager: Cell_manager):
        global player_name
        self.name = player_name
        # Initiating a cell_manager variable and giving it the Player_controler instance
        self.cell_manager = cell_manager
        self.cell_manager.player = self
        # Player position defaults
        self.direction = 'north'
        # Draw first screen + bind keys to functions
        self.draw_view()
        self.bind_keyboard()
        
    # Binds keyboard inputs to their respective commands
    def bind_keyboard(self):
        self.cell_manager.bind_all('w', self.move_forward)
        self.cell_manager.bind_all('a', self.turn_left)
        self.cell_manager.bind_all('d', self.turn_right)
        self.cell_manager.bind_all('<Up>', self.move_forward)
        self.cell_manager.bind_all('<Left>', self.turn_left)
        self.cell_manager.bind_all('<Right>', self.turn_right)

    # Gives arguments to the cell_managers dwaw_view method
    def draw_view(self):
        self.cell_manager.draw_view(self.x, self.y, self.direction)

    # Manages the players movement forward - 'W' key input
    def move_forward(self, bind):
        match self.direction:
            case 'north':
                if self.cell_manager.map[self.x-1][self.y] == 1:
                    self.x-=1
            case 'east':
                if self.cell_manager.map[self.x][self.y+1] == 1:
                    self.y+=1
            case 'south':
                if self.cell_manager.map[self.x+1][self.y] == 1:
                    self.x+=1
            case 'west':
                if self.cell_manager.map[self.x][self.y-1] == 1:
                    self.y-=1
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


# Tells the player they have lost and returns to the main_screen
class GameOver(Tk, General_methods):
    def __init__(self, char_name):
        super().__init__()
        self.set_up_window('GAME OVER', 600, 600)
        self.config(bg='black')
        Button(self, text='YOU LOST', foreground='white', background='black', font='Helvetica 50', command=lambda: [self.destroy(), Main_screen(char_name)]).place(relx=.5, rely=.5, anchor=CENTER)


# Tells the player they have won and returns to the Main_screen
class GameWin(Tk, General_methods):
    def __init__(self, char_name):
        super().__init__()
        self.set_up_window('YOU WON', 600, 600)
        self.config(bg='white')
        Button(self, text='TRY AGAIN?', font='Helvetica 50', bg='white', command=lambda: [self.destroy(), Main_screen(char_name)]).place(relx=.5, rely=.5, anchor=CENTER)


# Start of the program
''' TEST
char_login = Char_login()
char_login.mainloop()
'''
main_screen = Main_screen()
main_screen.mainloop()