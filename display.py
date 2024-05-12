import os
import random
import numpy as np
from time import sleep, time
import pygame


def pygame_rounded_line(screen, color, p, q, linewidth=4):
    pygame.draw.line(screen, color, p, q, linewidth)
    pygame.draw.circle(screen, color, p, linewidth/2)
    pygame.draw.circle(screen, color, q, linewidth/2)


class Quit(BaseException):
    pass


class Display:
    def __init__(
        self, width=2160, height=3840, kwargs={"flags": pygame.FULLSCREEN, "display": 1},
        animation_duration = 0.2, hold_time = 2
    ):
        os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"
        self.width = width
        self.height = height
        self._dj_end = 0
        self._choice_end = 0
        self._choice_in = 0
        self._error = 0
        self._queued = None
        self._spinner = None
        self.animation_duration = animation_duration
        self.hold_time = hold_time
        self.playing = []

        pygame.init()
        self.screen = pygame.display.set_mode((width, height), **kwargs)

    def add_playing(self, title, artist):
        self.playing.append([title, artist])

    def remove_playing(self):
        self.playing = self.playing[1:]

    def draw_bg(self):
        self.screen.fill((150, 150, 255))

    def draw_now_playing(self):
        fontsize = self.width // 30
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)
        medium_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 2)
        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)
        lw = fontsize * 1.3
        lstart = self.width // 2 - lw * (len("DJ Markov") - 1) / 2
        for i, letter in enumerate("DJ Markov"):
            t = big_font.render(letter, False, (0, 0, 0))
            y = (self.height - t.get_height()) // 2 - self.height // 40 * np.sin(2 * (time() - i / 16)) ** 20
            self.screen.blit(t, (lstart + lw * i - t.get_width() // 2, y))

        t = medium_font.render("Now playing", False, (0, 0, 0))
        self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 2 + fontsize * 4))
        # TODO: animate these joining and leaving
        for i, (title, artist) in enumerate(self.playing):
            t = font.render(title, False, (0, 0, 0))
            self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 2 + fontsize * (6.5 + 3 * i)))
            t = font.render(artist, False, (0, 0, 0))
            self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 2 + fontsize * (7.5 + 3 * i)))

    def dj(self):
        self._dj_end = time() + 0.8

    def show_choice(self, display_names, weights, winner):
        self._choice_in = time() + self.animation_duration
        self._choice_end = time() + 20 + self.animation_duration + random.random() * 10
        self._display_names = display_names
        self._weights = weights / sum(weights)
        a = 0
        for i, w in enumerate(weights):
            if i == winner:
                self._end_rot = -(a + random.random() * w * 2 * np.pi)
                break
            a += w * 2 * np.pi
        self._queued = display_names[winner]

    def draw_choice(self):
        fontsize = self.width // 30
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)

        x1 = 25 * self.width // 64
        x2 = - self.width // 2

        if time() < self._choice_in:
            x = x1 + (x2 - x1) * (self._choice_in - time()) / self.animation_duration
        elif time() > self._choice_end + self.hold_time:
            if self._queued is not None:
                self.add_playing(*self._queued)
                self._queued = None
            x = x1 + (x2 - x1) * (time() - self._choice_end - self.hold_time) / self.animation_duration
        else:
            x = x1

        r = 3 * self.width // 8

        pygame.draw.circle(self.screen, (255, 255, 255), (x, self.height // 2), r)
        pygame.draw.circle(self.screen, (0, 0, 0), (x, self.height // 2), r, 4)
        a = self._end_rot + 12 * max(0, self._choice_end - time() - 15) + 1.5 * 4/15 * min(15, max(0, self._choice_end - time())) ** 2
        for w, (title, artist) in zip(self._weights, self._display_names):
            pygame.draw.line(self.screen, (0, 0, 0), (x, self.height // 2), (x + r * np.cos(a), self.height // 2 + r * np.sin(a)), 4)

            next_a = a + w * 2 * np.pi

            # Write title
            lsp = np.pi / 45
            start_a = max(a + lsp, (a + next_a) / 2 - len(title) * lsp / 2)
            r2 = r - self.width // 15
            for i, letter in enumerate(title):
                t = font.render(letter, False, (0, 0, 0))
                la = start_a + (1 + i) * lsp
                if la > next_a - lsp:
                    break
                t = pygame.transform.rotate(t, - 90 - la * 180/np.pi)
                self.screen.blit(t, (
                    x + r2 * np.cos(la) - t.get_width() // 2,
                    self.height // 2 + r2 * np.sin(la) - t.get_height() // 2))

            # Write artist
            lsp = np.pi / 43
            start_a = max(a + lsp, (a + next_a) / 2 - len(artist) * lsp / 2)
            r2 = r - self.width // 15 - self.width // 30
            for i, letter in enumerate(artist):
                t = font.render(letter, False, (0, 0, 0))
                la = start_a + (1 + i) * lsp
                if la > next_a - lsp:
                    break
                t = pygame.transform.rotate(t, - 90 - la * 180/np.pi)
                self.screen.blit(t, (
                    x + r2 * np.cos(la) - t.get_width() // 2,
                    self.height // 2 + r2 * np.sin(la) - t.get_height() // 2))

            a = next_a

        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)
        t = big_font.render("Selecting next song", False, (0, 0, 0))
        self.screen.blit(t, (self.width // 2 - t.get_width() // 2, x - 3 * self.width // 64))

        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 6 * self.width // 64, self.height // 2), (self.width - x + self.width // 6 + 6 * self.width // 64, self.height // 2), 17)
        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 6 * self.width // 64, self.height // 2), (self.width - x + self.width // 12 + 6 * self.width // 64, self.height // 2 + self.width // 50), 17)
        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 6 * self.width // 64, self.height // 2), (self.width - x + self.width // 12 + 6 * self.width // 64, self.height // 2 - self.width // 50), 17)

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
        self.draw_now_playing()
        if time() < self._choice_end + self.hold_time + self.animation_duration:
            self.draw_choice()
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
