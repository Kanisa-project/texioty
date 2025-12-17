import datetime
import random
from dataclasses import dataclass
from tkinter import END
from typing import Optional, List, Callable, Tuple

from settings import themery as t, utils as u
import texity
import texoty
from settings.utils import PRO_TIPS

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
            "welcome": {
                'name': 'welcome',
                'usage': '"welcome"',
                'call_func': self.welcome_message,
                'lite_desc': 'Displays a welcoming message.',
                'full_desc': ['Displays a welcoming message with a few commands to get started.',
                              'Available at any point using the system.'],
                'possible_args': {' - ': 'No arguments available.'},
                'args_desc': {' - ': 'No arguments available.'},
                'examples': ['welcome'],
                'group_tag': 'HLPR',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
            },
            "commands": {
                'name': 'commands',
                'usage': '"commands"',
                'call_func': self.display_available_commands,
                'lite_desc': 'Displays available commands.',
                'full_desc': ['Displays all commands available to use in the active Texioty mode.',
                              'Available at any point using the system.'],
                'possible_args': {' - ': 'No arguments available.'},
                'args_desc': {' - ': 'No arguments available.'},
                'examples': ['commands'],
                'group_tag': 'HLPR',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
            },
            "help": {
                'name': 'help',
                'usage': '"help (GROUP_TAG) (COMMAND_NAME)"',
                'call_func': self.display_help_message,
                'lite_desc': 'Displays a helpful message.',
                'full_desc': ['Displays some helpful tips and info based on the active Texioty mode.',
                              'Available at any point using the system.'],
                'possible_args': {'(GROUP_TAG)': self.txo.master.active_helpers,
                                  '(COMMAND_NAME)': list(self.txo.master.registry.commands.keys())},
                'args_desc': {'(GROUP_TAG)': 'Group tag for getting help with.',
                              '(COMMAND_NAME)': 'Name of the command to get help with.'},
                'examples': ['help help', 'help', 'help HLPR', 'help commands'],
                'group_tag': 'HLPR',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
            }
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

    def display_help_message(self, help_topic: Optional[str] = None):
        """
        Print the available commands for use with a header added to the top.
        :param help_topic:
        :param args:
        :return:
        """
        self.txo.clear_add_header()
        print(help_topic, "HELPER_TAGE")
        if help_topic:
            if help_topic in self.txo.master.active_helpers:
                self.txo.helper_tag_break(help_topic)
                available_commands = self.txo.master.registry.commands
                for command in available_commands:
                    if available_commands[command].group_tag == help_topic:
                        self.txo.priont_command_midd(self.txo.master.registry.commands[command])

            elif help_topic in self.txo.master.registry.commands:
                self.txo.priont_command_full(self.txo.master.registry.commands[help_topic])
            else:    # Wrong help_topic provided.
                self.txo.priont_string(f"Sorry, I don't recognize '{help_topic}' as a helper tag or any commands.")
                self.txo.priont_string("⦓⦙ Here are a list of different helper tags:")
                self.txo.priont_list(self.txo.master.active_helpers, "Helper Tags:")
                self.txo.priont_string("⦓⦙ Here are a list of different commands:")
                self.txo.priont_list(random.sample(sorted(self.txo.master.registry.commands), 3), "Commands:")
        else:    # No group_tag provided.
            self.txo.priont_string("⦓⦙ Seems like you might need help, good luck!")
            self.txo.priont_string("   Anything that can be done in this program can be")
            self.txo.priont_string("   done through this Texioty widget.")
            self.txo.priont_string("⦓⦙ Here are a list of different helper tags:")
            self.txo.priont_list(self.txo.master.active_helpers, parent_key="Helper Tags:")

    def display_available_commands(self):
        """Prints out all the commands that are available."""
        self.clear_texoty()
        available_commands = self.txo.master.registry.commands
        for helper_group in self.txo.master.active_helpers:
            self.txo.helper_tag_break(helper_group)
            for command in available_commands:
                if available_commands[command].group_tag == helper_group:
                    self.txo.priont_command_lite(self.txo.master.registry.commands[command])

    def clear_texoty(self):
        """Clear all the text from texoty and replace the header."""
        self.txo.delete("0.0", END)
        self.txo.set_header()

    def welcome_message(self):
        """
        Display welcoming messages with a few commands to get started.

        """
        self.txo.clear_add_header("Welcome!")
        today_date = datetime.datetime.date(datetime.datetime.now())
        today_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
            datetime.datetime.weekday(today_date)]
        self.txo.priont_string(
            f"⦓⦙ Welcome to Texioty! The date is {today_date} on a {today_day}.\n")

        self.txo.priont_string(f"PRO TIP⁍ {random.choice(PRO_TIPS)}")
