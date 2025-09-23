import datetime
import json
import random
import tkinter as tk
from dataclasses import dataclass
from os.path import exists
from typing import Dict, Any
from utils import get_stock_price
import settings as s
import theme as t
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
        # self.configure(text="Texioty:  ")

        # INITIATE DIARY VARIABLES
        self.diary_line_length = 75
        self.diarySentenceList = []
        self.in_diary_mode = False

        self.registry = CommandRegistry({})

        self.helper_dict = {}
        self.available_profiles = s.available_profiles
        self.active_profile = self.available_profiles["guest"]

        self.texoty = texoty.TEXOTY(int(width) + 16, int(height), master=self)
        self.texoty.grid(column=0, row=0)
        self.texity = texity.TEXITY(width=int(width // 6), master=self)
        self.texity.grid(column=0, row=1)

        self.texity.focus_set()
        self.texity.bind('<KP_Enter>', lambda e: self.process_command())
        self.texity.bind('<Return>', lambda e: self.process_command())

        # Set up basic commands for Texioty to know automatically.
        self.known_commands_dict = {
            "welcome": [self.welcome_message, "Displays a message of helping helpfulness.",
                     {}, [], s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
            "help": [self.display_help_message, "Displays a message of helping helpfulness.",
                     {}, [], s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
            "commands": [self.display_available_commands, "Displays all available commands.",
                         {}, [], s.rgb_to_hex(t.GREEN_YELLOW), s.rgb_to_hex(t.BLACK)],
            "login": [self.log_profile_in, "This logs the user into a profile: ",
                      {'guest': "Basic account with a few permissions."},
                      [], s.rgb_to_hex(t.DIM_GREY), s.rgb_to_hex(t.BLACK)],
            "dear_sys,": [self.start_diary_mode, "Starts a diary entry.",
                     {}, [], s.rgb_to_hex(t.VIOLET_RED), s.rgb_to_hex(t.BLACK)],
            "/until_next_time": [self.stop_diary_mode, "Ends a diary entry.",
                     {}, [], s.rgb_to_hex(t.VIOLET_RED), s.rgb_to_hex(t.BLACK)],
            "exit": [self.close_program, "Exits the program.",
                     {}, [], s.rgb_to_hex(t.PURPLE), s.rgb_to_hex(t.BLACK)],
        }

        self.welcome_message([])
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

    def add_helper_widget(self, helper_type: str, helper_widget):
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

    def clear_texoty(self):
        """Clear all the text from texoty and replace the header."""
        self.texoty.delete("0.0", tk.END)
        self.texoty.set_header()

    def welcome_message(self, welcoming_msgs: list):
        """
        Display welcoming messages with a few commands to get started.

        """
        self.texoty.clear_add_header("Welcome!")
        # price_dict = get_stock_price('GME')
        # welcoming_msgs.append(f'<{price_dict["ticker"]}>   {price_dict['name']} is at ${price_dict["price"]} since {price_dict["updated"]}.')
        today_date = datetime.datetime.date(datetime.datetime.now())
        today_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
            datetime.datetime.weekday(today_date)]
        self.texoty.priont_string(
            f"⦓⦙ Welcome to Texioty! The date is {today_date} on a {today_day}.")
        for msg in welcoming_msgs:
            self.texoty.priont_string("⦓⦙ " + msg)
        self.texoty.priont_string("\n")

        cmnds = [random.choice(["help", "commands"]),
                 random.choice(["kre8dict", "dear_sys,"]),
                 random.choice(["exit"])]
        self.texoty.priont_list(cmnds, parent_key="Here are a few commands you could try:")
        sequence = ["glyph add 2", "glyth add 4", "kin8"]
        self.texoty.priont_string("")
        self.texoty.priont_list(sequence, parent_key="Or try this sequence of commands:", numbered=True)
        self.texoty.priont_string("⦓⦙ Type 'glyph add 2' and press enter, then 'glyth add 4' and press enter.")
        self.texoty.priont_string("⦓⦙ Finally type 'kin8' and press enter, the result should show on the right.")


    def process_command(self, event=None):
        """
        Process the command before executing it. Decide which helpers to use or if just a regular command.
        :return:
        """
        match self.current_mode:
            case "Texioty":
                parsed_input = self.texity.parse_input_command()
                if not parsed_input:
                    self.texity.command_string_var.set("")
                    return
                command = parsed_input[0]
                arguments = parsed_input[1:]
                self.execute_command(command, arguments)
            case "Diary":
                if self.texity.parse_diary_line() != "/until_next_time":
                    parsed_input = self.texity.parse_diary_line()
                    self.add_diary_line(parsed_input)
                else:
                    self.execute_command("/until_next_time", [])
            case "Questionnaire":
                parsed_input = self.texity.parse_question_response()
                self.helper_dict["PRUN"][0].store_response(parsed_input)
            case "Gaim":
                self.helper_dict["GAIM"][0].process_command()
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

    def start_diary_mode(self, args) -> datetime.datetime:
        """Begin diary entry and add a timestamp line to the beginning of the entry."""
        start_now = datetime.datetime.now()
        self.current_mode = "Diary"
        self.texoty.priont_string(f"\n-Entering diary mode-   {start_now}")
        opening_line = timestamp_line_entry(start_now, 'dear_sys,', lead_line='ts',
                                            follow_line=' ' * (self.diary_line_length - len('dear_sys,')))
        self.diarySentenceList = [opening_line]
        return start_now

    def add_diary_line(self, new_line):
        """Add a line to the current diary entry."""
        self.texoty.priont_string(f'  [+{"".join(random.sample(new_line, len(new_line)))}')
        self.diarySentenceList.append(timestamp_line_entry(datetime.datetime.now(), new_line, lead_line='  ',
                                                           follow_line='_' * (self.diary_line_length - len(
                                                               new_line) - 2)))

    def stop_diary_mode(self, args) -> datetime.datetime:
        """End a diary entry and save the entry to a file."""
        end_now = datetime.datetime.now()
        self.current_mode = "Texioty"
        self.texoty.priont_string(f"-Exiting diary mode-   {end_now}\n")
        ending_line = timestamp_line_entry(end_now, '/until_next_time', lead_line='ts',
                                           follow_line=' ' * (self.diary_line_length - len('/until_next_time')))
        self.diarySentenceList.append(ending_line)
        create_date_entry(end_now, self.diarySentenceList)
        return end_now

    def create_profile(self, args):
        """Create a new profile."""
        if "yes" in args:
            self.texoty.priont_string("Creating a new profile...")
            profile_name = self.helper_dict["PRUN"][0].question_prompt_dict['profile_name'][1]
            password = self.helper_dict["PRUN"][0].question_prompt_dict['password'][1]
            color_theme = self.helper_dict["PRUN"][0].question_prompt_dict['color_theme'][1]
            color_theme = t.DEFAULT_THEMES[color_theme]
            self.available_profiles[profile_name] = s.TexiotyProfile(profile_name, password, color_theme)
            save_path = f".profiles/{profile_name}.json"
            print(save_path)
            with open(save_path, 'w') as f:
                f.write(json.dumps({"texioty": self.available_profiles[profile_name].__dict__}, indent=4, sort_keys=True,
                                   default=lambda o: o.__dict__, ensure_ascii=False))
            self.texoty.priont_string(f"Profile '{profile_name}' created.")


def create_date_entry(entry_time: datetime.datetime, entry_list: list):
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
