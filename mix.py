import json
import mashup
import os
import random

with open("data/mixability") as f:
    mixability = json.load(f)
with open("out/data.json", "w") as f:
    pass

scores = []

n = 0

for s1, ms in mixability.items():
    scores = []
    for s2, m in ms.items():
        if m > 0:
            scores.append((s2, m))

    scores.sort(key=lambda i: -i[1])
    for s in scores[:2]:
        print(f"Mixing {s1} and {s[0]}")
        m = mashup.Mixer(s1, s[0])
        m.load_songs()
        m.analyse(False)
        m.mix()
        m.export(f"out/{n}.mp3")
        data = {
            "filename": f"out/{n}.mp3",
            "song1": s1,
            "song2": s[0],
            "fade_end": m.fade_end,
            "song2_fade_end": m.song2_fade_end,
            "rating": s[1],
        }
        with open("out/data.json", "a") as f:
            json.dump(data, f)
            f.write("\n")
        n += 1
