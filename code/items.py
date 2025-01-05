######### IMPORT ##############

from settings import *
from inventory import *

######### SPRITEs ##############

ITEM_TEST = pygame.image.load(os.path.join('..', 'graphics', 'item-test.png'))                                          # load sprite of the ITEM_TEST
ITEM_TEST2 = pygame.image.load(os.path.join('..', 'graphics', 'item-test2.png'))                                          # load sprite of the ITEM_TEST2

######### CLASSes ##############

class Items:
    def __init__(self):
        self.DATA = {}                                                                                                  # creating/initializing Dictionary and assigning it to the variable

    def add(self, pos, name):
        self.pos = pos
        self.name = name
        self.offset = vector()
        self.inventory = Inventory()

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
                if abs(coord[0] - self.player_center[0]) <= 100 and abs(coord[1] - self.player_center[1]) <= 100:                                                                                 # ; [0] = x; [1] = y;
                    self.remove(key)
                    self.inventory.add_item(key)