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

ch0.set_volume(0.3)
ch1.set_volume(0.3)


ch2.load_file("keyboard-sounds/DJ.wav")

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
    height = 900
    width = height * 9 // 16
    display = Display(width, height, {})
else:
    display = Display(width=1080, height=1920)
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

        if playing.curr_pos > current["fade_end"] + 2000:
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
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_f]:
            #    if pygame.K_f not in pressed:
            #        playing.seek(playing.curr_pos + 15)
            #        pressed.append(pygame.K_f)
            # elif pygame.K_f in pressed:
            #    pressed.remove(pygame.K_f)

            dj_buttons = [
                (pygame.K_z, "keyboard-sounds/DJ.wav", "DJ!"),
                (pygame.K_x, "keyboard-sounds/Dictionary.wav", "Dictionary"),
                (pygame.K_c, "keyboard-sounds/Scratch.wav", None),
                (pygame.K_v, "keyboard-sounds/Scratch2.wav", None),
                (pygame.K_b, "keyboard-sounds/scratch3.wav", None),

                (pygame.K_q, "phrases/activating.wav", None),
                (pygame.K_w, "phrases/arm-extend.wav", None),
                (pygame.K_e, "phrases/destroy-humans-activated.wav", None),
                (pygame.K_r, "phrases/destroy-humans-mode-deactivated.wav", None),
                (pygame.K_t, "phrases/foxdog.wav", None),
                (pygame.K_y, "phrases/ymca.wav", None),
                (pygame.K_u, "phrases/hello-matt.wav", None),
                (pygame.K_o, "phrases/death.wav", None),
                (pygame.K_p, "phrases/dance.wav", None),
                (pygame.K_1, "phrases/dj2.wav", "DJ!"),
                (pygame.K_2, "phrases/dj.wav", "DJ!"),
                (pygame.K_3, "phrases/no-repeats.wav", None),
                (pygame.K_4, "phrases/one-more-song.wav", None),
                (pygame.K_5, "phrases/party.wav", None),
                (pygame.K_6, "phrases/robot.wav", None),
                (pygame.K_8, "phrases/the-end.wav", None),
                (pygame.K_9, "phrases/updates.wav", None),
                (pygame.K_0, "phrases/ending.wav", None),
            ]

            n = random.choice([
                ("ahhhhh.wav", None),
                ("BZZhorn.wav", None),
                ("comeon2.wav", None),
                ("Comeon.wav", None),
                ("Dictionary.wav", "Dictionary"),
                ("DJ.wav", "DJ!"),
                ("Excellent.wav", "Excellent!"),
                ("getout.wav", None),
                ("good.wav", None),
                ("go.wav", None),
                ("HEUUUUUUUUUUGH.wav", None),
                ("horn.wav", None),
                ("lesson.wav", None),
                ("OKAY.wav", None),
                ("onemoretime.wav", None),
                ("one.wav", None),
                ("ooowww.wav", None),
                ("o.wav", None),
                ("peeeeew.wav", None),
                ("reversecymbal.wav", None),
                ("rewind.wav", None),
                ("Scratch2.wav", None),
                ("scratch3.wav", None),
                ("scratchdown.wav", None),
                ("Scratch.wav", None),
                ("sonic.wav", None),
                ("stab2.wav", None),
                ("stab.wav", None),
                ("three.wav", None),
                ("two.wav", None),
                ("verygood.wav", None),
                ("wooo.wav", None),
                ("yeeeeeeeah.wav", None),
            ])
            dj_buttons.append((pygame.K_n, f"keyboard-sounds/{n[0]}", n[1]))

            for key, file, text in dj_buttons:
                if keys[key]:
                    if key not in pressed:
                        ch3.load_file(file)
                        ch3.play()
                        if text is not None:
                            display.dj(text)
                        pressed.append(key)
                elif key in pressed:
                    pressed.remove(key)
            display.tick()

    except Quit:
        break
    except BaseException as e:
        ch0.stop()
        ch1.stop()
        ch2.stop()
        display.error(e)
