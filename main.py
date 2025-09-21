import os
import tkinter as tk
import texioty
import subprocess
import threading
from spell_depicter import SpellDepicter

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
        self.texioty_frame = texioty.Texioty(width=screen_w//3, height=screen_h*.93)
        spell_depicter = SpellDepicter(width=100, height=100, master=self)
        self.texioty_frame.add_helper_widget("SPLD", spell_depicter)
        self.widget_dict = {
            "TXTY": self.texioty_frame,
            "SPLD": spell_depicter
        }
        self.texioty_frame.grid()
        linux_user = os.getcwd().split("/")[2]
        self.texioty_frame.log_profile_in([linux_user, "p455"])

if __name__ == '__main__':
    root = tk.Tk()

    root.configure(background='#0f6faa')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = Application(screen_width, screen_height, master=root)
    app.mainloop()
