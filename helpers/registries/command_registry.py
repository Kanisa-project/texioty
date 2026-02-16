import inspect
from dataclasses import dataclass
from typing import Dict, Any

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
        if help_symb in self.commands:
            del self.commands[help_symb]
            return

        to_delete = [name for name, cmd in self.commands.items() if getattr(cmd, "group_tag", None) == help_symb]
        for name in to_delete:
            del self.commands[name]

    def add_command_dict(self, command_info: Dict[str, Any]):
        try:
            self.commands[command_info["name"]] = texity.Command(name=command_info["name"],
                                                                 usage=command_info["usage"],
                                                                 call_func=command_info["call_func"],
                                                                 lite_desc=command_info["lite_desc"],
                                                                 full_desc=command_info["full_desc"],
                                                                 possible_args=command_info["possible_args"],
                                                                 args_desc=command_info["args_desc"],
                                                                 examples=command_info["examples"],
                                                                 group_tag=command_info["group_tag"],
                                                                 font_color=command_info["font_color"],
                                                                 back_color=command_info["back_color"])
            # print(command_info["name"], "added to registry.")
        except KeyError as e:
            print(f"Missing key in command dictionary: {e}")



    def execute_command(self, name: str, exec_args: tuple) -> None:
        """
        Executes the command being used in Texity.
        :param name: Name of the command being executed.
        :param exec_args: Arguments to be used in the command execution.
        :return:
        """
        command = self.commands.get(name)
        if not command:
            print(f"Command '{name}' not found.")
            return

        cmd_handler = command.call_func
        print("Inspecting", name, inspect.getfullargspec(cmd_handler).annotations)
        try:
            if len(inspect.getfullargspec(cmd_handler).args) == 1:
                cmd_handler()
            else:
                cmd_handler(*exec_args)
        except Exception as e:
            print(f"Error executing '{name}': {e}", exec_args)

    def register_command(self, cmd_name, cmd_config):
        print(cmd_config)
        self.commands[cmd_name] = texity.Command(**cmd_config)
