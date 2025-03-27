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

from settings import *


######### CLASSes #############

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)                                                                                        # use group's original instruction set to set up the new class (Sprite)
        self.image = surf                                                                                               # storing image(sprite)
        self.rect = self.image.get_frect(topleft = pos)                                                                 # get_frect = get float rectangle position (better precision)
        self.z = z                                                                                                      # z axis (Layers)
        self.y_sort = self.rect.centery                                                                                 # y axis (needed for drawing objects in right order, when object is at front or behind something)
        self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)                                                                             # needed to initialize the parent Sprite class with those same values
        self.hitbox = self.rect.copy()                                                                                  # initialize new variable that stores rect. position of BorderSprite()'s Object

class CollidableSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)                                                                             # needed to initialize the parent Sprite class with those same values
		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)                                                     # initialize new variable that stores rect. position of BorderSprite()'s Object

class TransitionSprite(Sprite):
	def __init__(self, pos, size, target, groups):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.target = target
