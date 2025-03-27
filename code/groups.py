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

import settings
from items import Items

######### CLASSes ##############
class AllSprites(settings.pygame.sprite.Group):
    def __init__(self):
        super().__init__()                                                                                              # inherit all the functionality and attributes of the pygame.sprite.Group class
        self.SCREEN = settings.pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        self.offset = settings.vector()                                                                                          # creating offset for camera

    def draw(self, player_center):                                                                                      # drawing method for camera
        self.offset.x = -(player_center[0] - settings.WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - settings.WINDOW_HEIGHT / 2)

        # LAYERS (SORTING CLASSES IN LAYERS)
        bg_sprites = [sprite for sprite in self if sprite.z < settings.WORLD_LAYERS['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == settings.WORLD_LAYERS['main']], key=lambda sprite: sprite.y_sort) # lambda = quick, one-time function  #creating a sorting key function that extracts the y_sort attribute from each sprite object. Allows the sprites to be sorted based on their y_sort value. Used to determine their vertical drawing order
        fg_sprites = [sprite for sprite in self if sprite.z > settings.WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):                                                                # return all sprites that are in this class (AllSprites) and in these layers
            for sprite in layer:
                if isinstance(sprite, Items):
                    if sprite.is_drawing:
                        pass
                    else:
                        continue        # if Item shouldn't be drawn, skip drawing section of the code
                self.SCREEN.blit(sprite.image, sprite.rect.topleft + self.offset)
