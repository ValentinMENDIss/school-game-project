######### IMPORT ##############

from settings import *

######### CLASSes ##############

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Your Inventory: {self.items}")

    def remove_item(self, item):
        self.items.remove(item)

    def show_items(self):
        print(self.items)