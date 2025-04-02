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
    "intro-tutorial": {
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

def play_cutscene(game, surface, location):
    data = cutscene_data[location]
    images_data = data["images"]
    text_data = data["text"]
    music_data = data["music"]
    audio_data = data["audio"]
    render_game_bool = data["render-game"]

    if music_data:
        music_player.play(music_data)
    
    if location == "intro":
        for idx, image in enumerate(images_data):
            if audio_data[idx] != None:
                audio = settings.pygame.mixer.Sound(audio_data[idx])
                audio.play()
            if render_game_bool:
                game.handle_game_events()
                game.render_new_game_world()
                settings.pygame.display.flip()
                game.clock.tick(game.fps_lock) 
            else:
                surface.fill(BLACK_COLOR)
            if image:
                image_rect = image.get_rect()
                image_width, image_height = image.get_size()
                scaler = 4
                new_width = int(image_width * scaler)
                new_height = int(image_height * scaler)
                scaled_image = settings.pygame.transform.scale(image,(new_height,new_width))
                image_rect.center = (settings.WINDOW_WIDTH // 2.18, settings.WINDOW_HEIGHT // 2.2)
                surface.blit(scaled_image, image_rect)
            if text_data:
                draw_text(surface, idx, text_data)
            settings.pygame.display.update()
            timer.start(3000, loop=True)                                                       # set timer for 'n' ms
            while timer.is_finished == False:
                timer.update()                                                              # update timer's state
                for event in settings.pygame.event.get():
                    if event.type == settings.pygame.QUIT:
                        settings.pygame.quit()
                    if event.type == settings.pygame.KEYDOWN:
                        if event.key ==  settings.pygame.K_e:
                            timer.is_finished = True
        music_player.stop_music()
        
def draw_text(surface, idx, text_data):
    text_surface = settings.SMALLTEXT.render(text_data[idx], True, (WHITE_COLOR)).convert_alpha()
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = (settings.WINDOW_WIDTH // 2, 500)
    surface.blit(text_surface, text_surface_rect)
