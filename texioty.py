import json
import os.path
import random
import tkinter as tk
# from dataclasses import dataclass
from typing import Callable
# import inspect
from helpers.digiary import Digiary
from helpers.registries.command_registry import CommandRegistry
from helpers.tex_helper import TexiotyHelper
# from helpers.registries.gaim_registry import GaimRegistry
from settings import utils as u
# from helpers.registries.prompt_registry import PromptRegistry
# from helpers.tex_helper import TexiotyHelper
from settings import themery as t, konfig as k

import texoty
import texity

# @dataclass
# class CommandRegistry:
#     """
#     A registry for custom commands for use within Texioty.
#     """
#     commands: Dict[str, texity.Command]
#
#     def remove_commands(self, help_symb: str):
#         """
#         Remove a command from the registry.
#         """
#         if help_symb in self.commands:
#             del self.commands[help_symb]
#             return
#
#         to_delete = [name for name, cmd in self.commands.items() if getattr(cmd, "group_tag", None) == help_symb]
#         for name in to_delete:
#             del self.commands[name]
#
#     def add_command_dict(self, command_info: Dict[str, Any]):
#         try:
#             self.commands[command_info["name"]] = texity.Command(name=command_info["name"],
#                                                                  usage=command_info["usage"],
#                                                                  handler=command_info["call_func"],
#                                                                  lite_desc=command_info["lite_desc"],
#                                                                  full_desc=command_info["full_desc"],
#                                                                  possible_args=command_info["possible_args"],
#                                                                  args_desc=command_info["args_desc"],
#                                                                  examples=command_info["examples"],
#                                                                  group_tag=command_info["group_tag"],
#                                                                  font_color=command_info["font_color"],
#                                                                  back_color=command_info["back_color"])
#             print(command_info["name"], "added to registry.")
#         except KeyError as e:
#             print(f"Missing key in command dictionary: {e}")
#
#
#
#     def execute_command(self, name: str, exec_args: tuple) -> None:
#         """
#         Executes the command being used in Texity.
#         :param name: Name of the command being executed.
#         :param exec_args: Arguments to be used in the command execution.
#         :return:
#         """
#         command = self.commands.get(name)
#         if not command:
#             print(f"Command '{name}' not found.")
#             return
#
#         cmd_handler = command.handler
#         print("Inspecting", name, inspect.getfullargspec(cmd_handler).annotations)
#         try:
#             if len(inspect.getfullargspec(cmd_handler).args) == 1:
#                 cmd_handler()
#             else:
#                 cmd_handler(*exec_args)
#         except Exception as e:
#             print(f"Error executing '{name}': {e}", exec_args)


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

        self.active_helpers = k.UNLOCKED_HELPERS
        self.available_profiles = u.available_profiles
        self.active_profile = self.available_profiles[k.ACTIVE_PROFILE_USERNAME]

        self.texoty = texoty.TEXOTY(int(width*k.TEXOTY_W_MODIFIER),
                                    int(height*k.TEXOTY_H_MODIFIER), master=self)
        # self.texoty = texoty.TEXOTY(int(width) + 16, int(height), master=self)
        self.texoty.grid(column=0, row=0, columnspan=1)
        self.texity = texity.TEXITY(width=int(width*k.TEXITY_W_MODIFIER), master=self)
        # self.texity = texity.TEXITY(width=int(width // 6), master=self)
        self.texity.grid(column=0, row=1, columnspan=1)

        self.texity.focus_set()
        self.texity.bind('<KP_Enter>', lambda e: self.process_texity())
        self.texity.bind('<Return>', lambda e: self.process_texity())

        self.digiary = Digiary(self.texoty, self.texity)
        self.base_helper = TexiotyHelper(self.texoty, self.texity)
        self.default_helpers = {"TXTY": [self],
                                "HLPR": [self.base_helper],
                                "DIRY": [self.digiary]}
        self.active_helper_dict = self.default_helpers
        self.deciding_function = None


        self.helper_commands_dict = {
            "login": {
                'name': 'login',
                'usage': '"login [PROFILE_NAME] [PROFILE_PASSWORD]"',
                'call_func': self.log_profile_in,
                'lite_desc': "Logs the user into a profile. ",
                'full_desc': ['Logs a user into the system with a Texioty profile.',
                              'Can only be performed in Texioty mode.'],
                'possible_args': self.available_profiles,
                'args_desc': {'[PROFILE_NAME]': ['The name of the profile to log in with.', str],
                              '[PROFILE_PASSWORD]': ['The password of the profile to log in with.', str]},
                'examples': ['login trevor 8716', 'login bluebeard p455'],
                'group_tag': 'TXTY',
                'font_color': u.rgb_to_hex(t.PURPLE),
                'back_color': u.rgb_to_hex(t.BLACK)},
            "exit": {
                'name': 'exit',
                'usage': '"exit"',
                'call_func': self.close_program,
                'lite_desc': "Exits Texioty.",
                'full_desc': ['Exits Texioty.'],
                'possible_args':{' - ': 'No arguments available.'},
                'args_desc': {' - ': ['No arguments available.', None]},
                'examples': ['exit'],
                'group_tag': "TXTY",
                'font_color': u.rgb_to_hex(t.PURPLE),
                'back_color': u.rgb_to_hex(t.BLACK)},
            "test_tags": {
                'name': 'test_tags',
                'usage': '"test_tags"',
                'call_func': self.priont_test_tags,
                'lite_desc': "Prints some tags for testing.",
                'full_desc': ['Prints some tags for testing.'],
                'possible_args':{' - ': 'No arguments available.'},
                'args_desc': {' - ': ['No arguments available.', None]},
                'examples': ['test_tags'],
                'group_tag': "TXTY",
                'font_color': u.rgb_to_hex(t.PURPLE),
                'back_color': u.rgb_to_hex(t.BLACK)},
            "konfig": {
                'name': 'konfig',
                'usage': '"konfig"',
                'call_func': self.priont_test,
                'lite_desc': "Prints some tags for testing.",
                'full_desc': ['Prints some tags for testing.'],
                'possible_args':{' - ': 'No arguments available.'},
                'args_desc': {' - ': ['No arguments available.', None]},
                'examples': ['konfig'],
                'group_tag': "TXTY",
                'font_color': u.rgb_to_hex(t.PURPLE),
                'back_color': u.rgb_to_hex(t.BLACK)}
        }
        # self.helper_commands = self.active_helper_dict["HLPR"][0].helper_commands|self.known_commands_dict
        # self.active_helper_dict['HLPR'][0].welcome_message()
        self.add_command_group(self.helper_commands_dict)

    def display_konfig_settings(self):
        pass

    def priont_test_tags(self):
        self.texoty.clear_add_header("Testing tags")
        listed_test_str = [
            "_"*75,
            "="*75,
            "▒"*75,
            "T"*75,
            "@"*75
        ]
        for i, test_str in enumerate(listed_test_str):
            self.texoty.priont_string(test_str)
        for i, test_str in enumerate(listed_test_str):
            rand_colo = u.rgb_to_hex(random.choice(t.RANDOM_COLORS))
            rand_colo2 = u.rgb_to_hex(random.choice([t.BLACK, t.WHITE, t.GREY25]))
            x_start = random.randint(0, 59)
            self.texoty.tag_area(rand_colo, rand_colo2, f'{i}.{x_start}', f'{i}.{x_start+(5*i)}')
            # self.texoty.priont_colorized_string(test_str,
            #                                     u.rgb_to_hex(rand_colo), u.rgb_to_hex(rand_colo2),
            #                                     f'1.0', f'1.3')
                                            # f'{random.randint(0, 2)}.{random.randint(0, 6)}',
                                            # f'{random.randint(0, 6)}.{random.randint(0, 6)}')

    def add_command_group(self, group_of_cmds: dict):
        # print(group_of_cmds)
        for command in group_of_cmds:
            # print("COM", command)
            self.registry.add_command_dict(group_of_cmds[command])

    def remove_commands(self):
        self.registry.commands = {}
        self.active_helpers = k.UNLOCKED_HELPERS

    def change_current_mode(self, new_mode: str, new_commands: dict):
        """
        Properly sets a new mode for Texioty. Current valid options are:
        Gaim, Diary, Texioty, Questionnaire, and Decisioning
        """
        self.current_mode = new_mode
        self.remove_commands()
        self.add_command_group(new_commands)

    def default_mode(self):
        """
        Resets the mode back to Texioty and applies default helpers.
        """
        self.current_mode = "Texioty"
        self.texity.no_options()
        self.remove_commands()
        self.add_command_group(self.helper_commands_dict)
        for key, helper in self.default_helpers.items():
            # print(key, helper)
            self.add_helper_widget(key, helper[0])

    def close_program(self):
        """
        Literally just close the whole application.
        :param args:
        :return:
        """
        self.master.quit()

    def add_helper_widget(self, group_tag: str, helper_widget):
        """
        Add a helper widget and all of its commands to texioty while supplying access to texoty.
        :param group_tag: Symbol of helper (e.g. TXTY GAIM DIRY)
        :param helper_widget:
        :return:
        """
        # helper_widget.txo = self.texoty
        try:
            if len(helper_widget.helper_commands) > 0:
                self.add_command_group(helper_widget.helper_commands)
        except AttributeError:
            # print(f"No helper_commands found for {group_tag}.")
            pass
        self.active_helper_dict[group_tag] = [helper_widget]

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
                print("TXTY:", parsed_input)
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
                self.active_helper_dict["PRUN"][0].profilemake.store_response(parsed_input)

            case "Decisioning":
                parsed_input = self.texity.parse_decision()
                print("DECISIONED:", parsed_input, self.deciding_function)
                if isinstance(self.deciding_function, Callable):
                    self.deciding_function(parsed_input)
                    # self.deciding_function = None
                else:
                    self.texoty.priont_string(f"Deciding function not set. {self.deciding_function}")

            case "Gaim":
                parsed_input = self.texity.parse_gaim_command()
                print("GAIM:", parsed_input)
                if isinstance(parsed_input, str):
                    self.execute_command(parsed_input, [])
                else:
                    self.execute_command(parsed_input[0], parsed_input[1:])

                if self.active_helper_dict["GAIM"][0].current_gaim:
                    prefix = self.active_helper_dict["GAIM"][0].current_gaim.gaim_prefix
        self.texity.command_string_var.set(prefix)

    def set_texity_input(self, new_input):
        self.texity.command_string_var.set(new_input)
        self.texity.focus_set()

    def execute_command(self, command, arguments):
        """
        Execute the processed command, then add it to the list of processed commands.
        :param command: The command to be using.
        :param arguments: Arguments for the command to use.
        :return:
        """
        # self.clear_texoty()
        # print("cmd args", command, arguments)
        if command in self.registry.commands:
            try:
                self.registry.execute_command(command, arguments)
            except PermissionError as e:
                self.texoty.priont_string(str(e))
            except KeyError as e:
                self.texoty.priont_string(f"Missing the {e} key or something.")
                self.texoty.priont_list(list(e.args))
        else:
            self.texoty.priont_string(f"⦙⦓ Uhh, I don't recognize '{command}'")
        self.texity.full_command_list.append(self.texity.command_string_var.get())
        if self.current_mode == "Texioty":
            self.texoty.priont_string(u.random_loading_phrase())

    def log_profile_in(self, prof_name: str, prof_pass: str):
        """Check args[0] for a username and args[1] for a password. Logs in a profile if a match."""
        print("LogIN", prof_name, prof_pass)
        try:
            if prof_name in self.available_profiles:
                try:
                    if prof_pass == self.available_profiles[prof_name].password:
                        self.texoty.priont_string(f"⦙⦓ Welcome, {prof_name}!")
                        self.active_profile = self.available_profiles[prof_name]
                        self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                                     self.active_profile.color_theme[1],
                                                     16,
                                                     self.active_profile.color_theme[2])
                    else:
                        self.texoty.priont_string(f"⦙⦓ Wrong password, buster.")
                except IndexError:
                    self.texoty.priont_string(f"⦙⦓ Don't forget to type a password.")
            else:
                self.texoty.priont_string(f"⦙⦓ I don't recognize '{prof_name}' as profile username.")
                self.active_helper_dict['PRUN'][0].prompt_texioty_profile()
        except IndexError:
            self.texoty.priont_string("⦙⦓ What username to login to?")

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
        print('create_profile_args: ', args)
        if "yes" in args:
            self.texoty.priont_string("Creating a new profile...")
            profile_name = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['profile_name'][1]
            password = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['password'][1]
            color_theme = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['color_theme'][1]
            color_theme = t.DEFAULT_THEMES[color_theme]
            self.available_profiles[profile_name] = u.TexiotyProfile(profile_name, password, color_theme)
            save_path = f"filesOutput/.profiles/{profile_name}.json"
            # print(save_path)
            if not os.path.exists(save_path):
                with open(save_path, 'w') as f:
                    f.write(json.dumps({"texioty": self.available_profiles[profile_name].__dict__}, indent=4, sort_keys=True,
                                       default=lambda o: o.__dict__, ensure_ascii=False))
                    self.texoty.priont_string(f"Profile '{profile_name}' created.")

            else:
                self.texoty.priont_string(f"Profile '{profile_name}' already exists, did not create.")

    # def dl_youtube_vid(self, args):
    #     self.texoty.priont_string("Attempting to download:")
    #     self.texoty.priont_string(f"    {args}")
    #     u.download_youtube_video(args)
    #     self.texoty.priont_string(f"Maybe finished, maybe completed.")

    def priont_test(self):
        self.texoty.priont_dict({
            "Striong": "This is a string",
            "Iont": 3456123978,
            "Flioat": 1.236978,
            "List": ["one", 2, "tree", 45, 6.7],
            "Dict": {
                "INT": 654,
                "STiroRn": "StRiNg",
                "FLoooatT": 3.21,
                "LT": [0, "1", 3],
                "DCT": {'BOOL': True,
                        "Dict22": {
                            "this": "one2"
                        }}
            }
        })
