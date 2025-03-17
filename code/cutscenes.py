import pygame
from settings import *
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
        "music": None
    },
    "intro-tutorial": {
        "images": [
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_up.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_down.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_left.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_right.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','E.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
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
        "music": os.path.join('..', 'data', 'music', 'soft-piano-live-drums-music.mp3')
    },
    "tutorial":{
        "images": [
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_up.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_down.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_left.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','arrowkey_right.png')),
            pygame.image.load(os.path.join('..','graphics','tutorial','E.png')),
            ],
        "text":[
            "To move forward press",
            "To move backwards press",
            "To move left press",
            "To move right press",
            "To interact with an NPC press",
            ],
        "music": os.path.join('..', 'data', 'music', 'soft-piano-live-drums-music.mp3')
        }
    
}

def play_cutscene(surface, location):
    data = cutscene_data[location]
    images_data = data["images"]
    text_data = data["text"]
    music_data = data["music"]

    if music_data:
        music_player.play(music_data)
    
    if location == "intro":
        for idx, image in enumerate(images_data):
            surface.fill((255, 255, 255))
            if image:
                image_rect = image.get_rect()
                image_width, image_height = image.get_size()
                scaler = 4
                new_width = int(image_width * scaler)
                new_height = int(image_height * scaler)
                scaled_image = pygame.transform.scale(image,(new_height,new_width))
                image_rect.center = (WINDOW_WIDTH // 2.18, WINDOW_HEIGHT // 2.2)
                surface.blit(scaled_image, image_rect)
            if text_data:
                draw_text(surface, idx, text_data)
            pygame.display.update()
            timer.start(3000, loop=True)                                                       # set timer for 'n' ms
            while timer.is_finished == False:
                timer.update()                                                              # update timer's state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key ==  pygame.K_e:
                            timer.is_finished = True
        music_player.stop_music()
        
def draw_text(surface, idx, text_data):
    text_surface = SMALLTEXT.render(text_data[idx], True, (0, 0, 0)).convert_alpha()
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = (WINDOW_WIDTH // 2, 500)
    surface.blit(text_surface, text_surface_rect)