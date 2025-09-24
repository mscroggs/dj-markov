import json

try:
    with open("config.json") as f:
        config = json.load(f)
except:
    config = {}

mode = config.get("mode", "demo")
name = config.get("name", "Robo-DJ")
windowed = config.get("windowed", False)
no_repeats = config.get("no-repeats", False)
dj_rate = config.get("dj-rate", 0.01)
startup = config.get("startup", False)
hey_ya_ymca = config.get("hey_ya_ymca", False)
start_later = config.get("start_later", False)
width = config.get("width", None)
height = config.get("height", None)
start_asleep = config.get("start_asleep", False)
matt2025 = config.get("matt2025", False)
