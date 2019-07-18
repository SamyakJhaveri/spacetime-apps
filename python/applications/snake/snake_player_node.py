import time
import random
import spacetime
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World, Direction, FRAMETIME
from snake_physics_node import main as phmain
from snake_visualizer_node import draw_border, visualize_frames
from spacetime import Node
from curses import wrapper

from threading import Thread
import curses

def player_execution(df):
    wrapper(player_client, df)

def init_player(df):
    snake = Snake()
    df.add_one(Snake, snake)
    df.commit()
    df.push()
    return snake

def player_client(stdscr, df):
    curses.start_color()
    curses.curs_set(0)
<<<<<<< HEAD
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

=======
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    snake_colors = []
>>>>>>> a5a09129a6da3dcc954eda3ec976ecaebfa716bd
    draw_border(stdscr)
    snake = init_player(df)
    while not snake.start_game:
        df.pull_await()

    # Ask the player to press any key to continue
    input_thread = Thread(
        target=take_user_input, args=(stdscr, df, snake), daemon=True)
    vis_thread = Thread(
        target=visualize_frames, args=(stdscr, df), daemon=True)

    vis_thread.start()
    input_thread.start()


    input_thread.join()
    vis_thread.join()

def parse_key(key, snake):
    if key == 27:
        snake.crashed = True
    else:
        #print (key)
        if key == 260 and snake.button_direction != Direction.RIGHT:
            snake.set_button_direction(Direction.LEFT)
        elif key == 261 and snake.button_direction != Direction.LEFT:
            snake.set_button_direction(Direction.RIGHT)
        elif key == 259 and snake.button_direction != Direction.DOWN:
            snake.set_button_direction(Direction.UP)
        elif key == 258 and snake.button_direction != Direction.UP:
            snake.set_button_direction(Direction.DOWN)

def take_user_input(stdscr, df, snake):
    while snake.crashed is not True:
        key = stdscr.getch()
        parse_key(key, snake)
        df.commit()
        df.push()

def main():
    player_node = Node(
        player_execution, dataframe=["127.0.0.1", 8000], Types=[Snake, Apple])
    player_node.start()

if __name__ == "__main__":
    main()
