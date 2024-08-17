import json

try:
    with open("config.json") as f:
        config = json.load(f)
except:
    config = {}

mode = config["mode"] if "mode" in config else "demo"
name = config["name"] if "name" in config else "DJ Markov"
windowed = config["windowed"] if "windowed" in config else False
