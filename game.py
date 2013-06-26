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

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Girl(GameElement):
    IMAGE = "Girl"
    KEY = False
    POWER = False
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
    def interact(self, player):
        player.POWER = True
        GAME_BOARD.draw_msg("The princess gave you special powers!")

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

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        player.inventory.append(self)
        player.KEY = True
        GAME_BOARD.draw_msg("You just picked up a key! You have %d items!"%(len(player.inventory)))

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    def interact(self, player):
        if player.POWER and player.KEY:
            GAME_BOARD.draw_msg("You opened the door!")
            #SOLID = False
            open_door = DoorOpen()
            GAME_BOARD.register(open_door)
            GAME_BOARD.set_el(self.x, self.y, open_door)

        
       # GAME_BOARD.draw_msg("You need a key!")


    

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (4,6),
        (1,1),
        (3,5),
        (6,3)
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

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 3, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0,5, key)

    closed_door = DoorClosed()
    GAME_BOARD.register(closed_door)
    GAME_BOARD.set_el(5,1, closed_door)


    GAME_BOARD.draw_msg("This game is wicked awesome.")
    #GAME_BOARD.draw_msg("Board game.")

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
        GAME_BOARD.erase_msg()
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
               
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
                for item in PLAYER.inventory: 
                    print "%s" % item
