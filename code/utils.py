import settings

def render_text(surface, text, pos_x, pos_y, color=(0,0,0), size=25):
        TEXT = settings.pygame.font.Font(settings.os.path.join('..', 'font', 'Pixeltype.ttf'), size)
        
        text = TEXT.render(str(text), True, color).convert_alpha()        # render an enemy text
        textrect = text.get_rect()
        textrect.center = (pos_x, pos_y)

        surface.blit(text, textrect)
