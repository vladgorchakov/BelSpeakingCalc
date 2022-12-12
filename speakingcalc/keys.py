import pygame


class CalcKeys:
    def __init__(self):

        self.operators = {
            pygame.K_KP_PLUS: ('plus', '+'),
            pygame.K_KP_MINUS: ('minus', '-'),
            pygame.K_KP_DIVIDE: ('divide', '/'),
            pygame.K_KP_MULTIPLY: ('multiply', '*'),
        }

        self.digits = {
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


class KeysScaner:
    def __init__(self, calc):
        self.calc = calc
        self.keys = CalcKeys()

    def process_key_down(self, event):
        # Если нажата клавиша с цифрой
        if event.key in self.keys.digits.keys():
            self.calc.write_digit(self.keys.digits[event.key])

        # Если нажата клавиша с арифметическими оператором
        elif event.key in self.keys.operators.keys():
            self.calc.process_operator(self.keys.operators[event.key])

        # Если нажата клавиша с точкой
        elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
            self.calc.process_point()

        # Если нажата клавиша BACKSPACE
        elif event.key == pygame.K_BACKSPACE:
            self.calc.process_backspace()

        # Если нажата клавиша ENTER
        elif event.key == pygame.K_KP_ENTER:
            self.calc.process_equal()

        # выход по ESC
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            exit()

    def scan(self):
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        exit()

                    case pygame.KEYDOWN:
                        self.process_key_down(event)
