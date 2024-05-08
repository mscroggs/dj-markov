import random
import mashup
import os

files = os.listdir("music")
# random.shuffle(files)

scores = []

for f in files:
    for g in files:
        if f != g:
            m = mashup.Mixer(f"music/{f}", f"music/{g}")
            m.load_songs()
            m.analyse()
            if m.mixability > 0:
                scores.append((f"music/{f}", f"music/{g}", m.mixability))
                print(scores[-1])

scores.sort(key=lambda i: i[2])

for i, s in enumerate(scores[:5]):
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse()
    m.mix()
    m.export(f"out/worst{i + 1}.mp3")

for i, s in enumerate(scores[-5:]):
    m = mashup.Mixer(s[0], s[1])
    m.load_songs()
    m.analyse()
    m.mix()
    m.export(f"out/best{5 - i}.mp3")

