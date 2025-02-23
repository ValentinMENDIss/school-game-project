import pygame

from settings import *
from timer import Timer
from music import Music
music_player = Music()
timer = Timer()

cutscene_data = {
    "intro": {
        "images": [
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png')),
            pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png'))
        ],
        "text": [
            "Welcome to the game!",
            "It's an intro ... you clearly have seen that coming.",
            "From here on I will not interrupt you anymore.",
            "Have fun in this humble game :3"
        ],
        "music": os.path.join('..', 'data', 'music', 'soft-piano-live-drums-music.mp3')
    }
}

def play_cutscene(screen, location):
    if location in cutscene_data:
        data = cutscene_data[location]
        images = data["images"]
        text = data["text"]
        music = data["music"]
        
        if music:
            music_player.play(music)

        for idx, image in enumerate(images):
            screen.fill((255, 255, 255))
            image_rect = image.get_rect()
            image_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            screen.blit(image, image_rect)
            if text:
                text_surface = SMALLTEXT.render(text[idx], True, (0, 0, 0)).convert_alpha()
                text_surface_rect = text_surface.get_rect()
                text_surface_rect.center = (WINDOW_WIDTH // 2, 500)
                screen.blit(text_surface, text_surface_rect)
            pygame.display.update()
            timer.start(3000, loop=True)                                                       # set timer for 'n' ms
            while timer.is_finished == False:
                timer.update()                                                              # update timer's state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key ==  pygame.K_SPACE:
                            pass
                        
        music_player.stop_music()
#                if timer.is_finished:                                                       # if timer is finished
#                    idx += 1
#                    print(idx)
#                    timer.is_finished = False