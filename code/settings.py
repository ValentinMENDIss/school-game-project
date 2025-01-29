######### IMPORT ##############

import pygame
import sys
import os
from pygame.math import Vector2 as vector
import time
import random

pygame.mixer.init()
pygame.font.init()																										# initialize pygame.font framework (needed for text)

######### CONSTANTS ###########

WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720																					# setting up window's width and height
TILE_SIZE = 64																											# Tile size (tileset)

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

######### MUSIC ##############
MAIN_MUSIC = os.path.join('..', 'data', 'music', 'main-music.mp3')

######### SPRITEs ##############
## ENTITIES ##
PLAYER_R = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_walk_2.png'))]

PLAYER_L = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_walk_2.png'))]

PLAYER_B = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_walk_2.png'))]

PLAYER_F = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_walk_2.png'))]


## NPC'S SPRITE/S
NPC_IDLE = pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png'))                                         # load sprite of the NPC (in action: idle) # for now it's the same image, but in the future there will be a separate one.

## SKY ##
SKY_BG_1 = pygame.image.load(os.path.join('..', 'graphics', 'clouds', '1.png'))
SKY_BG_2 = pygame.image.load(os.path.join('..', 'graphics', 'clouds', '2.png'))
SKY_BG_3 = pygame.image.load(os.path.join('..', 'graphics', 'clouds', '3.png'))
SKY_BG_4 = pygame.image.load(os.path.join('..', 'graphics', 'clouds', '4.png'))

## ITEMS ##
ITEM_TEST = pygame.image.load(os.path.join('..', 'graphics', 'item-test.png'))                                          # load sprite of the ITEM_TEST
ITEM_TEST2 = pygame.image.load(os.path.join('..', 'graphics', 'item-test2.png'))                                        # load sprite of the ITEM_TEST2

## BUTTON ##
START_IMG = pygame.image.load(os.path.join('..', 'graphics', 'start-button.png'))		                                # load image for start button
START_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'start-button-pressed.png'))
EXIT_IMG = pygame.image.load(os.path.join('..', 'graphics', 'exit-button.png'))		                                    # load image for exit button
EXIT_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'exit-button-pressed.png'))		                                    # load image for exit button
RETURN_IMG = pygame.image.load(os.path.join('..', 'graphics', 'return-button.png'))		                                # load image for return button
RETURN_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'return-button-pressed.png'))		                                # load image for return button
SETTINGS_IMG = pygame.image.load(os.path.join('..', 'graphics', 'settings-button.png'))		                                # load image for settings button
SETTINGS_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'settings-button-pressed.png'))		                                # load image for settings button
TEST_IMG = pygame.image.load(os.path.join('..', 'graphics', 'test-button.png'))
TEST_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'test-button-pressed.png'))
SURRENDER_IMG = pygame.image.load(os.path.join('..', 'graphics', 'surrender-button.png'))
SURRENDER_IMG_PRESSED = pygame.image.load(os.path.join('..', 'graphics', 'surrender-button-pressed.png'))

## HEALTHBAR ##
HEALTH_0 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '0%.png'))
HEALTH_10 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '10%.png'))
HEALTH_20 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '20%.png'))
HEALTH_36 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '36%.png'))
HEALTH_52 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '52%.png'))
HEALTH_60 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '60%.png'))
HEALTH_68 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '68%.png'))
HEALTH_100 = pygame.image.load(os.path.join('..', 'graphics', 'healthbar', '100%.png'))
