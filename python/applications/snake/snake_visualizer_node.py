import time
import random
import spacetime
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World, Direction, FRAMETIME
from spacetime import Node
from curses import wrapper

from threading import Thread
import curses


def visualize(df):
    wrapper(visualizer, df)

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
    stdscr.addch(
        World.display_height,
        World.display_width, curses.ACS_LRCORNER, curses.color_pair(1))


    #stdscr.addch(, )
    #stdscr.addch(, )
    #stdscr.addch(, )


def visualizer(stdscr, df):
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    draw_border(stdscr)
    vis_thread = Thread(
        target=visualize_frames, args=(stdscr, df), daemon=True)

    vis_thread.start()
    vis_thread.join()

def visualize_frames(stdscr, df):
    try:
        snakes, apple = list(), None
        while not snakes and not apple:
            df.pull_await()
            snakes = df.read_all(Snake)
            apples = df.read_all(Apple)
            if apples:
                apple = apples[0]
        # We have an apple, and some snakes!!
            prev_snakes_pos, prev_apple_pos = show_frame(
                stdscr, apple, snakes, dict(),
                None)

        while any(not snake.crashed for snake in snakes):
            start_t = time.perf_counter()
            df.pull()
            df.checkout()
            prev_snakes_pos, prev_apple_pos = show_frame(
                stdscr, apple, snakes, prev_snakes_pos,
                prev_apple_pos)
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


def show_frame(
        stdscr, apple, snakes, prev_snakes_pos,
        prev_apple_pos):
    if prev_apple_pos != apple.apple_position:
        display_apple(stdscr, apple.apple_position)
    prev_snakes_pos = display_snakes(
        stdscr, snakes, prev_snakes_pos)
    stdscr.refresh()
    return prev_snakes_pos, apple.apple_position

def display_apple(stdscr, position):
    stdscr.addch(position[1], position[0], '@', curses.color_pair(1))

def display_snakes(stdscr, snakes, prev_snakes_pos):
    snake_dict = {
        snake.oid: snake
        for snake in snakes
    }

    for oid, snake in snake_dict.items():
        prev_pos = prev_snakes_pos.setdefault(oid, list())
        for x, y in prev_pos:
            stdscr.addch(y, x, ' ', curses.color_pair(1))
        for i, pos in enumerate(snake.snake_position):
            x, y = pos
            stdscr.addch(y, x, str(snake.assigned_player) if i == 0 else '.', curses.color_pair(1))

        prev_snakes_pos[oid] = snake.snake_position

    return prev_snakes_pos

def main():
    vis_node = Node(
        visualize, dataframe=["127.0.0.1", 8000], Types=[Snake, Apple])
    vis_node.start()

if __name__ == "__main__":
    main()