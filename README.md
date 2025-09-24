# Robo-DJ

## Adding a playlist
Run:

```bash
python3 analyse_songs.py
python3 mix.py
```

## Running Robo-DJ
Run:

```bash
python3 player.py
```

## Config

Robo-DJ can be configured by editing config.json

| Setting        | Default value | Purpose |
| -------------- | ------------- | ------- |
| `mode`         | `"demo"`      | Which folder of songs to use |
| `name`         | `"Robo-DJ"`   | The name of the robot - will be displayed on screen |
| `windowed`     | `False`       | Run in windowed mode? |
| `no-repeats`   | `False`       | Avoid repeats? |
| `dj-rate`      | `0.01`        | How often is says "DJ" |
| `startup`      | `False`       | Include start up sequence |
| `hey_ya_ymca`  | `False`       | Force start to be Hey Ya! followed by YMCA |
| `start_later`  | `False`       | Start later in first song |
| `width`        | `None`        | Width of screen |
| `height`       | `None`        | Height of screen |
| `start_asleep` | `False`       | Boot up already asleep |
| `matt2025`     | `False`       | Features for Matt's 2025 tour |
