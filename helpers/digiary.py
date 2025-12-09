import datetime
import glob
import random
from os.path import exists
from typing import Optional

from settings import themery as t, utils as u

from helpers.tex_helper import TexiotyHelper

FULL_HELP = {
    "dear_sys,": {"usage": "dear_sys,",
                  "arg_desc": {'': "No args needed"},
                  "examples": ["dear_sys,"]},
    "/until_next_time": {"usage": "/until_next_time",
                         "arg_desc": {'': "No args needed"},
                         "examples": ["/until_next_time"]},
    "redear": {"usage": "redear",
               "arg_desc": {'': "No args needed"},
               "examples": ["redear"]}
}

class Digiary(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.diary_line_length = 75
        self.diarySentenceList = []
        self.in_diary_mode = False
        self.helper_commands["dear_sys,"] = {"name": "dear_sys,",
                                             "usage": '"dear_sys,"',
                                             "call_func": self.start_diary_mode,
                                             "lite_desc": "Starts a diary entry.",
                                             "full_desc": ["Starts a diary entry.",
                                                           "Can only be used in Texioty mode."],
                                             "possible_args": {' - ': 'No arguments available.'},
                                             "args_desc": {' - ': 'No arguments available.'},
                                             'examples': ['dear_sys,'],
                                             "group_tag": "DIRY",
                                             "font_color": u.rgb_to_hex(t.VIOLET_RED),
                                             "back_color": u.rgb_to_hex(t.BLACK)}
        self.helper_commands["/until_next_time"] = {"name": "/until_next_time",
                                                    "usage": '"/until_next_time"',
                                                    "call_func": self.stop_diary_mode,
                                                    "lite_desc": "Ends a diary entry.",
                                                    "full_desc": ["Ends a diary entry.",
                                                                  "Can only be used inside of Digiary mode."],
                                                    "possible_args": {' - ': 'No arguments available.'},
                                                    "args_desc": {' - ': 'No arguments available.'},
                                                    'examples': ['/until_next_time'],
                                                    "group_tag": "DIRY",
                                                    "font_color": u.rgb_to_hex(t.VIOLET_RED),
                                                    "back_color": u.rgb_to_hex(t.BLACK)}
        self.helper_commands["redear"] = {"name": "redear",
                                          "usage": '"redear"',
                                          "call_func": self.select_diary_entry_date,
                                          "lite_desc": "Select a date to read through.",
                                          "full_desc": ["Select a date to read through.",
                                                        "Can only be used in Texioty mode."],
                                          "possible_args": {' - ': 'No arguments available.'},
                                          "args_desc": {' - ': 'No arguments available.'},
                                          'examples': ['redear'],
                                          "group_tag": "DIRY",
                                          "font_color": u.rgb_to_hex(t.VIOLET_RED),
                                          "back_color": u.rgb_to_hex(t.BLACK)}
        

    def start_diary_mode(self) -> datetime.datetime:
        """Begin a diary entry and add a timestamp line to the beginning of the entry."""
        start_now = datetime.datetime.now()
        self.txo.master.current_mode = "Diary"
        self.txo.priont_string(f"\n┎Entering diary mode─⸦ {start_now}")
        opening_line = timestamp_line_entry(start_now, 'dear_sys,', lead_line='ts',
                                            follow_line=' ' * (self.diary_line_length - len('dear_sys,')))
        self.diarySentenceList = [opening_line]
        return start_now

    def add_diary_line(self, new_line):
        """Add a line to the current diary entry.⎸⎹"""
        self.txo.priont_string(f'┠⹕ {"".join(random.sample(new_line, len(new_line)))}')
        self.diarySentenceList.append(timestamp_line_entry(datetime.datetime.now(), new_line, lead_line='  ',
                                                           follow_line='_' * (self.diary_line_length - len(
                                                               new_line) - 2)))

    def stop_diary_mode(self) -> datetime.datetime:
        """End a diary entry and save the entry to a file."""
        end_now = datetime.datetime.now()
        self.txo.master.current_mode = "Texioty"
        self.txo.priont_string(f"┖Exiting diary mode─⸦ {end_now}\n")
        ending_line = timestamp_line_entry(end_now, '/until_next_time', lead_line='ts',
                                           follow_line=' ' * (self.diary_line_length - len('/until_next_time')))
        self.diarySentenceList.append(ending_line)
        create_date_entry(end_now, self.diarySentenceList)
        return end_now

    def select_diary_entry_date(self):
        self.txo.master.prompt_runner.tcg_lab.decide_decision("wat even am i?", glob.glob('.diary/*.txt'))
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.priont_date_entry

    def priont_date_entry(self, entry_filename):
        with open(entry_filename, "r") as dentry:
            lines = dentry.readlines()
            for line in lines:
                self.txo.priont_string(line)

    def display_help_message(self, group_tag: Optional[str] = None):
        super().display_help_message(group_tag)
        if group_tag and group_tag == "DIRY":
            self.txo.priont_dict(FULL_HELP)

def create_date_entry(entry_time: datetime.datetime, entry_list: list):
    """
    Create a date entry for today.
    :param entry_time: Exact time the entry was created.
    :param entry_list: List of entry lines.
    :return:
    """
    entry_date_name = f'{entry_time.year}_{entry_time.month}_{entry_time.day}'
    # entry_list.pop(len(entry_list) - 3)
    if exists(f'.diary/{entry_date_name}.txt'):
        with open(f'.diary/{entry_date_name}.txt', 'a') as f:
            for ent in entry_list:
                f.write(ent + "\n")
            f.write("\n")
    else:
        with open(f'.diary/{entry_date_name}.txt', 'w') as f:
            for ent in entry_list:
                f.write(ent + "\n")
            f.write("\n")


def timestamp_line_entry(entry_time: datetime.datetime, entry_line: str, lead_line=" ", follow_line=" ") -> str:
    """
    Take an entry line and add a time stamp with a lead and follow string.

    :param entry_time: Hour:Minute:Seconds
    :param entry_line: Text to be timestamped
    :param lead_line: Text to the left of the entry_line
    :param follow_line: Text to the right of the entry_line
    :return:
    """
    time_stamp = f'{entry_time.hour:02d}:{entry_time.minute:02d}:{entry_time.second:02d}'
    ret_str = lead_line + entry_line + follow_line
    if lead_line == "ts":
        ret_str = '  ' + entry_line + follow_line + time_stamp
        if entry_line == "dear_sys," or entry_line == "/until_next_time":
            ret_str = entry_line + follow_line + time_stamp + f':{entry_time.microsecond:2d}'

    return ret_str
