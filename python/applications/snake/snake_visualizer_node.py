import time
import sys
import spacetime
import pygame
from multiprocessing import freeze_support
from rtypes import pcc_set, dimension, primarykey
from snake_datamodel import Snake, Apple, World
from spacetime import Node


display_width = 500
display_height = 500
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)
window_color = (200,200,200)

def display_snake(display, snake_position):
    for position in snake_position:
        pygame.draw.rect(display,red,pygame.Rect(position[0],position[1],10,10))

def display_apple(display,apple_position,apple):
    display.blit(apple,(apple_position[0],apple_position[1]))

def display_final_score(display, display_text,final_score):
    largeText = pygame.font.Font('FreeSansBoldOblique.ttf',32)
    TextSurf = largeText.render(display_text,True,black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    display.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)

def init_display():
    apple_image = pygame.image.load('apple.jpg')
    clock = pygame.time.Clock()

    pygame.init()
    display = pygame.display.set_mode((display_width,display_height))

    display.fill(window_color)
    pygame.display.update()
    return display, apple_image, clock

def show_frame(display, apple1, snake, apple_image):
    display.fill(window_color)
    display_apple(display,apple1.apple_position,apple_image)
    display_snake(display, snake.snake_position)
    pygame.display.update()
    pygame.display.set_caption("Sacred Games "+" Score :"+str(snake.score))


def visualize(dataframe):
    display, apple_image, clock = init_display()
    snake = None
    apple1 = None
    while not snake and not apple1:
        dataframe.pull_await()
        snakes = dataframe.read_all(Snake)
        if snakes:
            snake = snakes[0]
        apples = dataframe.read_all(Apple)
        if apples:
            apple1 = apples[0]
    show_frame(display, apple1, snake, apple_image)

    while snake.crashed is not True:
        dataframe.pull()
        dataframe.checkout()
        show_frame(display, apple1, snake, apple_image)
        clock.tick(5)

def main():

    visualizer_node = Node(visualize, dataframe = ["smoke.ics.uci.edu", 8000], Types = [Snake, Apple])
    visualizer_node.start()

if __name__ == "__main__":
    main()
