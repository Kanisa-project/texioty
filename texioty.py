import datetime
import json
import os
import random
import logging
import sys
import tkinter as tk
from dataclasses import dataclass
from os.path import exists
from typing import Dict, Any

import prompt_runner as pRunner
import settings as s
import texoty
import texity

@dataclass
class CommandRegistry:
    """
    A registry for custom commands for use within Texioty.
    """
    commands: Dict[str, texity.Command]

    def add_command(self, name: str, handler: Any, msg: str, p_args: Any, e_args: Any,
                    t_color: str, b_color: str) -> None:
        """
        Add a new command that Texity will recognize and Texoty can display.
        :param name: Name of the command, also the command itself.
        :param handler: Defined function for execution.
        :param msg: A message of helping for the help display.
        :param p_args: Possible arguments for Texity.
        :param e_args: Exact arguments for Texity to use.
        :param t_color: Text color for help display.
        :param b_color: Background color for help display.
        :return:
        """
        self.commands[name] = texity.Command(name=name,
                                             handler=handler,
                                             help_message=msg,
                                             possible_args=p_args,
                                             executed_args=e_args,
                                             text_color=t_color,
                                             bg_color=b_color)

    def execute_command(self, name: str, args: tuple) -> None:
        """
        Executes the command being used in Texity.
        :param name: Name of the command being executed.
        :param args: Arguments to be used in the command execution.
        :return:
        """
        command = self.commands.get(name)
        if command:
            print(command.handler)
            command.handler(args)
        else:
            print(f"Command '{name}' not found.")


class Texioty(tk.LabelFrame):
    def __init__(self, width, height, master=None):
        """
        Textual input from Texity, such as commands and other necessary inputs. Textual output from Texoty, such as help display
        and confirmation prompting.

        :param width: Width of the Texioty Widget frame.
        :param height: Height of the Texioty Widget frame.
        :param master: Parent widget
        """
        super(Texioty, self).__init__(master)
        self.current_mode = "Texioty"
        self.in_play_gaim_mode = False
        self.configure(text="Texioty:  ")

        # INITIATE DIARY VARIABLES
        self.diary_line_length = 75
        self.diarySentenceList = []
        self.in_diary_mode = False

        self.registry = CommandRegistry({})

        self.helper_dict = {}
        self.available_profiles = s.available_profiles
        self.active_profile = self.available_profiles["bluebeard"]

        self.texoty = texoty.TEXOTY(int(width) + 16, int(height), master=self)
        self.texoty.grid(column=0, row=0)
        self.texity = texity.TEXITY(width=int(width // 6), master=self)
        self.texity.grid(column=0, row=1)
        self.texo_w = self.texoty.texoty_w
        self.in_questionnaire_mode = False

        self.texity.focus_set()
        self.texity.bind('<KP_Enter>', lambda e: self.process_command())
        self.texity.bind('<Return>', lambda e: self.process_command())

        # Set up basic commands for Texioty to know automatically.
        self.known_commands_dict = {
            "help": [self.display_help_message, "Displays a message of hope and help.",
                     {}, [], s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "exit": [self.close_program, "Exits the program.",
                     {}, [], s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "commands": [self.display_available_commands, "Displays all available commands.",
                         {}, [], s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "login": [self.log_profile_in, "This logs the user into a profile: ",
                      {'guest': "Basic account with a few permissions."}, [], s.rgb_to_hex(s.LIGHT_GREEN),
                      s.rgb_to_hex(s.BLACK)],
            "logout": [self.log_profile_out, "This logs the user out of a profile.",
                       {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "depict": [self.draw_depiction, "Draw a depiction of something.",
                       {"mtg": "Depict a Magic The Gathering spell."}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            # "dear_sys,": [self.start_diary_mode, "Creates a new .diary/ entry.",
            #               {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            # "/until_next_time": [self.stop_diary_mode, "Ends and saves the .diary/ entry.",
            #                      {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            # "echo": [self.handle_errors, "Echo some errors.",
            #          {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "quit": [self.quit_gaim, "Quit any gaim you might be playing.",
                     {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            # "add_recipe": [self.prepare_new_recipe, "Add a new recipe.",
            #                {}, [], s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)]

        }

        # Add the basic commands for Texioty.
        self.all_commands = {}
        self.add_command_dict(self.known_commands_dict)

    def add_command_dict(self, command_dict: dict):
        """
        Add another dictionary of commands to the registry for Texioty to use.
        :param command_dict: Dictionary of commands to add to registry.
        :return:
        """
        for command in command_dict:
            self.registry.add_command(name=command,
                                      handler=command_dict[command][0],
                                      msg=command_dict[command][1],
                                      p_args=command_dict[command][2],
                                      e_args=command_dict[command][3],
                                      t_color=command_dict[command][4],
                                      b_color=command_dict[command][5])
            self.texoty.tag_config(f'{command}',
                                   background=f'{command_dict[command][5]}', foreground=f'{command_dict[command][4]}')

    def close_program(self, args):
        """
        Literally just close the whole application.
        :param args:
        :return:
        """
        self.master.destroy()
        
    def draw_depiction(self, args):
        if "mtg" in args:
            pass

    def add_helper_widget(self, helper_type: str, helper_widget: tk.Widget):
        """
        Add a helper widget and all of its commands to texioty while supplying access to texoty.
        :param helper_type: Type of helper (e.g. Database/API/Other)
        :param helper_widget:
        :return:
        """
        helper_widget.txo = self.texoty
        if len(helper_widget.texioty_commands) > 0:
            self.add_command_dict(helper_widget.texioty_commands)
        self.helper_dict[helper_type] = [helper_widget]

    def display_helper_widgets(self, args):
        """
        Displays any helper widgets that have been added to texioty.
        :param args:
        :return:
        """
        for key, value in self.helper_dict.items():
            self.texoty.priont_list(items=value, list_key=key)
            self.texoty.priont_break_line()

    def display_help_message(self, args):
        """
        Print the available commands for use with a header added to the top.
        :param args:
        :return:
        """
        self.texoty.clear_add_header()
        if self.active_profile:
            self.texoty.priont_string('\n⦓PROFILE⦙ ' + self.active_profile.username)
        self.texoty.priont_string("⦓⦙ Seems like you might need help, good luck!")
        self.texoty.priont_string("   Anything that can be done in this program can be")
        self.texoty.priont_string("   done through this Texioty widget.")
        self.texoty.priont_string("⦓⦙ Here are a couple of easy commands to get you started: \n\n")
        self.texoty.priont_command(self.registry.commands["help"])
        self.texoty.priont_command(self.registry.commands["commands"])

    def display_available_commands(self, args):
        """Prints out all the commands that are available."""
        self.clear_texoty()
        command_index = 2
        for command in self.registry.commands:
            self.texoty.priont_command(self.registry.commands[command])
            command_index += 1

    def perform_echo(self, eko_msg=""):
        """Prints whatever is typed after 'echo'."""
        self.texoty.clear_no_header()
        # self.texoty.priont_int("", len(colors_list))
        for msg in eko_msg:
            self.texoty.priont_echo(msg, text_color=s.rgb_to_hex(s.BLACK),
                                    bg_color=s.rgb_to_hex(s.RANDOM_COLOR3))

    def clear_texoty(self):
        """Clear all the text from texoty and replace the header."""
        self.texoty.delete("0.0", tk.END)
        self.texoty.set_header()

    def process_command(self, event=None):
        """
        Process the command before executing it. Decide which helpers to use or if just a regular command.
        :return:
        """
        if self.in_questionnaire_mode:
            parsed_input = self.texity.parse_question_response()
            self.store_response(parsed_input)
        elif self.in_play_gaim_mode and self.texity.parse_gaim_play() != "quit":
            parsed_input = self.texity.parse_gaim_play()
            self.execute_gaim_play(parsed_input)
        elif self.in_diary_mode and self.texity.parse_diary_line() != "/until_next_time":
            parsed_input = self.texity.parse_diary_line()
            self.add_diary_line(parsed_input)
        else:
            parsed_input = self.texity.parse_input_command()
            command = parsed_input[0]
            arguments = parsed_input[1:]
            self.execute_command(command, arguments)
        if self.in_play_gaim_mode and self.gaim_player.loaded_gaim == "Hangman":
            self.texity.command_string_var.set("guess ")
        elif self.in_play_gaim_mode and self.gaim_player.loaded_gaim == "Blackjack":
            self.texity.command_string_var.set("blackjack ")
        else:
            self.texity.command_string_var.set("")

    def execute_command(self, command, arguments):
        """
        Execute the processed command, then add it to the list of processed commands.
        :param command: The command to be using.
        :param arguments: Arguments for the command to use.
        :return:
        """
        # self.clear_texoty()
        if command in self.registry.commands:
            try:
                self.registry.execute_command(command, arguments)
            except PermissionError as e:
                self.texoty.priont_string("Sorry dude, you ain't got hangman.")
                self.texoty.priont_string(str(e))
            except KeyError as e:
                self.texoty.priont_string(f"Missing the {e} key or something.")
                self.texoty.priont_list(list(e.args))

            if "play" in command:
                self.in_play_gaim_mode = self.gaim_player.inGaim
        else:
            self.texoty.priont_string(f"⦓⦙ Uhh, I don't recognize '{command}'")
            # self.texoty.priont_string(f"⦓⦙ Uhh, I don't recognize '{command}'. Try one of these instead:")
            # self.display_help_message(arguments)
        self.texity.full_command_list.append(self.texity.command_string_var.get())
        if self.in_play_gaim_mode or self.in_questionnaire_mode:
            pass
        else:
            self.texoty.priont_string("⦓⦙ " + s.random_loading_phrase())

    def log_profile_in(self, args):
        """Check args[0] for a username and args[1] for a password. Logs in a profile if a match."""
        try:
            if args[0] in self.available_profiles:
                try:
                    if args[1] == self.available_profiles[args[0]].password:
                        self.texoty.priont_string(f"⦓⦙ Welcome, {args[0]}!")
                        self.active_profile = self.available_profiles[args[0]]
                        self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                                     self.active_profile.color_theme[1],
                                                     16,
                                                     self.active_profile.color_theme[2])
                    else:
                        self.texoty.priont_string(f"⦓⦙ Wrong password, buster.")
                except IndexError:
                    self.texoty.priont_string(f"⦓⦙ Don't forget to type a password.")
            else:
                self.texoty.priont_string(f"⦓⦙ I don't recognize '{args[0]}' as profile username.")
        except IndexError:
            self.texoty.priont_string("⦓⦙ What username to login to?")

    def log_profile_out(self, args):
        if self.active_profile:
            self.texoty.priont_string(f"Logging {self.active_profile.username} out. Goodbye!")
            self.active_profile = self.available_profiles["guest"]
            self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                         self.active_profile.color_theme[1],
                                         16,
                                         self.active_profile.color_theme[2])
        else:
            self.texoty.priont_string("You have to log in before you can log out.")

    def start_diary_mode(self, args) -> datetime:
        """Start a diary entry."""
        start_now = datetime.datetime.now()
        self.in_diary_mode = True
        self.texoty.priont_string(f"-Entering diary mode-   {start_now}")
        opening_line = timestamp_line_entry(start_now, 'dear_sys,', lead_line='ts',
                                            follow_line=' ' * (self.diary_line_length - len('dear_sys,')))
        self.diarySentenceList = [opening_line]
        return start_now

    def add_diary_line(self, new_line):
        self.texoty.priont_string(f'  [+{"".join(random.sample(new_line, len(new_line)))}')
        self.diarySentenceList.append(timestamp_line_entry(datetime.datetime.now(), new_line, lead_line='  ',
                                                           follow_line='_' * (self.diary_line_length - len(
                                                               new_line) - 2)))

    def stop_diary_mode(self, args) -> datetime:
        """Stop a diary entry."""
        end_now = datetime.datetime.now()
        self.in_diary_mode = False
        self.texoty.priont_string(f"-Exiting diary mode-   {end_now}")
        ending_line = timestamp_line_entry(end_now, '/until_next_time', lead_line='ts',
                                           follow_line=' ' * (self.diary_line_length - len('/until_next_time')))
        self.diarySentenceList.append(ending_line)
        create_date_entry(end_now, self.diarySentenceList)
        return end_now

    def get_responses(self):
        self.texoty.priont_dict(self.question_prompt_dict)

    def handle_errors(self, error_message: str, severity="INFO"):
        text_color = s.BLACK
        if severity == "ERROR":
            text_color = s.ORANGE_RED
        self.texoty.priont_string(f"⦓⦙ {severity}: {error_message}")

    def execute_gaim_play(self, parsed_input):
        gaim_command = parsed_input.split()[0]
        gaim_args = parsed_input.split()[1]
        # print(gaim_command, gaim_args)
        if gaim_command == "guess":
            self.texoty.priont_string(f"execute gaimplay: {parsed_input}")
            self.registry.execute_command(gaim_command, gaim_args)
        if "hit" in gaim_args or "stay" in gaim_args:
            self.texoty.priont_string(f"execute gaimplay: {parsed_input}")
            self.registry.execute_command(gaim_command, gaim_args)

    def quit_gaim(self, args):
        self.texoty.priont_string("Quitting...")
        self.in_play_gaim_mode = False


def create_date_entry(entry_time: datetime, entry_list: list):
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


def timestamp_line_entry(entry_time: datetime, entry_line: str, lead_line=" ", follow_line=" ") -> str:
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
