import time
import random
import math
import spacetime
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World, Direction, FRAMETIME
from spacetime import Node
from curses import wrapper

from threading import Thread
import curses
snake_color = []

def init_bot(df):
    snake = Snake()
    df.add_one(Snake, snake)
    df.commit()
    df.push()
    return snake

def bot_execution(df):
    snake = init_bot(df)
    while not snake.start_game:
        df.pull_await()

    defeat_player(df, snake)

def set_key(key, snake):
    if key is not snake.button_direction:
        snake.set_button_direction(key)

def defeat_player(df, snake):
    for key in make_decision(df, snake):
        set_key(key, snake)
        df.commit()
        df.push_await()
        df.pull_await()


def determine_next_position_of_snake_head(snake, p_direction):
    snake_head_local = snake.snake_head
    if p_direction == Direction.RIGHT:
        snake_head_local =  [snake_head_local[0] + 1, snake_head_local[1]]

    elif p_direction == Direction.LEFT:
        snake_head_local =  [snake_head_local[0] - 1, snake_head_local[1]]

    elif p_direction == Direction.DOWN:
        snake_head_local =  [snake_head_local[0], snake_head_local[1] + 1]

    elif p_direction == Direction.UP:
        snake_head_local =  [snake_head_local[0], snake_head_local[1] - 1]

    return snake_head_local

def make_decision(df, snake):
    directions = {
        Direction.LEFT: [Direction.UP, Direction.DOWN, Direction.LEFT],
        Direction.RIGHT: [Direction.UP, Direction.DOWN, Direction.RIGHT],
        Direction.UP: [Direction.LEFT, Direction.RIGHT, Direction.UP],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT, Direction.DOWN],
    }

    apple = df.read_all(Apple)[0]
    final_direction = snake.button_direction #setting the final direction to be

    # equal to existing button_direction by default

    while not snake.crashed:
        min_dist = 10000
        start_t = time.perf_counter()
        possible_directions = directions[snake.button_direction]

        #Now computing which direction to go to in order to reach the apple
        for i in range (3):
            s_h_l = determine_next_position_of_snake_head(snake, possible_directions[i])
            #'s_h_l' stands for snake head local position predicted by the
            # possible directions of the snake
            d2 = math.sqrt(pow((apple.apple_position[0] - s_h_l[0]), 2) + pow((apple.apple_position[1] - s_h_l[1]), 2))

            if min_dist > d2 and s_h_l not in snake.snake_position[:-1]:
                min_dist = d2
                final_direction = possible_directions[i]
            else:
                continue

        #snake.button_direction = final_direction
        yield final_direction


        end_t = time.perf_counter()
        if (end_t - start_t) < FRAMETIME:
            time.sleep(FRAMETIME - end_t + start_t)
    raise StopIteration()

def main():
    bot_node = Node(bot_execution, dataframe=["127.0.0.1", 8000], Types=[Snake, Apple])
    bot_node.start()


if __name__ == "__main__":
    main()
