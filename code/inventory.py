######### IMPORT ##############

from settings import *
from hud import *

######### CLASSes ##############

class Inventory:
    def __init__(self, game):
        self.items = []
        self.game = game

    def add_item(self, item):
        self.hud = self.game.hud
        self.items.append(item)

        self.hud.add_item(item)
#        print(f"Your Inventory: {self.items}")
#        print(f"Your Health was increased: {self.game.player.health}")
#        print(f"{ITEM_INTERACT_DATA}")

    def remove_item(self, item):
        self.items.remove(item)

    def show_items(self):
        print(self.items)
