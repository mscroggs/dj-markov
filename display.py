import random
import numpy as np
from time import sleep
import pygame

width = 2160
height = 3840

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, display=1)


brot = {
    "pos": (-0.75, 0.03),
    "screen_pos": (width // 3, height // 3),
    "unit": 0.001,
}


def set_equal(a, b):
    a = b[:a.shape[0], :a.shape[1]]


pixels = pygame.surfarray.pixels2d(screen)

coords = np.zeros((width, height), dtype=np.complex)

while True:
    top_left = tuple(i - brot["unit"] * j for i, j in zip(brot["pos"], brot["screen_pos"]))
    bottom_right = (top_left[0] + width * brot["unit"], top_left[1] + height * brot["unit"])

    print(top_left)
    print(bottom_right)

    imaginary_axis = np.linspace(top_left[1], bottom_right[1], num=height)
    for i in range(height):
        coords.real[:, i] = np.linspace(top_left[0], bottom_right[0], num=width)
    for i in range(width):
        coords.imag[i, :] = np.linspace(bottom_right[1], top_left[1], num=height)

    filter = np.ones(coords.shape, dtype=bool)
    mask = np.ones(coords.shape, dtype=bool)
    data = np.zeros(coords.shape, dtype=np.complex128)

    pixels[:] = 0
    for i in range(100):
        data[filter] = data[filter] ** 2 + coords[filter]
        mask = np.logical_and(filter, data.real ** 2 + data.imag**2 > 4)
        pixels[mask] = i * 2
        filter = np.logical_and(np.logical_not(mask), filter)
        print(i)

    print(pixels)
    # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(200, 200, width-400, height-400))
    pygame.display.update()
    brot["unit"] *= 0.9
    #sleep(0.5)
