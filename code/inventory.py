######### IMPORT ##############

import settings
from hud import *
from timer import Timer

######### CLASSes ##############


class Inventory:
    def __init__(self, game):
        self.items = []
        self.items_dict = {}
        self.game = game
        self.timer = Timer()

    def add_item(self, item):
        self.hud = self.game.hud
        self.items.append(item)
        self.hud.add_item(item)

    def remove_item(self, item):
        self.items.remove(item)
        self.hud.remove_item(item)

    def show_items(self):
        print(self.items)
    
    def show_menu(self, surface):
        self.is_running = True
        self.initialized = False
        self.items_dict = {}
        while self.is_running:
            # INITIALIZING BUTTONS
            EXIT_BUTTON = Button(20, settings.WINDOW_HEIGHT - 20, scale=0.50, image=settings.UI_INVENTORY_IMG, hovered_image=settings.UI_INVENTORY_IMG)
            BACKGROUND_COLOR = ((255, 255, 255))

            # SETTING TEXT FOR MENU
            heading_text = "Your Items"

            # DEFINING TEXT VARIABLES
            headingtext = settings.HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = settings.pygame.mouse.get_pos()

            # DRAWING ON THE SURFACE
            surface.fill(BACKGROUND_COLOR)
            surface.blit(headingtext, headingtextrect)

            ## DRAWING BUTTONS ##
            self.__draw_items(surface, items_pos_init_x=300, items_pos_init_y=200)
            for button in [EXIT_BUTTON]:                     # iterate through every single button instance and draw it to the screen
                button.draw(surface)

            ## EVENTS ##
            for event in settings.pygame.event.get():
                if event.type == settings.pygame.QUIT:                                                                               # exit game function
                    self.game.running = False
                    exit()
                if event.type == settings.pygame.MOUSEBUTTONDOWN:
                    if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.is_running = False
                    for item_button in self.items_dict:
                        if item_button.checkForInput(MENU_MOUSE_POS):
                            item = self.items_dict[item_button]["item"]
                            self.item_show_info(surface, MENU_MOUSE_POS, item)
            for item_button in self.items_dict:
                if item_button.checkForInput(MENU_MOUSE_POS):     
                    item_button.hovered_on = True
                    if self.timer.active == False and not self.timer.is_finished:                         # if timer hasn't been started yet:
                        self.timer.start(500)                                                       # set timer for 'n' ms
                    self.timer.update()                                                              # update timer's state
                    if self.timer.is_finished:                                                       # if timer is finished
                        item = self.items_dict[item_button]["item"]
                        self.item_show_info(surface, MENU_MOUSE_POS, item)
                else:
                    if item_button.hovered_on:
                        self.timer.stop(loop=True)
                        item_button.hovered_on = False
                    
            self.game.clock.tick(60)
            settings.pygame.display.update()

    def __draw_items(self, surface, items_pos_init_x, items_pos_init_y, max_length=(settings.WINDOW_WIDTH - 200)):
        items_pos_x = items_pos_init_x
        items_pos_y = items_pos_init_y
        for item in self.items:
            if item.name == "item-test":
                item_image = settings.ITEM_TEST.convert_alpha()
            elif item.name == "item-test2":
                item_image = settings.ITEM_TEST2.convert_alpha()
            button = Button(items_pos_x , items_pos_y, scale=1, image=item_image)
            if self.initialized == False:
                new_item_info = {button: {'item': item}}
                self.items_dict.update(new_item_info)
            items_pos_x += 100
            if items_pos_x >= max_length:
                items_pos_y += 100
                items_pos_x = items_pos_init_x
            button.draw(surface)
        self.initialized = True
            
    def item_show_info(self, surface, MENU_MOUSE_POS, item):
        info_text = f"{item.name}\n{item.rarity}"
        # Initialize variables to store the total height and maximum width
        text_height = 0
        text_width = 0

        lines = info_text.splitlines()                                                                                   # Split the text into lines
        for line in lines:
            width, height = settings.SMALLTEXT.size(line)
            text_height += height
            if width > text_width:
                text_width = width
            
        infotext = settings.SMALLTEXT.render(info_text, True, (0, 0, 0)).convert_alpha()                                     # render a Small Text
        infotextrect = infotext.get_rect()                                                                          # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
        
        mouse_x_pos = MENU_MOUSE_POS[0]
        mouse_y_pos = MENU_MOUSE_POS[1]
        offset_x = 15
        offset_y = 15

        infotextrect.topleft = (mouse_x_pos + offset_x, mouse_y_pos + offset_y)

        settings.pygame.draw.rect(surface, (226, 233, 236), (mouse_x_pos, mouse_y_pos, text_width + (2*offset_x), text_height + (2*offset_y)))
        surface.blit(infotext, infotextrect)
