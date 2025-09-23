import tkinter as tk
from dataclasses import dataclass
from typing import Any


@dataclass
class Command:
    name: str
    handler: Any
    help_message: str
    possible_args: dict
    executed_args: tuple
    text_color: str
    bg_color: str


class TEXITY(tk.Entry):
    def __init__(self, width, master=None):
        """
        Text input for Texioty, it can accept commands and different types of entries.
        """
        # Set up the command list/cycling and different entry modes.
        self.full_command_list = []
        self.kom_index = 0
        self.command_string_var = tk.StringVar()
        self.isTestingKeys = False
        self.isInPrompt = False
        super(TEXITY, self).__init__(master=master, background=master.active_profile.color_theme[1], width=width-5,
                                     textvariable=self.command_string_var)
        # Bind the up and down arrow keys to cycle through the used command list.
        self.bind('<Up>', lambda e: self.command_list_previous())
        self.bind('<Down>', lambda e: self.command_list_next())

    def parse_input_command(self) -> list:
        """
        Returns a list of command arguments.
        :return: command argument list
        """
        text_input = self.command_string_var.get().strip()
        # Simply splits Texity input by spaces.
        return text_input.split() if text_input else []

    def parse_diary_line(self) -> str:
        text_input = self.command_string_var.get()
        return text_input

    def parse_question_response(self) -> str:
        """
        Returns the questions response as a string, including the entire Texity input.
        :return: entire string from Texity
        """
        text_input = self.command_string_var.get().split("›")[-1]
        return text_input

    def parse_gaim_play(self) -> str:
        text_input = self.command_string_var.get()
        return text_input

    def command_list_previous(self):
        """Changes the input box to the previous command in the list."""
        if self.command_string_var.get() == '':
            self.kom_index = 0
        if self.kom_index <= len(self.full_command_list) - 1:
            self.kom_index += 1
            # Unsure why final_kom is needed, Texity command cycling works pretty well though.
            final_kom = clamp(len(self.full_command_list) - self.kom_index, 0, len(self.full_command_list) - 1)
            self.command_string_var.set(self.full_command_list[final_kom])
        self.icursor(tk.END)

    def command_list_next(self):
        """Changes the input box to the next command in the list."""
        if self.kom_index >= 1:
            self.kom_index -= 1
            # Unsure why final_kom is needed, Texity command cycling works pretty well though.
            final_kom = clamp(len(self.full_command_list) - self.kom_index, 0, len(self.full_command_list) - 1)
            self.command_string_var.set(self.full_command_list[final_kom])
        if self.kom_index == 0:
            self.command_string_var.set('')
        self.icursor(tk.END)

    def respond_to_prompt(self):
        pass


def clamp(n, minn, maxn) -> int:
    return max(min(maxn, n), minn)
