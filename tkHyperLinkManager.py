# Sourced from effbot.org

from tkinter import *


class HyperlinkManager:

    def __init__(self, txo):

        self.links = {}
        self.txo = txo

        self.txo.tag_config("hyper", foreground="blue", underline=1)

        self.txo.tag_bind("hyper", "<Enter>", self._enter)
        self.txo.tag_bind("hyper", "<Leave>", self._leave)
        self.txo.tag_bind("hyper", "<Button-1>", self._click)

        self.txo.tag_config("command", foreground="darkblue", underline=1, background="lightblue")

        self.txo.tag_bind("command", "<Enter>", self._enter)
        self.txo.tag_bind("command", "<Leave>", self._leave)
        self.txo.tag_bind("command", "<Button-1>", self._click_cmd)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated txo widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def add_cmd(self, action):
        # add an action to the manager.  returns tags to use in
        # associated txo widget
        tag = "command-%d" % len(self.links)
        self.links[tag] = action
        return "command", tag

    def _enter(self, event):
        self.txo.config(cursor="hand2")

    def _leave(self, event):
        self.txo.config(cursor="")

    def _click(self, event):
        for tag in self.txo.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

    def _click_cmd(self, event):
        for tag in self.txo.tag_names(CURRENT):
            if tag[:8] == "command-":
                self.links[tag]()
                return
