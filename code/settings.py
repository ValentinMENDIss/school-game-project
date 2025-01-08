######### IMPORT ##############

import pygame
import sys
import os
from pygame.math import Vector2 as vector
import time
import random
pygame.mixer.init()

######### CONSTANTS ###########

WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
TILE_SIZE = 32

pygame.font.init()

######### TEXT ##############
SMALLTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 25)  # set Font and Size for the Small Text
HEADINGTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 65)  # set Font and Size for the Small Text

######### SFX ##############
YIPPEE_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'yippee-tbh.mp3'))
MENU_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'menu.wav'))
PICKUP_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'pickup.wav'))

######### SPRITEs ##############
ITEM_TEST = pygame.image.load(os.path.join('..', 'graphics', 'item-test.png'))                                          # load sprite of the ITEM_TEST
ITEM_TEST2 = pygame.image.load(os.path.join('..', 'graphics', 'item-test2.png'))                                          # load sprite of the ITEM_TEST2
