import os
import tkinter as tk
import texioty

from helpers.digiary import Digiary
from helpers.registries.api_registry import ApiRegistry
from helpers.registries.gaim_registry import GaimRegistry
from helpers.registries.help_registry import HelpRegistry
from helpers.registries.prompt_registry import PromptRegistry
from settings.utils import check_file_exists
from settings import konfig as k


# def start_simple_client():
#     client_script_path = "./test_client.py"
#     threading.Thread(target=subprocess.run, args=(["python", client_script_path], )).start()


class Application(tk.Frame):
    def __init__(self, screen_w: int, screen_h: int, master=None):
        """
        Primary application window with all the widgets required.
        :param master:
        """
        super().__init__(master)
        self.txty = texioty.Texioty(width=screen_w, height=screen_h)
        self.available_helpers = {
            "TXTY": self.txty,
            "DIRY": Digiary,
            "GAIM": GaimRegistry,
            "PRUN": PromptRegistry,
            "HLPR": HelpRegistry,
            "HAPI": ApiRegistry
        }
        for group_tag in k.UNLOCKED_HELPERS:
            if group_tag is not "TXTY":
                self.txty.add_helper_widget(group_tag, self.available_helpers[group_tag](self.txty.texoty, self.txty.texity))

        self.txty.grid()
        # Get the user from the OS and attempt to log them into Texioty.
        linux_user = os.getcwd().split("/")[2]
        if check_file_exists(f'filesOutput/.profiles/{linux_user}.json'):
            # self.txty.log_profile_in([linux_user, "1631"])
            pass
        else:
            self.txty.active_helper_dict["PRUN"][0].profilemake.prompt_texioty_profile()


if __name__ == '__main__':
    root = tk.Tk()

    root.configure(background='#0f6faa')
    if not k.hasTitleBar:
        root.attributes('-type', "splash")
    root.attributes('-fullscreen', k.isFullscreen)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = Application(screen_width, screen_height, master=root)
    app.mainloop()
    # app.PijunCooper.watcher.stop()
