from tkinter import *
from random import choice


# Constants declarations
WALL_COLOR = choice(('#FF9C07', '#FFA8F9', '#90AF90'))
DOOR_OUTLIER_COLOR = '#404040'
DOOR_WOOD_COLOR = '#853411'

class Drawing_functions():
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