import json
import os.path
import random
import tkinter as tk
from typing import Callable, Dict

from helpers.pijun import PijunCooper
from helpers.promptaires.digiary.digiary import Digiary
from helpers.promptaires.prompt_helper import UserResponse, ResponseType, Question
from helpers.registries.command_registry import CommandRegistry
from helpers.registries.gaim_registry import GaimRegistry
from helpers.tex_helper import TexiotyHelper
from settings import utils as u
from settings import themery as t, konfig as k, alphanumers as a
from helpers.promptaires.profilizer import PROFILE_NAMING_KEYS

import texoty
import texity


class Texioty(tk.LabelFrame):
    def __init__(self, width, height, helper_registry=None, master=None):
        """
        Textual input from Texity, such as commands and other necessary inputs. Textual output from Texoty, such as help display
        and confirmation prompting.

        :param width: Width of the Texioty Widget frame.
        :param height: Height of the Texioty Widget frame.
        :param master: Parent widget
        """
        super(Texioty, self).__init__(master)
        self.helper_registry = helper_registry
        self.current_mode = "Texioty"
        self.command_registry = CommandRegistry({})

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

        # self.digiary = Digiary(self.texoty, self.texity)
        # self.base_helper = TexiotyHelper(self.texoty, self.texity)
        # self.gaim_registry = GaimRegistry(self.texoty, self.texity)
        # self.cooper = PijunCooper(self.texoty, self.texity)
        # self.default_helpers = {"TXTY": [self],
        #                         "HLPR": [self.base_helper],
        #                         "DIRY": [self.digiary]}
        # self.active_helper_dict = self.default_helpers
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
        self.add_command_group(self.helper_commands_dict)

        if helper_registry:
            for tag, helper in helper_registry.get_all_helpers().items():
                if hasattr(helper, "helper_commands"):
                    for cmd_name, cmd_config in helper.helper_commands.items():
                        self.command_registry.register_command(cmd_name, cmd_config)

    def register_helper_commands(self, helper_tag: str):
        if self.helper_registry:
            helper = self.helper_registry.get_helper(helper_tag)
            if helper and hasattr(helper, "helper_commands"):
                for cmd_name, cmd_config in helper.helper_commands.items():
                    self.command_registry.register_command(cmd_name, cmd_config)

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
            self.command_registry.add_command_dict(group_of_cmds[command])

    def remove_commands(self):
        self.command_registry.commands = {}
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
        for key, helper in self.helper_registry.get_all_helpers().items():
            # print(key, helper)
            self.register_helper_commands(key)

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
                self.helper_registry.get_helper("PRUN").profilemake.store_response(parsed_input)

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

                if self.helper_registry.get_helper("GAIM").current_gaim:
                    prefix = self.helper_registry.get_helper("GAIM").current_gaim.gaim_prefix
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
        if command in self.command_registry.commands:
            try:
                self.command_registry.execute_command(command, arguments)
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
        # print("LogIN", prof_name, prof_pass)
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
                        k.ACTIVE_PROFILE_USERNAME = prof_name
                    else:
                        self.texoty.priont_string(f"⦙⦓ Wrong password, buster.")
                except IndexError:
                    self.texoty.priont_string(f"⦙⦓ Don't forget to type a password.")
            else:
                self.texoty.priont_string(f"⦙⦓ I don't recognize '{prof_name}' as profile username.")
        except IndexError:
            self.texoty.priont_string("⦙⦓ What username to login to?")

    # def log_profile_out(self, args):
    #     if self.active_profile:
    #         #TODO Save each used command for the profile
    #         self.texoty.priont_string(f"Logging {self.active_profile.username} out. Goodbye!")
    #         self.active_profile = self.available_profiles["guest"]
    #         self.texoty.set_header_theme(self.active_profile.color_theme[0],
    #                                      self.active_profile.color_theme[1],
    #                                      16,
    #                                      self.active_profile.color_theme[2])
    #     else:
    #         self.texoty.priont_string("You have to log in before you can log out.")

    # def create_profile(self, args):
    #     """Create a new profile."""
    #     print('create_profile_args: ', args)
    #     if "yes" in args:
    #         self.texoty.priont_string("Creating a new profile...")
    #         profile_name = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['profile_name'][1]
    #         password = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['password'][1]
    #         color_theme = self.active_helper_dict["PRUN"][0].profilemake.question_prompt_dict['color_theme'][1]
    #         color_theme = t.DEFAULT_THEMES[color_theme]
    #         self.available_profiles[profile_name] = u.TexiotyProfile(profile_name, password, color_theme)
    #         save_path = f"filesOutput/.profiles/{profile_name}.json"
    #         if not os.path.exists(save_path):
    #             with open(save_path, 'w') as f:
    #                 f.write(json.dumps({"texioty": self.available_profiles[profile_name].__dict__}, indent=4, sort_keys=True,
    #                                    default=lambda o: o.__dict__, ensure_ascii=False))
    #                 self.texoty.priont_string(f"Profile '{profile_name}' created.")
    #
    #         else:
    #             self.texoty.priont_string(f"Profile '{profile_name}' already exists, did not create.")

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

    def responses_to_profile(self, responses: Dict[str, Question]):
        """Create any kind of profile."""
        self.texoty.priont_string("Creating a new profile...")
        save_dict = {}
        for key in responses:
            match responses[key].user_response.response_type:
                case ResponseType.BOOL:
                    save_dict[key] = responses[key].user_response.bool_response
                case ResponseType.STRING:
                    save_dict[key] = responses[key].user_response.str_response
                case ResponseType.INT:
                    save_dict[key] = responses[key].user_response.int_response
                case ResponseType.LIST:
                    save_dict[key] = responses[key].user_response.list_response
                case ResponseType.FLOAT:
                    save_dict[key] = responses[key].user_response.float_response
                case ResponseType.DECISION:
                    save_dict[key] = responses[key].user_response.float_response
        profile_name = f"{save_dict['profile_name']}"
        save_path = f"filesOutput/.profiles/testing/{profile_name}.json"
        if not os.path.exists(save_path):
            with open(save_path, 'w') as f:
                f.write(json.dumps(save_dict, indent=4, sort_keys=True,
                                   default=lambda o: dict(o) if isinstance(o, dict) else (
                                       o.__dict__ if hasattr(o, '__dict__') else str(o)
                                   ), ensure_ascii=False))
                self.texoty.priont_string(f"Profile '{profile_name}' created.")
        else:
            self.texoty.priont_string(f"Profile '{profile_name}' already exists, did not create.")

        # self.texoty.priont_dict(responses)

