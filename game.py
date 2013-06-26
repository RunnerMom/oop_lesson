# Bessie, Gowri & Julie

#For Tomorrow:
#Look at the engine file and make the screen bigger
    # done. Modified screen size at the top of engine.py
#Message if you get to the door without key or power
    # done
# show a bunch of hearts (non-solid) if you kiss the boy
    # added one heart
# make a new room if you open the door
# new room looks completely different and has more stuff
# add ability to push boulder or other object
# door is surrounded by trees and one boulder to move 
# new room has: chest surrounded by horns and a block,
# add a new player 



import core
import pyglet
from pyglet.window import key       #imports the key method from pyglet.window module - python library
                                    #
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####

class Rock(GameElement):
    # GLOBAL = Rock           # we need to do this so that we can call the position of the rock
    IMAGE = "Rock"
    SOLID = True
    def interact(self,player):
        pass
        # if player.GEM:
        # #     if direction == "right":
        #         print "I am moving the rock to the right"
     
        # # if the girl is to the left of the rock, push the rock right.
        #     if player 
        
        #     # if the girl is to the bottom of the rock, push the rock up.
        #     # if the girl is above the rock, push the rock down
        #     # if the girl is to the right of the rock, push the rock left.

        #     # direction == "up":
        # #     # return (rock.x, rock.y-1)

        #        GAME_BOARD.set_el(boy.x-1, boy.y, heart)    #the position of the hearts around the boy
        # GAME_BOARD.set_el(boy.x+1, boy.y, heart)
        # GAME_BOARD.set_el(boy.x, boy.y-1, heart)
        # GAME_BOARD.set_el(boy.x, boy.y+1, heart)

class Tree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Girl(GameElement):    #The girl is the main PLAYER in the game
    IMAGE = "Girl"
    KEY = False             #We need to know if she has the key and the power
    POWER = False           #Initially, she has neither of them
    GEM = False
    def next_pos(self, direction):      #this function defines the movement of the player
        if direction == "up":
            return (self.x, self.y-1)   #moves up one, by subtracting from the y coordinate
                                        #(X,Y) is a tuple

        elif direction == "down":
            return (self.x, self.y+1)   #moves down one, by adding from the y coordinate
        elif direction == "left":
            return (self.x-1, self.y)   #moves left by subtracting from the x coordinate
        elif direction == "right":
            return (self.x+1, self.y)   #moves right by adding from the x coordinate
        return None  

    def __init__(self):                 #why do we need this?
        GameElement.__init__(self)
        self.inventory = []             #creates empty inventory list

class Princess(GameElement):
    IMAGE = "Princess"
    SOLID = True
    def interact(self, player):         #this defines the interactions of the Princess with the player
        player.POWER = True             # The princess turns POWER to True
        GAME_BOARD.draw_msg("The princess gave you special powers!")

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True
    def interact(self, player):             #This defines the interaction of the Boy with the player
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)   #we remove the player from her current position
        GAME_BOARD.set_el(0, 0, PLAYER)         # we re-set her position at 0,0
        GAME_BOARD.draw_msg("You kissed a boy! Back to the start for you!")
        heart=Heart()                       #we register a heard once she kisses a boy
        GAME_BOARD.register(heart)
        GAME_BOARD.set_el(boy.x-1, boy.y, heart)    #the position of the hearts around the boy
        GAME_BOARD.set_el(boy.x+1, boy.y, heart)
        GAME_BOARD.set_el(boy.x, boy.y-1, heart)
        GAME_BOARD.set_el(boy.x, boy.y+1, heart)
   

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self, player):             #defines interaction between player and Blue Gem
        player.inventory.append(self)       #Player inventory will be appended with Gem
        player.GEM = True
        GAME_BOARD.draw_msg("You just acquired a gem!  You have %d items!"%(len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):             #defines interaction between player nad Key
        player.inventory.append(self)       #Player inventory will be appended with Key
        player.KEY = True                   #The Key variable is also set to True
        GAME_BOARD.draw_msg("You just picked up a key! You have %d items!"%(len(player.inventory)))

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False                   #The open door is not solid, so you can walk through it.



class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True                    #Closed door is solid, you can not walk through it.
    def interact(self, player):     #defines interaction between player and closed door
        if player.POWER and player.KEY: # if the player has the key and the power, she can open the door
            GAME_BOARD.draw_msg("You opened the door!")
            
            open_door = DoorOpen()      #calls the open_door as an instance of the class DoorOpen
            GAME_BOARD.register(open_door)  #registers this object with the game
            GAME_BOARD.set_el(self.x, self.y, open_door)    #Puts the open door in the position of the closed door
        elif player.POWER:
            GAME_BOARD.draw_msg("You have special power, but you still need a key to open the door")
        elif player.KEY:
            GAME_BOARD.draw_msg("You have the key, but you still need the Princess to give you special powers")
        else:
            GAME_BOARD.draw_msg("You need a key and special powers to enter this door")
        
       # GAME_BOARD.draw_msg("You need a key!")
    





####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (4,6),
        (1,1),
        (3,5),
        (6,2)
    ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    global PLAYER
    PLAYER = Girl()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 1, PLAYER)
        
    tree_positions = [
        (5,0),
        (5,1),
        (7,0),
        (7,1)
    ]

    trees =[]
    
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(trees)

    global boy
    boy = Boy()
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(2,4, boy)
 

    cindy = Princess()
    GAME_BOARD.register(cindy)
    GAME_BOARD.set_el(5,4, cindy)
   

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 3, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0,5, key)

    closed_door = DoorClosed()
    GAME_BOARD.register(closed_door)
    GAME_BOARD.set_el(6,1, closed_door)

    # heart = Heart()
    # GAME_BOARD.register(heart)
    # GAME_BOARD.set_el(0,0, heart)
    # GAME_BOARD.del_el(heart.x, heart.y)

    GAME_BOARD.draw_msg("This game is wicked awesome.")


 

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
    elif KEYBOARD[key.RIGHT]:                       #Right function in key method
        direction = "right"
    #     GAME_BOARD.draw_msg("You pressed right")
    #     next_x = PLAYER.x +1
    #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    #     GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    # elif KEYBOARD[key.SPACE]:
    #     GAME_BOARD.erase_msg()

    if direction:                       # if the player has hit a direction key
        GAME_BOARD.erase_msg()          # erase the last message displayed
        next_location = PLAYER.next_pos(direction)      #call the next_pos function defined in Player Class and set that to next_location
        next_x = next_location[0]         # the first element in the tuple is the X coordinate
        next_y = next_location[1]         # the 2nd element in the tuple is the y coordinate.

        if next_x >= GAME_WIDTH or next_x<0:            #what to do if the player moves outside the boundary
            GAME_BOARD.draw_msg("Can't move there!")
                                                        #don't move the player at all

        elif next_y >= GAME_HEIGHT or next_y<0:
            GAME_BOARD.draw_msg("Can't move there!")
          

        else:                           #if the player has hit a key and we are still in the boundary, then do the following...

            existing_el = GAME_BOARD.get_el(next_x, next_y)  # get_el will return a list, existing_el will contain the class of object
            
# determine which way the player moved by calculating next_x-PLAYER.x (the next square for the player minus the current square)
# the direction that the player moves in each axis is either +1 or -1. We can
# to get the next location of the rock, add that same amount to the current location of the rock

            if existing_el:  
                # if we have any value for existing_el, this means we are allowed to move
                existing_el.interact(PLAYER)    # calling interaction ?????

            if existing_el is None or not existing_el.SOLID: # if there's nothing in the next location or if there 
                                                             # is a non-solid object
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)        # deletes player at current location
                GAME_BOARD.set_el(next_x, next_y, PLAYER)    # moves player to next location
 

            elif existing_el.IMAGE == "Rock" and PLAYER.GEM: # checking to see if the player has a gem when running into rock      
                nextrock_x = existing_el.x + next_x - PLAYER.x  #defining the rock move on x-axis      
                nextrock_y = existing_el.y + next_y - PLAYER.y  #definning the rock move on the y-axis
#### check for boundary of game
#####
                if nextrock_x >= GAME_WIDTH or nextrock_x<0:            #what to do if the player attempts to move rock outside the boundary of x-axis
                            GAME_BOARD.draw_msg("Can't move there!")  
                            

                elif nextrock_y >= GAME_HEIGHT or nextrock_y<0:         #what to do if the player attempts to move rock outside bounder of y-axis
                    GAME_BOARD.draw_msg("Can't move there!")

                elif GAME_BOARD.get_el(nextrock_x, nextrock_y) :        #what to do if the player is running rock into another object
                    GAME_BOARD.draw_msg("Can't move there!")

                else:                           #if the player has hit a key and we are still in the boundary, then do the following...

                    GAME_BOARD.del_el(existing_el.x, existing_el.y)        # deletes rock at current location
                    GAME_BOARD.set_el(nextrock_x, nextrock_y, existing_el)    # moves rock to next location
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)        # deletes player at current location
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)    # moves player to next location

            elif existing_el.IMAGE == "Rock" and not PLAYER.GEM:    # telling player that gems are needed to move rock if player doesn't have the gem
                GAME_BOARD.draw_msg("You need a gem to move the rocks!")     


"""
create a new game board if the player opens the door and crossed through

"""
if (PLAYER.x, PLAYER.y) == (6,0):
    
    for x in range(GAME_WIDTH):
        for y in range (GAME_HEIGHT):
            GAME_BOARD.del_el(x, y, GAME_BOARD.get_el(x,y))


