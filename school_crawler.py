from tkinter import *
from random import *
import pathlib, os


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
    def set_up_window(self, title: str, win_width: int, win_height: int):
        self.geometry('%dx%d+%d+%d'%(win_width, win_height, (self.winfo_screenwidth()-win_width)//2, (self.winfo_screenheight()-win_height)//2))
        self.configure(bg='white')
        self.title(title)


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
    
    def enemy(self, keyword):
        self.cvs.create_polygon(
            246, 219,
            257, 256,
            276, 275,
            311, 256,
            303, 218,
            281, 200,
            width=0, fill='#FF8C00', tags='enemy'
        )
        self.cvs.create_polygon(
            247, 292,
            274, 327,
            342, 246,
            width=0, fill='#C8E6C9', tags='enemy'
        )
        self.cvs.create_polygon(
            244, 307,
            207, 378,
            267, 325,
            width=0, fill='#FF6BD8', tags='enemy'
        )
        self.cvs.create_polygon(
            395, 201,
            361, 250,
            385, 289,
            width=0, fill='#FFD971', tags='enemy'
        )
        self.cvs.create_polygon(
            351, 254,
            263, 348,
            384, 306,
            width=0, fill='#FFB3A6', tags='enemy'
        )
        self.cvs.create_oval(
            315, 333,
            382, 400,
            width=0, fill='#ECFF5E', tags='enemy'
        )
    
    def boss(self, keyword):
        self.cvs.create_oval(
            260, 260,
            340, 340,
            width=0, fill='#4400FF', tags='boss'
        )
        self.cvs.create_polygon(
            300, 200,
            280, 260,
            320, 260,
            width=0, fill='#D900FF', tags='boss'
        )
        self.cvs.create_polygon(
            320, 340,
            280, 340,
            300, 400,
            width=0, fill='#D900FF', tags='boss'
        )
        self.cvs.create_polygon(
            340, 280,
            340, 320,
            400, 300,
            width=0, fill='#FF9900', tags='boss'
        )
        self.cvs.create_polygon(
            260, 280,
            200, 300,
            260, 320,
            width=0, fill='#FF9900', tags='boss'
        )
        self.cvs.create_polygon(
            371, 230,
            315, 258,
            343, 286,
            width=0, fill='#008CFF', tags='boss'
        )
        self.cvs.create_polygon(
            258, 315,
            230, 371,
            286, 343,
            width=0, fill='#008CFF', tags='boss'
        )
        self.cvs.create_polygon(
            229, 229,
            258, 286,
            286, 258,
            width=0, fill='#1EFF00', tags='boss'
        )
        self.cvs.create_polygon(
            343, 315,
            315, 343,
            371, 371,
            width=0, fill='#1EFF00', tags='boss'
        )


# Creates a window asking for the player's name
class Get_char_name(Tk, General_methods):
    def __init__(self):
        super().__init__()
        self.set_up_window('Select your name', 300, 300)
        self.char_name = StringVar()
        global player_name
        self.char_name.set(player_name)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        Entry(self, textvariable=self.char_name, background='black', foreground='white').grid(row=0)
        Button(self, text='SELECT', borderwidth=0, background='black', foreground='white', command=lambda:[self.destroy(), Main_screen(self.char_name.get())]).grid(row=1)
        self.mainloop()
       

# Creates the main menu screen
class Main_screen(Tk, General_methods):
    def __init__(self, char_name):
        super().__init__()
        self.set_up_window('Title screen', 600, 600)
        global player_name
        player_name = char_name
        self.cvs = Canvas(self, bg='white')
        self.cvs.pack(fill='both', expand=True)
        self.draw_background()
        self.add_buttons()
        self.add_animations()

    # Creates the START, CONTROLS and QUIT buttons
    def add_buttons(self):
        frame = Frame(self, bg='white')
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1); frame.rowconfigure(1, weight=1); frame.rowconfigure(2, weight=1); frame.rowconfigure(3, weight=1)
        frame.place(relx=.5, rely=.5, anchor=CENTER)
        global player_name
        Label(self, text='Welcome ' + player_name, bg='white').place(relx=.5, y=20, anchor=CENTER) # Character greeting label
        Button(frame, text='START', borderwidth=0, background='black', foreground='white', command=lambda:[self.destroy(), Get_difficulty()]).grid(row=1, sticky=EW) # Start button
        Button(frame, text='CONTROLS', borderwidth=0, background='black', foreground='white', command=lambda: [self.destroy(), Controls()]).grid(row=2, sticky=EW) # Controls button
        Button(frame, text='QUIT', borderwidth=0, background='black', foreground='white', command=self.destroy).grid(row=3, sticky=EW) # Quit button

    # Creates the buttons
    def draw_background(self):
        self.cvs.create_polygon(
            300, 600,
            120, 50,
            300, 126,
            width=0, fill='#C8E6C9'
        )
        self.cvs.create_polygon(
            300, 600,
            450, 387,
            300, 126,
            width=0, fill='#FFA8F9'
        )
        self.cvs.pack()

    # Adds animaions to the background
    def add_animations(self):
        multiplier = -1
        self.cvs.create_polygon(
            495, 30,
            495, 197,
            406, 143,
            width=0, fill='#93D1C9', tags='upper_left_crystal'
        )
        self.cvs.create_polygon(
            500, 88,
            500, 255,
            583, 201,
            width=0, fill='#71F9E8', tags='upper_right_crystal'
        )
        try:
            # The while True loop will try to access the cvs even after it's been destroyed and a new window has been displayed (for example after pressing the START or CONTROLS buttons)
            # So I raise an exception to break out of the loop but print the exception type in case it's something unexpected
            while True:
                multiplier=-multiplier
                for i in range(80):
                    self.cvs.move('upper_left_crystal', 0, multiplier)
                    self.cvs.move('upper_right_crystal', 0, -multiplier)
                    self.cvs.after(50)
                    self.cvs.update()

        except Exception as e:
            print(e)


# Creates a window which explains the basic controls to the player
class Controls(Tk, General_methods):
    def __init__(self):
        super().__init__()
        self.set_up_window('Controls', 600, 600)

        try: # Exception in case the images aren't available
            current_dir = pathlib.Path(__file__).parent.resolve()
            current_dir = os.path.join(current_dir, 'assets', 'controls')
            self.controls_img = []
            for i in range(8):
                i+=1
                self.controls_img.append(PhotoImage(file=os.path.join(current_dir, 'controls' + str(i) + '.png')))
        except Exception as e:
            print(e)
            input('Missing assets, please download again or unzip the files. Press the <Enter> key to terminate.')
        self.current_image_num = 0
        self.current_image = Label(self, image=self.controls_img[self.current_image_num])
        self.current_image.place(relx=.5, rely=.5, anchor=CENTER)
        self.next_btn = Button(self, text='NEXT', font='Helvetica 30', command=self.next_image)
        self.next_btn.place(x=520, y=550, anchor=CENTER)

    # Switches to the next image and returns to the Main_screen after the last one
    def next_image(self):
        self.current_image_num += 1
        self.current_image.config(image=self.controls_img[self.current_image_num])
        if self.current_image_num > 6:
            global player_name
            self.next_btn.config(text='END', command=lambda: [self.destroy(), Main_screen(player_name)])


# Creates a window to get the difficulty level for this game
class Get_difficulty(Tk, General_methods):
    def __init__(self):
        super().__init__()
        self.set_up_window('Difficulty setting', 300, 300)
        self.difficulty = IntVar()
        self.difficulty.set(1)
        rad_txt = ('Easy', 'Normal', 'Hard')
        self.columnconfigure(0, weight=1)
        for i in range(4):
            self.rowconfigure(i, weight=1)
        for i in range(3):
            Radiobutton(self, text=rad_txt[i], value=i+1, variable=self.difficulty, background='black', foreground='white', borderwidth=0).grid(row=i, column=0, sticky=FILL_GRID)
        Button(text='SELECT', background='black', foreground='white', borderwidth=0, command=self.start_game).grid(row=3, column=0, sticky=FILL_GRID)

    # Inititializes all the classes needed for the game
    def start_game(self):
        self.destroy()
        game_manager = Cell_manager(self.difficulty.get())
        Player(game_manager)


# Creates the game map and creates a window displaying what the player sees
class Cell_manager(Tk, General_methods, Draw_methods):
    def __init__(self, difficulty):
        super().__init__()
        self.set_up_window('Dungeon', 600, 600)
        self.cvs = Canvas(self, bg='black')
        self.cvs.pack(fill='both', expand=True)
        self.player = Player

        ''' TEST while I don't generate enemies on the map
        has_enemy = False
        while not has_enemy: # Checks whether there are any enemies on the map, if not (happens only about 15 times in a thousand and is too hard to fix) generates a new one
            self.create_map(difficulty)
            has_enemy = False
            for x in range(len(self.map)):
                if 3 in self.map[x]:
                    has_enemy = True
        '''
        self.create_map(difficulty)

    def create_map(self, difficulty: int):
        '''
        Function for creating a game map

        Creates a grid in the form of a double layered list with the same number of rows and columns and the length of it's sides depending on the difficulty setting.
        Creates a path through said grid from the spawn to the boss.
        Creates branches from that path and puts enemies at their ends.
        '''

        grid = self.return_square_grid(25)

        for i in range(1000):
            self.return_map(self.return_square_grid(25))
            print(i)
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
            for counter in range(3): # Branch can be extended at most 3 times
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
                        grid[current_cell_x][current_cell_y] = CD['floor'] # TEST CD['enemy']
                        raise Loop_Break_Exception
                    # If there's a door or the boss anywhere around the next cell create an enemy and end branch
                    for x in (-1, 0, 1):
                        for y in (-1, 0, 1):
                            if grid[next_cell_x+x][next_cell_y+y] in (2, 3, 4): 
                                grid[current_cell_x][current_cell_y] = CD['floor'] # TEST CD['enemy']
                                raise Loop_Break_Exception
                    current_cell_x = next_cell_x
                    current_cell_y = next_cell_y
                    grid[current_cell_x][current_cell_y] = CD['floor']              
                grid[current_cell_x][current_cell_y] = CD['floor'] # TEST CD['enemy']
        except Loop_Break_Exception:
            pass

    # Checks what kind of cell is at the given coordinates and draws a part of the player's view based on it and the keyword specifying it's place in the view
    def evaluate_cell(self, cell_num, keyword):
        match cell_num:
            case 0: # Wall
                self.wall(keyword)
            case 2: # Floor
                self.door(keyword)
            case 3: # Enemy
                self.enemy(keyword)
            case 4: # Boss
                self.boss(keyword)

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
class Player():
    def __init__(self, cell_manager: Cell_manager):
        global player_name
        self.name = player_name
        # Initiating a cell_manager variable and giving it the Player instance
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
Get_char_name()