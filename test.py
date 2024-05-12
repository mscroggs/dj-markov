import pytest
import json


@pytest.mark.parametrize("mode", ["demo"])
def test_library(mode):
    with open(f"out/{mode}/info.json") as f:
        info = json.load(f)
    transitions = {}
    with open(f"out/{mode}/data.json") as f:
        for line in f:
            data = json.loads(line)
            if data["song1"] not in transitions:
                transitions[data["song1"]] = []
            transitions[data["song1"]].append(data)

    for i in info:
        if i not in transitions:
            raise ValueError(f"{i} is a dead end")
