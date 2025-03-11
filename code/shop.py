# shop.py
from inventory import Inventory
from items import Items
from settings import *

class Shop:
    def __init__(self, game):
        self.game = game
        #self.items_for_sale = [
        #    Items((0, 0), "item-test", self.game.all_sprites, rarity="RARE", game=self.game),
        #    Items((0, 0), "item-test2", self.game.all_sprites, rarity="EPIC", game=self.game)
        #]
        self.selected_item_index = 0

    def display_shop(self, surface):
        self.running = True
        while self.running:
            # Display shop background
            surface.fill((255, 255, 255))  # White background for the shop
            heading_text = "Shop"
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()
            headingtextrect = headingtext.get_rect(center=(WINDOW_WIDTH // 2, 50))
            surface.blit(headingtext, headingtextrect)

            # Display items for sale
            #for index, item in enumerate(self.items_for_sale):
            #    item_text = f"{item.name} - Price: {self.get_item_price(item)}"
            #    item_surface = SMALLTEXT.render(item_text, True, (0, 0, 0)).convert_alpha()
            #    item_rect = item_surface.get_rect(center=(WINDOW_WIDTH // 2, 100 + index * 30))
            #    surface.blit(item_surface, item_rect)

            # Highlight selected item
            #selected_item_text = f"> {self.items_for_sale[self.selected_item_index].name} <"
            #selected_item_surface = HEADINGTEXT.render(selected_item_text, True, (255, 0, 0)).convert_alpha()
            #selected_item_rect = selected_item_surface.get_rect(center=(WINDOW_WIDTH // 2, 100 + self.selected_item_index * 30))
            #surface.blit(selected_item_surface, selected_item_rect)
            
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



    def get_item_price(self, item):
        # Define prices for items
        prices = {
            "item-test": 10,
            "item-test2": 20
        }
        return prices.get(item.name, 0)

    def purchase_item(self):
        item = self.items_for_sale[self.selected_item_index]
        price = self.get_item_price(item)
        if self.game.player.gold >= price:  # Assuming player has a gold attribute
            self.game.player.gold -= price
            self.game.inventory.add_item(item)
            print(f"Purchased {item.name} for {price} gold.")
        else:
            print("Not enough gold!")

    def navigate_items(self, direction):
        if direction == "up":
            self.selected_item_index = (self.selected_item_index - 1) % len(self.items_for_sale)
        elif direction == "down":
            self.selected_item_index = (self.selected_item_index + 1) % len(self.items_for_sale)

