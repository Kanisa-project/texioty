import datetime
import glob
import random
from os.path import exists
from typing import Callable

from src.texioty.helpers.promptaires.prompt_helper import BasePrompt
from src.texioty.helpers.registries.command_definitions import bind_commands, DIRY_COMMANDS
from src.texioty.settings import themery as t, utils as u


class Digiary(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.diary_line_length = 75
        self.diarySentenceList = []
        self.in_diary_mode = False
        self.helper_commands = bind_commands(DIRY_COMMANDS, {
            '/until_next_time': self.stop_diary_mode,
            'dear_sys,': self.start_diary_mode,
            'redear': self.select_diary_entry_date,
        })
        

    def start_diary_mode(self) -> datetime.datetime:
        """Begin a diary entry and add a timestamp line to the beginning of the entry."""
        start_now = datetime.datetime.now()
        self.txo.master.current_mode = "Diary"
        self.txo.priont_string(f"\n┎Entering diary mode⸦🮞{start_now}")
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
        self.txo.priont_string(f"┖Exiting diary mode─⸦🮝{end_now}\n")
        ending_line = timestamp_line_entry(end_now, '/until_next_time', lead_line='ts',
                                           follow_line=' ' * (self.diary_line_length - len('/until_next_time')))
        self.diarySentenceList.append(ending_line)
        create_date_entry(end_now, self.diarySentenceList)
        return end_now

    def select_diary_entry_date(self):
        """Decide which dated diary entry to read."""
        self.decide_decision("What date to read?", glob.glob('filesOutput/.diary/*.txt'))
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.priont_date_entry

    def priont_date_entry(self, entry_filename):
        """Priont each line of a dated diary entry."""
        with open(entry_filename, "r") as dentry:
            lines = dentry.readlines()
            for line in lines:
                self.txo.priont_string(line)
        self.txo.master.default_mode()


def create_date_entry(entry_time: datetime.datetime, entry_list: list):
    """
    Create a date entry for today.
    :param entry_time: Exact time the entry was created.
    :param entry_list: List of entry lines.
    :return:
    """
    entry_date_name = f'{entry_time.year}_{entry_time.month}_{entry_time.day}'
    # entry_list.pop(len(entry_list) - 3)
    if exists(f'filesOutput/.diary/{entry_date_name}.txt'):
        with open(f'filesOutput/.diary/{entry_date_name}.txt', 'a') as f:
            for ent in entry_list:
                f.write(ent + "\n")
            f.write("\n")
    else:
        with open(f'filesOutput/.diary/{entry_date_name}.txt', 'w') as f:
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
