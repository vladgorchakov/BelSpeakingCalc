from decimal import Decimal
import pygame
from .colors import Colors
from .interface import Window, CalcWindow
from os import path
from .keys import CalcKeys
from .speaker import Speaker


class Calculator(Window):
    def __init__(self, weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator', ):
        self.calc_window = CalcWindow(weight=1024, height=768, color=Colors.BLACK.value, caption='Calculator')
        self.speaker = Speaker(f'./{path.dirname(path.relpath(__file__))}/sounds/')
        self.keys = CalcKeys()
        self.__num1 = ''
        self.__buf = ''
        self.__answer = ''
        self.__current_field = self.calc_window.operand_field1
        self.__clear = False
        self.__operator = None

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

    def write_digit(self, event):
        if event.key in self.keys.digits.keys():
            if self.__clear and self.__answer:
                self.calc_window.clear_fields()
                self.__clear = False

            self.__num1 += self.keys.digits[event.key]
            print(self.keys.digits[event.key], end='')
            self.__current_field.write(self.__num1)
            self.speaker.say_digit_or_operation(self.keys.digits[event.key])

    def process_operator(self, event):
        # Если первый операнд не пустой
        if self.__num1:
            self.__buf = self.__num1
            self.__num1 = ''

        # Если операция производиться с результатом вычисления прошлого выражения
        elif not self.__num1 and self.__answer:
            self.calc_window.clear_fields()  # Очистка полей ввода
            self.calc_window.operand_field1.write(str(self.__answer))  # Запись результата прошлого выражения в
            # поле ввода операнда 1
            self.__buf = self.__answer  # Значение результата сохраняется в буфер
            self.__answer = ''  # Очистка переменной хранения результата

        self.__operator = self.keys.operators[event.key]  # получение списка с символом и названием оператора
        # соответсвующего нажатой клавише
        print(self.__operator[1], end='')
        self.calc_window.operation_field.write(self.__operator[1])  # Запись символа оператора в поле
        # вывода ввода оператора
        self.speaker.say_digit_or_operation(self.__operator[0])  # Вывод звукового сопровождения
        self.__current_field = self.calc_window.operand_field2  # Смена активного (текущего) поля
        # на поле второго операнда

    def process_point(self):
        if self.__num1.count('.') < 1:  # Если число содержит 0 точек
            self.__num1 += '.'  # Добавить точку к числу
            print('.', end='')  # Вывести точку в консоль
            self.__current_field.write(self.__num1)  # Вывести полученную строку в текущее поле
            self.speaker.say_digit_or_operation('point')  # Вывести звуковое сопровождение

    def process_backspace(self):
        if self.__num1:  # Если строка хранить что-то (не пустая)
            self.__num1 = self.__num1[:-1]  # Уменьшение строки на один символ
            self.__current_field.write(self.__num1)  # Вывод полученой строки в активное текущее поле

    def run(self):
        self.calc_window.show_window()

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()

                    case pygame.KEYDOWN:
                        # Если нажата клавиша с цифрами
                        if event.key in self.keys.digits.keys():
                            self.write_digit(event)

                        # Если нажата клавиша с арифметическими оператора
                        elif event.key in self.keys.operators.keys():
                            self.process_operator(event)

                        # Если нажата клавиша с точкой
                        elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                            self.process_point()

                        # Если нажата клавиша BACKSPACE
                        elif event.key == pygame.K_BACKSPACE:
                            self.process_backspace()

                        elif event.key == pygame.K_KP_ENTER:
                            if self.__num1 and self.__buf:
                                self.__answer = str(self.calculate(self.__num1, self.__buf, self.__operator[1]))
                                print(f' = {self.__answer}')
                                self.calc_window.answer_field.write(f'={self.__answer}')
                                self.speaker.say_answer(self.__answer)
                                self.__num1 = ''
                                self.__buf = ''
                                self.__current_field = self.calc_window.operand_field1
                                self.__clear = True

                            ### ДОПИСАТЬ ОКРУГЛЕНИЕ И УДАЛЕНИЕ ЛИШНИХ НУЛЕЙ ЕСЛИ ТИП инт

            self.calc_window.run()
