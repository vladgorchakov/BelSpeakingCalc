import time
import pygame


def say_digit_or_operation(value):
    sound = pygame.mixer.Sound(f'{value}.wav')
    sound.play()


def say_answer(ans):
    say_digit_or_operation('equal')
    for num in str(ans):
        if num.isdigit:
            time.sleep(0.8)
            say_digit_or_operation(num)


def calculate(value1: str, value2: str, op: str) -> (int, float):
    match op:
        case '+':
            return int(value2) + int(value1)
        case '-':
            return int(value2) - int(value1)
        case '*':
            return int(value2) * int(value1)
        case '/':
            return int(value2) / int(value1)


def digit_key_decoder(key):
    match key:
        case pygame.K_KP0:
            return '0'
        case pygame.K_KP1:
            say_digit_or_operation('1')
            return '1'
        case pygame.K_KP2:
            return '2'
        case pygame.K_KP3:
            return '3'
        case pygame.K_KP4:
            return '4'
        case pygame.K_KP5:
            return '5'
        case pygame.K_KP6:
            return '6'
        case pygame.K_KP7:
            return '7'
        case pygame.K_KP8:
            return '8'
        case pygame.K_KP9:
            return '9'


def main():
    pygame.init()

    W = 600
    H = 400

    sc = pygame.display.set_mode((W, H))
    pygame.display.set_caption('My calculator')

    WHITE = (255, 255, 255)
    sc.fill(WHITE)
    pygame.display.update()

    FPS = 60
    clock = pygame.time.Clock()

    num1 = ''
    buf = ''
    num_operators = {
        pygame.K_KP_PLUS: ('plus', '+'),
        pygame.K_KP_MINUS: ('minus', '-'),
        pygame.K_KP_DIVIDE: ('divide', '/'),
        pygame.K_KP_MULTIPLY: ('multiply', '*'),
        pygame.K_EQUALS: ('equal', '=')
    }

    while 1:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    exit()
                case pygame.KEYDOWN:
                    if event.key not in num_operators.keys():
                        input_value = digit_key_decoder(event.key)
                        if input_value:
                            num1 += input_value
                            print(input_value, end=' ')
                            say_digit_or_operation(input_value)

                    elif event.key in num_operators.keys() and event.key != pygame.K_EQUALS:
                        buf = num1
                        num1 = ''
                        operator = num_operators[event.key]
                        print(operator[1], end=' ')
                        say_digit_or_operation(operator[0])

                    elif event.key == pygame.K_EQUALS:
                        answer = calculate(num1, buf, operator[1])
                        print(f' = {answer}')
                        say_answer(answer)
                        num1 = ''
                        buf = ''

        clock.tick(FPS)


if __name__ == '__main__':
    main()
