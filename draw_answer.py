from enum import Enum
import pygame
import time


class Colors(Enum):
    WHITE = (255, 255, 255),
    RED = (255, 0, 0),
    GREEN = (0, 255, 0),
    BLUE = (0, 0, 255),
    BLACK = (0, 0, 0)


class Window:
    def __init__(self, weight, height, color):
        self.w = weight
        self.h = height
        self.window_color = color
        pygame.init()


class OperandWindow(Window):
    def __init__(self, sc, weight, height, color, font_size=72, font_color=Colors.WHITE.value):
        super().__init__(weight, height, color)
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(font_color)
        self.font = pygame.font.SysFont(pygame.font.get_default_font()[0], font_size)
        self.font_color = font_color
        self.sc = sc

    def clear(self):
        self.surface.fill(self.window_color)
        pygame.display.update()

    def write(self, text='input value'):
        font_surface = self.font.render(text, 1, self.font_color, self.window_color)
        font_pos = font_surface.get_rect(center=(self.w // 2, self.h // 2))
        self.surface.blit(font_surface, font_pos)
        self.sc.blit(self.surface, self.surface.get_rect())
        pygame.display.update()


sc = pygame.display.set_mode((600, 400))
sc.fill(Colors.BLACK.value)
pygame.display.update()

op1 = OperandWindow(sc, 580, 100, Colors.GREEN.value)
op1.write('Hello World')

# print(pygame.font.get_fonts())
# op1.write('Hello')
#
#
# def get_text_surface(text, font):
#     return font.render(text, 1, (0,0,0), (255,255,255))
#
#
# f = pygame.font.Font('wiguru.ttf', 56)
# sc_text1 = f.render('Прыветанне!!!', 1, (255,0,0), (25,100,89))
# sc_text2 = f.render('Прывет!!!', 1, (255,0,0), (25,100,89))
# pos1 = sc_text1.get_rect(center=(300, 100))
# pos2 = sc_text2.get_rect(center=(300, 200))
# sc_text1.
#
# sc.fill((0,0,0))
# sc.blit(sc_text1, pos1)
# sc.blit(sc_text2, pos2)
# pygame.display.update()


while True:
    pass