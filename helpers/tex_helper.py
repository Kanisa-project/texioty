import datetime
import random
from dataclasses import dataclass
from tkinter import END
from typing import Optional, List, Callable, Tuple

from settings import themery as t, utils as u
import texity
import texoty


ALPHA_BLK_DICT = {
    ' ': ['   ', '   ', '   '],
    '-': ['   ', ' ▁▁', '▔▔ '],
    '_': ['   ', '   ', '▁▁▁'],
    '!': [' ▅▆', ' ▐▛', ' ▗▖'],
    '?': ['▗▅▃', ' ▗▛', ' ▗▖'],
    '/': ['  ▆', ' ▐▛', '▆  '],
    '.': ['   ', '   ', ' ▅ '],
    ':': ['   ', ' ▀ ', ' ▀ '],
    '(': ['▗  ', '▌  ', '▚  '],
    '{': ['▗  ', '▞  ', '▚  '],
    ')': ['  ▖', '  ▐', '  ▞'],
    '}': ['  ▖', '  ▚', '  ▞'],
    '%': ['▀ ▞', ' ▞ ', '▞ ▗'],
    '0': ['▗▆▖', '▌.▋', '▙▃▖'],
    '1': ['▃▅▆', ' ▉ ', ' ▛ '],
    '2': ['▂▃▃', ' ▃▛', '▟▂▂'],
    '3': ['━━▗', ' ━▐', '▁▁▟'],
    '4': ['  ', '▐▁▌', ' ▔▌'],
    '5': ['▗━┓', ' ▚▖', '▚▁▞'],
    '6': ['▗━▃', '▌▗▁', '▚▁▞'],
    '7': ['▃▅▆', ' ▉ ', ' ▛ '],
    '8': ['▗━▖', '▐━▎', '▐▂▌'],
    '9': ['━━▖', '  ▌', '▃▁▞'],
    'a': [' ▄ ', '▐▁▌', '▛▔▜'],
    'b': ['▗━▖', '▐━▎', '▐▂▌'],
    'c': ['▗━┓', '▌  ', '▚▁▞'],
    'd': ['▄━▖', '▌ ▐', '▙▂▞'],
    'e': ['▗━━', '▐━ ', '▟▁▁'],
    'f': ['▄━━', '▐━ ', '▐  '],
    'g': ['▗━▃', '▌▗▁', '▚▁▞'],
    'h': ['▗ ▗', '▌▁▐', '▌▔▞'],
    'i': ['▗▃▃', ' ▟ ', '▄▙▖'],
    'j': ['━━▖', '  ▌', '▃▁▞'],
    'k': ['▖ ▖', '▌▞ ', '▌ ▚'],
    'l': ['▖  ', '▐  ', '▟▄▖'],
    'n': ['▗▖▗', '▌▚▐', '▌▝▟'],
    'm': ['▗ ▖', '▞▚▚', '▌ ▐'],
	'o': ['▗▆▖', '▌ ▋', '▙▃▘'],
    'p': ['▗━▖', '▌▁▌', '▌  '],
    'q': ['▗▆▖', '▌ ▋', '▚▃▙'],
    'r': ['▗━▃', '▌▁▞', '▌ ▚'],
    's': ['▗━┓', ' ▚▖', '▚▁▞'],
    't': ['▃▅▆', ' ▉ ', ' ▛ '],
    'u': ['▗ ▗', '▌ ▐', '▚▃▟'],
    'v': ['▖ ▗', '▐ ▐', ' ▚▘'],
    'w': ['▖ ▗', '▌▗▐', '▚▘▚'],
    'x': ['▖ ▗', '▝▆▘', '▞ ▚'],
    'y': ['▖ ▖', '▚▞ ', '▟  '],
    'z': ['▂▃▃', ' ▃▛', '▟▂▂']
    }


@dataclass
class Question:
    key: str
    prompt: str
    default: Optional[str] = None
    choices: Optional[List[str]] = None
    validator: Optional[Callable[[str], Tuple[bool, Optional[str]]]] = None


class TexiotyHelper:
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        self.txo = txo
        self.txi = txi
        self.helper_commands = {
            "welcome": [self.welcome_message, "Displays a welcoming message.",
                     {}, "HLPR", u.rgb_to_hex(t.GREEN_YELLOW), u.rgb_to_hex(t.BLACK)],
            "help": [self.display_help_message, "Displays a message of helpfulness.",
                     {}, "HLPR", u.rgb_to_hex(t.GREEN_YELLOW), u.rgb_to_hex(t.BLACK)],
            "commands": [self.display_available_commands, "Displays all available commands.",
                         {}, "HLPR", u.rgb_to_hex(t.GREEN_YELLOW), u.rgb_to_hex(t.BLACK)],
        }

    def print_block_font(self, blk_word: str):
        top_line = ''
        mid_line = ''
        bot_line = ''
        for letter in blk_word:
            top_line += " " + ALPHA_BLK_DICT[letter][0] + " "
            mid_line += " " + ALPHA_BLK_DICT[letter][1] + " "
            bot_line += " " + ALPHA_BLK_DICT[letter][2] + " "
        self.txo.priont_string(top_line)
        self.txo.priont_string(mid_line)
        self.txo.priont_string(bot_line)

    def display_title(self, title_word: str, clear_it=True):
        """
        Using the 'block font' displays the title of the current menu.
        :param title_word: Word for displaying.
        :param clear_it: If the texoty should be cleared before displaying.
        :return:
        """
        if clear_it:
            self.txo.clear_no_header()
        self.txo.priont_string(random.choice('─━═_')*(len(title_word)*5))
        self.print_block_font(title_word)
        self.txo.priont_string(random.choice('─━═_')*(len(title_word)*5))

    def display_help_message(self, args):
        """
        Print the available commands for use with a header added to the top.
        :param args:
        :return:
        """
        self.txo.clear_add_header()
        self.txo.priont_string("⦓⦙ Seems like you might need help, good luck!")
        self.txo.priont_string("   Anything that can be done in this program can be")
        self.txo.priont_string("   done through this Texioty widget.")
        self.txo.priont_string("⦓⦙ Here are a couple of easy commands to get you started: \n\n")
        self.txo.priont_command(self.txo.master.registry.commands["help"])
        self.txo.priont_command(self.txo.master.registry.commands["commands"])

    def display_available_commands(self):
        """Prints out all the commands that are available."""
        self.clear_texoty()
        available_commands = self.txo.master.registry.commands
        for helper_group in self.txo.master.active_helpers:
            self.txo.command_group_break(helper_group)
            for command in available_commands:
                if available_commands[command].helper_symbol == helper_group:
                    self.txo.priont_command(self.txo.master.registry.commands[command])

    def clear_texoty(self):
        """Clear all the text from texoty and replace the header."""
        self.txo.delete("0.0", END)
        self.txo.set_header()

    def welcome_message(self, welcoming_msgs: list):
        """
        Display welcoming messages with a few commands to get started.

        """
        self.txo.clear_add_header("Welcome!")
        today_date = datetime.datetime.date(datetime.datetime.now())
        today_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
            datetime.datetime.weekday(today_date)]
        self.txo.priont_string(
            f"⦓⦙ Welcome to Texioty! The date is {today_date} on a {today_day}.")
        for msg in welcoming_msgs:
            self.txo.priont_string("⦓⦙ " + msg)
        self.txo.priont_string("\n")
        # self.ask_form([Question(key="one", prompt="Is this a question?", default='Yes',
        #                        choices=['Yes', 'No'], widget='entry'),
        #                Question(key="two", prompt="What is your name?", default='John',
        #                         choices=['John', 'Jane', 'Jeremy'], widget='option'),
        #                Question(key="three", prompt="Which color:", default='Green',
        #                         choices=['Red', 'Green', 'Blue'], widget='option',
        #                         validator=self.txo.priont_string)])
