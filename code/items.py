######### IMPORT ##############

from settings import *

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

        self.DATA[name] = {}
        self.DATA[name][self.pos] = {}
        self.DATA[name][self.pos]["x"] = pos[0]
        self.DATA[name][pos]["y"] = pos[1]

    def draw(self, surface):

        print(self.DATA)

        for item in self.DATA:
            print(item)
            #if item == "item-test":
            for key, value in  self.DATA.items():
                for coord, coord_data in value.items():
                        #print(f"Key/Name: {key}, Coordinates: {coord}, x: {coord_data['x']}, y: {coord_data['y']}")    # diagnosing code/printing out values inside of self.DATA dictionary
                    self.item_pos_x = coord_data['x']
                    self.item_pos_y = coord_data['y']

                    if key == "item-test":
                        self.image = ITEM_TEST.convert_alpha()
                    elif key == "item-test2":
                        self.image = ITEM_TEST2.convert_alpha()

                    self.rect = self.image.get_frect(center=(self.item_pos_x, self.item_pos_y))
                    print(self.item_pos_x, self.item_pos_y)
                    surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_position(self):
        print("\nUwU 1 ", self.DATA[self.name][self.pos]['x'])
        print("UwU 2 ", self.DATA[self.name][self.pos]['x'])
        print(self.DATA)