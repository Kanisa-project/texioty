from typing import Any, Callable, Dict, List
import re

from src.texioty.core import texity


# class CommandValidationError(Exception):
#     pass

# class CommandBuilder:
#     REQUIRED_FIELDS = ['name', 'usage', 'call_func', 'lite_desc',
#                        'full_desc', 'possible_args', 'args_desc',
#                        'examples', 'group_tag', 'font_color',
#                        'back_color']
#     FIELD_TYPES = {
#         'name': str,
#         'usage': str,
#         'call_func': Callable,
#         'lite_desc': str,
#         'full_desc': (list, tuple),
#         'possible_args': dict,
#         'args_desc': dict,
#         'examples': (list, tuple),
#         'group_tag': str,
#         'font_color': str,
#         'back_color': str
#     }
#     VALID_GROUP_TAGS = ['HLPR', 'DIRY', 'PRUN', 'FOTO', 'TXTY', 'GAIM', 'HAPI']
#     def __init__(self, name: str):
#         self._data: Dict[str, Any] = {'name': name}
#
#     def set_usage(self, usage: str) -> 'CommandBuilder':
#         if not isinstance(usage, str):
#             raise CommandValidationError(f"Usage must be a string, not {type(usage)}")
#         self._data['usage'] = usage
#         return self

    # def set_callback(self, call_func: Callable) -> 'CommandBuilder':
    #     if not callable(call_func):
    #         raise CommandValidationError(f"Callback must be a callable, not {type(call_func)}")
    #     self._data['call_func'] = call_func
    #     return self
    #
    # def set_lite_desc(self, lite_desc: str) -> 'CommandBuilder':
    #     if not isinstance(lite_desc, str):
    #         raise CommandValidationError(f"Lite description must be a string, not {type(lite_desc)}")
    #     self._data['lite_desc'] = lite_desc
    #     return self
    #
    # def set_full_desc(self, full_desc: List[str]) -> 'CommandBuilder':
    #     if not isinstance(full_desc, (list, tuple)):
    #         raise CommandValidationError(f"Full description must be a list or tuple, not {type(full_desc)}")
    #     if not all(isinstance(arg, str) for arg in full_desc):
    #         raise CommandValidationError("All elements in full description must be strings.")
    #     self._data['full_desc'] = full_desc

    # def set_possible_args(self, possible_args: Dict[str, Any]) -> 'CommandBuilder':
    #     if not isinstance(possible_args, dict):
    #         raise CommandValidationError(f"Possible arguments must be a dictionary, not {type(possible_args)}")
    #     self._data['possible_args'] = possible_args
    #     return self
    #
    # def set_args_desc(self, args_desc: Dict[str, Any]) -> 'CommandBuilder':
    #     if not isinstance(args_desc, dict):
    #         raise CommandValidationError(f"Argument descriptions must be a dictionary, not {type(args_desc)}")
    #     self._data['args_desc'] = args_desc
    #     return self
    #
    # def set_examples(self, examples: List[str]) -> 'CommandBuilder':
    #     if not isinstance(examples, (list, tuple)):
    #         raise CommandValidationError(f"Examples must be a list or tuple, not {type(examples)}")
    #     if not all(isinstance(example, str) for example in examples):
    #         raise CommandValidationError("All examples must be strings")
    #     self._data['examples'] = examples
    #     return self
    #
    # def set_group_tag(self, group_tag: str) -> 'CommandBuilder':
    #     if not isinstance(group_tag, str):
    #         raise CommandValidationError(f"Group tag must be a string, not {type(group_tag)}")
    #     if group_tag not in self.VALID_GROUP_TAGS:
    #         raise CommandValidationError(f"Invalid group tag: {group_tag}")
    #     self._data['group_tag'] = group_tag
    #     return self
    #
    # def set_colors(self, font_color: str, back_color: str) -> 'CommandBuilder':
    #     self.set_font_color(font_color)
    #     self.set_back_color(back_color)
    #     return self
    #
    # def set_font_color(self, color: str) -> 'CommandBuilder':
    #     self._validate_colors(color, "font_color")
    #     self._data['font_color'] = color
    #     return self
    #
    # def set_back_color(self, color: str) -> 'CommandBuilder':
    #     self._validate_colors(color, "back_color")
    #     self._data['back_color'] = color
    #     return self

    # def _validate_colors(self, color: str, field_name: str) -> None:
    #     if not isinstance(color, str):
    #         raise CommandValidationError(f"{field_name} must be a string, not {type(color)}")
    #     if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
    #         raise CommandValidationError(f"Invalid {field_name} format. Must be a hex color code (e.g., #FFFFFF).")
    #
    # def _validate_all(self) -> None:
    #     missing_fields = self.REQUIRED_FIELDS - set(self._data.keys())
    #     if missing_fields:
    #         raise CommandValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    #     for field, expected_type in self.FIELD_TYPES.items():
    #         if field in self._data:
    #             value = self._data[field]
    #             if not isinstance(value, expected_type):
    #                 raise CommandValidationError(f"Invalid type for {field}. Expected {expected_type}, got {type(value)}")
    #
    # def build(self) -> texity.Command:
    #     self._validate_all()
    #     try:
    #         return texity.Command(**self._data)
    #     except Exception as e:
    #         raise CommandValidationError(f"Error building command: {e}") from e



# class CommandFactory:
#     @staticmethod
#     def from_dict(command_dict: Dict[str, Any]) -> texity.Command:
#         if 'name' not in command_dict:
#             raise CommandValidationError("Command dictionary must contain a 'name' key.")
#         name = command_dict['name']
#         builder = CommandBuilder(name)
#
#         field_setters = {
#             'usage': builder.set_usage,
#             'call_func': builder.set_callback,
#             'lite_desc': builder.set_lite_desc,
#             'full_desc': builder.set_full_desc,
#             'possible_args': builder.set_possible_args,
#             'args_desc': builder.set_args_desc,
#             'examples': builder.set_examples,
#             'group_tag': builder.set_group_tag,
#             'font_color': lambda x: builder.set_font_color(x),
#             'back_color': lambda x: builder.set_back_color(x)
#         }
#
#         for field, value in command_dict.items():
#             if field == 'name':
#                 continue
#             if field in field_setters:
#                 field_setters[field](value)
#             else:
#                 raise CommandValidationError(f"Invalid field: {field}")
#         return builder.build()

    # @staticmethod
    # def from_dicts(command_dicts: Dict[str, Dict[str, Any]]) -> Dict[str, texity.Command]:
    #     commands = {}
    #     errors = []
    #     for name, command_dict in command_dicts.items():
    #         try:
    #             commands[name] = CommandFactory.from_dict(command_dict)
    #         except CommandValidationError as e:
    #             raise CommandValidationError(f"Error building command '{name}': {e}") from e
    #     if errors:
    #         error_msg = "Errors building commands:\n" + "\n".join(errors)
    #         raise CommandValidationError(error_msg)
    #     return commands