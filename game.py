import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 6
GAME_HEIGHT = 6

#### Put class definitions here ####

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Girl(GameElement):
    IMAGE = "Girl"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None  

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

class Princess(GameElement):
    IMAGE = "Princess"
    SOLID = True

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True
    def interact(self, player):
        # GAME_BOARD.del_el(PLAYER.x,PLAYER.y, PLAYER)
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(0, 0, PLAYER)
        GAME_BOARD.draw_msg("You kissed a boy! Back to the start for you!")

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem!  You have %d items!"%(len(player.inventory)))


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
 #    #initialize and register rock 1
 #    rock = Rock()
 #    GAME_BOARD.register(rock)
 #    GAME_BOARD.set_el(1, 2, rock)
 #    print "The rock is at", (rock.x, rock.y)

 #    #initialize and register rock 2
 #    rock2 = Rock()
 #    GAME_BOARD.register(rock2)
 #    GAME_BOARD.set_el(2,1,rock2)

 #    #initialize and register rock 3
 #    rock3 = Rock()
 #    GAME_BOARD.register(rock3)
 #    GAME_BOARD.set_el(3,2, rock3)

 # #initialize and register rock 4
 #    rock4 = Rock()
 #    GAME_BOARD.register(rock4)
 #    GAME_BOARD.set_el(2,3, rock4)

    rock_positions = [
        (2,2),
        (1,1),
        (3,2),
        (3,3)
    ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Girl()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 1, PLAYER)
    print PLAYER

    
    boy = Boy()
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(2,4, boy)
    print boy

    cindy = Princess()
    GAME_BOARD.register(cindy)
    GAME_BOARD.set_el(5,4, cindy)
    print cindy

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    #GAME_BOARD.draw_msg("Board game.")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    #This will return True if the up arrow key is being pressed

   # KEYBOARD[key.up]
def keyboard_handler():
    direction=None

    if KEYBOARD[key.UP]:
        direction = "up"
    #     GAME_BOARD.draw_msg("You pressed up")
    #     next_y = PLAYER.y -1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    #     GAME_BOARD.draw_msg("You pressed down")
    #     next_y = PLAYER.y +1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    #     GAME_BOARD.draw_msg
    #     ("You pressed left")
    #     next_x = PLAYER.x -1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    #     GAME_BOARD.draw_msg("You pressed right")
    #     next_x = PLAYER.x +1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    # elif KEYBOARD[key.SPACE]:
    #     GAME_BOARD.erase_msg()
# #print (PLAYER.x, PLAYER.y)
# print PLAYER.next_pos("up")
# print (PLAYER.x, PLAYER.y)
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x >= GAME_WIDTH or next_x<0:
            GAME_BOARD.draw_msg("Can't move there!")
            GAME_BOARD.set_el(PLAYER.x, PLAYER.y, PLAYER)

        elif next_y >= GAME_HEIGHT or next_y<0:
            GAME_BOARD.draw_msg("Can't move there!")
            GAME_BOARD.set_el(PLAYER.x, PLAYER.y, PLAYER)

        else:

            existing_el = GAME_BOARD.get_el(next_x, next_y)  #returns the object in that location
            
            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.erase_msg()
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
