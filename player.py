import numpy as np
import json
import random
from time import time
from display import Display, Quit
from just_playback import Playback

if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode = "demo"

songdata = {}
with open(f"out/{mode}/data.json") as f:
    for line in f:
        data = json.loads(line)
        if data["song1"] not in songdata:
            songdata[data["song1"]] = []
        songdata[data["song1"]].append(data)
with open(f"out/{mode}/info.json") as f:
    info = json.load(f)

ch0 = Playback()
ch1 = Playback()
ch2 = Playback()

ch2.load_file("keyboard-sounds/DJ.wav")

current = random.choice(random.choice(list(songdata.values())))
next = None
choice_shown = False

current_channel = 0
ch0.load_file(current["filename"])

# display = Display(450, 800, {})
display = Display()
display.add_playing(info[current["song1"]]["title"], info[current["song1"]]["artist"])
display.draw_bg()
display.update()
ch0.play()


while True:
    try:
        if random.random() > 0.8:
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
            weights = np.array([i["rating"] for i in options])
            weights /= sum(weights)
            next = np.random.choice(options, p=weights)
            queued.load_file(next["filename"])

        if playing.curr_pos > current["fade_end"]:
            display.remove_playing()
            queued.play()
            queued.seek(current["song2_fade_end"] + playing.curr_pos - current["fade_end"])
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
