import os
import tkinter as tk
import texioty

from helpers.registry_manager import HelperRegistry, HelperConfig
from helpers.promptaires.digiary.digiary import Digiary
from helpers.registries.gaim_registry import GaimRegistry
from helpers.registries.prompt_registry import PromptRegistry
from settings.utils import check_file_exists
from settings import konfig as k



class Application(tk.Frame):
    def __init__(self, screen_w: int, screen_h: int, master=None):
        """
        Primary application window with all the widgets required.
        :param master:
        """
        super().__init__(master)
        self.helper_registry = HelperRegistry()
        self._register_helpers()
        self.txty = texioty.Texioty(width=screen_w, height=screen_h, helper_registry=self.helper_registry)

        self.helper_registry.initialize_all(
            self.txty.texoty, self.txty.texity,
            config_tags=k.UNLOCKED_HELPERS
        )
        for tag in k.UNLOCKED_HELPERS:
            self.txty.register_helper_commands(tag)
        self.txty.grid()

        # Get the user from the OS and attempt to log them into Texioty.
        linux_user = os.getcwd().split("/")[2]
        if check_file_exists(f'filesOutput/.profiles/{linux_user}.json'):
            self.txty.log_profile_in(linux_user, "1802")
            pass
        else:
            pass
            # self.txty.active_helper_dict["PRUN"][0].profilemake.prompt_texioty_profile()

    def _register_helpers(self):
        """Register all available helpers in the registry."""
        self.helper_registry.register(HelperConfig(
            tag="DIRY",
            class_ref=Digiary,
            priority=1,
            enabled=True,
            dependencies=[]
        ))
        self.helper_registry.register(HelperConfig(
            tag="PRUN",
            class_ref=PromptRegistry,
            priority=1,
            enabled=True,
            dependencies=[]
        ))
        self.helper_registry.register(HelperConfig(
            tag="GAIM",
            class_ref=GaimRegistry,
            priority=2,
            enabled=True,
            dependencies=["PRUN"]
        ))




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