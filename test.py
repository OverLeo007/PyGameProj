import pygame
import os
pygame.mixer.init(channels=2)
print(os.getcwd() + '\\data\\boom_music.mp3')
boom = pygame.mixer.Sound(os.path.join('data', 'boom_sound.wav'))
boom.play(loops=-1)
while True:
    pass