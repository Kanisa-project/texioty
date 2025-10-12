import tkinter as tk
from dataclasses import dataclass
from typing import Any


@dataclass
class Command:
    name: str
    handler: Any
    help_message: str
    possible_args: dict
    helper_symbol: str
    text_color: str
    bg_color: str


class TEXITY(tk.Entry):
    def __init__(self, width, master=None):
        """
        Text input for Texioty, it can accept commands and different types of entries.
        """
        self.full_command_list = []
        self.kom_index = 0
        self.command_string_var = tk.StringVar()
        self.isTestingKeys = False
        self.isInPrompt = False
        self.isDecidingDecision = False
        self.current_possible_options = []
        self.current_option_bindings = []
        self.master = master
        super(TEXITY, self).__init__(master=master, background=master.active_profile.color_theme[1], width=width-5,
                                     textvariable=self.command_string_var)
        self.bind('<Up>', lambda e: self.command_list_previous())
        self.bind('<Down>', lambda e: self.command_list_next())

    def no_options(self):
        for i, option in enumerate(self.current_possible_options):
            self.unbind(str(i))
            self.unbind(f"<KP_{i}>")

    def bind_new_options(self, new_options: list):
        """Bind each number to a possible option."""
        self.current_possible_options = new_options
        for i, option in enumerate(new_options):
            self.current_option_bindings.append(self.bind(str(i), lambda e, option=option: self.command_string_var.set(f" - {option}")))
            self.current_option_bindings.append(self.bind(f"<KP_{i}>", lambda e, option=option: self.command_string_var.set(f" - {option}")))

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

    def parse_decision(self):
        decision = self.command_string_var.get().split(" - ")[-1]
        self.master.default_mode()
        return decision

    def parse_gaim_command(self) -> str|list:
        list_input = self.command_string_var.get().split()
        if list_input[0] in ['new', 'load', 'save', 'stop']:
            return list_input[0]
        return list_input

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



def clamp(n, minn, maxn) -> int:
    return max(min(maxn, n), minn)
