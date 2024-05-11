import json
import random
from time import sleep
from just_playback import Playback

songdata = {}
with open("out/data.json") as f:
    for line in f:
        data = json.loads(line)
        if data["song1"] not in songdata:
            songdata[data["song1"]] = []
        songdata[data["song1"]].append(data)

ch0 = Playback()
ch1 = Playback()
ch2 = Playback()

ch2.load_file("keyboard-sounds/DJ.wav")

current = random.choice(random.choice(list(songdata.values())))
next = None

current_channel = 0
ch0.load_file(current["filename"])
ch0.play()


while True:
    if random.random() > 0.99:
        ch2.play()

    if current_channel == 0:
        playing = ch0
        queued = ch1
    else:
        playing = ch1
        queued = ch0

    if next is None:
        next = random.choice(songdata[current["song2"]])
        queued.load_file(next["filename"])

    if playing.curr_pos > current["fade_end"]:
        queued.play()
        queued.seek(current["song2_fade_end"] + playing.curr_pos - current["fade_end"])
        playing.pause()
        current_channel = 1 - current_channel
        current = next
        next = None

    sleep(1)