from enum import Enum
import os
import random
import numpy as np
import config
from time import sleep, time
import pygame

djblue = (163, 218, 234)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]


class Mode(Enum):
    BLANK = 0
    BOOT = 1
    READY = 2
    PLAYING = 3
    SLEEP = 4
    END = 5


def pygame_rounded_line(screen, color, p, q, linewidth=4):
    pygame.draw.line(screen, color, p, q, linewidth)
    pygame.draw.circle(screen, color, p, linewidth/2)
    pygame.draw.circle(screen, color, q, linewidth/2)


class Quit(BaseException):
    pass


class Display:
    def __init__(
        self, width=2160, height=3840, kwargs={"flags": pygame.FULLSCREEN, "display": 0},
        animation_duration = 0.2, hold_time = 2
    ):
        os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"
        self.width = width
        self.height = height
        self.mode = None
        self._dj_end = 0
        self._loading_message = None
        self._loading_colors = None
        self._sleep_t = -100
        self._blank_char = 0
        self._blank_t = -100
        self._dj_text = "DJ!"
        self._choice_end = 0
        self._choice_in = 0
        self._error = 0
        self._sleep_zs = []
        self._loading_start = 0
        self._ending_start = 0
        self._next_song = 0
        self._song_in = None
        self._song_out = None
        self._queued = None
        self._spinner = None
        self._tran_start = None
        self.animation_duration = animation_duration
        self.hold_time = hold_time
        self.playing = []

        pygame.init()
        self.screen = pygame.display.set_mode((width, height), **kwargs)

    def add_playing(self, title, artist):
        self._song_in = time() + self.animation_duration
        self.playing.append([title, artist])

    def show_loading(self):
        self.mode = Mode.BOOT
        self._loading_start = time()
        self._loading_message = [0.5, "Booting"]
        self._loading_colors = [colors[0] for _ in range(13)]
        for i in range(12):
            while self._loading_colors[i] == self._loading_colors[i + 1]:
                self._loading_colors[i + 1] = random.choice(colors)

    def show_ready(self):
        self.mode = Mode.READY

    @property
    def is_loading(self):
        return self.mode == Mode.BOOT

    @property
    def is_ready(self):
        return self.mode == Mode.READY

    @property
    def is_sleeping(self):
        return self.mode == Mode.SLEEP

    @property
    def is_blank(self):
        return self.mode == Mode.BLANK

    def show_ending(self):
        self.mode = Mode.END
        self._ending_start = time()

    @property
    def is_ending(self):
        return self.mode == Mode.END

    def remove_playing(self):
        self._song_out = time() + self.animation_duration

    def draw_bg(self):
        if self.is_sleeping or self.is_blank:
            self.screen.fill((0, 0, 0))
        else:
            self.screen.fill(djblue)

    def draw_now_playing(self):
        fontsize = self.width // 30 * 2
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)
        middle_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 4)
        medium_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 2)
        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)
        lw = fontsize * 1.3
        lstart = self.width // 2 - lw * (len(config.name) - 1) / 2
        for i, letter in enumerate(config.name):
            t = big_font.render(letter, False, (0, 0, 0))
            y = (self.height - t.get_height()) // 25 - self.height // 15 * np.sin(2 * (time() - i / 16)) ** 20
            self.screen.blit(t, (lstart + lw * i - t.get_width() // 2, y))

        if len(self.playing) > 1:
            if self._tran_start is None:
                self._tran_start = time()
            if time() - self._tran_start < 3:
                if time() % 1.0 < 0.5:
                    t = middle_font.render("COMPUTING TRANSITION", False, (0, 0, 0))
                    self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 25 + fontsize * 4))
            else:
                t = medium_font.render("Now playing", False, (0, 0, 0))
                self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 25 + fontsize * 4))
        else:
            self._tran_start = None
            t = medium_font.render("Now playing", False, (0, 0, 0))
            self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 25 + fontsize * 4))
        x0 = self.width / 2
        y0 = self.height / 25 + fontsize * 6.5
        x1 = self.width / 2
        y1 = self.height / 25 + fontsize * 9.5
        if self._song_out is not None:
            if time() > self._song_out:
                self.playing = self.playing[1:]
                self._song_out = None
            else:
                x0 = - self.width / 2 + self.width * (self._song_out - time()) / self.animation_duration
                y1 = y0 + (y1 - y0) * (self._song_out - time()) / self.animation_duration
        if self._song_in is not None:
            if time() > self._song_in:
                self._song_in = None
            else:
                y1 = y1 + self.height * (self._song_in - time()) / self.animation_duration
        if len(self.playing) > 0:
            title_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", min(
                fontsize, self.width // len(self.playing[0][0]) * 2
            ))
            t = title_font.render(self.playing[0][0], False, (0, 0, 0))
            self.screen.blit(t, (x0 - t.get_width() / 2, y0- t.get_height() / 2))
            artist_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", min(
                fontsize, self.width // len(self.playing[0][1]) * 2
            ))
            t = artist_font.render(self.playing[0][1], False, (0, 0, 0))
            self.screen.blit(t, (x0 - t.get_width() / 2, y0 + fontsize- t.get_height() / 2))
        if len(self.playing) > 1:
            title_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", min(
                fontsize, self.width // len(self.playing[1][0]) * 2
            ))
            t = title_font.render(self.playing[1][0], False, (0, 0, 0))
            self.screen.blit(t, (x1 - t.get_width() / 2, y1- t.get_height() / 2))
            artist_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", min(
                fontsize, self.width // len(self.playing[1][1]) * 2
            ))
            t = artist_font.render(self.playing[1][1], False, (0, 0, 0))
            self.screen.blit(t, (x1 - t.get_width() / 2, y1 + fontsize - t.get_height() / 2))

    def dj(self, text="DJ!"):
        self._dj_text = text
        self._dj_end = time() + 0.8

    def show_choice(self, display_names, weights, winner, next_song):
        added = [winner]
        n = [display_names[winner]]
        w = [weights[winner]]

        while len(n) < min(6, len(display_names)):
            add = random.choice([i for i, _ in enumerate(display_names) if i not in added])
            if random.random() > 0.5:
                added.append(add)
                n.append(display_names[add])
                w.append(weights[add])
            else:
                added = [add] + added
                n = [display_names[add]] + n
                w = [weights[add]] + w

        new_winner = added.index(winner)

        w = np.array(w)
        w /= sum(w)

        self._choice_in = time() + self.animation_duration
        self._choice_end = time() + 10 + self.animation_duration + random.random() * 5
        self._display_names = n
        self._weights = w
        a = 0
        for i, w in enumerate(w):
            if i == new_winner:
                self._end_rot = -(a + random.random() * w * 2 * np.pi)
                break
            a += w * 2 * np.pi
        self._queued = display_names[winner]
        self._next_song = next_song

    def draw_choice(self):
        fontsize = self.width // 30
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)

        x1 = 25 * self.width // 64
        x1 = self.width // 2
        x2 = - self.width // 2

        if time() < self._choice_in:
            x = x1 + (x2 - x1) * (self._choice_in - time()) / self.animation_duration
        elif time() > self._choice_end + self.hold_time:
            x = x1 + (x2 - x1) * (time() - self._choice_end - self.hold_time) / self.animation_duration
        else:
            x = x1

        r = 3 * self.width // 8

        pygame.draw.circle(self.screen, (255, 255, 255), (x, self.height // 5), r)
        pygame.draw.circle(self.screen, (0, 0, 0), (x, self.height // 5), r, 4)
        a = self._end_rot + 2.5 * max(0, self._choice_end - time() - 5) + 0.25 * min(5, max(0, self._choice_end - time())) ** 2
        for w, (title, artist) in zip(self._weights, self._display_names):
            pygame.draw.line(self.screen, (0, 0, 0), (x, self.height // 5), (x + r * np.cos(a), self.height // 5 + r * np.sin(a)), 4)

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
                    self.height // 5 + r2 * np.sin(la) - t.get_height() // 2))

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
                    self.height // 5 + r2 * np.sin(la) - t.get_height() // 2))

            a = next_a

        mark = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load("dj4.png").convert_alpha(),
                                   (self.width // 8, self.width // 8)),
            -a * 180/np.pi)
        self.screen.blit(mark, (x - mark.get_width() / 2, self.height / 5 - mark.get_height() / 2))

        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)
        t = big_font.render("RANDOM SELECTION", False, (0, 0, 0))
        self.screen.blit(t, (self.width // 2 - t.get_width() // 2, x + 3 * self.width // 64 + self.height // 8))

        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 20 * self.width // 64, self.height // 5), (self.width - x + self.width // 6 + 20 * self.width // 64, self.height // 5), 17)
        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 20 * self.width // 64, self.height // 5), (self.width - x + self.width // 12 + 20 * self.width // 64, self.height // 5 + self.width // 50), 17)
        pygame_rounded_line(self.screen, (0, 0, 0), (self.width - x + self.width // 20 + 20 * self.width // 64, self.height // 5), (self.width - x + self.width // 12 + 20 * self.width // 64, self.height // 5 - self.width // 50), 17)

    def draw_dj(self):
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//max(2, len(self._dj_text) - 5))
        t = font.render(self._dj_text, False, (0, 0, 0))
        self.screen.blit(t, (
            (self.width - t.get_width()) // 2 + random.randrange(11) - 5,
            (self.height - t.get_height()) // 25 + random.randrange(11) - 5,
        ))

    def draw_loading(self):
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//10)
        d = time() - self._loading_start
        t = font.render("Initialising.", False, (0, 0, 0))
        self.screen.blit(t, (
            self.width // 9,
            self.height // 30 - t.get_height() // 2,
        ))

        if d > self._loading_message[0]:
            self._loading_message[0] += 0.08
            self._loading_message[1] = random.choice([
                "Installing bass",
                "Enabling kill all humans module",
                "Setting phasars to DISCO",
                "Downloading all music",
                "Turning volume to 11%",
                "01010000 01000001 01010010 01010100 01011001 00100001",
            ])
            if d > 4:
                self._loading_colors = self._loading_colors[1:]
                if len(self._loading_colors) == 0:
                    self.draw_bg()
                    self.update()
                    sleep(0.5)
                    self.mode = Mode.PLAYING
                    return
            else:
                self._loading_colors = self._loading_colors[1:] + [random.choice(colors)]
                while self._loading_colors[-1] == self._loading_colors[-2]:
                    self._loading_colors[-1] = random.choice(colors)

        message = self._loading_message[1]

        msg_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//max(11, 1 + len(message) // 2))
        t = msg_font.render(message, False, (0, 0, 0))
        self.screen.blit(t, (
            (self.width - t.get_width()) // 2,
            self.height // 10 - t.get_height() // 2
        ))

        for i, c in enumerate(self._loading_colors):
            self.screen.fill(c, pygame.Rect(0, self.height - i * (self.height // 14), self.width, self.height // 14))

    def draw_sleeping(self):
        fontsize = self.width // 30 * 2
        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)

        lw = fontsize * 1.3
        lstart = self.width // 2 - lw * (len(config.name) - 1) / 2
        t = big_font.render("A", False, (0, 0, 0))
        y = (self.height - t.get_height()) // 25
        for i, letter in enumerate(config.name):
            t = big_font.render(letter, False, djblue)
            self.screen.blit(t, (lstart + lw * i - t.get_width() // 2, y))

        self._sleep_zs = [z for z in self._sleep_zs if z["y"] > -80]

        if len(self._sleep_zs) < 5:
            self._sleep_zs.append({
                "x": self.width / 4 + random.random() * self.width / 2,
                "y": y + lw,
                "xsp": (random.random() - 0.5) * self.width / 500,
                "ysp": (0.5 + 0.5 * random.random()) * self.width / 500,
                "size": 1,
                "char": "z" if random.random() < 0.7 else "ζ"
            })

        for z in self._sleep_zs:
            font = pygame.font.SysFont("Fixedsys Excelsior 3.01", int(fontsize * z["size"] / 10))
            t = font.render(z["char"], False, djblue)
            self.screen.blit(t, (int(z["x"]), int(z["y"])))

        dt = (time() - self._sleep_t) * 150
        self._sleep_t = time()
        if dt > 10:
            return

        for z in self._sleep_zs:
            z["size"] += dt * 0.05
            z["y"] -= dt * 0.5 * z["ysp"]
            z["x"] += dt * 0.1 * (z["xsp"] + (random.random() - 0.5))

    def draw_ready(self):
        fontsize = self.width // 30 * 2
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)
        middle_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 4)
        medium_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 2)
        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize * 5 // 2)
        lw = fontsize * 1.3
        lstart = self.width // 2 - lw * (len(config.name) - 1) / 2
        for i, letter in enumerate(config.name):
            t = big_font.render(letter, False, (0, 0, 0))
            y = (self.height - t.get_height()) // 25 - self.height // 15 * np.sin(2 * (time() - i / 16)) ** 20
            self.screen.blit(t, (lstart + lw * i - t.get_width() // 2, y))

        t = medium_font.render("Ready", False, (0, 0, 0))
        self.screen.blit(t, ((self.width - t.get_width()) // 2, (self.height - t.get_height()) // 25 + fontsize * 4))

    def draw_blank(self):
        chars = "/-\\|"
        if time() > self._blank_t + 0.5:
            self._blank_char += 1
            self._blank_t = time()
        fontsize = self.width // 30 * 2
        big_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", fontsize)

        t = big_font.render(chars[self._blank_char % len(chars)], False, djblue)
        self.screen.blit(t, (self.width - t.get_width(), self.height - t.get_height()))

    def draw_ending(self):
        font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//10)
        d = time() - self._ending_start
        if d % 0.9 < 0.3:
            t = font.render("Shutting down.", False, (0, 0, 0))
        elif d % 0.9 < 0.6:
            t = font.render("Shutting down..", False, (0, 0, 0))
        else:
            t = font.render("Shutting down...", False, (0, 0, 0))
        self.screen.blit(t, (
            self.width // 9,
            self.height // 30 - t.get_height() // 2,
        ))

        message = "Goodbye"

        msg_font = pygame.font.SysFont("Fixedsys Excelsior 3.01", self.width//max(11, 1 + len(message) // 2))
        t = msg_font.render(message, False, (0, 0, 0))
        self.screen.blit(t, (
            (self.width - t.get_width()) // 2,
            self.height // 10 - t.get_height() // 2
        ))

    def update(self):
        pygame.display.update()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Quit

        self.draw_bg()

        if self.is_ending:
            self.draw_ending()
            self.update()
            return
        if self.is_sleeping:
            self.draw_sleeping()
            self.update()
            return
        if self.is_blank:
            self.draw_blank()
            self.update()
            return
        if self.is_loading:
            self.draw_loading()
            self.update()
            return
        if self.is_ready:
            self.draw_ready()
            if time() < self._dj_end:
                self.draw_dj()
            self.update()
            return

        if self._queued is not None and time() > self._next_song:
            self.add_playing(*self._queued)
            self._queued = None

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
        t = font.render(config.name, False, (0, 0, 255))
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
