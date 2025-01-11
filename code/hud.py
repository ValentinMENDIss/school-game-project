######### IMPORT ##############

from settings import  *

######### CLASSes ############
class HUD:
    def __init__(self, player):
        self.items = []
        self.player = player
        self.pos_x , self.pos_y = (WINDOW_WIDTH // 2 - 20), (WINDOW_HEIGHT // 2 - 85)

    def add_item(self, item):
        self.items.append(item)

    def check_player_health(self, surface, player):
        if player.health == 0:
            surface.blit(HEALTH_0, (self.pos_x, self.pos_y))
        elif player.health > 0 and player.health <= 10:
            surface.blit(HEALTH_10, (self.pos_x, self.pos_y))
        else:
            surface.blit(HEALTH_100, (self.pos_x, self.pos_y))


    def draw(self, surface):
        self.offset = 0
        for item in self.items:
            if item == "item-test":
                self.image = ITEM_TEST.convert_alpha()
            elif item == "item-test2":
                self.image = ITEM_TEST2.convert_alpha()

            self.get_x_coords = WINDOW_WIDTH // 2 - (16 * len(self.items))
            self.get_y_coords = WINDOW_HEIGHT - 50

            surface.blit(self.image, (self.get_x_coords + self.offset, self.get_y_coords))     # Draw every single item in the middle of the x axes of the screen/surface, change coordinates based on how many items are there and add self.offset to put every item slightly after previous picture. On y axes put it slightly above the WINDOW_HEIGHT value
            self.offset += 35

        self.check_player_health(surface, self.player)

