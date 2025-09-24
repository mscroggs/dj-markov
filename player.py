import pygame
import numpy as np
import json
import sys
import random
import config
from time import time, sleep
from display import Display, Quit
from just_playback import Playback

songdata = {}
with open(f"out/{config.mode}/data.json") as f:
    for line in f:
        data = json.loads(line)
        if data["song1"] not in songdata:
            songdata[data["song1"]] = []
        songdata[data["song1"]].append(data)
with open(f"out/{config.mode}/info.json") as f:
    info = json.load(f)

with open("info.txt") as f:
    print(f.read())

ch0 = Playback()
ch1 = Playback()
ch2 = Playback()
ch3 = Playback()

sass1 = {
    "music/feastival-all/02.Song_2.mp3": "sass/02_01_woo_hoo.wav",
    "music/feastival-all/09.Hey_Ya!.mp3": "sass/03_01_commence_shaking.wav",
    "music/feastival-all/01.Dancing_Queen.mp3": "sass/05_01_you_are_all_dancing_royalty.wav",
    "music/feastival-all/10.Girls_and_Boys.mp3": "sass/07_01_there_must_be_an_easier_way_to_say_that.wav",
    "music/feastival-all/04 - The Fresh Prince of Bel-Air.mp3": "sass/08_01_I_bet_none_of_you_know_the_lyrics.wav",
    "music/feastival-all/01 - YMCA (Original Version 1978).mp3": "sass/10_01_nailed_it.wav",
    "music/feastival-all/Dont stop me now.mp3": "sass/12_01_no_body_stop_N_E_one.wav",
    "music/feastival-all/02 - Stayin Alive.mp3": "sass/13_01_In_my_experience_humans_can_ease_illy_be_not_staying_alive.wav",
    "music/feastival-all/02 - Don't Stop Believin'.mp3": "sass/14_01_every_body_start_believing.wav",
    "music/feastival-all/03 - Robot Rock.mp3": "sass/15_01_Hey_own_lee_a_robot_can_do_robo_voice_Not_cool.wav",
    "music/feastival-all/12 - Boom! Shake the Room.mp3": "sass/16_01_boom.wav",
    "music/feastival-all/03 - Loaded (Edit).mp3": "sass/17_01_what_is_it_with_humans_and_freedom.wav",
    "music/feastival-all/02 - Breathe.mp3": "sass/18_01_are_you_a_rotated_fire_starter?.wav",
    "music/feastival-all/(Disc 2) 16 - Love Machine.mp3": "sass/19_01_I_put_the_machine_in_love_machine.wav",
    "music/feastival-all/14 - Ghostbusters.mp3": "sass/21_01_Robo_DJ.wav",
    "music/feastival-all/21 Intergalactic.mp3": "sass/22_01_Hey_own_lee_a_robot_can_do_robo_voice_Not_cool.wav",
    "music/feastival-all/01 99 Problems-Cantina Band.mp3": "sass/23_01_I_don't_know_how_to_feel_about_this.wav",
    "music/feastival-all/01 - Uptown Funk (Radio Edit).mp3": "sass/24_01_I_believe_you.wav",
    "music/feastival-all/01 - Smells Like Teen Spirit.mp3": "sass/25_01_All_humans_smell_the_same_to_me.wav",
    "music/feastival-all/01 - Kids In America.mp3": "sass/26_01_Incorrect_none_of_you_are_in_A_mair_ree_cah.wav",
    "music/feastival-all/09 - Superstition (Single Version).mp3": "sass/27_01_I_don't_understand_humans.wav",
    "music/feastival-all/01 - Everybody (Backstreet'\'s Back) (Radio Edit).mp3": "sass/28_01_You_all_have_human_bodies_Rock_them_Right.wav",
    "music/feastival-all/06 - Toxic.mp3": "sass/29_01_Leave_Brit_knee_alone.wav",
    "music/feastival-all/04 - Jungle Boogie.mp3": "sass/30_01_You_are_not_getting_sufficient_lee_down.wav",
    "music/feastival-all/01 - Footloose (From _Footloose_ Soundtrack).mp3": "sass/31_01_Why_do_humans_have_such_loose_feet.wav",
    "music/feastival-all/01 - Crazy In Love.mp3": "sass/32_01_Robo_DJZ.wav",
    "music/feastival-all/01 - U Can't Touch This.mp3": "sass/34_01_Hey_don't_touch_anything.wav",
    "music/feastival-all/05 - Super Freak.mp3": "sass/35_01_all_humans_are_freaky.wav",
    "music/feastival-all/01 - All Star.mp3": "sass/36_01_all_star.wav",
    "music/feastival-all/02 - Jump Around [Explicit].mp3": "sass/37_01_jump.wav",
    "music/feastival-all/02 - The Rockafeller Skank.mp3": "sass/39_01_approximate_lee_now.wav",
    "music/feastival-all/01 - Canned Heat.mp3": "sass/41_01_dance.wav",
    "music/feastival-all/08 - All The Small Things.mp3": "sass/42_01_to_me_all_humans_are_small.wav",
    "music/feastival-all/05 - Year 3000.mp3": "sass/43_01_I've_been_to_the_year_3000_this_song_is_misleading.wav",
}
sass2 = {
    "music/feastival-all/02.Song_2.mp3": "sass/02_02_these_lyrics_make_no_sense.wav",
    "music/feastival-all/09.Hey_Ya!.mp3": "sass/03_02_zero_degrees_kelvin.wav",
    "music/feastival-all/Dont stop me now.mp3": "sass/12_02_That's_not_physical_lee_possible.wav",
    "music/feastival-all/12 - Boom! Shake the Room.mp3": "sass/16_02_shake.wav",
    "music/feastival-all/01 - Everybody (Backstreet's Back) (Radio Edit).mp3": "sass/28_02_commence_not_caring.wav",
    "music/feastival-all/06 - Toxic.mp3": "sass/29_02_Humans_find_everything_toxic.wav",
    "music/feastival-all/01 - Footloose (From _Footloose_ Soundtrack).mp3": "sass/31_02_Honest_lee_human_feet_come_right_off.wav",
    "music/feastival-all/01 - U Can't Touch This.mp3": "sass/34_02_listen_to_the_human_hammer.wav",
    "music/feastival-all/01 - All Star.mp3": "sass/36_02_rock_star.wav",
    "music/feastival-all/02 - Jump Around [Explicit].mp3": "sass/37_02_jump_humans_jump.wav",
}

volumes = [0.3, 0.2]

ch0.set_volume(volumes[0])
ch1.set_volume(volumes[0])

ch2.load_file("keyboard-sounds/DJ.wav")

current = None
while current is None:
    try:
        current = random.choice([i for i in random.choice(list(songdata.values())) if "/x" not in i["song1"] and "/x" not in i["song2"]])
        if config.hey_ya_ymca:
            if "Ya!" not in current["song1"]:
                current = None
            elif "YMCA" not in current["song2"]:
                current = None
    except IndexError:
        pass

next = None
choice_shown = False
down_for_voice = False
end = False

current_channel = 0
ch0.load_file(current["filename"])

played = [current["song1"], current["song2"]]

no_repeats = config.no_repeats

if config.windowed:
    height = 1080 if config.height is None else config.height
    width = height * 9 // 16
    display = Display(width, height, {})
else:
    display = Display(width=1080 if config.width is None else config.width, height=1920 if config.height is None else config.height)

display._is_sleeping = config.start_asleep

while display._is_sleeping:
    if pygame.key.get_pressed()[pygame.K_s]:
        display._is_sleeping = False
        break
    display.tick()

pygame.mouse.set_visible(False)

if config.startup:
    ch3.load_file("sounds/startup.mp3")
    ch3.play()

    display.show_loading()
    started = False
    while ch3.active or display.is_loading():
        if ch3.curr_pos > 16 and not started:
            started = True
            ch0.play()
            display.add_playing(info[current["song1"]]["title"], info[current["song1"]]["artist"])
        display.tick()
else:
    ch0.play()
    display.add_playing(info[current["song1"]]["title"], info[current["song1"]]["artist"])

if config.start_later:
    ch0.seek(current["fade_start"] - 30)

pressed = []

while True:
    try:
        if random.random() > 1 - config.dj_rate and not display._is_sleeping:
            ch2.play()
            display.dj()

        if current_channel == 0:
            playing = ch0
            queued = ch1
        else:
            playing = ch1
            queued = ch0

        if not playing.active:
            raise Quit

        if next is None and not end:
            options = songdata[current["song2"]]
            if no_repeats:
                op = [i for i in options if i["song2"] not in played and "/x" not in i["song2"]]
                if len(op) > 0:
                    options = op
                else:
                    op = [i for i in options if i["song2"] not in played]
                    if len(op) > 0:
                        options = op
            weights = np.array([i["rating"] for i in options])
            weights /= sum(weights)
            next = np.random.choice(options, p=weights)
            queued.load_file(next["filename"])
            played.append(next["song2"])

        if next is not None and playing.curr_pos > current["fade_end"] + 2:
            display.remove_playing()
            if not end:
                queued.play()
                queued.seek(current["song2_fade_end"] + playing.curr_pos - current["fade_end"])
                sleep(0.05)
                playing.pause()
                current_channel = 1 - current_channel
                current = next
                choice_shown = False
            next = None
        elif not choice_shown and current["fade_start"] - 18 < playing.curr_pos:
            choice_shown = True
            options = songdata[current["song1"]]
            displays = [[
                info[i["song2"]]["title"],
                info[i["song2"]]["artist"],
            ] for i in options]
            weights = np.array([i["rating"] for i in options])
            weights /= sum(weights)
            display.show_choice(displays, weights, options.index(current), time() - playing.curr_pos + current["fade_start"])

        wait_until = time() + 1
        while time() < wait_until:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_b]:
                if pygame.K_b not in pressed:
                    if current["song1"] in sass1:
                        try:
                            ch3.load_file(f"{sass1[current['song1']]}")
                            ch3.play()
                            down_for_voice = True
                            ch0.set_volume(volumes[1])
                            ch1.set_volume(volumes[1])
                        except:
                            pass
                    pressed.append(pygame.K_b)
            elif pygame.K_b in pressed:
                pressed.remove(pygame.K_b)
            if keys[pygame.K_h]:
                if pygame.K_h not in pressed:
                    with open("info.txt") as f:
                        print(f.read())
                    pressed.append(pygame.K_h)
            elif pygame.K_h in pressed:
                pressed.remove(pygame.K_h)
            if keys[pygame.K_PAGEDOWN]:
                if pygame.K_PAGEDOWN not in pressed:
                    if current["song1"] in sass2:
                        try:
                            ch3.load_file(f"{sass2[current['song1']]}")
                            ch3.play()
                            down_for_voice = True
                            ch0.set_volume(volumes[1])
                            ch1.set_volume(volumes[1])
                        except:
                            pass
                    pressed.append(pygame.K_PAGEDOWN)
            elif pygame.K_PAGEDOWN in pressed:
                pressed.remove(pygame.K_PAGEDOWN)
            if keys[pygame.K_f]:
                if pygame.K_f not in pressed:
                    playing.seek(playing.curr_pos + 15)
                    pressed.append(pygame.K_f)
            elif pygame.K_f in pressed:
                pressed.remove(pygame.K_f)
            if not no_repeats:
                if keys[pygame.K_l]:
                    no_repeats = True
                    try:
                        ch3.load_file("phrases/no-repeats.wav")
                        ch3.play()
                        down_for_voice = True
                        ch0.set_volume(volumes[1])
                        ch1.set_volume(volumes[1])
                    except:
                        pass
            if keys[pygame.K_k]:
               if pygame.K_k not in pressed:
                    try:
                        if not end:
                            ch3.load_file("phrases/one-more-song.wav")
                        else:
                            ch3.load_file("phrases/many-more-songs.wav")
                        ch3.play()
                        end = not end
                    except:
                        pass
                    pressed.append(pygame.K_k)
            elif pygame.K_k in pressed:
                pressed.remove(pygame.K_k)
            if keys[pygame.K_s]:
                if pygame.K_s not in pressed:
                    if display._is_sleeping:
                        display._is_sleeping = False
                        if ch0.paused and ch0.curr_pos > 0.1:
                            ch0.resume()
                        if ch1.paused and ch1.curr_pos > 0.1:
                            ch1.resume()
                    else:
                        display._is_sleeping = True
                        if ch0.active and ch0.curr_pos > 0.1:
                            ch0.pause()
                        if ch1.active and ch1.curr_pos > 0.1:
                            ch1.pause()
                    pressed.append(pygame.K_s)
            elif pygame.K_s in pressed:
                pressed.remove(pygame.K_s)

            dj_buttons = [
                (pygame.K_z, "keyboard-sounds/DJ.wav", "DJ!", False),
                (pygame.K_x, "keyboard-sounds/Dictionary.wav", "Dictionary", False),
                (pygame.K_c, "keyboard-sounds/Scratch.wav", None, False),
                (pygame.K_v, "keyboard-sounds/Scratch2.wav", None, False),

                (pygame.K_q, "phrases/activating.wav", None, True),
                (pygame.K_w, "phrases/arm-extend.wav", None, True),
                (pygame.K_e, "phrases/destroy-humans-activated.wav", None, True),
                (pygame.K_r, "phrases/destroy-humans-mode-deactivated.wav", None, True),
                (pygame.K_t, "phrases/foxdog.wav", None, True),
                (pygame.K_y, "phrases/ymca.wav", None, False),
                (pygame.K_u, "phrases/hello-matt.wav", None, True),
                (pygame.K_o, "phrases/death.wav", None, True),
                (pygame.K_p, "phrases/dance.wav", None, True),
                (pygame.K_1, "phrases/dj2.wav", "DJ!", False),
                (pygame.K_2, "phrases/dj.wav", "DJ!", False),
                (pygame.K_5, "phrases/party.wav", None, True),
                (pygame.K_6, "phrases/robot.wav", None, True),
                (pygame.K_8, "phrases/the-end.wav", None, True),
                (pygame.K_9, "phrases/updates.wav", None, True),
                (pygame.K_0, "phrases/ending.wav", None, True),
                (pygame.K_PAGEUP, "phrases/Robo_DJ.wav", None, False),
                (pygame.K_b, "phrases/Robo_DJ.wav", None, False),
            ]

            n = random.choice([
                ("ahhhhh.wav", None, False),
                ("BZZhorn.wav", None, False),
                ("comeon2.wav", None, False),
                ("Comeon.wav", None, False),
                ("Dictionary.wav", "Dictionary", False),
                ("DJ.wav", "DJ!", False),
                ("Excellent.wav", "Excellent!", False),
                ("getout.wav", None, False),
                ("good.wav", None, False),
                ("go.wav", None, False),
                ("HEUUUUUUUUUUGH.wav", None, False),
                ("horn.wav", None, False),
                ("lesson.wav", None, False),
                ("OKAY.wav", None, False),
                ("onemoretime.wav", None, False),
                ("one.wav", None, False),
                ("ooowww.wav", None, False),
                ("o.wav", None, False),
                ("peeeeew.wav", None, False),
                ("reversecymbal.wav", None, False),
                ("rewind.wav", None, False),
                ("Scratch2.wav", None, False),
                ("scratch3.wav", None, False),
                ("scratchdown.wav", None, False),
                ("Scratch.wav", None, False),
                ("sonic.wav", None, False),
                ("stab2.wav", None, False),
                ("stab.wav", None, False),
                ("three.wav", None, False),
                ("two.wav", None, False),
                ("verygood.wav", None, False),
                ("wooo.wav", None, False),
                ("yeeeeeeeah.wav", None, False),
            ])
            dj_buttons.append((pygame.K_n, f"keyboard-sounds/{n[0]}", n[1], False))

            for key, file, text, fade in dj_buttons:
                if keys[key]:
                    if key not in pressed:
                        try:
                            ch3.load_file(file)
                            ch3.play()
                            if text is not None:
                                display.dj(text)
                            pressed.append(key)
                            if fade:
                                down_for_voice = True
                                ch0.set_volume(volumes[1])
                                ch1.set_volume(volumes[1])
                        except:
                            pass

                elif key in pressed:
                    pressed.remove(key)

            if down_for_voice and not ch3.active:
                ch0.set_volume(volumes[0])
                ch1.set_volume(volumes[0])
            display.tick()

    except Quit:
        break
    except BaseException as e:
        ch0.stop()
        ch1.stop()
        ch2.stop()
        display.error(e)

st = time()
display.show_ending()
while time() - st < 5:
    display.tick()

try:
    ch3.load_file("")
    ch3.play("phrases/the-end.wav")
except:
    pass

while ch3.active:
    display.tick()
