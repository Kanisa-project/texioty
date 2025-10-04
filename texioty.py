import json
import tkinter as tk
from dataclasses import dataclass
from typing import Dict, Any

from helpers.digiary import Digiary
from helpers.gaim_registry import GaimRegistry
import settings as s
import theme as t
from helpers.prompt_runner import PromptRunner
from helpers.tex_helper import TexiotyHelper
import texoty
import texity

@dataclass
class CommandRegistry:
    """
    A registry for custom commands for use within Texioty.
    """
    commands: Dict[str, texity.Command]

    def remove_commands(self, help_symb: str):
        """
        Remove a command from the registry.
        """
        pass

    def add_command(self, name: str, handler: Any, msg: str, p_args: Any, help_symb: Any,
                    t_color: str, b_color: str) -> None:
        """
        Add a new command that Texity will recognize and Texoty can display.
        :param name: Name of the command, also the command itself.
        :param handler: Defined function for execution.
        :param msg: A message of helping for the help display.
        :param p_args: Possible arguments for Texity.
        :param help_symb: Symbol of helper that contains this command.
        :param t_color: Text color for help display.
        :param b_color: Background color for help display.
        :return:
        """
        self.commands[name] = texity.Command(name=name,
                                             handler=handler,
                                             help_message=msg,
                                             possible_args=p_args,
                                             helper_symbol=help_symb,
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
            # print(command.handler)
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
        self.registry = CommandRegistry({})

        self.active_helpers = ['TXTY', 'HLPR', 'DIRY', 'GAIM', 'PRUN']
        self.available_profiles = s.available_profiles
        self.active_profile = self.available_profiles["guest"]

        self.texoty = texoty.TEXOTY(int(width) + 16, int(height), master=self)
        self.texoty.grid(column=0, row=0)
        self.texity = texity.TEXITY(width=int(width // 6), master=self)
        self.texity.grid(column=0, row=1)

        self.texity.focus_set()
        self.texity.bind('<KP_Enter>', lambda e: self.process_texity())
        self.texity.bind('<Return>', lambda e: self.process_texity())

        self.base_helper = TexiotyHelper(self.texoty, self.texity)
        self.digiary = Digiary(self.texoty, self.texity)
        self.gaim_registry = GaimRegistry(self.texoty, self.texity)
        self.prompt_runner = PromptRunner(self.texoty, self.texity)
        self.default_helpers = {"TXTY": [self],
                                "HLPR": [self.base_helper],
                                "DIRY": [self.digiary],
                                "GAIM": [self.gaim_registry],
                                "PRUN": [self.prompt_runner]}
        self.active_helper_dict = self.default_helpers

        self.known_commands_dict = {
            "login": [self.log_profile_in, "This logs the user into a profile. ",
                      self.available_profiles, "TXTY", s.rgb_to_hex(t.DIM_GREY), s.rgb_to_hex(t.BLACK)],
            "exit": [self.close_program, "Exits Texioty.",
                     {}, "TXTY", s.rgb_to_hex(t.PURPLE), s.rgb_to_hex(t.BLACK)],
        }
        self.helper_commands = self.active_helper_dict["HLPR"][0].helper_commands|self.known_commands_dict
        self.active_helper_dict['HLPR'][0].welcome_message([])
        self.add_command_dict(self.known_commands_dict)

    def add_command_dict(self, command_dict: dict):
        """
        Add another dictionary of commands to the registry for Texioty to use.
        :param command_dict: Dictionary of commands to add to registry.
        :return:
        """
        for command in command_dict:
            # print(command, command_dict[command])
            if command_dict[command][3] not in self.active_helpers:
                self.active_helpers.append(command_dict[command][3])
            self.registry.add_command(name=command,
                                      handler=command_dict[command][0],
                                      msg=command_dict[command][1],
                                      p_args=command_dict[command][2],
                                      help_symb=command_dict[command][3],
                                      t_color=command_dict[command][4],
                                      b_color=command_dict[command][5])
            self.texoty.tag_config(f'{command}',
                                   background=f'{command_dict[command][5]}', foreground=f'{command_dict[command][4]}')

    def remove_commands(self):
        self.registry.commands = {}
        self.active_helpers = []

    def change_current_mode(self, new_mode: str, new_commands: dict):
        self.current_mode = new_mode
        # print('old_commands: ', self.registry.commands)
        self.remove_commands()
        self.add_command_dict(new_commands)
#         print('new_commands: ', self.registry.commands)

    def default_mode(self):
        self.current_mode = "Texioty"
        self.remove_commands()
        for key, helper in self.default_helpers.items():
            self.add_helper_widget(key, helper[0])


    def close_program(self, args):
        """
        Literally just close the whole application.
        :param args:
        :return:
        """
        self.master.destroy()

    def add_helper_widget(self, helper_symbol: str, helper_widget):
        """
        Add a helper widget and all of its commands to texioty while supplying access to texoty.
        :param helper_symbol: Symbol of helper (e.g. TXTY GAIM DIRY)
        :param helper_widget:
        :return:
        """
        # helper_widget.txo = self.texoty
        if len(helper_widget.helper_commands) > 0:
            self.add_command_dict(helper_widget.helper_commands)
        self.active_helper_dict[helper_symbol] = [helper_widget]

    def clear_texoty(self):
        """Clear all the text from texoty and replace the header."""
        self.texoty.delete("0.0", tk.END)
        self.texoty.set_header()

    def process_texity(self, event=None):
        """
        Process the command before executing it. Decide which helpers to use or if just a regular command.
        :return:
        """
        prefix = ''
        match self.current_mode:
            case "Texioty":
                parsed_input = self.texity.parse_input_command()
                if not parsed_input:
                    return
                command = parsed_input[0]
                arguments = parsed_input[1:]
                self.execute_command(command, arguments)
            case "Diary":
                if self.texity.parse_diary_line() != "/until_next_time":
                    parsed_input = self.texity.parse_diary_line()
                    self.active_helper_dict["DIRY"][0].add_diary_line(parsed_input)
                else:
                    self.execute_command("/until_next_time", [])
            case "Questionnaire":
                parsed_input = self.texity.parse_question_response()
                self.active_helper_dict["PRUN"][0].store_response(parsed_input)
            case "Gaim":
                parsed_input_list = self.texity.parse_gaim_command()
                helper_gaim_cmds = self.active_helper_dict["GAIM"][0].current_gaim.gaim_commands|self.active_helper_dict["GAIM"][0].current_gaim.helper_commands
                print(list(helper_gaim_cmds.keys()))
                if parsed_input_list[0] in list(helper_gaim_cmds.keys()):
                    # self.texoty.priont_string(f"Found {parsed_input_list[0]}")
                    self.execute_command(parsed_input_list[0], parsed_input_list[1:])
                if self.active_helper_dict["GAIM"][0].current_gaim:
                    prefix = self.active_helper_dict["GAIM"][0].current_gaim.gaim_prefix
        self.texity.command_string_var.set(prefix)

    def execute_gaim_command(self, command, arguments):
        pass

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
        else:
            self.texoty.priont_string(f"⦓⦙ Uhh, I don't recognize '{command}'")
            # self.texoty.priont_string(f"⦓⦙ Uhh, I don't recognize '{command}'. Try one of these instead:")
            # self.display_help_message(arguments)
        self.texity.full_command_list.append(self.texity.command_string_var.get())
        if self.current_mode == "Texioty":
            self.texoty.priont_string(s.random_loading_phrase())

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
                self.active_helper_dict['PRUN'][0].prompt_texioty_profile()
        except IndexError:
            self.texoty.priont_string("⦓⦙ What username to login to?")

    def log_profile_out(self, args):
        if self.active_profile:
            #TODO Save each used command for the profile
            self.texoty.priont_string(f"Logging {self.active_profile.username} out. Goodbye!")
            self.active_profile = self.available_profiles["guest"]
            self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                         self.active_profile.color_theme[1],
                                         16,
                                         self.active_profile.color_theme[2])
        else:
            self.texoty.priont_string("You have to log in before you can log out.")

    def create_profile(self, args):
        """Create a new profile."""
        if "yes" in args:
            self.texoty.priont_string("Creating a new profile...")
            profile_name = self.active_helper_dict["PRUN"][0].question_prompt_dict['profile_name'][1]
            password = self.active_helper_dict["PRUN"][0].question_prompt_dict['password'][1]
            color_theme = self.active_helper_dict["PRUN"][0].question_prompt_dict['color_theme'][1]
            color_theme = t.DEFAULT_THEMES[color_theme]
            self.available_profiles[profile_name] = s.TexiotyProfile(profile_name, password, color_theme)
            save_path = f".profiles/{profile_name}.json"
            print(save_path)
            with open(save_path, 'w') as f:
                f.write(json.dumps({"texioty": self.available_profiles[profile_name].__dict__}, indent=4, sort_keys=True,
                                   default=lambda o: o.__dict__, ensure_ascii=False))
            self.texoty.priont_string(f"Profile '{profile_name}' created.")
