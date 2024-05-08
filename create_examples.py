import json
import mashup
import os
import random

with open("data/mixability") as f:
    mixability = json.load(f)

scores = []

for s1, ms in mixability.items():
    for s2, m in ms.items():
        if m > 0:
            scores.append((s1, s2, m))

scores.sort(key=lambda i: i[2])

j = 0
i = 0
while i < 5:
    print(j)
    s = scores[j]
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse(False)
    if min(m.fade_in_length, m.fade_out_length) > 1000:
        print(f"Mixing {s[0]} and {s[1]}")
        m.mix(True)
        m.export(f"out/worst{i + 1}.mp3")
        i += 1
    j += 1

j = -1
i = 0
while i < 5:
    print(j)
    s = scores[j]
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse(False)
    print(m.fade_in_length, m.fade_out_length)
    if min(m.fade_in_length, m.fade_out_length) > 1000:
        print(f"Mixing {s[0]} and {s[1]}")
        m.mix(True)
        m.export(f"out/best{i + 1}.mp3")
        i += 1
    j -= 1

