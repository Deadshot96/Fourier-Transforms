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

        self.points = list()
        self.drawFlag = True

    def display_init(self):

        pygame.init()
        pygame.display.init()
        pygame.font.init()

        winDims = self.width, self.height
        self.win = pygame.display.set_mode(winDims)
        pygame.display.set_caption("Arbitrary Fourier Tranform")
        self.win.fill(MIDBLACK)

        self.gameRect = pygame.Rect((self.xoff, self.yoff, self.win_width, self.win_height))
        self.gameWin = self.win.subsurface(self.gameRect)
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

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     x, y = pygame.mouse.get_pos()

                #     if self.drawFlag and self.gameRect.collidepoint(x - self.xoff, y - self.yoff):
                #         x -= self.xoff
                #         y -= self.yoff
                #         print("In MOUSEBUTTONDOWN: ", x, y, sep="\t")
                #         self.gameWin.set_at((x, y), MID_WHITE)
                #         pygame.display.update()
                #         self.points.append((x, y))

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drawFlag = False

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        self.gameWin.fill(STEEL_BLUE)
                        self.points.clear()
                        self.drawFlag = True

            pressed = pygame.mouse.get_pressed()

            if pressed[0]:
                    x, y = pygame.mouse.get_pos()

                    if self.drawFlag and self.gameRect.collidepoint(x - self.xoff, y - self.yoff):
                        x -= self.xoff
                        y -= self.yoff
                        self.gameWin.set_at((x, y), MID_WHITE)
                        self.points.append((x, y))

                        if len(self.points) > 2:
                            p1 = self.points[-1]
                            p2 = self.points[-2]

                            pygame.draw.line(self.gameWin, MID_WHITE, p2, p1) 

            self.draw()

        self.quit()



if __name__ == "__main__":
    X = Main()
    X.run()