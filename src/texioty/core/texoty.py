import random
from tkinter import *
from typing import TYPE_CHECKING
from tkHyperLinkManager import HyperlinkManager
import webbrowser
from functools import partial
from src.texioty.core import texity

if TYPE_CHECKING:
    from src.texioty.core.texioty import Texioty

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
        self.active_profile = None
        self.texoty_h = height // 19
        self.texoty_w = int(width // 4.2)
        self.y_line_index = 0
        self.master: "Texioty" = master
        super(TEXOTY, self).__init__(master=master,
                                     height=self.texoty_h,
                                     width=self.texoty_w,
                                     spacing2=0)
        self.header_defaults = {
            "title": "Welcome to Texioty",
            "right_status": "",
            "bottom_status": "",
            "top_charset": "░▒▓🮑🮒🮐🮔",
            "bottom_charset": "─┈╌═",
            "show_username": True

        }
        self.header_state = dict(self.header_defaults)
        self.set_header()
        self.scroll_bar = Scrollbar(master=self.master, width=10, command=self.yview)
        self['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.propagate(False)
        self.scroll_bar.grid(column=1, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.hyperlink = HyperlinkManager(self)
        self._tag_cache = set()

    def priont_hyperlink(self, tex: str, link: str, line_index=END):
        self.insert(line_index, tex, self.hyperlink.add(partial(webbrowser.open, link)))
        self.yview(END)

    def priont_click_command(self, tex: str, link: str, line_index=END):
        self.insert(line_index, tex, self.hyperlink.add_cmd(partial(self.master.set_texity_input, link)))
        self.priont_string('')

    @staticmethod
    def _fit_header_text(text: str, width: int) -> str:
        text = str(text or "")
        if width <= 0:
            return ""
        if len(text) >= width:
            return text[:width]
        return text + (" " * (width - len(text)))

    @staticmethod
    def _build_header_fill(width: int, charset: str, patterned: bool = True):
        if width <= 0:
            return ""
        if not charset:
            return " " * width
        fill = ""
        if patterned:
            for i in range(width):
                if i % 2 == 0:
                    index = int(i / max(width, 1) * (len(charset) - 1))
                    fill += charset[index]
                else:
                    fill += random.choice(charset)
        else:
            for _ in range(width):
                fill += random.choice(charset)
        return fill

    def _compose_header_top_line(self, title: str, username: str, right_status: str, top_charset: str) -> str:
        width = self.texoty_w
        title = str(title or "")
        username = str(username or "")
        right_status = str(right_status or "")

        right_parts = [part for part in [right_status, username] if part]
        right_text = " | ".join(right_parts)

        if right_text:
            reserved_right = min(len(right_text) + 1, max(width // 2, 1))
            left_width = max(width - reserved_right, 1)
            left_text = self._fit_header_text(title, left_width)
            right_width = max(width - len(left_text), 0)
            right_text = right_text[-right_width:] if right_width > 0 else ""
            fill_width = max(right_width - len(right_text), 0)
            filler = self._build_header_fill(fill_width, top_charset)
            return f"{left_text}{filler}{right_text}"

        left_text = self._fit_header_text(title, width)
        return left_text

    def _compose_header_bottom_line(self, bottom_status: str, bottom_charset: str) -> str:
        inner_width = max(self.texoty_w - 2, 0)
        bottom_status = str(bottom_status or "")

        if bottom_status:
            label = f" {bottom_status} "
            if len(label) > inner_width:
                label = label[:inner_width]
            fill_width = max(inner_width - len(label), 0)
            filler = self._build_header_fill(fill_width, bottom_charset, patterned=False)
            return f"╙{label}{filler}╛"

        filler = self._build_header_fill(inner_width, bottom_charset, patterned=False)
        return f"╙{filler}╛"

    def set_header(self, msg=None, right_status=None, bottom_status=None, show_username=None):
        """
        Set a heading with a message and interesting looking lines
        :param msg: Whatever you want to display for the user.
        :param right_status:
        :param bottom_status:
        :param show_username:
        :return:
        """
        self.delete("0.0", 'end')
        if self.master.active_profile:
            self.active_profile = self.master.active_profile
        else:
            self.active_profile = self.master.available_profiles["guest"]

        if msg is not None:
            self.header_state["title"] = msg
        if right_status is not None:
            self.header_state["right_status"] = right_status
        if bottom_status is not None:
            self.header_state["bottom_status"] = bottom_status
        if show_username is not None:
            self.header_state["show_username"] = show_username
        username = self.active_profile.username if self.header_state["show_username"] else ""
        top_line = self._compose_header_top_line(
            self.header_state["title"],
            username,
            self.header_state["right_status"],
            self.header_state["top_charset"]
        )
        bottom_line = self._compose_header_bottom_line(
            self.header_state["bottom_status"],
            self.header_state["bottom_charset"]
        )
        self.set_text_on_line(0, top_line)
        self.set_text_on_line(2, bottom_line)
        self.configure(bg=self.active_profile.color_theme[2])

    def update_header_status(self, right_status=None, bottom_status=None):
        """
        Update just the runtime status portions of header.
        """
        if right_status is not None:
            self.header_state["right_status"] = right_status
        if bottom_status is not None:
            self.header_state["bottom_status"] = bottom_status
        self.set_header()

    def set_header_theme(self, primary_color: str, secondary_color: str, len_msg: int, font_color: str = "black"):
        self.make_text_colored(font_color, primary_color, f"1.0", f"1.{self.texoty_w - len_msg}")
        self.make_text_colored(secondary_color, primary_color, f"1.{self.texoty_w - len_msg}", f"1.{self.texoty_w}")
        self.make_text_colored(font_color, primary_color, f"1.{self.texoty_w}", f"1.end")

    def make_text_colored(self, fg_color, bg_color, start_index, end_index):
        """Apply a color tag between two indices."""
        tag_name = f"{fg_color}_{bg_color}"
        if tag_name not in self._tag_cache:
            try:
                self.tag_configure(tag_name, foreground=fg_color, background=bg_color)
            finally:
                self.tag_configure(tag_name, foreground=str(fg_color), background=str(bg_color))
            self._tag_cache.add(tag_name)
        self.tag_add(tag_name, start_index, end_index)


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
                # mstrpc_a += 1
                # mstrpc_str = self.artay_method_dict[random.choice(*args)](mstrpc_w, mstrpc_a)
                self.priont_string(
                    f"{'║'}{' ' * (((self.texoty_w - mstrpc_w) // 2) - 1)}{' ' * (((self.texoty_w - mstrpc_w) // 2) - 2)}{'║'}")
            else:
                self.priont_string(f"{'║'}{' ' * (self.texoty_w - 2)}{'║'}")

    def clear_add_header(self, header_msg="", right_status=None, bottom_status=None):
        """ Clear Texoty display and replace the header. """
        self.delete("0.0", 'end')
        self.set_header(header_msg, right_status=right_status, bottom_status=bottom_status)

    def clear_no_header(self, fillIt=False, fill_space=" "):
        """ Clear Texoty display and do not replace the header. """
        self.delete("0.0", 'end')
        if fillIt:
            for h in range(self.texoty_h):
                self.insert(END, fill_space * self.texoty_w)

    def priont_dict(self, dioct: dict, parent_key=None):
        """
        Iterate through a dictionary and display each key/value pair.

        :param parent_key: The parent key in a nested dictionary.
        :param dioct: Dictionary to iterate through.
        """
        for key, value in dioct.items():
            if parent_key:
                prefix = (" " * len(parent_key)) + "⠈⠘⠸⡇"[parent_key.count(".") % 5]
                whole_key = parent_key+"."+key
            else:
                prefix = ''
                whole_key = key
            self.priont_string(f'{prefix}{key}┐')

            if isinstance(dioct[key], list):  # LIST
                self.priont_list(dioct[key], parent_key=whole_key)
            elif isinstance(dioct[key], texity.Command):  # COMMAND
                self.priont_command_lite(dioct[key])
            elif isinstance(dioct[key], dict):  # DICT
                self.priont_dict(dioct[key], parent_key=whole_key)
            else:
                self.priont_string(f'{" " * len(whole_key)}└{dioct[key]}')

    def priont_command_lite(self, command: texity.Command):
        """
        Display a command with its lite description.
        :param command:
        :return:
        """
        self.priont_command_colorized(f'\n{command.name}╕', command.font_color, command.back_color)
        help_message_text = f'{" "*len(command.name)}╘► {command.lite_desc}'
        self.priont_command_colorized(help_message_text, command.font_color, command.back_color)
        self.yview(END)

    def priont_command_midd(self, command: texity.Command):
        """
        Display a command with its lite description and some extra info.
        """
        self.priont_command_colorized(f'\n{command.name}╕', command.font_color, command.back_color)
        help_message_text = f'{" "*len(command.name)}╘► {command.lite_desc}'
        self.priont_command_colorized(help_message_text, command.font_color, command.back_color)
        self.priont_full_command_desc(command.full_desc)
        rando_examp = random.choice(command.examples)
        self.priont_string('\nClickable examples ➤  ')
        self.priont_click_command(rando_examp, rando_examp)
        self.yview(END)

    def priont_command_full(self, command: texity.Command):
        """
        Display a command with its full description and examples.
        :param command:
        :return:
        """
        self.priont_command_colorized(f'{command.name}╕', command.font_color, command.back_color)
        help_message_text = f'{" " * len(command.name)}└► {command.lite_desc}'
        self.priont_command_colorized(help_message_text, command.font_color, command.back_color)
        usage_message_text = f'\nHow to use─►  {command.usage}\n'
        self.priont_colorized_string(usage_message_text, command.back_color, command.font_color)
        self.priont_string('')
        self.priont_dict(command.args_desc)
        self.priont_string('')
        self.priont_dict(command.possible_args)

        self.priont_string('')
        rando_examp = random.choice(command.examples)
        self.priont_click_command(rando_examp, rando_examp)
        self.priont_break_line()
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
            break_line += random.choice('┉┅')
        self.insert(END, f"\n╫{break_line}╫", 'break_line')

    def helper_tag_break(self, group_tag: str):
        """
        Adds a break line in Texoty with style.
        :return:
        """
        break_line = ""
        helper_shades = '▓▒░'
        help_shade = ''
        for shade in helper_shades:
            help_shade += shade * 7
        bg = self.active_profile.color_theme[2]
        fg = self.active_profile.color_theme[0]
        self.tag_configure('break_line', foreground=fg, background=bg)
        for _ in range(self.texoty_w - 28):
            break_line += random.choice('┉┅')
        self.insert(END, f"\n╫{help_shade}{group_tag} {break_line}╫", 'break_line')


    def priont_foto_option(self, opt_num: int, foto_name: str, foto: PhotoImage):
        self.insert(END, f"{opt_num}- {foto_name} ")
        self.image_create(END, image=foto)
        self.insert(END, '\n')
        self.yview(END)

    def priont_string(self, striong: str, line_index=END):
        """
        Display a string of text at line_index.

        @param line_index: Index of where on the line to insert text.
        @param striong: String to display.
        """
        # self.insert(line_index, striong)
        self.insert(line_index, striong + "\n")
        self.yview(END)

    def tag_area(self, fore_color: str, back_color: str, start_pos: str, end_pos: str):
        tag_name = f'{fore_color}_{random.randint(0, 9999)}'
        self.tag_configure(tag_name, foreground=fore_color, background=back_color)
        self.tag_add(tag_name, start_pos, end_pos)

    def priont_colorized_string(self, striong: str, text_color='', back_color='', start_pos = f'1.0', end_pos='end'):
        tag_name = f'{back_color}_{text_color}_{start_pos}_{end_pos}'
        if tag_name not in self._tag_cache:
            try:
                self.tag_configure(tag_name, foreground=text_color, background=back_color)
            except Exception:
                self.tag_configure(tag_name, foreground=str(text_color), background=str(back_color))
            self._tag_cache.add(tag_name)
        # start_pos = f'1.0'
        # end_pos = f'1.{len(striong)}'
        # self.tag_add(tag_name, start_pos, end_pos)
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
        if tag_name not in self._tag_cache:
            try:
                self.tag_configure(tag_name, foreground=text_color, background=bg_color)
            except Exception:
                self.tag_configure(tag_name, foreground=str(text_color), background=str(bg_color))
            self._tag_cache.add(tag_name)
        start_pos = f'1.0'
        end_pos = f'1.{len(striong)}'
        self.tag_add(tag_name, start_pos, end_pos)
        self.insert(END, striong, tag_name)
        self.insert(END, '\n')
        self.yview(END)

    def priont_int(self, iont: int, parent_key=None):
        """
        Display an integer on texoty.
        :param parent_key: If the integer is from a dictionary.
        :param iont: Integer for displaying.
        :return:
        """
        leading_spaces = " " * len(parent_key)
        self.priont_string(f'{leading_spaces}└{iont}')

    def priont_float(self, flioat: float, parent_key=None):
        """
        Display a float.
        :param parent_key: If the float is in a dictionary.
        :param flioat: The float to display.
        :return:
        """
        leading_spaces = " " * len(parent_key)
        self.priont_string(f'{leading_spaces}└{flioat}')

    def priont_full_command_desc(self, desc_list: list):
        for item in desc_list:
            self.priont_string(f' -{item}')

    def priont_list(self, items: list, parent_key=None, numbered=False):
        """
        Display a list of items on texoty, each item in the list on its own line.

        @param items:
        @param list_key:
        @param parent_key:
        @param numbered:
        """

        if parent_key:
            leading_spaces = " " * len(parent_key)
        else:
            leading_spaces = ""

        if parent_key:
            # self.priont_string(parent_key + "┐")
            for item in items:
                prefix = "└" if items.index(item) == len(items) - 1 else "├"
                if numbered:
                    prefix = str(items.index(item)) + prefix
                if isinstance(item, str) and item.startswith('http'):
                    self.priont_hyperlink("Click Me", item)
                else:
                    self.priont_string(f'{leading_spaces}{prefix}{item}')
        else:
            for item in items:
                prefix = "└" if items.index(item) == len(items) - 1 else "├"
                if numbered:
                    prefix = str(items.index(item)) + prefix
                if isinstance(item, str) and item.startswith('http'):
                    self.priont_hyperlink("Click Me", item)
                else:
                    self.priont_string(f'{leading_spaces}{prefix}{item}')


    def set_text_on_line(self, line_number: int, text: str):
        """
        Insert plain basic text on the line_number line.
        :param line_number: Line to insert text.
        :param text: Text to insert at the beginning of line_number.
        :return:
        """
        line_start_index = f"{line_number}.0"
        line_end_index = f"{line_number}.end"
        self.delete(line_start_index, line_end_index)
        self.insert(line_start_index, self._fit_header_text(text, self.texoty_w))
