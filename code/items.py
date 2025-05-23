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
from gamedata import *

######### CLASSes ##############

class Items(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups, rarity, game):                                                                 # Positional arguments → Then keyword arguments
        super().__init__(groups)
        self.game = game
        self.pos = pos
        self.name = name
        self.rarity = rarity
        self.image = ITEM_TEST.convert_alpha()
        self.rect = self.image.get_frect(center=(self.pos))
        self.z = WORLD_LAYERS['item']
        self.y_sort = self.rect.centery
        self.offset = vector()
        self.effect = None
        self.multiplier = None
        self.is_drawing = True
        self.IsTakeable = True

        if self.rarity == "RARE":
            self.item_data = ITEM_RARITY_DATA_RARE
        elif self.rarity == "EPIC":
            self.item_data = ITEM_RARITY_DATA_EPIC


    def pickup_logic(self, player_center):
        if self.IsTakeable:
            self.player_center = player_center
            if abs(self.pos[0] - self.player_center[0]) <= 100 and abs(self.pos[1] - self.player_center[1]) <= 100:         # ; [0] = x; [1] = y;
                pygame.mixer.Sound.play(PICKUP_SOUND)                                                                       # play sound
                self.game.inventory.add_item(self)
                self.is_drawing = False                                                                                                 # remove the item from all sprites groups atfter pickup, avoiding reprocessing
                self.IsTakeable = False
            self.game.action = None                                                                                         # reset variable that stores action (from action handling)

    def use_item(self):
        self.random_abilities()
        self.destroy_item()

    def random_abilities(self):
        # random select of abilities
        self.effect, self.multiplier = random.choice(list(self.item_data.items()))
        if self.effect == "health_mul":
            self.game.player.health *= self.multiplier
            self.game.player.change_health(self.multiplier)
            print(f"Health increased by {self.multiplier * 100:.1f}%")
        elif self.effect == "stamina_mul":
            self.game.player.stamina *= self.multiplier
            self.game.player.change_stamina(self.multiplier)
            print(f"Stamina increased by {self.multiplier * 100:.1f}%")
        elif self.effect == "damage_mul":
            self.game.player.damage *= self.multiplier
            self.game.player.change_damage(self.multiplier)
            print(f"Attack increased by {self.multiplier * 100:.1f}%")
        elif self.effect == "defence_mul":
            self.game.player.defence *= self.multiplier
            self.game.player.change_defence(self.multiplier)
            print(f"Defence increased by {self.multiplier * 100:.1f}%")

    def destroy_item(self):
        self.game.inventory.remove_item(item=self)
        self.kill()
#####################################################################################################

#                    if key == "item-test" or key == "item-test2": # Überprüfen, ob das Item ein "Health"-Item ist und den Multiplikator anwenden
#                        self.game.player.health = self.game.player.health * self.multiplicator  # Health erhöhen
#                        print(self.game.player.health)
#                        ITEM_INTERACT_DATA.append(key)
#
