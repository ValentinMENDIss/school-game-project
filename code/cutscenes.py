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


import settings
from timer import Timer
from music import Music
from entities import *

music_player = Music()
timer = Timer()


cutscene_data = {
    "intro": {
        "id": 0,
        "images": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        "text": [
            "<A Call from the Void>: ...",
            "Hello?",
            "...",
            "Can you hear me?",
            "it's time to go!",
            "...",
            "is someone there at all?",
            "...",
            "...",
            "HELLO!???",
            "it's time to wake up!",
        ],
        "music": None,
        "audio": [
            None,
            settings.PICKUP_SOUND,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        "render-game": False,
    },
    "intro-mother1": {
        "id": 1,
        "images": [
            None,
            None,
            None,
            None
        ],
        "text": [
            "Wake up my dear!",
            "Did you forget?",
            "It's your first day in school today",
            "Come on, we need to go faster, we are already late"
        ],
        "music": None,
        "audio": [
            None,
            None,
            None,
            None
        ],
        "render-game": True,
    },
    "intro-path-to-school": {
        "id": 2,
        "images": [
            None,
            None,
        ],
        "text": [
            "Hello, I see you want to get to school?",
            "take this path then!",
        ],
        "music": None,
        "audio": [
            None,
            None,
        ],
        "render-game": True,
    },
    "intro-tutorial": {
        "id": None,
        "images": [
            settings.pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            settings.pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_up.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_down.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_left.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_right.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','E.png')),
            settings.pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            settings.pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
        ],
        "text": [
            "Welcome to the game!",
            "It's an intro ... you clearly have seen that coming.",
            "To move forward press",
            "To move backwards press",
            "To move left press",
            "To move right press",
            "To interact with an NPC press",
            "From here on I will not interrupt anymore.",
            "Have fun in this humble game :3",
        ],
        "music": os.path.join('..', 'data', 'music', 'soft-piano-live-drums-music.mp3'),
        "audio": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ], 
        "render-game": False,
    },
    "tutorial":{
        "id": None,
        "images": [
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_up.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_down.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_left.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_right.png')),
            settings.pygame.image.load(os.path.join('..','graphics','tutorial','E.png')),
            ],
        "text":[
            "To move forward press",
            "To move backwards press",
            "To move left press",
            "To move right press",
            "To interact with an NPC press",
            ],
        "music": os.path.join('..', 'data', 'music', 'soft-piano-live-drums-music.mp3'),
        "audio": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        "render-game": False,
    },
}

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


def choose_cutscene(cutscene_order):
    for location in cutscene_data:
        if cutscene_data[location]["id"] == cutscene_order:
            return location
        else:
            pass

def play_cutscene(game, surface, location):
    data = cutscene_data[location]
    images_data = data["images"]
    text_data = data["text"]
    music_data = data["music"]
    audio_data = data["audio"]
    render_game_bool = data["render-game"]

    if music_data:
        music_player.play(music_data)
    
    for idx, image in enumerate(images_data):
        clock = pygame.time.Clock()
        check_audio(audio_data, idx)
        ##############################################################
        # Testing: Moving NPC in Cutscene(while rendering game)
        ##############################################################
        #if location == "intro":
        #    if idx == 2:
        #    npc_move(game, dt, move_x=10, move_y=0)
        ##############################################################
        if location == "intro-mother1":
            if idx == 1:
                npc_move(game, clock, move_x=50, move_y=0)
            if idx == 2:
                npc_move(game, clock, move_x=-20, move_y=0)

        if render_game_bool:
            render_game(game)
        else:
            surface.fill(BLACK_COLOR)
        if image:
            draw_image(image, scaler)
        if text_data:
            draw_text(surface, idx, text_data)
        settings.pygame.display.update()
        timer.start(3000, loop=True)                                                       # set timer for 'n' ms
        while timer.is_finished == False:
            timer.update()                                                              # update timer's state
            events()
    music_player.stop_music()


def events():
    for event in settings.pygame.event.get():
        if event.type == settings.pygame.QUIT:
            settings.pygame.quit()
        if event.type == settings.pygame.KEYDOWN:
            if event.key ==  settings.pygame.K_e:
                timer.is_finished = True

def draw_text(surface, idx, text_data):
    text_surface = settings.SMALLTEXT.render(text_data[idx], True, (WHITE_COLOR)).convert_alpha()
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = (settings.WINDOW_WIDTH // 2, 500)
    surface.blit(text_surface, text_surface_rect)

def draw_image(image, scaler):
    image_rect = image.get_rect()
    image_width, image_height = image.get_size()
    new_width = int(image_width * scaler)
    new_height = int(image_height * scaler)
    scaled_image = settings.pygame.transform.scale(image,(new_height,new_width))
    image_rect.center = (settings.WINDOW_WIDTH // 2.18, settings.WINDOW_HEIGHT // 2.2)
    surface.blit(scaled_image, image_rect)

def check_audio(audio_data, idx):
    if audio_data[idx] != None:
        audio = settings.pygame.mixer.Sound(audio_data[idx])
        audio.play()

def render_game(game):
    game.handle_game_events()
    game.render_new_game_world(draw_hud=False)
    settings.pygame.display.flip()
    game.clock.tick(game.fps_lock) 

def npc_move(game, clock, move_x=0, move_y=0):
    for npc in game.npcs_on_current_screen:
        if npc.name == "player-mother":
            if move_x > 0:
                while move_x > 0:
                    dt = clock.tick(game.fps_lock) / 1000
                    npc.move(dt, direction_x=1)
                    move_x -= 1
                    npc_move_handle(game)
            elif move_x < 0:
                while move_x < 0:
                    dt = clock.tick(game.fps_lock) / 1000
                    npc.move(dt, direction_x=-1)
                    move_x += 1
                    npc_move_handle(game)
            elif move_x < 0:
                while move_x < 0:
                    dt = clock.tick(game.fps_lock) / 1000
                    npc.move(dt, direction_x=-1)
                    move_x += 1
                    npc_move_handle(game)
            if move_y > 0:
                while move_y > 0:
                    dt = clock.tick(game.fps_lock) / 1000
                    npc.move(dt, direction_x=-1)
                    move_x += 1
                    npc_move_handle(game)
            elif move_y < 0:
                    dt = clock.tick(game.fps_lock) / 1000
                    npc.move(dt, direction_x=-1)
                    move_x += 1
                    npc_move_handle(game)
                                        
def npc_move_handle(game):
    game.handle_game_events()
    game.render_new_game_world(draw_hud=False)
    settings.pygame.display.flip()
    game.clock.tick(game.fps_lock)
   