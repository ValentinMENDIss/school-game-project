######### IMPORT ##############

import pygame
import sys
import os
from pygame.math import Vector2 as vector
import time
import random
pygame.mixer.init()

######### CONSTANTS ###########

WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720																					# setting up window's width and height
TILE_SIZE = 64																											# Tile size (tileset)

pygame.font.init()																										# initialize pygame.font framework (needed for text)

######### LAYERS ##############
WORLD_LAYERS = {																										# Dictionary that store Sprite Layers
	'water': 0,
	'bg': 1,
	'shadow': 2,
    'item': 3,
	'main': 4,
	'top': 5
}

######### TEXT ##############
SMALLTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 25)                                           # set Font and Size for the Small Text
HEADINGTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 65)                                         # set Font and Size for the Small Text

######### SFX ##############
YIPPEE_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'yippee-tbh.mp3'))
MENU_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'menu.wav'))
PICKUP_SOUND = pygame.mixer.Sound(os.path.join('..', 'data', 'sound', 'pickup.wav'))

######### SPRITEs ##############
ITEM_TEST = pygame.image.load(os.path.join('..', 'graphics', 'item-test.png'))                                          # load sprite of the ITEM_TEST
ITEM_TEST2 = pygame.image.load(os.path.join('..', 'graphics', 'item-test2.png'))                                        # load sprite of the ITEM_TEST2

HEALTH_0 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '0%.png'))
HEALTH_10 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '10%.png'))
HEALTH_20 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '20%.png'))
HEALTH_36 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '36%.png'))
HEALTH_52 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '52%.png'))
HEALTH_60 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '60%.png'))
HEALTH_68 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '68%.png'))
HEALTH_100 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '100%.png'))

