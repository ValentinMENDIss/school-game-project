from inventory import Inventory
from items import Items
from settings import *
from button import Button

class Shop:
    def __init__(self, game):
        self.game = game
        self.items_updated = False
        self.items = {
            "item-test": {
                "name": "Apple",
                "rarity": "RARE",
                "price": 5.99
            },
            "item-test2": {
                "name": "Water Bottle",
                "rarity": "Epic",
                "price": 1.99
            }
        }

    def display_shop(self, surface):
        self.running = True
        while self.running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Display shop background
            surface.fill((255, 255, 255))  # White background for the shop
            heading_text = "Shop"
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()
            headingtextrect = headingtext.get_rect(center=(WINDOW_WIDTH // 2, 50))
            surface.blit(headingtext, headingtextrect)
            self.display_items(surface, MENU_MOUSE_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.current_screen = "game"
                    
            self.check_input()
                
            pygame.display.update()


    def check_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[self.game.input.key_bindings["shop_toggle"]]:
            self.running = False
            self.game.current_screen = "game"


    def display_items(self, surface, MENU_MOUSE_POS):
        column_count = 0                                        # y coordinates
        row_count = 0                                           # x coordinates
        items_pos_init_x = 300
        items_pos_init_y = 200
        max_length = (WINDOW_WIDTH - 200)
        for item in self.items:
            local_item = self.items[item]
            if item == "item-test":
                item_image = ITEM_TEST.convert_alpha()
            if item == "item-test2":
                item_image = ITEM_TEST2.convert_alpha()           
            else:
                item_image = ITEM_TEST.convert_alpha()
            items_pos_x = items_pos_init_x + (100 * row_count)
            items_pos_y = items_pos_init_y + (100 * column_count)
            if items_pos_x >= max_length:
                row_count = 0
                column_count += 1
                items_pos_x = items_pos_init_x + (100 * row_count)
                items_pos_y = items_pos_init_y + (100 * column_count)
            button = Button(items_pos_x , items_pos_y, scale=1, image=item_image)
            button.draw(surface)
            row_count += 1
        self.items_updated = True