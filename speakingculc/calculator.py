from decimal import Decimal
import pygame
from .colors import Colors
from .interface import Window, CalcWindow
from os import path
from .keys import CalcKeys
from .speaker import Speaker


class Calculator(Window):
    def __init__(self, weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator',):
        self.calc_window = CalcWindow(weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator')
        self.speaker = Speaker(f'./{path.dirname(path.relpath(__file__))}/sounds/')
        self.keys = CalcKeys()

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

    def run(self):
        self.calc_window.show_window()
        num1 = ''
        buf = ''
        op = self.calc_window.op1
        clear = False
        answer = ''

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()

                    case pygame.KEYDOWN:
                        if event.key in self.keys.num_pad_digits.keys():
                            if clear and answer:
                                self.calc_window.clear_fields()
                                clear = False

                            num1 += self.keys.num_pad_digits[event.key]
                            print(self.keys.num_pad_digits[event.key], end='')
                            op.write(num1)
                            self.speaker.say_digit_or_operation(self.keys.num_pad_digits[event.key])

                        elif event.key in self.keys.operators.keys():
                            if num1:
                                buf = num1
                                num1 = ''

                            elif not num1 and answer:
                                self.calc_window.clear_fields()
                                self.calc_window.op1.write(str(answer))
                                buf = answer
                                answer = ''

                            operator = self.keys.operators[event.key]
                            print(operator[1], end='')
                            self.calc_window.operation.write(operator[1])
                            self.speaker.say_digit_or_operation(operator[0])
                            op = self.calc_window.op2

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
                                self.calc_window.answer.write(f'={answer}')
                                self.speaker.say_answer(answer)
                                num1 = ''
                                buf = ''
                                op = self.calc_window.op1
                                clear = True

                            ### ДОПИСАТЬ ОКРУГЛЕНИЕ И УДАЛЕНИЕ ЛИШНИХ НУЛЕЙ ЕСЛИ ТИП инт

            self.calc_window.run()
