import time
import pygame
from decimal import Decimal


def drow_text(text, f, sc):
    RED = (255, 0, 0)
    YELLOW = (239, 228, 176)
    WHITE = (255, 255, 255)

    W = 600
    H = 400

    sc_text = f.render(text, 1, RED, YELLOW)
    pos = sc_text.get_rect(center=(W // 2, 80))

    sc.fill(WHITE)
    sc.blit(sc_text, pos)
    pygame.display.update()

def say_digit_or_operation(value):
    sound = pygame.mixer.Sound(f'{value}.wav')
    sound.play()


def say_answer(ans):
    say_digit_or_operation('equal')
    if ans == 'error_zero_division':
        time.sleep(0.8)
        say_digit_or_operation(ans)
    else:
        for num in str(ans):
            time.sleep(0.8)
            if num.isdigit():
                say_digit_or_operation(num)
            elif num == '-':
                say_digit_or_operation('negative')
            elif num == '.':
                say_digit_or_operation('point')


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value: str):
    try:
        float(value)
        return True
    except ValueError:
        return False


def calculate(value1: str, value2: str, op: str) -> (int, float):
    values = [value1, value2]
    for i in range(len(values)):
        if is_int(values[i]):
            values[i] = int(values[i])
        elif is_float(values[i]):
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


def main():
    pygame.init()

    W = 600
    H = 400

    sc = pygame.display.set_mode((W, H))
    pygame.display.set_caption('My calculator')

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (239, 228, 176)

    f_sys = pygame.font.SysFont('arial', 72)
    f = pygame.font.Font('cabana.ttf', 72)
    drow_text(text='He', f=f_sys, sc = sc)

    FPS = 60
    clock = pygame.time.Clock()

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

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    exit()
                case pygame.KEYDOWN:
                    if event.key in num_pad_digits.keys():
                        num1 += num_pad_digits[event.key]
                        print(num_pad_digits[event.key], end='')
                        drow_text(text=num1, f=f_sys, sc=sc)
                        say_digit_or_operation(num_pad_digits[event.key])

                    elif event.key in ariphemitic_operators.keys():
                        buf = num1
                        num1 = ''
                        operator = ariphemitic_operators[event.key]
                        print(operator[1], end='')
                        say_digit_or_operation(operator[0])

                    elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                        num1 += '.'
                        print('.', end='')
                        say_digit_or_operation('point')

                    elif event.key == pygame.K_KP_ENTER:
                        answer = calculate(num1, buf, operator[1])
                        print(f' = {answer}')
                        say_answer(answer)
                        num1 = ''
                        buf = ''
        clock.tick(FPS)


if __name__ == '__main__':
    main()
