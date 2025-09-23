import os
import tkinter as tk
import texioty
import subprocess
import threading

from gaims.gaim_runner import GaimRegistry
from spell_depicter import SpellDepicter
from prompt_runner import PromptRunner
from gaims import casino, candy_slinger, hangman
from utils import check_file_exists


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
        spell_depicter = SpellDepicter(self.txty.texoty, self.txty.texity)
        prompt_runner = PromptRunner(self.txty.texoty, self.txty.texity)
        gaim_registry = GaimRegistry(self.txty.texoty, self.txty.texity)
        gaim_registry.add_available_game("hangman", hangman.HangmanRunner(self.txty.texoty, self.txty.texity))
        gaim_registry.add_available_game("casino", casino.CasinoRunner(self.txty.texoty, self.txty.texity))
        gaim_registry.add_available_game("candy_slinger", candy_slinger.CandySlingerRunner(self.txty.texoty, self.txty.texity))
        self.txty.add_helper_widget("DPCT", spell_depicter)
        self.txty.add_helper_widget("PRUN", prompt_runner)
        self.txty.add_helper_widget("GAIM", gaim_registry)
        self.widget_dict = {
            "TXTY": self.txty,
            "DPCT": spell_depicter,
            "PRUN": prompt_runner,
            "GAIM": gaim_registry
        }
        self.txty.grid()
        # Get the user from the OS and attempt to log them into Texioty.
        linux_user = os.getcwd().split("/")[2]
        if check_file_exists(f'.profiles/{linux_user}.json'):
            # self.txty.log_profile_in([linux_user, "1631"])
            pass
        else:
            self.txty.helper_dict["PRUN"][0].prompt_texioty_profile()
            

if __name__ == '__main__':
    root = tk.Tk()

    root.configure(background='#0f6faa')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = Application(screen_width, screen_height, master=root)
    app.mainloop()
