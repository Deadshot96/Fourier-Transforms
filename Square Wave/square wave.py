import pygame
from settings import *
import math

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
        
        self.N = 4
        self.wave = list()
        self.numWavePoints = 650
        self.time = 0
        self.timeDelta = 0.05
        self.x = 20
        self.xDelta = 1
        self.circle_pos_x = int(self.win_width * 0.25)
        self.circle_pos_y = self.win_height // 2
        self.circle_pos = self.circle_pos_x, self.circle_pos_y
        self.circle_radius = self.win_height // 6


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

    def draw(self):
        self.gameWin.fill(STEEL_BLUE)
        x, y = self.circle_pos

        lineX = int(self.circle_radius * 3) + self.xoff + self.circle_pos_x
        lineY1 = self.circle_pos_y - int(self.circle_radius * 2) 
        lineY2 = self.circle_pos_y + int(self.circle_radius * 2) 
        
        pygame.draw.line(self.gameWin, MIDBLACK, (lineX, lineY1), (lineX, lineY2), 2)
            
        for i in range(self.N):

            prevX, prevY = x, y
            n = i * 2 + 1

            radius = self.circle_radius * 4 / (n * math.pi)
            # x = self.circle_radius * math.cos(self.time) + self.circle_pos_x
            # y = self.circle_radius * math.sin(self.time) + self.circle_pos_y
            x += radius * math.cos(n * self.time)
            y += radius * math.sin(n * self.time)

            pygame.draw.line(self.gameWin, MIDBLACK, (prevX, prevY), (x, y), 1)
            pygame.draw.circle(self.gameWin, MIDBLACK, (prevX, prevY), radius, 1)
            
        self.wave.insert(0, y)
        prevX, prevY = lineX, self.wave[0]
        pygame.draw.line(self.gameWin, MIDBLACK, (x, y), (lineX, y), 2)

        for i in range(1, len(self.wave)):
            y = self.wave[i]
            x = i + lineX
            pygame.draw.line(self.gameWin, MIDBLACK, (prevX, prevY), (x, y), 1)
            # pygame.draw.circle(self.gameWin, MIDBLACK, (x, y), 1)
            prevX, prevY = x, y

        if len(self.wave) > self.numWavePoints:
            self.wave.pop()
        
        self.time += self.timeDelta
        pygame.display.update()

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
            pygame.display.update()

        self.quit()
        

if __name__ == "__main__":
    X = Square_Wave()
    X.run()