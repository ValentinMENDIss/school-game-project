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
        self.offset = vector()

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
                    #print(f"Key/Name: {key}, Coordinates: {coord}, x: {coord_data['x']}, y: {coord_data['y']}")    # diagnosing code/printing out values inside of self.DATA dictionary
                    self.item_pos_x = coord_data['x']
                    self.item_pos_y = coord_data['y']

                    if key == "item-test":
                        self.image = ITEM_TEST.convert_alpha()
                    elif key == "item-test2":
                        self.image = ITEM_TEST2.convert_alpha()

                    self.rect = self.image.get_frect(center=(self.item_pos_x, self.item_pos_y))

                    self.offset.x = -(self.player_center[0] - WINDOW_WIDTH / 2)
                    self.offset.y = -(self.player_center[1] - WINDOW_HEIGHT / 2)

                self.get_position()
                surface.blit(self.image, self.rect.center + self.offset)

    def get_position(self):
            self.data_copy = self.DATA.copy()
            for key, value in self.data_copy.items():
                for coord, coord_data in value.items():
                    self.pickup_logic(key, coord, self.player_center)

                    #print(f"name: {key}, coord: {coord}")
                    #print(coord[0])
                    #print(coord[1])
            #print(self.DATA)

    def pickup_logic(self, key, coord, player_center):
        #print(coord)
        keys = pygame.key.get_just_pressed()                                                                            # initialize new variable(keys) that will get user's input, but the buttons can be detected as pressed and not as hold too.
        if keys[pygame.K_e]:                                                                                            # if just pressed key is e do following:
            if abs(coord[0] - player_center[0]) <= 100 and abs(coord[1] - player_center[1]) <= 100:                                                                                 # ; [0] = x; [1] = y;
                if not self.print_message_flag:
                    self.remove(key)

                    print("hello world, we are back :3. YIPPEE!!!!!!!!!!!!!!!!!!")
                    print(abs(coord[0] - player_center[0]))
                    print(abs(coord[1] - player_center[1]))
                self.print_message_flag = True                                                                          # self.print_message_flag is needed, so that if we want, let's say, to print the text out, it will print it out the text only one time and not five, or even more times.
        else:
            self.print_message_flag = False