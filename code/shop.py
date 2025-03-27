from inventory import Inventory
from items import Items
from settings import *
from ui import Button
from timer import Timer

class Shop:
    def __init__(self, game):
        self.debug = False
        self.game = game
        self.items_updated = False
        self.items = {
            "item-test": {
                "name": "Apple",
                "rarity": "RARE",
                "price": 5.99,
                "item_button": None
            },
            "item-test2": {
                "name": "Water Bottle",
                "rarity": "EPIC",
                "price": 1.99,
                "item_button": None
            }
        }
        self.action = None
        self.timer = Timer()

    def display_shop(self, surface):
        self.is_running = True
        while self.is_running:
            interacted_item = None
            # DEFINING CONSTANT VARIABLES
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
                    self.game.running = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if self.items[item]["item_button"].checkForInput(MENU_MOUSE_POS):
                            self.action = "buy_item"
                            interacted_item = item
            for item in self.items:
                item_button = self.items[item]["item_button"]
                if item_button.checkForInput(MENU_MOUSE_POS):     
                    item_button.hovered_on = True
                    if self.timer.active == False and not self.timer.is_finished:                         # if timer hasn't been started yet:
                        self.timer.start(500)                                                       # set timer for 'n' ms
                    self.timer.update()                                                              # update timer's state
                    if self.timer.is_finished:                                                       # if timer is finished
                        self.item_show_info(surface, MENU_MOUSE_POS, item)
                else:
                    if item_button.hovered_on:
                        self.timer.stop(loop=True)
                        item_button.hovered_on = False
 
                    
            if self.action == "buy_item":
                self.buy_item(interacted_item)

            self.check_input()
                
            pygame.display.update()


    def check_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[self.game.input.key_bindings["shop_toggle"]]:
            self.is_running = False
            self.game.action = None
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
            local_item["item_button"] = button
            button.draw(surface)
            row_count += 1
        self.items_updated = True
        
    def item_show_info(self, surface, MENU_MOUSE_POS, item):
        info_text =f"{self.items[item]['name']}\n{self.items[item]['rarity']}\n{self.items[item]['price']}"
        # Initialize variables to store the total height and maximum width
        text_height = 0
        text_width = 0

        lines = info_text.splitlines()                                                                                   # Split the text into lines
        for line in lines:
            width, height = SMALLTEXT.size(line)
            text_height += height
            if width > text_width:
                text_width = width
            
        infotext = SMALLTEXT.render(info_text, True, (0, 0, 0)).convert_alpha()                                     # render a Small Text
        infotextrect = infotext.get_rect()                                                                          # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
        
        mouse_x_pos = MENU_MOUSE_POS[0]
        mouse_y_pos = MENU_MOUSE_POS[1]
        offset_x = 15
        offset_y = 15

        infotextrect.topleft = (mouse_x_pos + offset_x, mouse_y_pos + offset_y)

        pygame.draw.rect(surface, (226, 233, 236), (mouse_x_pos, mouse_y_pos, text_width + (2*offset_x), text_height + (2*offset_y)))
        surface.blit(infotext, infotextrect)

    
    def buy_item(self, item):
        item_price = self.items[item]["price"]
        if item_price > self.game.player.money:
            print("Not enough money to buy this item")
        else:
            print(f"Money before transaction: {self.game.player.money}")
            created_item = Items((0, 0), item, self.game.all_sprites, rarity=self.items[item]["rarity"], game=self.game)
            self.game.player.money = round(self.game.player.money - item_price, 2)
            self.game.inventory.add_item(created_item) 
            self.items.pop(item)
            if self.debug:
                print(f"Inventory: {self.game.inventory}\nShop Items: {self.items}")
                print(f"Money after transaction: {self.game.player.money}")
        self.action = None
