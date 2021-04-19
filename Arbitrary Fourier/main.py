import pygame
import math
from settings import *

class Main:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.win_width = WIN_WIDTH
        self.win_height = WIN_HEIGHT
        self.xoff = X_OFF
        self.yoff = Y_OFF
        self.fps = FPS
        self.win = None
        self.gameWin = None
        self.gameWidth = None
        self.clock = None
        self.titleFont = None

    def display_init(self):

        pygame.init()
        pygame.display.init()
        pygame.font.init()

        winDims = self.width, self.height
        self.win = pygame.display.set_mode(winDims)
        pygame.display.set_caption("Arbitrary Fourier Tranform")
        self.win.fill(MIDBLACK)

        self.gameWin = self.win.subsurface((self.xoff, self.yoff, self.win_width, self.win_height))
        self.gameWin.fill(STEEL_BLUE)

        self.clock = pygame.time.Clock()

        self.titleFont = pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE)
        title = self.titleFont.render(TITLE_TEXT, 1, GOLD)
        w, h = title.get_size()

        blitX = (self.width - w) // 2
        blitY = (self.yoff - h) // 2

        self.win.blit(title, (blitX, blitY))
        pygame.display.update()


    def draw(self):
        pass

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

            self.draw()

        self.quit()



if __name__ == "__main__":
    X = Main()
    X.run()