from decimal import Decimal
import pygame
import time
from .colors import Colors
from .interface import Window, OperandWindow
from os import path, getcwd
from .speaker import Speaker


class Calculator(Window):
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
        self.operators = {
            pygame.K_KP_PLUS: ('plus', '+'),
            pygame.K_KP_MINUS: ('minus', '-'),
            pygame.K_KP_DIVIDE: ('divide', '/'),
            pygame.K_KP_MULTIPLY: ('multiply', '*'),
        }

        self.num_pad_digits = {
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

        self.speaker = Speaker()

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

    def clear_fields(self):
        self.window.fill(self.window_color)

    def run(self):
        self.show_window()

        num1 = ''
        buf = ''
        op = self.op1
        clear = False
        answer = ''

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()

                    case pygame.KEYDOWN:
                        if event.key in self.num_pad_digits.keys():
                            if clear and answer:
                                self.clear_fields()
                                clear = False

                            num1 += self.num_pad_digits[event.key]
                            print(self.num_pad_digits[event.key], end='')
                            op.write(num1)
                            self.speaker.say_digit_or_operation(self.num_pad_digits[event.key])

                        elif event.key in self.operators.keys():
                            if num1:
                                buf = num1
                                num1 = ''

                            elif not num1 and answer:
                                self.clear_fields()
                                self.op1.write(str(answer))
                                buf = answer
                                answer = ''

                            operator = self.operators[event.key]
                            print(operator[1], end='')
                            self.operation.write(operator[1])
                            self.speaker.say_digit_or_operation(operator[0])
                            op = self.op2

                        elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                            if num1.count('.') < 1:
                                num1 += '.'
                                print('.', end='')
                                op.write(num1)
                                self.speaker.say_digit_or_operation('point')

                        elif event.key == pygame.K_BACKSPACE:
                            if num1:
                                num1 = num1[:-1]
                                op.write(num1)

                        elif event.key == pygame.K_KP_ENTER:
                            if num1 and buf:
                                answer = str(self.calculate(num1, buf, operator[1]))
                                print(f' = {answer}')
                                self.answer.write(f'={answer}')
                                self.speaker.say_answer(answer)
                                num1 = ''
                                buf = ''
                                op = self.op1
                                clear = True

                            ### ДОПИСАТЬ ОКРУГЛЕНИЕ И УДАЛЕНИЕ ЛИШНИХ НУЛЕЙ ЕСЛИ ТИП инт

            self.clock.tick(self.fps)
