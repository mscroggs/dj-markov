from mutagen.id3 import ID3
import json
import mashup
import os
import random

if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode = "demo"

with open(f"data/{mode}/mixability") as f:
    mixability = json.load(f)
with open(f"out/{mode}/data.json", "w") as f:
    pass

scores = []
info = {}

for song in mixability:
    tags = ID3(song)
    info[song] = {"title": tags["TIT2"].text[0], "artist": tags["TPE1"].text[0]}
with open(f"out/{mode}/info.json", "w") as f:
    json.dump(info, f)

to_mix = []
for s1, ms in mixability.items():
    scores = []
    for s2, m in ms.items():
        if m > 0:
            scores.append((s2, m))

    scores.sort(key=lambda i: -i[1])
    for s in scores:
        to_mix.append((s1, s[0], s[1]))

bad_songs = []
again = True
while again:
    remove = [i for i in mixability if i not in bad_songs and i not in [j[0] for j in to_mix]]
    if len(remove) == 0:
        break
    to_mix = [i for i in to_mix if i[1] not in remove]
    bad_songs += remove

for n, (song1, song2, score) in enumerate(to_mix):
    print(f"Mixing {song1} and {song2}")
    m = mashup.Mixer(song1, song2)
    m.load_songs()
    m.analyse(False)
    m.mix()
    m.export(f"out/{mode}/{n}.mp3")
    data = {
        "filename": f"out/{mode}/{n}.mp3",
        "song1": song1,
        "song2": song2,
        "fade_start": m.fade_start,
        "fade_end": m.fade_end,
        "song2_fade_end": m.song2_fade_end,
        "rating": score,
    }
    with open(f"out/{mode}/data.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
    n += 1
