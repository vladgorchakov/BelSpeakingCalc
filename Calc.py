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


class OperandWindow(Window):
    def __init__(self, weight, height, color, font='arial', font_size=72, font_color=Colors.WHITE.value):
        super().__init__(weight, height, color)
        self.surface = pygame.Surface((self.w, self.h))
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

    def clear(self):
        self.surface.fill(self.window_color)
        pygame.display.update()

    def write(self, text='input value'):
        operand_text = self.font.render(text, 1, self.font_color, self.window_color)
        position_text = operand_text.get_rect(center=(self.w // 2, self.h // 2))
        self.surface.blit(operand_text, position_text)
        pygame.display.update()

    def get(self):
        return self


class Calculator(Window):
    def __init__(self, surf, weight=600, height=400, color=Colors.BLACK.value, caption='Calculator',):
        super().__init__(weight, height, color)
        pygame.init()
        self.caption = caption
        self.window = pygame.display.set_mode((self.w, self.h))

    @staticmethod
    def say_digit_or_operation(value):
        sound = pygame.mixer.Sound(f'{value}.wav')
        sound.play()

    def say_answer(self, ans):
        self.say_digit_or_operation('equal')
        if ans == 'error_zero_division':
            time.sleep(0.8)
            self.say_digit_or_operation(ans)
        else:
            for num in str(ans):
                time.sleep(0.8)
                if num.isdigit():
                    self.say_digit_or_operation(num)
                elif num == '-':
                    self.say_digit_or_operation('negative')
                elif num == '.':
                    self.say_digit_or_operation('point')

    def show_window(self):
        self.window.fill(self.window_color)
        pygame.display.update()

    def run(self):
        self.show_window()
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()


w = 600
h = 400

op1 = OperandWindow(580, 100, Colors.GREEN.value)
calc = Calculator(surf=op1)
calc.run()

