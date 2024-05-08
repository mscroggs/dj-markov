import json
import mashup
import os
import random

try:
    with open("data/songlist") as f:
        songs = [line.strip() for line in f]
except FileNotFoundError:
    songs = []


def find_files(dir):
    out = []
    for file in os.listdir(dir):
        if not file.startswith("."):
            path = f"{dir}/{file}"
            if os.path.isdir(path):
                out += find_files(path)
            elif os.path.isfile(path) and file.endswith(".mp3"):
                out.append(path)
    return out


for file in find_files("music"):
    if file not in songs:
        songs.append(file)
        with open("data/songlist", "a") as f:
            f.write(f"{file}\n")

try:
    with open("data/mixability") as f:
        mixability = json.load(f)
except FileNotFoundError:
    mixability = {}


def get_mixability(song1, song2):
    global mixability
    if song1 not in mixability:
        mixability[song1] = {}
    if song2 not in mixability[song1]:
        try:
            m = mashup.Mixer(song1, song2)
            m.load_songs()
            m.analyse()
        except:
            pass
        mixability[song1][song2] = m.mixability

        with open("data/mixability", "w") as f:
            json.dump(mixability, f)

    return mixability[song1][song2]


for (i, s1) in enumerate(songs):
    for (j, s2) in enumerate(songs):
        print(f"{1 + i * len(songs) + j} / {len(songs) ** 2}")
        get_mixability(s1, s2)
