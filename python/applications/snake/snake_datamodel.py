import sys
import random
import uuid
import math
import numpy as np
from enum import Enum
from rtypes import pcc_set, merge
from rtypes import dimension, primarykey

FRAMETIME = 1.0/5

@pcc_set
class Snake(object):
    @property
    def direction_vector(self):
        return np.array(self.snake_position[0])-np.array(self.snake_position[1])

    oid = primarykey(str)
    player_id = dimension(str)
    snake_id = dimension(str)
    snake_head = dimension(list)
    snake_position = dimension(list)
    score = dimension(int)
    start_game = dimension(bool)
    done = dimension(bool)
    winner = dimension(bool)
    crashed = dimension(bool)
    button_direction = dimension(int)
    prev_button_direction = dimension(int)

    def __init__(self):
        self.oid = str(uuid.uuid4())
        self.player_id = str(uuid.uuid4())
        self.snake_id = str(uuid.uuid4())
        self.score = 0
        self.start_game = False
        self.done = False
        self.winner = False
        self.world = World()
        self.crashed = False
        self.button_direction = 1
        self.prev_button_direction = 1

    def set_button_direction(self, direction):
        self.prev_button_direction = self.button_direction
        self.button_direction = direction
        #print (self.prev_button_direction, self.button_direction)

@pcc_set
class Apple(object):
    oid = primarykey(int)
    apple_position = dimension(list)

    def __init__(self):
        self.oid = random.randint(0, sys.maxsize)
        self.apple_position = [
            random.randrange(1, World.display_width),
            random.randrange(1, World.display_height)]

class World():
    display_width = 50
    display_height = 20


class Direction(object):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3