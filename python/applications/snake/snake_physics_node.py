import time
import sys, random, math
import spacetime
import argparse
from uuid import uuid4
from random import randint
from multiprocessing import freeze_support
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World, Direction, FRAMETIME
from snake_bot import bot_execution
from snake_visualizer_node import visualize
from spacetime import Node
import numpy as np

WAIT_FOR_START = 5
def accepting_players(dataframe, player_count):
    #function for completing phase 1 of 'game_physics' function
    #Deleting all the previous snakes:
    # print("There are {} snakes.".format(len(dataframe.read_all(Snake))))
    #dataframe.delete_all(Snake)

    no_players = True
    while no_players:
        dataframe.checkout_await()
        players = dataframe.read_all(Snake)
        print (len(players))
        if len(players) < player_count:
            continue
        return True

def initializing_apple(dataframe):
    #function for completing part of phase 2 of 'game_physics()' function
    apple = Apple()
    dataframe.add_one(Apple, apple)
    dataframe.commit()

def collision_with_apple(apple_position,score):
    apple_position = [random.randrange(1, World.display_width),random.randrange(1, World.display_height)]
    score += 1
    return apple_position,score

def collision_with_boundaries(snake_head):
    return snake_head[0]>=World.display_width or snake_head[0]<=0 or snake_head[1]>=World.display_height or snake_head[1]<=0

def collision_with_self(snake_position):
    return snake_position[0] in snake_position[1:]

def is_direction_blocked(snake_position, current_direction_vector):
    return collision_with_boundaries(snake_position[0]) or collision_with_self(snake_position)

def generate_snake(snake, apple):

    if snake.button_direction == Direction.RIGHT:
        snake.snake_head =  [snake.snake_head[0] + 1, snake.snake_head[1]]

    elif snake.button_direction == Direction.LEFT:
        snake.snake_head =  [snake.snake_head[0] - 1, snake.snake_head[1]]

    elif snake.button_direction == Direction.DOWN:
        snake.snake_head =  [snake.snake_head[0], snake.snake_head[1] + 1]

    elif snake.button_direction == Direction.UP:
        snake.snake_head =  [snake.snake_head[0], snake.snake_head[1] - 1]

    #else:
        #pass


    if snake.snake_head == apple.apple_position:
        apple.apple_position, snake.score = collision_with_apple(apple.apple_position, snake.score)
        snake.snake_position = [snake.snake_head] + snake.snake_position

    else:
        snake.snake_position = [snake.snake_head] + snake.snake_position
        snake.snake_position = snake.snake_position[:-1]


def play_game(dataframe):
    #look at what the frame has done
    #put in dataframe checkout at the beginning and commit at the end
    #read the command dring dataframe checkout
    #once read, the command needs to be committed

    snakes = dataframe.read_all(Snake)
    apple = dataframe.read_all(Apple)[0]
    print ("Starting game")
    while any(not snake.crashed for snake in snakes):
        start_t = time.perf_counter()
        dataframe.checkout()
        for snake in snakes:
            if snake.crashed:
                continue
            generate_snake(snake, apple)
            snake.crashed = is_direction_blocked(
                snake.snake_position, snake.direction_vector)
        dataframe.commit()
        end_t = time.perf_counter()
        if end_t - start_t < FRAMETIME:
            time.sleep(FRAMETIME - end_t + start_t)


    return snake.score

def game_physics(df, num_players):
    #checkout and commit
    #phase 1: accepting players
    accepting_players(df, num_players)

    #phase 2: execute each frame of the game - the first frame must set up the game
    # by placing the apple in the world and adding it to the dataframe
    initializing_apple(df)
    for i, snake in enumerate(df.read_all(Snake)):
        x, y = random.randint(4, World.display_width-1), random.randint(1, World.display_height-1)
        snake.snake_head = [x, y]
        snake.snake_position = [snake.snake_head, [x-1, y], [x-2, y]]
        snake.start_game = True
        snake.assigned_player = i + 1
    df.commit()


    # print ("Ready to play the game.")
    #phase 3: when the game concludes/ends, finish it
    final_score = play_game(df)#removed 'apple_image' parameter because that is part of the 'Visualizer' Node
    # print("The Score is {}.".format(final_score))
    pass

def main(port, pcount, bcount):

    #server
    physics_node = Node(game_physics, server_port = port, Types = [Snake, Apple])
    physics_node.start_async(pcount + bcount)

    for i in range(bcount):
        bot = Node(bot_execution, dataframe=["127.0.0.1", port], Types = [Snake, Apple])
        bot.start_async()

    visualize_node = Node(visualize, dataframe=["127.0.0.1", port], Types=[Snake, Apple])
    visualize_node.start_async()
    physics_node.join()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000, help='The port of the remote dataframe (default: 8000)')
    parser.add_argument('--players', type=int, default=1, help='The number of human players playing the game.')
    parser.add_argument('--bots', type=int, default=1, help='The number of Bot players playing the game.')
    args = parser.parse_args()
    freeze_support()
    main(args.port, args.players, args.bots)