import json

try:
    with open("config.json") as f:
        config = json.load(f)
except:
    config = {}

mode = config["mode"] if "mode" in config else "demo"
name = config["name"] if "name" in config else "DJ Markov"
windowed = config["windowed"] if "windowed" in config else False
no_repeats = config["no-repeats"] if "no-repeats" in config else False
dj_rate = config["dj-rate"] if "dj-rate" in config else 0.01
startup = config["startup"] if "startup" in config else False
hey_ya_ymca = config["hey_ya_ymca"] if "hey_ya_ymca" in config else False
start_later = config["start_later"] if "start_later" in config else False
width = config["width"] if "width" in config else None
height = config["height"] if "height" in config else None
