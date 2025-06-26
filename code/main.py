#    School-Game-Project - Adventure style school game
#    Copyright (C) 2025 Valentin Virstiuc <valentin.vir@proton.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


######### IMPORT ##############
import pygame
import settings
settings.init()
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite, BorderSprite, CollidableSprite, TransitionSprite, TransitionCutsceneSprite
from groups import *
from dialog import *
from menu import *
from inventory import *
from hud import *
from items import *
from gamedata import *
from input import *
from timer import Timer
from music import Music
from gametime import GameTime
from cutscenes import play_cutscene, choose_cutscene
from shop import *

import cProfile

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
        self.is_running = True
        self.action = None                                                                                           # declare/initialize self.action variable that has a default value: False
        self.timer = Timer()
        self.menu = Menu(self)
        self.shop = Shop(self)
        self.input = UserInput(self)
        self.inventory = Inventory(self)
        self.music = Music()
        self.game_time = GameTime()
        self.time = 0
        self.pressed_start_time = 0
        self.pressed_duration = 5000
        self.fps_lock = 60
        self.menu_fps_lock = 15
        self.music_paused = False
        self.current_screen = "menu"
        self.initialized = False

        self.npcs_on_current_screen = []
        self.items_on_current_screen = []

        # CONFIGURING PYGAME
        self.SCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF # | pygame.FULLSCREEN
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.SCREEN_FLAGS)                                            # create screen with (x,y) (tuple)
        pygame.display.set_caption("School-Game-Project(11. Grade)")                                                    # set/change title (caption) of the window
        self.clock = pygame.time.Clock()                                                                                # create a clock
        self.ticks = pygame.time.get_ticks()                                                                            # get ticks (needed in order to count how much time is gone)

        # INTERACTION SETTINGS
        self.action_start_time = 0                                                                                    # interaction start time variable
        self.action_duration = 5000                                                                                   # duration of interaction with NPC variable

        # GROUPS
        self.all_sprites = AllSprites()                                                                                 # create a sprite group # assigns to AllSprites() Class
        self.collision_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        self.transition_cutscene_sprites = pygame.sprite.Group()

        self.transition_target = 0
        self.dt = 0

        self.saved_data = load_saved_data()
        self.cutscene_order = self.saved_data['cutsceneOrder']

        self.import_assets()                                                                                            # import tilesets (assets)
        # DEBUGGING VARIABLEs
        self.debug = False
        if self.cutscene_order == 0:
            self.show_cutscene = True
        else:
            self.show_cutscene = False
        

    def change_resolution(self, new_window_width, new_window_height, screen_flag=None, activate_type=None):
        if screen_flag:
            if activate_type == "activate":
                self.SCREEN_FLAGS |= screen_flag
            elif activate_type == "deactivate":
                self.SCREEN_FLAGS &= ~screen_flag
        settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT = new_window_width, new_window_height
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.SCREEN_FLAGS)

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx')),                         # load world.tmx file (with given location of it)
                         'world2': load_pygame(os.path.join('..', 'data', 'maps', 'world2.tmx')),
                         'school-building-bottom-left': load_pygame(os.path.join('..', 'data', 'maps', 'school-building-bottom-left.tmx')),
                         'neighborhood': load_pygame(os.path.join('..', 'data', 'maps', 'neighborhood.tmx')),
                         'player-home': load_pygame(os.path.join('..', 'data', 'maps', 'player-home.tmx'))}
                        

    def setup(self, tmx_map, player_start_pos):
        # clear the map
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites):
            group.empty()
        self.npcs_on_current_screen = []
        self.items_on_current_screen = []

        self.background_layer = self.create_static_layer(tmx_map=tmx_map, layer_name='Terrain')

        # GET ENTITIES' POSITION
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:                                      # check whether the object's name is Player and its properties for pos(position). Check also whether it is the same as player_start_pos
                if Player.initiated:
                    self.player.teleport((obj.x, obj.y))
                    self.all_sprites.add(self.player)
                    #print("OLD PLAYER")
                else:
                    self.player = Player(self.input, (obj.x, obj.y), self.all_sprites, self.collision_sprites)
                    #print("NEW PLAYER")
            if obj.name == 'Character':
                if obj.properties['enemy'] == False:
                    if obj.properties['dialog']:
                        self.npc = NPC_Friendly(obj.properties['entity-name'], (obj.x, obj.y), self.all_sprites, game=self, dialog_bool=True)
                    else:
                        self.npc = NPC_Friendly(obj.properties['entity-name'], (obj.x, obj.y), self.all_sprites, game=self, dialog_bool=False)
                    self.npcs_on_current_screen.append(self.npc)
                if obj.properties['enemy']:
                    self.npc_enemy = NPC_Enemy(obj.properties['entity-name'], (obj.x, obj.y), self.all_sprites, game=self, dialog_bool=False)
                    self.npcs_on_current_screen.append(self.npc_enemy)
                if obj.properties['shop'] == True:
                    self.npc_shop = NPC_Shop(obj.properties['entity-name'], (obj.x, obj.y), self.all_sprites, game=self, dialog_bool=False)
                    self.npcs_on_current_screen.append(self.npc_shop)

        # GET ITEMS' POSITION
        for obj in tmx_map.get_layer_by_name('Items'):
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test':
                self.item_test = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites, rarity="RARE",  game=self)
                self.items_on_current_screen.append(self.item_test)
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test2':
                self.item_test2 = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites, rarity="EPIC", game=self)
                self.items_on_current_screen.append(self.item_test2)
        # GET OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Objects'):
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        # GET COLLISION OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        try:
            for obj in tmx_map.get_layer_by_name('CutscenePoints'):
                TransitionCutsceneSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['cutscene-id']), self.transition_cutscene_sprites)
        except ValueError:
            print("No CutscenePoints")

        # GET TRANSITION OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Transitions'):
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

    def create_static_layer(self, tmx_map, layer_name):
        layer = pygame.Surface((tmx_map.width * TILE_SIZE, tmx_map.height * TILE_SIZE), pygame.SRCALPHA)
        for x, y, surf in tmx_map.get_layer_by_name(layer_name).tiles():
            layer.blit(surf, (x * TILE_SIZE, y * TILE_SIZE))
        return layer

    # MENU LOGIC
    def display_menu(self, startup=False):
        if startup:
            self.menu.show(self.display_surface, startup=True)
        else:
            self.menu.show(self.display_surface)                                                                                     # show menu
        if self.menu.exit_action:
            self.is_running = False

    # GET PRESSED KEYS
    def menu_get_pressed_keys(self, action):
        if self.input.menu_input(action) == None:
            self.input.menu_input(action)
        else:
            self.menu.get_pressed_keys_action = self.input.menu_input(action)

    def get_random_interact_text(self, data):
        random_number = random.randint(0, len(data) - 1)
        self.random_interact_text = data[random_number]
        return f"{self.random_interact_text}"

    def check_map_transition(self):                                                                                                           # check whether player is colliding with transition points
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.transition_fade_in()
            self.transition_target = sprites[0].target
            self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])                                                   # import this one specific tileset (mapset/asset)
            self.transition_fade_out()
            
    def check_cutscene_transition(self):
        sprite = [sprite for sprite in self.transition_cutscene_sprites if sprite.rect.colliderect(self.player.hitbox) and sprite.played == False]
        if sprite:
            play_cutscene(game=self, surface=self.display_surface, location=choose_cutscene(sprite[0].cutscene_id))
            sprite[0].played = True

    def transition_fade_in(self):
        alpha = 0
        while alpha < 255:
            # Create a black surface for fading (same size as screen/display_surface)
            self.fade_surface = pygame.Surface(self.display_surface.get_size())
            self.handle_game_events()
            self.fade_surface.set_alpha(alpha)
            self.display_surface.blit(self.fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps_lock)
            alpha += 5

    def transition_fade_out(self):
        alpha = 255
        while alpha > 0:
            # Create a black surface for fading (same size as screen/display_surface)
            self.fade_surface = pygame.Surface(self.display_surface.get_size())
            self.handle_game_events()
            self.render_new_game_world()
            self.fade_surface.set_alpha(alpha)
            self.display_surface.blit(self.fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps_lock) 
            alpha -= 5

    # MAIN (RUN) LOGIC
    def run(self):
        self.is_running = True
        self.menu_startup = True 
        while self.is_running:
            self.handle_game_events()
            if not self.is_running:
                break
            self.render_game_world()
            self.show_interact_in_range()
            self.update_game_state()
            if self.debug:
                self.run_debug()
            if self.current_screen == "game":
                self.process_interactions()
                self.handle_music_system()
            pygame.display.flip()                        

    def run_debug(self):
        print(self.clock.get_fps())

    def handle_game_events(self):
        MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hud.settings_button.checkForInput(MOUSE_POS):
                    self.current_screen = "menu"
                if self.hud.inventory_button.checkForInput(MOUSE_POS):
                    self.inventory.show_menu(self.display_surface)


    def update_game_state(self):
        self.dt = self.clock.tick(self.fps_lock) / 1000
        self.game_time.update()
        self.input.update()  # check user's input
        self.check_map_transition() # check for map tps (teleport points/transitions)
        self.check_cutscene_transition()
        self.all_sprites.update(self.dt) # update all sprites

    def render_new_game_world(self, draw_hud=True):
        self.display_surface.fill((173, 216, 230))
        self.display_surface.blit(
            self.background_layer,
            (-(self.player.rect.center[0] - settings.WINDOW_WIDTH / 2),
            -(self.player.rect.center[1] - settings.WINDOW_HEIGHT / 2))
        )
        self.all_sprites.draw(self.player.rect.center)
        if draw_hud:
            self.hud.draw(self.display_surface)
            self.hud.draw_time(self.display_surface)

    def render_game_world(self):
        if self.current_screen == "game":
            if self.initialized == False:
                self.setup(self.tmx_maps['player-home'], 'spawn')                                                                     # import this one specific tileset (mapset/asset)
                self.hud = HUD(self, self.player)                                                                               # initializing HUD Class which is dependant on setup's method variables
                self.initialized = True
            self.display_surface.fill((173, 216, 230))
            self.display_surface.blit(
                self.background_layer,
                (-(self.player.rect.center[0] - settings.WINDOW_WIDTH / 2),
                -(self.player.rect.center[1] - settings.WINDOW_HEIGHT / 2))
            )
            self.all_sprites.draw(self.player.rect.center)
            self.hud.draw(self.display_surface)
            self.hud.draw_time(self.display_surface)
            #self.game_time.resume_game_time()
            if self.show_cutscene:
                self.current_screen = "cutscene"
        elif self.current_screen == "menu":
            # Menu logic
            if self.menu_startup:
                self.display_menu(startup=True)
                self.music.play_random()
                self.menu_startup = False
            else:
                self.display_menu()
            self.game_time.pause_game_time(self.clock.tick() / 1000)
        elif self.current_screen == "cutscene":
            play_cutscene(game=self, surface=self.display_surface, location=choose_cutscene(self.cutscene_order))
            self.cutscene_order += 1
            if self.cutscene_order != 1 and self.cutscene_order != 2:
                self.show_cutscene = False
                self.current_screen = "game"
                self.transition_fade_out()
                self.game_time.pause_game_time(self.clock.tick() / 1000)
        elif self.current_screen == "shop":
            self.shop.display_shop(self.display_surface)

    def show_interact_in_range(self):
        for npc in self.npcs_on_current_screen:
            npc.interactInRange(self.player.rect, self.display_surface)


    def handle_music_system(self):
        music_status = self.music.check_status()
        if music_status == "Paused" and self.music.paused == True:
            self.music.unpause()
        elif music_status == "Stopped":
            self.music.play_random()
        else:
            pass

    def process_interactions(self):
        # INTERACTION/ACTION HANDLING
        if self.action:                                                                                   # check whether interact condition is true or not (bool check)
            if self.action == "item_pickup":
                for item in self.items_on_current_screen:
                    item.pickup_logic(self.player.rect.center)
            elif self.action == "npc":
                self.process_npc_interactions()

    def process_npc_interactions(self):
        if isinstance(self.npc_interact, NPC_Friendly):
            self.npc_interact.interact(self.player.rect)
        elif isinstance(self.npc_interact, NPC_Enemy):
            self.npc_interact.interact(self.display_surface, self.player.rect)
        elif isinstance(self.npc_interact, NPC_Shop):
            self.npc_interact.interact() 



####### MAIN CODE ############
if __name__ == "__main__":                                                                                              # if code is in main.py (__main__) run following
    game = Game()                                                                                                       # initialize game() (class)
    game.run()                                                                                                          # run game (game-logic)

    ## DEBUG ##
    #cProfile.run('game.run()')
