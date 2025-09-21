import random
from tkinter import *
from tkHyperLinkManager import HyperlinkManager
import webbrowser
from functools import partial

import settings as s
import texioty
import texity


class TEXOTY(Text):
    """
    Text output for Texioty. Can go through a questionnaire prompt or display some helpful facts or assist in playing
    hangman or solving a riddle or master password game. Even does art eventually.
    """

    def __init__(self, width: int, height: int, master=None):
        """
        
        :param width: 
        :param height: 
        :param master: 
        """
        self.texoty_h = height // 19
        self.texoty_w = int(width // 4.2)
        self.y_line_index = 0
        self.master: texioty.Texioty = master
        self.active_profile = self.master.active_profile
        super(TEXOTY, self).__init__(master=master, bg=self.active_profile.color_theme[2], height=self.texoty_h,
                                     width=self.texoty_w,
                                     spacing2=0)
        self.set_header()
        self.hyperlink = HyperlinkManager(self)

    def priont_hyperlink(self, tex: str, link: str, line_index=END):
        self.insert(line_index, tex, self.hyperlink.add(partial(webbrowser.open, link)))
        self.yview(END)

    def set_header(self, msg="Welcome to Texioty"):
        """
        Set a heading with a message and interesting looking lines
        :param msg: Whatever you want to display for the user.
        :return:
        """
        welcome_line = msg
        half_blocks = '▄▌█▐▀'
        header_line = ""
        header_bot = ""
        # Checks if Texioty frame has an active profile logged in, else logins to a guest.
        if self.master.active_profile:
            self.active_profile = self.master.active_profile
        else:
            self.active_profile = self.master.available_profiles["guest"]
        for i in range(self.texoty_w):
            if i % 2 == 0:
                index = int(i / self.texoty_w * (len(half_blocks) - 1))
                header_line += half_blocks[index]
            else:
                header_line += random.choice(half_blocks)
            header_bot += random.choice('═─')
        self.set_text_on_line(0,
                              f"{welcome_line}{header_line[len(welcome_line):]}{header_line[len(self.active_profile.username):]}{self.active_profile.username}")
        self.set_text_on_line(2, f"╙{header_bot[2:]}╛")
        self.configure(bg=self.active_profile.color_theme[2])

    def set_header_theme(self, primary_color: str, secondary_color: str, len_msg: int, font_color: str = "black"):
        self.make_text_colored(font_color, primary_color, f"1.0", f"1.{self.texoty_w - len_msg}")
        self.make_text_colored(secondary_color, primary_color, f"1.{self.texoty_w - len_msg}", f"1.{self.texoty_w}")
        self.make_text_colored(font_color, primary_color, f"1.{self.texoty_w}", f"1.end")

    def make_text_colored(self, fg_color, bg_color, start_index, end_index):
        self.tag_configure(f"{fg_color}_{bg_color}", background=bg_color, foreground=fg_color)
        self.tag_add(f"{fg_color}_{bg_color}", start_index, end_index)
        # self.tag_ranges(f'{fg_color}_{bg_color}')
        # self.tag_delete(f'{fg_color}_{bg_color}', '1.5', END)

    def create_masterpiece(self, *args):
        """
        Adds an artistic frame around the Texoty textuality.
        :param args: 
        :return: 
        """
        size = (35, 20)
        mstrpc_w = size[0]
        mstrpc_h = size[1]
        mstrpc_a = 0
        for th in range(int(self.texoty_h)):
            if th == 0:
                self.priont_string(f"{'╔'}{'═' * (self.texoty_w - 2)}{'╗'}")
            elif th + 1 == self.texoty_h:
                self.priont_string(f"{'╚'}{'═' * (self.texoty_w - 2)}{'╝'}")
            elif mstrpc_h >= th >= self.texoty_h - mstrpc_h:
                mstrpc_a += 1
                mstrpc_str = self.artay_method_dict[random.choice(*args)](mstrpc_w, mstrpc_a)
                self.priont_string(
                    f"{'║'}{' ' * (((self.texoty_w - mstrpc_w) // 2) - 1)}{mstrpc_str}{' ' * (((self.texoty_w - mstrpc_w) // 2) - 2)}{'║'}")
            else:
                self.priont_string(f"{'║'}{' ' * (self.texoty_w - 2)}{'║'}")

    def clear_add_header(self, header_msg=""):
        """ Clear Texoty display and replace the header. """
        self.delete("0.0", 'end')
        self.set_header()

    def clear_no_header(self):
        """ Clear Texoty display and do not replace the header. """
        self.delete("0.0", 'end')

    def priont_kre8dict(self, kre8dict: dict, indent=0):
        """
        Print and display the full kre8dict in Texoty.
        :param kre8dict: 
        :param indent: 
        :return: 
        """
        print(kre8dict)
        for key, value in kre8dict.items():
            self.priont_string(f'▐{key}╕')
            if isinstance(value, str):  # STRING
                self.priont_string(f'{" " * (len(key) + 1)}└{value}')
            elif isinstance(value, list):  # LIST
                self.priont_list(items=value, list_key=key)
            elif isinstance(value, int):  # INT
                self.priont_int(key, value)
            elif isinstance(value, float):  # FLOAT
                self.priont_float(key, value)
            elif isinstance(value, dict):  # DICT
                if indent == 1:
                    self.priont_dict(value, parent_key=key, indent=indent + 1)
                else:
                    self.priont_dict(value, parent_key=key, indent=indent + 1)

    def priont_dict(self, dioct: dict, parent_key=None, indent=0):
        """
        Iterate through a dictionary and display each key/value pair.

        :param indent: How much front spacing.
        :param parent_key: The parent key in a nested dictionary.
        :param dioct: Dictionary to iterate through.
        """
        for key, value in dioct.items():
            if parent_key:
                prefix = " " * (len(parent_key) - 1) + "▐"
            else:
                prefix = ""
            self.priont_string(f'{prefix}▐{key}┐')

            if isinstance(dioct[key], str):  # STRING
                self.priont_string(f'{" " * (len(key) + 1)}└{dioct[key]}')
            elif isinstance(dioct[key], list):  # LIST
                self.priont_list(dioct[key], parent_key=key)
            elif isinstance(dioct[key], int):  # INT
                self.priont_int(key, dioct[key])
            elif isinstance(dioct[key], float):  # FLOAT
                self.priont_float(key, dioct[key])
            elif isinstance(dioct[key], texity.Command):  # COMMAND
                self.priont_command(dioct[key])
            elif isinstance(dioct[key], dict):  # DICT
                if indent == 1:
                    self.priont_dict(dioct[key], parent_key=key, indent=indent + 1)
                else:
                    self.priont_dict(dioct[key], parent_key=key, indent=indent + 1)

    def priont_command(self, command: texity.Command):
        """
        Display a command on Texoty in a stylized and slightly complicated fashion.
        :param command:
        :return:
        """
        self.priont_break_line()
        self.priont_command_colorized(f'{command.name}╕', command.text_color, command.bg_color)
        if not command.possible_args:
            help_message_text = f'{" " * len(command.name)}╘► {command.help_message}'
            self.priont_command_colorized(help_message_text, command.text_color, command.bg_color)
        else:
            help_message_text = f'{" " * len(command.name)}╞► {command.help_message}'
            self.priont_command_colorized(help_message_text, command.text_color, command.bg_color)
            for p_arg_i, p_arg_k in enumerate(command.possible_args):
                prefix = " " * len(command.name)
                prefix += "└" if p_arg_i == len(command.possible_args) - 1 else "├"
                self.priont_command_colorized(prefix + p_arg_k + f"» {command.possible_args[p_arg_k]}",
                                              text_color=command.text_color, bg_color=command.bg_color)
        self.yview(END)

    def priont_break_line(self):
        """
        Adds a break line in Texoty with style.
        :return:
        """
        break_line = ""
        bg = self.active_profile.color_theme[2]
        fg = self.active_profile.color_theme[0]
        self.tag_configure('break_line', foreground=fg, background=bg)
        for _ in range(self.texoty_w - 2):
            break_line += random.choice('═─')
        self.insert(END, f"\n╫{break_line}╫", 'break_line')

    def priont_string(self, striong: str, line_index=END):
        """
        Display a string of text at line_index.

        @param line_index: Index of where on the line to insert text.
        @param striong: String to display.
        """
        self.insert(line_index, "\n" + striong)
        self.yview(END)

    def priont_echo(self, striong: str, text_color='', bg_color=''):
        """
        Display a striong on texoty in the color of font_color.

        @param striong:
        @param bg_color:
        @param text_color:
        """
        tag_name = f'{bg_color}_{text_color}'
        self.tag_configure(tag_name, foreground=text_color, background=bg_color)
        start_pos = f'1.0'
        end_pos = f'1.{len(striong)}'
        self.tag_add(tag_name, start_pos, end_pos)
        self.insert(END, striong, tag_name)
        self.insert(END, '\n')
        self.yview(END)

    def priont_command_colorized(self, striong: str, text_color='', bg_color=''):
        """
        Display a command with text_color and bg_color highlighting.

        @param striong: Text of command to display.
        @param bg_color: Color for the background.
        @param text_color: Color for the text.
        """
        tag_name = f'{bg_color}_{text_color}'
        self.tag_configure(tag_name, foreground=text_color, background=bg_color)
        start_pos = f'1.0'
        end_pos = f'1.{len(striong)}'
        self.tag_add(tag_name, start_pos, end_pos)
        self.insert(END, striong, tag_name)
        self.insert(END, '\n')
        self.yview(END)

    def priont_float(self, key_of_float: str, flioat: float):
        """
        Display a float.
        :param key_of_float: If the float is in a dictionary.
        :param flioat: The float to display.
        :return:
        """
        leading_spaces = " " * (len(key_of_float) + 1)
        self.priont_string(f'{leading_spaces}└{flioat}')

    def priont_number_list(self, number_list: list):
        """
        Display the number list from kre8dict.
        :param number_list: The list of numbers in numerical order.
        :return:
        """
        self.priont_string(str(number_list))

    def priont_list(self, items: list, list_key=None, parent_key=None):
        """
        Display a list of items on texoty, each item in the list on its own line.

        @param items:
        @param list_key:
        @param parent_key:
        """

        if list_key:
            leading_spaces = " " * (len(list_key) + 1)
        elif parent_key:
            leading_spaces = " " * len(parent_key)
        else:
            leading_spaces = " "

        if list_key == "number_list":
            self.priont_string(str(f'{leading_spaces}└{items}'))
        elif parent_key:
            self.priont_string(parent_key + "┐")
            for item in items:
                prefix = "└" if items.index(item) == len(items) - 1 else "├"
                if isinstance(item, str) and item.startswith('http'):
                    self.priont_hyperlink("Click Me", item)
                else:
                    self.priont_string(f'{leading_spaces}{prefix}{item}')
        else:
            for item in items:
                prefix = "└" if items.index(item) == len(items) - 1 else "├"
                if isinstance(item, str) and item.startswith('http'):
                    self.priont_hyperlink("Click Me", item)
                else:
                    self.priont_string(f'{leading_spaces}{prefix}{item}')

    def priont_int(self, key_of_int: str, iont: int):
        """
        Display an integer on texoty.
        :param key_of_int: If the integer is from a dictionary.
        :param iont: Integer for displaying.
        :return:
        """
        leading_spaces = " " * (len(key_of_int) + 1)
        self.priont_string(f'{leading_spaces}└{iont}')

    def set_text_on_line(self, line_number: int, text: str):
        """
        Insert plain basic text on the line_number line.
        :param line_number: Line to insert text.
        :param text: Text to insert at the beginning of line_number.
        :return:
        """
        line_start_index = f"{line_number}.0"
        self.insert(line_start_index, text)

    def set_char_on_line(self, x_loc, y_loc, char="┐"):
        self.insert(f"{x_loc}.{y_loc}", char)

    def create_foto_line(self, one, two):
        print(one, two)
        start_x = 0
        start_y = 3
        for i in range(20):
            if i % 2 == 0:
                start_y += 1
                self.set_char_on_line(0, 0, f"{' ' * i}┐\n")
            else:
                start_x += 1
                self.set_char_on_line(0, 0, f"{' ' * i}└\n")


def create_glyth_line(mstrpc_w, mstrpc_a) -> str:
    """
    Create a line of glyth like text with a total length of mstrpc_w.
    :param mstrpc_w: Width of the masterpiece.
    :param mstrpc_a: Amount of textual glyths or something.
    :return:
    """
    dots = random.choice('.:*')
    lines = random.choice('_-+/')
    return f"{dots * (mstrpc_w - mstrpc_a)}{lines}{dots * mstrpc_a}"


def create_glyph_line(mstrpc_w, mstrpc_a) -> str:
    """
    Create a line of glyph like text totaling length of mstrpc_w.
    :param mstrpc_w: Width of the masterpiece.
    :param mstrpc_a: Amount of textual glyths or something.
    :return:
    """
    dots = random.choice('▓▒░')
    lines = random.choice('▐▌▄▀')
    return f"{dots * (mstrpc_w - mstrpc_a)}{lines}{dots * mstrpc_a}"


def create_wordie_line(mstrpc_w, mstrpc_a) -> str:
    """
    Create a line of not wordie like text with the width of mstrpc_w.
    :param mstrpc_w: Width of the masterpiece.
    :param mstrpc_a: Amount of textual glyths or something.
    :return:
    """
    dots = random.choice('┐└┴┬├─┼┘┌')
    lines = random.choice('╚╔╩╦╠═╬')
    return f"{lines * (mstrpc_w - mstrpc_a)}{dots}{lines * mstrpc_a}"


def hyperlink_callback(url):
    webbrowser.open_new_tab(url)
