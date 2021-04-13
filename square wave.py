import pygame
from settings import *

class Square_Wave:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.win_width = WIN_WIDTH
        self.win_height = WIN_HEIGHT
        self.xoff = X_OFF
        self.yoff = Y_OFF
        self.fps = FPS
        self.clock = None
        self.win = None
        self.gameWin = None
        self.title_font = None

    def display_init(self):
        
        pygame.init()
        pygame.font.init()
        pygame.display.init()

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Square Wave - Fourier")
        
        self.gameWin = self.win.subsurface((self.xoff, self.yoff, self.win_width, self.win_height))

        self.win.fill(MIDBLACK)
        self.gameWin.fill(STEEL_BLUE)

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(TITLE_FONT, 40)
        title = self.title_font.render(TITLE_TEXT, 1, GOLD)
        w, h = title.get_size()
        blitX = (self.width - w) // 2
        blitY = (self.yoff - h) // 2

        self.win.blit(title, (blitX, blitY))

        pygame.display.update()


    def quit(self):
        pygame.font.quit()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        
        if not pygame.display.get_init():
            self.display_init()

        run = True
        while run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            pygame.display.update()

        self.quit()
        

if __name__ == "__main__":
    X = Square_Wave()
    X.run()