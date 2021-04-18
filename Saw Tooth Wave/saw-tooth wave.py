import pygame
from settings import *
import math

class SawToothWave(object):

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
        self.clock = None
        self.titleFont = None

        self.N = 10
        self.wave = list()
        self.numWavePoints = 650
        self.time = 0
        self.timeDelta = 0.05
        self.xDelta = 1
        self.circle_pos_x = int(self.win_width * 0.25)
        self.circle_pos_y = self.win_height // 2
        self.circle_pos = self.circle_pos_x, self.circle_pos_y
        self.circle_radius = self.win_height // 4

    def display_init(self):

        pygame.init()
        pygame.display.init()
        pygame.font.init()

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Saw-Tooth Wave - Fourier")

        gameRect = self.xoff, self.yoff, self.win_width, self.win_height
        self.gameWin = self.win.subsurface(gameRect)

        self.win.fill(MIDBLACK)
        self.gameWin.fill(STEEL_BLUE)

        self.clock = pygame.time.Clock()

        self.titleFont = pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE)
        title = self.titleFont.render(TITLE_TEXT, 1, GOLD)
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
        
        lineX = int(self.circle_radius * 2) + self.xoff + self.circle_pos_x
        lineY1 = self.circle_pos_y - int(self.circle_radius * 1.5) 
        lineY2 = self.circle_pos_y + int(self.circle_radius * 1.5) 

        pygame.draw.line(self.gameWin, MIDBLACK, (lineX, lineY1), (lineX, lineY2), 2)

        for i in range(1, self.N + 1):

            prevX, prevY = x, y

            radius =  2 * self.circle_radius / math.pi / i

            x += (radius * math.cos(i * self.time) * (-1) ** i)
            y += (radius * math.sin(i * self.time) * (-1) ** i)

            pygame.draw.line(self.gameWin, MIDBLACK, (prevX, prevY), (x, y), 1)
            pygame.draw.circle(self.gameWin, MIDBLACK, (prevX, prevY), radius, 1)

        self.wave.insert(0, y)
        prevX, prevY = lineX, self.wave[0]
        pygame.draw.line(self.gameWin, MIDBLACK, (x, y), (lineX, y), 2)

        for i in range(1, len(self.wave)):
            y = self.wave[i]
            x = i + lineX

            pygame.draw.line(self.gameWin, MIDBLACK, (prevX, prevY), (x, y), 1)
            prevX, prevY = x, y

        if len(self.wave) > self.numWavePoints:
            self.wave.pop()

        self.time += self.timeDelta
        pygame.display.update()

        print(len(self.wave))

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
    X = SawToothWave()
    X.run()