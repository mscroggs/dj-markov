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
        m = mashup.Mixer(song1, song2)
        m.load_songs()
        m.analyse()
        mixability[song1][song2] = m.mixability

        with open("data/mixability", "w") as f:
            json.dump(mixability, f)

    return mixability[song1][song2]


scores = []

for s1 in songs:
    for s2 in songs:
        if s1 != s2:
            m = get_mixability(s1, s2)
            if m > 0:
                scores.append((s1, s2, m))
                print(scores[-1])

scores.sort(key=lambda i: i[2])

for i, s in enumerate(scores[:5]):
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse()
    m.mix(True)
    m.export(f"out/worst{i + 1}.mp3")

for i, s in enumerate(scores[-5:]):
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse()
    m.mix(True)
    m.export(f"out/best{5 - i}.mp3")

