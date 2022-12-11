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
        self.__num = ''
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

    def write_digit(self, digit):
        if self.__clear and self.__answer:  # Если установлен флаг очисти
            # и получен результат вычисления предыдущего выражения
            self.calc_window.clear_fields()  # Тогда очистить поля ввода-вывода
            self.__clear = False  # Сбросить флаг очистки

        self.__num += digit  # Добавить символ к строке с числом
        print(digit, end='')  # Вывести в консоль
        self.__current_field.write(self.__num)  # Записать полученное значение в текущее поле
        self.speaker.say_digit_or_operation(digit)  # Вывести звуковое сопровождение

    def process_operator(self, operator):
        # Если первый операнд не пустой
        if self.__num:
            self.__buf = self.__num  # Сохранить число в буфер
            self.__num = ''  # Обнулить переменную

        # Если операция производиться с результатом вычисления прошлого выражения
        elif not self.__num and self.__answer:
            self.calc_window.clear_fields()  # Очистка полей ввода
            self.calc_window.operand_field1.write(str(self.__answer))  # Запись результата прошлого выражения в
            # поле ввода операнда 1
            self.__buf = self.__answer  # Значение результата сохраняется в буфер
            self.__answer = ''  # Очистка переменной хранения результата

        self.__operator = operator  # получение списка с символом и названием оператора
        # соответсвующего нажатой клавише
        print(self.__operator[1], end='')
        self.calc_window.operation_field.write(self.__operator[1])  # Запись символа оператора в поле
        # вывода ввода оператора
        self.speaker.say_digit_or_operation(self.__operator[0])  # Вывод звукового сопровождения
        self.__current_field = self.calc_window.operand_field2  # Смена активного (текущего) поля
        # на поле второго операнда

    def process_point(self):
        if self.__num.count('.') < 1:  # Если число содержит 0 точек
            self.__num += '.'  # Добавить точку к числу
            print('.', end='')  # Вывести точку в консоль
            self.__current_field.write(self.__num)  # Вывести полученную строку в текущее поле
            self.speaker.say_digit_or_operation('point')  # Вывести звуковое сопровождение

    def process_backspace(self):
        if self.__num:  # Если строка хранить что-то (не пустая)
            self.__num = self.__num[:-1]  # Уменьшение строки на один символ
            self.__current_field.write(self.__num)  # Вывод полученой строки в активное текущее поле

    def process_equal(self):
        if self.__num and self.__buf: # Если введены два числа (оператор?)
            self.__answer = str(self.calculate(self.__num, self.__buf, self.__operator[1]))  # Вызвать функцию выч.
            # значение выражения
            print(f' = {self.__answer}')  # Вывести результат в консоль
            self.calc_window.answer_field.write(f'={self.__answer}')  # Вывести результат в поле ответа
            self.speaker.say_answer(self.__answer)  # Вывести звуковое сопровождение
            self.__num = ''  # Обнулить переменную со вторым числом
            self.__buf = ''  # Обнулить переменную с буфером (первое число)
            self.__current_field = self.calc_window.operand_field1  # Установить, что последющим активное (текущее)
            # поле будет поле для операнда 1
            self.__clear = True  # Установить флаг очистки

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
                            self.write_digit(self.keys.digits[event.key])

                        # Если нажата клавиша с арифметическими оператора
                        elif event.key in self.keys.operators.keys():
                            self.process_operator(self.keys.operators[event.key])

                        # Если нажата клавиша с точкой
                        elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                            self.process_point()

                        # Если нажата клавиша BACKSPACE
                        elif event.key == pygame.K_BACKSPACE:
                            self.process_backspace()

                        # Если нажата клавиша ENTER
                        elif event.key == pygame.K_KP_ENTER:
                            self.process_equal()

                        # выход по ESC

            self.calc_window.run()

# ДОПИСАТЬ ОКРУГЛЕНИЕ И УДАЛЕНИЕ ЛИШНИХ НУЛЕЙ ЕСЛИ ТИП инт
