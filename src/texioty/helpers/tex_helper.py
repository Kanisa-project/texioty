import datetime
import random
from typing import Optional, TYPE_CHECKING

from src.texioty.helpers.registries.command_definitions import bind_commands, TEXIOTY_COMMANDS

from src.texioty.settings.utils import PRO_TIPS

if TYPE_CHECKING:
    from src.texioty.core.texity import TEXITY
    from src.texioty.core.texoty import TEXOTY

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
    def __init__(self, txo: "TEXOTY", txi: "TEXITY"):
        self.txo = txo
        self.txi = txi
        self.well_commands = {}
        self.helper_commands = bind_commands(TEXIOTY_COMMANDS,{
            'welcome': {
                'call_func':self.welcome_message,
                'possible_args': {},
                'args_desc': {}
            },
            'commands': {
                'call_func':self.display_all_available_commands,
                'possible_args': {},
                'args_desc': {}
            },
            'help': {
                'call_func':self.display_help_message,
                'possible_args': {
                    '(GROUP_TAG)': self.txo.master.active_helpers,
                    '(COMMAND_NAME)': self.txo.master.command_registry.commands,
                },
                'args_desc': {}
            },
        })

    def priont_block_font(self, blk_word: str):
        top_line = ''
        mid_line = ''
        bot_line = ''
        for letter in blk_word:
            top_line += " " + BLOCK_CHAR_DICT[letter.lower()][0] + " "
            mid_line += " " + BLOCK_CHAR_DICT[letter.lower()][1] + " "
            bot_line += " " + BLOCK_CHAR_DICT[letter.lower()][2] + " "
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
        self.txo.priont_string('')
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

        grouped_commands = {}
        for command_name, command_info in available_commands.items():
            grouped_commands.setdefault(command_info.group_tag, []).append(command_name)

        for helper_group in sorted(grouped_commands):
            self.txo.helper_tag_break(helper_group)
            for command_name in sorted(grouped_commands[helper_group]):
                self.txo.priont_command_lite(available_commands[command_name])

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
