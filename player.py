import random
from time import sleep
from just_playback import Playback

ch0 = Playback()
ch1 = Playback()
ch2 = Playback()

ch0.load_file("music/03 - Heroes.mp3")
ch1.load_file("music/03 - Heroes.mp3")

ch2.load_file("keyboard-sounds/DJ.wav")


ch0.play()

for i in range(10):
    sleep(1)
    sleep(1)
    ch2.play()
    ch1.play()
    ch1.seek(ch0.curr_pos)
    ch0.pause()
    sleep(1)
    ch2.play()
    ch0.play()
    ch0.seek(ch1.curr_pos)
    ch1.pause()
"""

import pygame

pygame.mixer.pre_init()
pygame.mixer.init()

ch0 = pygame.mixer.Channel(0)
ch1 = pygame.mixer.Channel(1)
ch2 = pygame.mixer.Channel(2)

# ch0.queue(pygame.mixer.Sound('out/best2.mp3'))

ch0.queue(pygame.mixer.Sound('music/03 - Heroes.mp3'))
ch1.queue(pygame.mixer.Sound('music/03 - Heroes.mp3'))

ch0.unpause()

for i in range(10):
    ch0.pause()
    sleep(1)
    ch0.unpause()
    ch2.play(pygame.mixer.Sound('keyboard-sounds/DJ.wav'))
    sleep(1)
    ch2.play(pygame.mixer.Sound('keyboard-sounds/DJ.wav'))


"""
