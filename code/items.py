######### IMPORT ##############

from settings import *
from gamedata import *

######### CLASSes ##############

class Items(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups, game):
        super().__init__(groups)
        self.game = game
        self.pos = pos
        self.name = name
        self.image = ITEM_TEST.convert_alpha()
        self.rect = self.image.get_frect(center=(self.pos))
        self.z = WORLD_LAYERS['item']
        self.y_sort = self.rect.centery
        self.offset = vector()
        self.inventory = self.game.inventory

    def pickup_logic(self, player_center):
        self.player_center = player_center
        if abs(self.pos[0] - self.player_center[0]) <= 100 and abs(self.pos[1] - self.player_center[1]) <= 100:         # ; [0] = x; [1] = y;
            pygame.mixer.Sound.play(PICKUP_SOUND)                                                                       # play sound
            pygame.mixer.music.stop()                                                                                   # stop sound
            self.inventory.add_item(self.name)
            self.kill()                                                                                                 # remove the item from all sprites groups atfter pickup, avoiding reprocessing
        self.game.action = None                                                                                         # reset variable that stores action (from action handling)
                         
#                    if key == "item-test":
#                        item_data = ITEM_INTERACT_DATA_RARE
#                    elif key == "item-test2":
#                        item_data = ITEM_INTERACT_DATA_EPIC
#                    else:
#                        continue

                    #random select of abilities
#                    effect, multiplier = random.choice(list(item_data.items()))
#                    if effect == "health_mul":
#                        self.game.player.health *= 1 + multiplier
#                        print(f"Health increased by {multiplier * 100:.1f}%")
#                    elif effect == "stamina_mul":
#                        self.game.player.stamina *= 1 + multiplier
#                        print(f"Stamina increased by {multiplier * 100:.1f}%")
#                    elif effect == "attack_mul":
#                        self.game.player.attack *= 1 + multiplier
#                        print(f"Attack increased by {multiplier * 100:.1f}%")
#                    elif effect == "defence_mul":
#                        self.game.player.defense *= 1 + multiplier
#                        print(f"Defense increased by {multiplier * 100:.1f}%")

#####################################################################################################

#                    if key == "item-test" or key == "item-test2": # Überprüfen, ob das Item ein "Health"-Item ist und den Multiplikator anwenden
#                        self.game.player.health = self.game.player.health * self.multiplicator  # Health erhöhen
#                        print(self.game.player.health)
#                        ITEM_INTERACT_DATA.append(key)
#                        
                    
                    
