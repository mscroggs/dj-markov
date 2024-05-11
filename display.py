import os
import random
import numpy as np
from time import sleep, time
import pygame


class Quit(BaseException):
    pass


class Display:
    def __init__(self, width=2160, height=3840, kwargs={"flags": pygame.FULLSCREEN, "display": 1}):
        os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"
        self.width = width
        self.height = height
        self._dj_end = 0
        self._error = 0

        pygame.init()
        self.screen = pygame.display.set_mode((width, height), **kwargs)

    def draw_bg(self):
        self.screen.fill((150, 150, 255))

    def dj(self):
        self._dj_end = time() + 0.8

    def draw_dj(self):
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//2)
        t = font.render("DJ!", False, (0, 0, 0))
        self.screen.blit(t, (
            (self.width - t.get_width()) // 2 + random.randrange(11) - 5,
            (self.height - t.get_height()) // 2 + random.randrange(11) - 5,
        ))

    def update(self):
        pygame.display.update()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Quit
        self.draw_bg()
        if time() < self._dj_end:
            self.draw_dj()
        self.update()

    def error(self, e):
        self._error = True
        self.screen.fill((0, 0, 255))
        fontsize = self.width // 43
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)
        t = font.render("DJ Markov", False, (0, 0, 255))
        pygame.draw.rect(self.screen, (150, 150, 150), pygame.Rect(
            (self.width - t.get_width() - 3) // 2,
            (self.height - t.get_height() - 3) // 2 - fontsize * 4,
            t.get_width() + 6, t.get_height() + 6,
        ))
        self.screen.blit(t, (
            (self.width - t.get_width()) // 2,
            (self.height - t.get_height()) // 2 - fontsize * 4,
        ))
        t = font.render("An error has occurred. To continue:", False, (255, 255, 255))
        self.screen.blit(t, (
            self.width // 2 - fontsize * 12,
            (self.height - t.get_height()) // 2 - fontsize * 2,
        ))
        t = font.render("Turn DJ Markov off and on again, or", False, (255, 255, 255))
        self.screen.blit(t, (
            self.width // 2 - fontsize * 12,
            (self.height - t.get_height()) // 2,
        ))
        t = font.render("Leave now and let someone else fix it", False, (255, 255, 255))
        self.screen.blit(t, (
            self.width // 2 - fontsize * 12,
            (self.height - t.get_height()) // 2 + fontsize * 2,
        ))

        error_detail = f"Error: {e.__class__.__name__}: {e}"
        line = 0
        text = []
        for word in error_detail.split() + ["<<END>>"]:
            if word == "<<END>>" or (
                len(text) > 0 and len(text) + len(word) + sum(len(w) for w in text) >= 50
            ):
                t = font.render(" ".join(text), False, (255, 255, 255))
                self.screen.blit(t, (
                    self.width // 2 - fontsize * 12,
                    (self.height - t.get_height()) // 2 + fontsize * (line + 4),
                ))
                text = []
                line += 1
            text.append(word)
        self.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise Quit
