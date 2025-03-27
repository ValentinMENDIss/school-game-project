######### IMPORT ##############

import settings
from ui import Button

######### CLASSes ############
class HUD:
    def __init__(self, game, player):
        self.game = game
        self.items = []
        self.player = player
        self.pos_x , self.pos_y = (settings.WINDOW_WIDTH // 2 - 20), (settings.WINDOW_HEIGHT // 2 - 85)
        self.initialized_time_text = False
        self.initialized_player_level_text = False
        self.initialized_money_text = False

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def check_player_health(self, surface, player):
        for max_health, image in HEALTH_THRESHOLDS:
            if player.health <= max_health:
                surface.blit(image, (self.pos_x, self.pos_y))
                break

    def draw(self, surface):
        self.draw_time(surface)
        self.draw_player_level(surface)
        self.draw_player_health(surface)
        self.draw_settings_button(surface)
        self.draw_inventory_button(surface)
        self.draw_player_money(surface)
        
    def update_time_text(self, new_time_text):
        if self.initialized_time_text == False:
            self.old_time_text = self.game.game_time.get_time_12hr()
            self.timetextfont = settings.HEADINGTEXT.render(self.old_time_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text
            self.timetextrect = self.timetextfont.get_rect()
            self.timetextrect.center = (settings.WINDOW_WIDTH // 2, 50)
            self.initialized_time_text = True

        if self.old_time_text != new_time_text:
            self.old_time_text = new_time_text
            self.timetextfont = settings.HEADINGTEXT.render(self.old_time_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text

            self.timetextrect = self.timetextfont.get_rect()                                                                    # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            self.timetextrect.center = (settings.WINDOW_WIDTH // 2, 50)                                      # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
            
            if self.game.debug:
                print("NEW_TIME_TEXT")

    def update_player_level_text(self, new_level_text):
        #if self.initialized_player_level_text == False:
        self.old_level_text = f"Level: {self.player.level}"
        self.leveltextfont = settings.HEADINGTEXT.render(self.old_level_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text
        self.leveltextrect = self.leveltextfont.get_rect()
        self.leveltextrect.center = (settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT - 100)
        self.initialized_player_level_text = True
        
        if self.old_level_text != new_level_text:
            self.old_level_text = new_level_text
            self.leveltextfont = settings.HEADINGTEXT.render(self.old_level_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text
            self.leveltextrect = self.leveltextfont.get_rect()                                                                    # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            self.leveltextrect.center = (settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT - 100)                                      # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
            
            if self.game.debug:
                print("NEW_LEVEL_TEXT")

    def update_money_text(self, new_money_text):
        if self.initialized_money_text == False:
            self.old_money_text = f"Money: {self.player.money}"
            self.moneytextfont = settings.HEADINGTEXT.render(self.old_money_text, True, (0, 0, 0)).convert_alpha()
            self.moneytextrect = self.moneytextfont.get_rect()
            self.moneytextrect.center = (200, settings.WINDOW_HEIGHT - 100)

        if self.old_money_text != new_money_text:
            self.old_money_text = new_money_text
            self.moneytextfont = settings.HEADINGTEXT.render(self.old_money_text, True, (0, 0, 0)).convert_alpha()
            self.moneytextrect = self.moneytextfont.get_rect()
            self.moneytextrect.center = (200, settings.WINDOW_HEIGHT - 100)
        
    def draw_time(self, surface):
        time_text = self.game.game_time.get_time_12hr()
        self.update_time_text(time_text)
        surface.blit(self.timetextfont, self.timetextrect)

    def draw_player_level(self, surface):
        level_text = f"Level: {self.player.level}"
        self.update_player_level_text(level_text)
        surface.blit(self.leveltextfont, self.leveltextrect)
        
    def draw_player_health(self,surface):
        for player_health ,obj in settings.HEALTH_THRESHOLDS:
            if self.player.health >= player_health:
                image = settings.pygame.transform.scale(obj, (340,164))
                imagerect = image.get_frect()
                imagerect.center = (settings.WINDOW_WIDTH / 2 , settings.WINDOW_HEIGHT - 50)
                surface.blit(image, imagerect)

    def draw_player_money(self, surface):
        money_text = f"Money: {self.player.money}"
        self.update_money_text(money_text)
        surface.blit(self.moneytextfont, self.moneytextrect)
                
    def draw_settings_button(self, surface):
        self.settings_button = Button(20, 20, scale=0.5, image=settings.UI_SETTINGS_IMG, hovered_image=settings.UI_SETTINGS_IMG)
        self.settings_button.draw(surface)
        
    def draw_inventory_button(self, surface):
        self.inventory_button = Button (20, settings.WINDOW_HEIGHT - 20, scale=0.5, image=settings.UI_INVENTORY_IMG, hovered_image=settings.UI_INVENTORY_IMG)
        self.inventory_button.draw(surface)
