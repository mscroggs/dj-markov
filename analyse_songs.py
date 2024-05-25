import json
import mashup
import os
import sys
import random

if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode = "demo"

os.system(f"mkdir -p data/{mode}")

try:
    with open(f"data/{mode}/songlist") as f:
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


for file in find_files(f"music/{mode}"):
    if file not in songs:
        songs.append(file)
        with open(f"data/{mode}/songlist", "a") as f:
            f.write(f"{file}\n")

try:
    with open(f"data/{mode}/mixability") as f:
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

        with open(f"data/{mode}/mixability", "w") as f:
            json.dump(mixability, f)

    return mixability[song1][song2]


for (i, s1) in enumerate(songs):
    for (j, s2) in enumerate(songs):
        if s1 != s2:
            print(f"{1 + i * len(songs) + j} / {len(songs) ** 2}")
            get_mixability(s1, s2)
