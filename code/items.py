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
                        self.game.player.health *= 1 + self.multiplier
                        print(f"Health increased by {self.multiplier * 100:.1f}%")
                    elif self.effect == "stamina_mul":
                        self.game.player.stamina *= 1 + self.multiplier
                        print(f"Stamina increased by {self.multiplier * 100:.1f}%")
                    elif self.effect == "damage_mul":
                        self.game.player.damage *= 1 + self.multiplier
                        print(f"Attack increased by {self.multiplier * 100:.1f}%")
                    elif self.effect == "defence_mul":
                        self.game.player.defense *= 1 + self.multiplier
                        print(f"Defense increased by {self.multiplier * 100:.1f}%")

    def destroy_item(self):
        self.game.hud.remove_item(item=self)
        self.kill()
#####################################################################################################

#                    if key == "item-test" or key == "item-test2": # Überprüfen, ob das Item ein "Health"-Item ist und den Multiplikator anwenden
#                        self.game.player.health = self.game.player.health * self.multiplicator  # Health erhöhen
#                        print(self.game.player.health)
#                        ITEM_INTERACT_DATA.append(key)
#
