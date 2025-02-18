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

    def remove_item(self, item):
        self.items.remove(item)
        self.hud.remove_item(item)

    def show_items(self):
        print(self.items)
