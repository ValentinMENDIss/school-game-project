######### IMPORT ##############

from settings import *

######### CLASSes ##############

class Items:
    def __init__(self, game):
        self.DATA = {}                                                                                                  # creating/initializing Dictionary and assigning it to the variable
        self.game = game

    def add(self, pos, name):
        self.pos = pos
        self.name = name
        self.offset = vector()
        self.inventory = self.game.inventory

        self.DATA[name] = {}
        self.DATA[name][self.pos] = {}
        self.DATA[name][self.pos]["x"] = pos[0]
        self.DATA[name][self.pos]["y"] = pos[1]

    def remove(self, name):
        del self.DATA[name]

    def draw(self, surface, player_center):
        self.player_center = player_center

        for item in self.DATA:
            for key, value in  self.DATA.items():
                for coord, coord_data in value.items():
                    self.item_pos_x = coord_data['x']
                    self.item_pos_y = coord_data['y']

                    if key == "item-test":
                        self.image = ITEM_TEST.convert_alpha()
                    elif key == "item-test2":
                        self.image = ITEM_TEST2.convert_alpha()

                    self.rect = self.image.get_frect(center=(self.item_pos_x, self.item_pos_y))

                    self.offset.x = -(self.player_center[0] - WINDOW_WIDTH / 2)
                    self.offset.y = -(self.player_center[1] - WINDOW_HEIGHT / 2)

                surface.blit(self.image, self.rect.center + self.offset)

    def pickup_logic(self):
        self.data_copy = self.DATA.copy()
        for key, value in self.data_copy.items():
            for coord, coord_data in value.items():
                if abs(coord[0] - self.player_center[0]) <= 100 and abs(coord[1] - self.player_center[1]) <= 100:       # ; [0] = x; [1] = y;
                    pygame.mixer.Sound.play(PICKUP_SOUND)                                                               # play sound
                    pygame.mixer.music.stop()                                                                           # stop sound
                    self.remove(key)                                                                                    # remove item from the floor
                    if key == "item-test" or key == "item-test2": # Überprüfen, ob das Item ein "Health"-Item ist und den Multiplikator anwenden
                        self.game.player.health = self.game.player.health * self.multiplicator  # Health erhöhen
                        print(self.game.player.health)
                        ITEM_INTERACT_DATA.append(key)
                        
                    self.inventory.add_item(key)                                                                                                                                        # add item to the inventory
                    
                    