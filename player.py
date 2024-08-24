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

volumes = [0.3, 0.1]

ch0.set_volume(volumes[0])
ch1.set_volume(volumes[0])

ch2.load_file("keyboard-sounds/DJ.wav")

current = None
while current is None:
    try:
        current = random.choice([i for i in random.choice(list(songdata.values())) if "/x" not in i["song1"] and "/x" not in i["song2"]])
    except IndexError:
        pass

next = None
choice_shown = False
down_for_voice = False

current_channel = 0
ch0.load_file(current["filename"])

played = [current["song1"], current["song2"]]

no_repeats = config.no_repeats

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
            if no_repeats:
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
            played.append(next["song2"])

        if playing.curr_pos > current["fade_end"] + 2:
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
            if keys[pygame.K_f]:
               if pygame.K_f not in pressed:
                   playing.seek(playing.curr_pos + 15)
                   pressed.append(pygame.K_f)
            elif pygame.K_f in pressed:
                pressed.remove(pygame.K_f)
            if not no_repeats:
                if keys[pygame.K_l]:
                    no_repeats = True
                    ch3.load_file("phrases/no-repeats.wav")
                    ch3.play()
                    down_for_voice = True
                    ch0.set_volume(volumes[1])
                    ch1.set_volume(volumes[1])

            dj_buttons = [
                (pygame.K_z, "keyboard-sounds/DJ.wav", "DJ!", False),
                (pygame.K_x, "keyboard-sounds/Dictionary.wav", "Dictionary", False),
                (pygame.K_c, "keyboard-sounds/Scratch.wav", None, False),
                (pygame.K_v, "keyboard-sounds/Scratch2.wav", None, False),
                (pygame.K_b, "keyboard-sounds/scratch3.wav", None, False),

                (pygame.K_q, "phrases/activating.wav", None, True),
                (pygame.K_w, "phrases/arm-extend.wav", None, True),
                (pygame.K_e, "phrases/destroy-humans-activated.wav", None, True),
                (pygame.K_r, "phrases/destroy-humans-mode-deactivated.wav", None, True),
                (pygame.K_t, "phrases/foxdog.wav", None, True),
                (pygame.K_y, "phrases/ymca.wav", None, False),
                (pygame.K_u, "phrases/hello-matt.wav", None, True),
                (pygame.K_o, "phrases/death.wav", None, True),
                (pygame.K_p, "phrases/dance.wav", None, True),
                (pygame.K_1, "phrases/dj2.wav", "DJ!", False),
                (pygame.K_2, "phrases/dj.wav", "DJ!", False),
                (pygame.K_4, "phrases/one-more-song.wav", None, True),
                (pygame.K_5, "phrases/party.wav", None, True),
                (pygame.K_6, "phrases/robot.wav", None, True),
                (pygame.K_8, "phrases/the-end.wav", None, True),
                (pygame.K_9, "phrases/updates.wav", None, True),
                (pygame.K_0, "phrases/ending.wav", None, True),
            ]

            n = random.choice([
                ("ahhhhh.wav", None, False),
                ("BZZhorn.wav", None, False),
                ("comeon2.wav", None, False),
                ("Comeon.wav", None, False),
                ("Dictionary.wav", "Dictionary", False),
                ("DJ.wav", "DJ!", False),
                ("Excellent.wav", "Excellent!", False),
                ("getout.wav", None, False),
                ("good.wav", None, False),
                ("go.wav", None, False),
                ("HEUUUUUUUUUUGH.wav", None, False),
                ("horn.wav", None, False),
                ("lesson.wav", None, False),
                ("OKAY.wav", None, False),
                ("onemoretime.wav", None, False),
                ("one.wav", None, False),
                ("ooowww.wav", None, False),
                ("o.wav", None, False),
                ("peeeeew.wav", None, False),
                ("reversecymbal.wav", None, False),
                ("rewind.wav", None, False),
                ("Scratch2.wav", None, False),
                ("scratch3.wav", None, False),
                ("scratchdown.wav", None, False),
                ("Scratch.wav", None, False),
                ("sonic.wav", None, False),
                ("stab2.wav", None, False),
                ("stab.wav", None, False),
                ("three.wav", None, False),
                ("two.wav", None, False),
                ("verygood.wav", None, False),
                ("wooo.wav", None, False),
                ("yeeeeeeeah.wav", None, False),
            ])
            dj_buttons.append((pygame.K_n, f"keyboard-sounds/{n[0]}", n[1], False))

            for key, file, text, fade in dj_buttons:
                if keys[key]:
                    if key not in pressed:
                        ch3.load_file(file)
                        ch3.play()
                        if text is not None:
                            display.dj(text)
                        pressed.append(key)
                        if fade:
                            down_for_voice = True
                            ch0.set_volume(volumes[1])
                            ch1.set_volume(volumes[1])

                elif key in pressed:
                    pressed.remove(key)

            if down_for_voice and not ch3.active:
                ch0.set_volume(volumes[0])
                ch1.set_volume(volumes[0])
            display.tick()

    except Quit:
        break
    except BaseException as e:
        ch0.stop()
        ch1.stop()
        ch2.stop()
        display.error(e)
