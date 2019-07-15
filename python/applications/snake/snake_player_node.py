import time
import random
import spacetime
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World, Direction, FRAMETIME
from snake_physics_node import main as phmain
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

def draw_border(stdscr):
    for i in range(World.display_width):
        stdscr.addch(0,i,curses.ACS_HLINE,curses.color_pair(1))
    for i in range(World.display_height):
        stdscr.addch(i ,World.display_width,curses.ACS_VLINE,curses.color_pair(1))
    for i in range(World.display_width):
        stdscr.addch(World.display_height,i,curses.ACS_HLINE,curses.color_pair(1))
    for i in range(World.display_height):
        stdscr.addch(i ,0,curses.ACS_VLINE,curses.color_pair(1))

    stdscr.addch(0 ,0,curses.ACS_ULCORNER,curses.color_pair(1))
    stdscr.addch(0 ,World.display_width,curses.ACS_URCORNER,curses.color_pair(1))
    stdscr.addch(World.display_height ,0,curses.ACS_LLCORNER,curses.color_pair(1))
    stdscr.addch(World.display_height ,World.display_width,curses.ACS_LRCORNER,curses.color_pair(1))


    #stdscr.addch(, )
    #stdscr.addch(, )
    #stdscr.addch(, )


def player_client(stdscr, df):
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    snake_colors = []
    draw_border(stdscr)
    snake = init_player(df)
    while not snake.start_game:
        df.pull_await()

    # Ask the player to press any key to continue
    input_thread = Thread(target=take_user_input, args=(stdscr, df, snake), daemon=True)
    vis_thread = Thread(target=visualizer, args=(stdscr, df), daemon=True)

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

def visualizer(stdscr, df):
    try:
        snakes, apple = list(), None
        while not snakes and not apple:
            df.pull_await()
            snakes = df.read_all(Snake)
            apples = df.read_all(Apple)
            if apples:
                apple = apples[0]
        # We have an apple, and some snakes!!
            prev_snakes_pos, prev_apple_pos = show_frame(stdscr, apple, snakes, dict(), None)

        while all(not snake.crashed for snake in snakes):
            start_t = time.perf_counter()
            df.pull()
            df.checkout()
            prev_snakes_pos, prev_apple_pos = show_frame(
                stdscr, apple, snakes, prev_snakes_pos, prev_apple_pos)
            end_t = time.perf_counter()
            if end_t - start_t < FRAMETIME:
                time.sleep(FRAMETIME - end_t + start_t)
    except Exception:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        print (list(s.snake_position for s in df.read_all(Snake)))
        print (list(a.apple_position for a in df.read_all(Apple)))
        raise


def show_frame(stdscr, apple, snakes, prev_snakes_pos, prev_apple_pos):
    if prev_apple_pos != apple.apple_position:
        display_apple(stdscr, apple.apple_position)
    prev_snakes_pos = display_snakes(stdscr, snakes, prev_snakes_pos)
    stdscr.refresh()
    return prev_snakes_pos, apple.apple_position

def display_apple(stdscr, position):
    stdscr.addch(position[1], position[0], '@', curses.color_pair(1))

def display_snakes(stdscr, snakes, prev_snakes_pos):
    snake_dict = {
        snake.oid: snake
        for snake in snakes
    }

    for i in range(1,6):
        snake_color[i] = curses.color_pair(i)
    for oid, snake in snake_dict.items():
        prev_pos = prev_snakes_pos.setdefault(oid, list())
        for x, y in prev_pos:
            stdscr.addch(y, x, ' ', curses.color_pair(1))
        for i, pos in enumerate(snake.snake_position):
            x, y = pos
            stdscr.addch(y, x, 'X' if i == 0 else 'o', snake_color[i])

        prev_snakes_pos[oid] = snake.snake_position

    return prev_snakes_pos

def visualizer_test(stdscr):
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.bkgd(' ', curses.color_pair(1))
    # for i in range(120):
    #     stdscr.addch(0, i, chr(i), curses.color_pair(1))
    try:
        for i in range(500):
            for j in range(27):
                stdscr.addch(j, i, '@', curses.color_pair(1))
    # stdscr.addch(0, 0, curses.ACS_ULCORNER, curses.color_pair(1))
    # stdscr.addch(0, 2, curses.ACS_URCORNER, curses.color_pair(1))
    # stdscr.addch(1, 2, curses.ACS_VLINE, curses.color_pair(1))
        stdscr.getch()
    except:
        return (i, j)

def main():
    #phmain(1)
    player_node = Node(player_execution, dataframe=["127.0.0.1", 8000], Types=[Snake, Apple])
    player_node.start()
    #visualizer_main()
if __name__ == "__main__":
    main()
    #print (wrapper(visualizer_test))