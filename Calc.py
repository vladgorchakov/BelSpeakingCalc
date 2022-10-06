from decimal import Decimal
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
    def __init__(self, sc, weight, height, color, position, font_size=72):
        super().__init__(weight, height, color)
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(self.window_color)
        self.font = pygame.font.SysFont(pygame.font.get_default_font()[0], font_size)
        self.sc = sc
        self.position = position


    def clear(self):
        self.surface.fill(self.window_color)
        pygame.display.update()

    def write(self, text, font_color=Colors.BLACK.value):
        font_surface = self.font.render(text, 1, font_color, self.window_color)
        font_pos = font_surface.get_rect(center=(self.w // 2, self.h // 2))
        self.surface.blit(font_surface, font_pos)
        self.sc.blit(self.surface, self.surface.get_rect(topleft=self.position))
        pygame.display.update()

    def get(self):
        return self


class Calculator(Window):
    def __init__(self, weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator',):
        super().__init__(weight, height, color)
        pygame.init()
        self.caption = caption
        self.window = pygame.display.set_mode((self.w, self.h))
        # self.op = [OperandWindow(self.window, self.w, 200, Colors.BLACK.value, (0, i)) for i in range(0, self.h, self.h // 4)]
        self.op1 = OperandWindow(self.window, 1000, 200, Colors.GREEN.value, (0, 0))
        self.op2 = OperandWindow(self.window, 1000, 200, Colors.GREEN.value, (0, 300))
        self.operation = OperandWindow(self.window, 1000, 200, Colors.BLUE.value, (0, 150))
        self.answer = OperandWindow(self.window, 1000, 200, Colors.WHITE.value, (0, 450))
        self.fps = 60
        self.clock = pygame.time.Clock()

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

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(value: str):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def calculate(self, value1: str, value2: str, op: str) -> (int, float):
        values = [value1, value2]
        for i in range(len(values)):
            if self.is_int(values[i]):
                values[i] = int(values[i])
            elif self.is_float(values[i]):
                values[i] = float(values[i])
            else:
                return 'invalid values'

        match op:
            case '+':
                return values[1] + values[0]
            case '-':
                return values[1] - values[0]
            case '*':
                return values[1] * values[0]
            case '/':
                try:
                    num = Decimal(values[1] / values[0])
                    print(num)
                    return num.quantize(Decimal('1.00'))
                except ZeroDivisionError:
                    return 'error_zero_division'

    def show_window(self):
        self.window.fill(self.window_color)
        pygame.display.update()

    def run(self):
        self.show_window()

        num1 = ''
        buf = ''

        ariphemitic_operators = {
            pygame.K_KP_PLUS: ('plus', '+'),
            pygame.K_KP_MINUS: ('minus', '-'),
            pygame.K_KP_DIVIDE: ('divide', '/'),
            pygame.K_KP_MULTIPLY: ('multiply', '*'),
        }

        num_pad_digits = {
            pygame.K_KP0: '0',
            pygame.K_KP1: '1',
            pygame.K_KP2: '2',
            pygame.K_KP3: '3',
            pygame.K_KP4: '4',
            pygame.K_KP5: '5',
            pygame.K_KP6: '6',
            pygame.K_KP7: '7',
            pygame.K_KP8: '8',
            pygame.K_KP9: '9'
        }

        op = self.op1
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()
                    case pygame.KEYDOWN:
                        if event.key in num_pad_digits.keys():
                            num1 += num_pad_digits[event.key]
                            print(num_pad_digits[event.key], end='')
                            op.write(num1)
                            self.say_digit_or_operation(num_pad_digits[event.key])

                        elif event.key in ariphemitic_operators.keys():
                            buf = num1
                            num1 = ''
                            operator = ariphemitic_operators[event.key]
                            print(operator[1], end='')
                            self.operation.write(operator[1])
                            self.say_digit_or_operation(operator[0])
                            op = self.op2

                        elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                            num1 += '.'
                            print('.', end='')
                            op.write(num1)
                            self.say_digit_or_operation('point')

                        elif event.key == pygame.K_KP_ENTER:
                            answer = self.calculate(num1, buf, operator[1])
                            print(f' = {answer}')
                            self.answer.write(str(answer))
                            self.say_answer(answer)
                            num1 = ''
                            buf = ''
                            op = self.op1


            self.clock.tick(self.fps)

calc = Calculator()
calc.run()

