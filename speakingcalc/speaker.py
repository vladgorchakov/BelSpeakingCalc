import time
from os import path
import pygame


class Speaker:
    def __init__(self, sound_dir):
        self.sounds_directory = sound_dir

    def create_path(self, file_name):
        if path.isfile(f'{self.sounds_directory}{file_name}.wav'):
            return f'{self.sounds_directory}{file_name}.wav'
        else:
            raise FileNotFoundError

    def say_digit_or_operation(self, value):
        sound = pygame.mixer.Sound(self.create_path(value))
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
