import random
from typing import Optional

from PIL.ImageChops import overlay

from helpers.promptaires.prompt_helper import BasePrompt
# import tkinter as tk
import numpy as np
import sounddevice as sd
from settings import utils as u, themery as t, alphanumers as a

def generate_sine_wave(freq, duration, sample_rate=44100):
    print(freq, duration, sample_rate)
    sw = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(freq * sw * 2 * np.pi).astype(np.float32)



class BeepBoops(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.helper_commands['beep'] = {
            'name': 'beep',
            'usage': '"beep"',
            'call_func': self.play_beep,
            'lite_desc': 'Plays a beep sound.',
            'full_desc': ['Plays a beep sound with a frequency of 440 Hz for 0.5 seconds.'],
            'possible_args': {' - ': 'No arguments available.'},
            'args_desc': {' - ': ['No arguments available.', None]},
            'examples': ['beep'],
            'group_tag': 'PRUN',
            'font_color': u.rgb_to_hex(t.CHARTREUSE),
            'back_color': u.rgb_to_hex(t.BLACK)
        }
        self.helper_commands['boop'] = {
            'name': 'boop',
            'usage': '"boop"',
            'call_func': self.play_boop,
            'lite_desc': 'Plays a boop sound.',
            'full_desc': ['Plays a boop sound with a frequency of 44 Hz for 0.5 seconds.'],
            'possible_args': {' - ': 'No arguments available.'},
            'args_desc': {' - ': ['No arguments available.', None]},
            'examples': ['boop'],
            'group_tag': 'PRUN',
            'font_color': u.rgb_to_hex(t.CHARTREUSE),
            'back_color': u.rgb_to_hex(t.BLACK)
        }

    def play_beep(self, beep_msg: Optional[str]="none"):
        note_list = []
        for letter in beep_msg:
            # print(letter)
            fs_dur_freq = a.ALPHANUMERIC_NOTE_PATTERNS[letter][0]
            print(fs_dur_freq, "FSDUR")
            fs = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[0]][0]
            duration = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[1]][1]
            freq = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[2]][2]
            data = generate_sine_wave(freq, duration, fs)
            # print(data, "DATA")
            note_list.append(data)
        concatted = np.concatenate(note_list)
        sd.play(concatted, 44100)
        self.txo.priont_string("Beep beep played!")


    def play_boop(self, boop_msg: Optional[str]="none"):
        note_list = []
        max_len = 0
        pad_list = []
        for letter in boop_msg:
            fs_dur_freq = a.ALPHANUMERIC_NOTE_PATTERNS[letter][0]
            fs = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[0]][0]
            duration = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[1]][1]
            freq = a.NOTE_PATTERN_FS_DUR_FREQ[fs_dur_freq[2]][2]
            data = generate_sine_wave(freq, duration, fs)
            note_list.append(data)
        max_len = max(len(note) for note in note_list)
        for note in note_list:
            print("MAX", max_len)
            note_padded = np.pad(note, (0, max_len - len(note)), mode='constant')
            pad_list.append(note_padded)
        pad_pounded = pad_list[0]
        for p_note in pad_list:
            pad_pounded += p_note
        pad_pounded /= len(pad_list)
        sd.play(pad_pounded, 44100)
        self.txo.priont_string("Boop boop played!")