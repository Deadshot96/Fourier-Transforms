import pygame
import math
from settings import *
from collections import namedtuple

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
        self.dftPointObj = namedtuple("dftPointObj", ["re", "im", "amp", "freq", "phase"])
        self.dftPoints = list()
        self.drawFlag = True
        self.time = 0
        self.dt = 0
        self.centrePos = self.win_width // 2, self.win_height // 2
        self.path = list()

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

    def epiCycle(self, x, y, angle):
        for index, ptObj in enumerate(self.dftPoints):
            prevX, prevY = x, y
            
            x += ptObj.amp * math.cos(ptObj.freq * self.time + ptObj.phase + angle)
            y += ptObj.amp * math.sin(ptObj.freq * self.time + ptObj.phase + angle)

            if index:
                pygame.draw.circle(self.gameWin, DIM_WHITE, (prevX, prevY), ptObj.amp, 1)
                pygame.draw.line(self.gameWin, DIM_WHITE, (prevX, prevY), (x, y), 1)

        pygame.display.update()
        return x, y

    def draw(self):
        if self.dftPoints:
            self.gameWin.fill(STEEL_BLUE)

            x, y = 0, 0
            x, y = self.epiCycle(x, y, 0)
            self.path.insert(0, (x, y))

            px, py = self.path[0]

            for i in range(1, len(self.path) - 1):
                x, y = self.path[i]
                pygame.draw.line(self.gameWin, MID_WHITE, (px, py), (x, y), 2)          
                px, py = x, y

            self.time += self.dt

            if self.time >= (math.pi * 2):
                self.time = 0
                self.path.clear()

        pygame.display.update()

    def dft(self):

        for k in range(len(self.points)):
            total = complex(0, 0)
            for n in range(len(self.points)):
                # phi = complex(0, -2 * math.pi * k * n / len(self.points))
                phi = -2 * math.pi * k * n / len(self.points)
                mul = complex(math.cos(phi), -math.sin(phi))
                total += (self.points[n] * mul)

            total /= len(self.points)
            re = total.real
            im = total.imag
            amp = abs(total)
            freq = k
            phase = math.atan2(im, re)

            obj = self.dftPointObj(re=re, im=im, amp=amp, freq=freq, phase=phase)
            self.dftPoints.append(obj) 

        self.dftPoints.sort(key=lambda x: x.amp, reverse=True)
        self.time = 0
        self.dt = 2 * math.pi / len(self.dftPoints)
        # print(self.dftPoints)

    def quit(self):
        pygame.font.quit()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        
        if not pygame.display.get_init():
            self.display_init()

        self.gameRect = pygame.Rect((0, 0, self.win_width, self.win_height))

        run = True
        while run:
            if self.drawFlag:
                self.clock.tick(self.fps)
            else:
                self.clock.tick(self.fps // 3)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drawFlag = False
                    self.points.reverse()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        self.gameWin.fill(STEEL_BLUE)
                        self.points.clear()
                        self.path.clear()
                        self.dftPoints.clear()
                        self.drawFlag = True
                        
                    if event.key == pygame.K_RETURN and not self.drawFlag:
                        self.dft()
                        
            pressed = pygame.mouse.get_pressed()
            px, py = -1, -1
            if pressed[0]:
                    x, y = pygame.mouse.get_pos()
                    x -= self.xoff
                    y -= self.yoff
                    flag = (px != x) and (py != y)

                    if self.drawFlag and self.gameRect.collidepoint(x, y) and flag:

                        self.gameWin.set_at((x, y), MID_WHITE)
                        pt = complex(x, y)
                        self.points.append(pt)
                        px, py = x, y

                        if len(self.points) > 2:
                            p1 = self.points[-1].real, self.points[-1].imag
                            p2 = self.points[-2].real, self.points[-2].imag

                            pygame.draw.line(self.gameWin, MID_WHITE, p2, p1, 2) 

            self.draw()

        self.quit()



if __name__ == "__main__":
    X = Main()
    X.run()