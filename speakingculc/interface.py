import pygame
from .colors import Colors


class Window:
    def __init__(self, weight, height, color):
        self.w = weight
        self.h = height
        self.window_color = color


class OperandWindow(Window):
    def __init__(self, sc, weight, height, color, position, font_size=128):
        super().__init__(weight, height, color)
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(self.window_color)
        self.font = pygame.font.SysFont(pygame.font.get_default_font()[0], font_size)
        self.sc = sc
        self.position = position

    def write(self, text, font_color=Colors.PINK.value):
        self.clear()
        font_surface = self.font.render(text, 1, font_color, self.window_color)
        font_pos = font_surface.get_rect(center=(self.w // 2, self.h // 2))
        self.surface.blit(font_surface, font_pos)
        self.sc.blit(self.surface, self.surface.get_rect(topleft=self.position))
        pygame.display.update()

    def clear(self):
        self.surface.fill(self.window_color)


class CalcWindow(Window):
    def __init__(self, weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator',):
        super().__init__(weight, height, color)
        pygame.init()
        self.caption = caption
        self.window = pygame.display.set_mode((self.w, self.h))
        self.op1 = OperandWindow(self.window, 1000, 150, Colors.BLACK.value, (0, 0))
        self.op2 = OperandWindow(self.window, 1000, 150, Colors.BLACK.value, (0, 300))
        self.operation = OperandWindow(self.window, 1000, 150, Colors.BLACK.value, (0, 150))
        self.answer = OperandWindow(self.window, 1000, 150, Colors.BLACK.value, (0, 450))
        self.fps = 60
        self.clock = pygame.time.Clock()

    def show_window(self):
        self.window.fill(self.window_color)
        pygame.display.update()

    def clear_fields(self):
        self.window.fill(self.window_color)

    def run(self):
        self.clock.tick(self.fps)
