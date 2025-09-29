import datetime
import random
from tkinter import END
import settings as s
import theme as t
import texity
import texoty

class TexiotyHelper:
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        self.txo = txo
        self.txi = txi
        self.helper_commands = {
            "welcome": [self.welcome_message, "Displays a welcoming message.",
                     {}, "HLPR", s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
            "help": [self.display_help_message, "Displays a message of helpfulness.",
                     {}, "HLPR", s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
            "commands": [self.display_available_commands, "Displays all available commands.",
                         {}, "HLPR", s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
        }


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

    def display_available_commands(self, args):
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
        self.txo.priont_string(
            f"⦓⦙ Welcome to Texioty! THis is from the helper widget.")
        for msg in welcoming_msgs:
            self.txo.priont_string("⦓⦙ " + msg)
        self.txo.priont_string("\n")
