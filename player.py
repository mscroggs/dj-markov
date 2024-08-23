import pygame
import numpy as np
import json
import sys
import random
import config
from time import time, sleep
from display import Display, Quit
from just_playback import Playback

songdata = {}
with open(f"out/{config.mode}/data.json") as f:
    for line in f:
        data = json.loads(line)
        if data["song1"] not in songdata:
            songdata[data["song1"]] = []
        songdata[data["song1"]].append(data)
with open(f"out/{config.mode}/info.json") as f:
    info = json.load(f)

ch0 = Playback()
ch1 = Playback()
ch2 = Playback()
ch3 = Playback()

ch2.load_file("keyboard-sounds/DJ.wav")
ch3.load_file("keyboard-sounds/Scratch.wav")

current = None
while current is None:
    try:
        current = random.choice([i for i in random.choice(list(songdata.values())) if "/x" not in i["song1"] and "/x" not in i["song2"]])
    except IndexError:
        pass

next = None
choice_shown = False

current_channel = 0
ch0.load_file(current["filename"])

if config.no_repeats:
    played = [current["song1"], current["song2"]]

if config.windowed:
    display = Display(450, 800, {})
else:
    display = Display()
display.add_playing(info[current["song1"]]["title"], info[current["song1"]]["artist"])
display.draw_bg()
display.update()
ch0.play()

pressed = []

while True:
    try:
        if random.random() > 1 - config.dj_rate:
            ch2.play()
            display.dj()

        if current_channel == 0:
            playing = ch0
            queued = ch1
        else:
            playing = ch1
            queued = ch0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            if "f" not in pressed:
                playing.seek(playing.curr_pos + 15)
            pressed.append("f")
        elif "f" in pressed:
            pressed.remove("f")
        if keys[pygame.K_d]:
            if "d" not in pressed:
                ch2.play()
                display.dj()
            pressed.append("d")
        elif "d" in pressed:
            pressed.remove("d")

        if next is None:
            options = songdata[current["song2"]]
            if config.no_repeats:
                op = [i for i in options if i["song2"] not in played and "/x" not in i["song2"]]
                if len(op) > 0:
                    options = op
                else:
                    op = [i for i in options if i["song2"] not in played]
                    if len(op) > 0:
                        options = op
            weights = np.array([i["rating"] for i in options])
            weights /= sum(weights)
            next = np.random.choice(options, p=weights)
            queued.load_file(next["filename"])
            if config.no_repeats:
                played.append(next["song2"])

        if playing.curr_pos > current["fade_end"]:
            display.remove_playing()
            queued.play()
            queued.seek(current["song2_fade_end"] + playing.curr_pos - current["fade_end"])
            sleep(0.05)
            playing.pause()
            current_channel = 1 - current_channel
            current = next
            next = None
            choice_shown = False
        elif not choice_shown and playing.curr_pos > current["fade_start"] - 18:
            choice_shown = True
            options = songdata[current["song1"]]
            displays = [[
                info[i["song2"]]["title"],
                info[i["song2"]]["artist"],
            ] for i in options]
            weights = np.array([i["rating"] for i in options])
            weights /= sum(weights)
            display.show_choice(displays, weights, options.index(current), time() - playing.curr_pos + current["fade_start"])

        wait_until = time() + 1
        while time() < wait_until:
            display.tick()
    except Quit:
        break
    except BaseException as e:
        ch0.stop()
        ch1.stop()
        ch2.stop()
        display.error(e)
