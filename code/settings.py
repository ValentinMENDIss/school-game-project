######### IMPORT ##############

import pygame
import sys
import os
from pygame.math import Vector2 as vector
import time

######### CONSTANTS ###########

WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
TILE_SIZE = 32

pygame.font.init()

SMALLTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 25)  # set Font and Size for the Small Text
HEADINGTEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), 65)  # set Font and Size for the Small Text
