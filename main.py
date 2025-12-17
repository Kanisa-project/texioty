import os
import tkinter as tk
import texioty
import subprocess
import threading

from helpers.arc_api import ArcApi
from helpers.gaim_registry import GaimRegistry
from helpers.pijun_cooper import PijunCooper
from helpers.prompt_registry import PromptRegistry
from helpers.tex_helper import TexiotyHelper
from helpers.digiary import Digiary
from settings.utils import check_file_exists


def start_simple_client():
    client_script_path = "./test_client.py"
    threading.Thread(target=subprocess.run, args=(["python", client_script_path], )).start()


class Application(tk.Frame):
    def __init__(self, screen_w: int, screen_h: int, master=None):
        """
        Primary application window with all the widgets required.
        :param master:
        """
        super().__init__(master)
        self.txty = texioty.Texioty(width=screen_w//3, height=screen_h*.93)
        base_helper = TexiotyHelper(self.txty.texoty, self.txty.texity)
        prompt_runner = PromptRegistry(self.txty.texoty, self.txty.texity)
        arcapi = ArcApi(self.txty.texoty, self.txty.texity)
        gaim_registry = GaimRegistry(self.txty.texoty, self.txty.texity)
        digiary = Digiary(self.txty.texoty, self.txty.texity)
        pijun_cooper = PijunCooper(self.txty.texoty, self.txty.texity)
        self.txty.add_helper_widget("HLPR", base_helper)
        self.txty.add_helper_widget("PRUN", prompt_runner)
        self.txty.add_helper_widget("GAIM", gaim_registry)
        self.txty.add_helper_widget("DIRY", digiary)
        self.txty.add_helper_widget("PIJN", pijun_cooper)
        self.txty.add_helper_widget("ARCA", arcapi)

        self.txty.grid()
        # Get the user from the OS and attempt to log them into Texioty.
        linux_user = os.getcwd().split("/")[2]
        if check_file_exists(f'.profiles/{linux_user}.json'):
            # self.txty.log_profile_in([linux_user, "1631"])
            pass
        else:
            self.txty.active_helper_dict["PRUN"][0].prompt_texioty_profile()

def run():
    if __name__ == '__main__':
        rroot = tk.Tk()
        rroot.configure(background='#0f6faa')
        rscreen_width = rroot.winfo_screenwidth()
        rscreen_height = rroot.winfo_screenheight()
        rapp = Application(rscreen_width, rscreen_height, master=root)
        rapp.mainloop()


if __name__ == '__main__':
    root = tk.Tk()

    root.configure(background='#0f6faa')
    # root.wm_attributes("-type", 'splash')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = Application(screen_width, screen_height, master=root)
    app.mainloop()
    # app.PijunCooper.watcher.stop()
