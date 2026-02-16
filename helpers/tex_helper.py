import datetime
import random
from tkinter import END
from typing import Optional

from settings import themery as t, utils as u
import texity
import texoty
from settings.utils import PRO_TIPS

BLOCK_CHAR_DICT = {
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



class TexiotyHelper:
    """
    A helper class for Texioty to use. Allows access to the TEXOTY and TEXITY objects.
    Provides the "welcome commands, help", commands for the help registry.

    """
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
                'args_desc': {' - ': ['No arguments available.', None]},
                'examples': ['welcome'],
                'group_tag': 'HLPR',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
            },
            "commands": {
                'name': 'commands',
                'usage': '"commands"',
                'call_func': self.display_all_available_commands,
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
                                  '(COMMAND_NAME)': list(self.txo.master.command_registry.commands.keys())},
                'args_desc': {' - ': ['No argument needed.', None],
                              '(GROUP_TAG)': ['Group tag for getting help with.', str],
                              '(COMMAND_NAME)': ['Name of the command to get help with.', str]},
                'examples': ['help help', 'help', 'help HLPR', 'help commands'],
                'group_tag': 'HLPR',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
            }
        }

    def priont_block_font(self, blk_word: str):
        top_line = ''
        mid_line = ''
        bot_line = ''
        for letter in blk_word:
            top_line += " " + BLOCK_CHAR_DICT[letter][0] + " "
            mid_line += " " + BLOCK_CHAR_DICT[letter][1] + " "
            bot_line += " " + BLOCK_CHAR_DICT[letter][2] + " "
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
        self.priont_block_font(title_word)
        self.txo.priont_string(random.choice('─━═_')*(len(title_word)*5))

    def display_help_message(self, help_topic: Optional[str] = None):
        """
        Print the available commands for use with a header added to the top.
        :param help_topic:
        :return:
        """
        self.txo.clear_add_header()
        # print(help_topic, "HELPER_TAGE")
        if help_topic:
            if help_topic in self.txo.master.active_helpers:
                self.txo.helper_tag_break(help_topic)
                available_commands = self.txo.master.command_registry.commands
                for command in available_commands:
                    if available_commands[command].group_tag == help_topic:
                        self.txo.priont_command_midd(self.txo.master.command_registry.commands[command])

            elif help_topic in self.txo.master.command_registry.commands:
                self.txo.priont_command_full(self.txo.master.command_registry.commands[help_topic])
            else:    # Wrong help_topic provided.
                self.txo.priont_string(f"Sorry, I don't recognize '{help_topic}' as a helper tag or any commands.")
                self.txo.priont_string("⦙⦓ Here are a list of the active helpers:")
                self.txo.priont_list(self.txo.master.active_helpers, "Helper Tags:")
                self.txo.priont_string("⦙⦓ Here are a list of different commands:")
                self.txo.priont_list(random.sample(sorted(self.txo.master.command_registry.commands), 3), "Commands:")
        else:    # No group_tag provided.
            self.txo.priont_string("⦙⦓ Seems like you might need help, good luck!")
            self.txo.priont_string("   Anything that can be done in this program can be")
            self.txo.priont_string("   done through this Texioty widget.")
            self.txo.priont_string("⦙⦓ Here are a list of the active helpers:")
            self.txo.priont_list(self.txo.master.active_helpers, parent_key="Helper Tags:")

    def display_all_available_commands(self):
        """Prints out all the commands that are available."""
        self.txo.clear_no_header()
        available_commands = self.txo.master.command_registry.commands
        # print(available_commands)
        for helper_group in self.txo.master.active_helpers:
            print(helper_group)
            self.txo.helper_tag_break(helper_group)
            for command in available_commands:
                if available_commands[command].group_tag == helper_group:
                    self.txo.priont_command_lite(self.txo.master.command_registry.commands[command])

    def welcome_message(self):
        """
        Display welcoming messages with a few commands to get started.

        """
        self.txo.clear_add_header("Welcome!")
        today_date = datetime.datetime.date(datetime.datetime.now())
        today_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
            datetime.datetime.weekday(today_date)]
        self.txo.priont_string(
            f"⦙⦓ Welcome to Texioty! The date is {today_date} on a {today_day}.\n")

        self.txo.priont_string(f"PRO TIP⁍ {random.choice(PRO_TIPS)}")
