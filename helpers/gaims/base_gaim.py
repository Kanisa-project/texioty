from typing import Optional

from helpers.tex_helper import TexiotyHelper
from settings import themery as t, utils as u
import json
import os
import tempfile
from datetime import datetime

SAVE_DIR = "filesOutput/saved_games/"

class BaseGaim(TexiotyHelper):
    def __init__(self, txo, txi, game_name: str):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.game_name = game_name
        self.gaim_prefix = ''
        self.group_tag = "GAIM"
        self.gaim_commands = {
            "new": {
                "name": "new",
                "usage": "'new'",
                "call_func": self.new_game,
                "lite_desc": f"Create a new game of {game_name}.",
                "full_desc": [],
                "possible_args": {},
                "args_desc": {},
                "examples": [],
                "group_tag": "GAIM",
                "font_color": u.rgb_to_hex(t.ALICE_BLUE),
                "back_color": u.rgb_to_hex(t.BLACK)
            },
            "load": {
                "name": "load",
                "usage": "'load'",
                "call_func": self.load_game,
                "lite_desc": f"Load a {game_name} saved game.",
                "full_desc": [],
                "possible_args": {},
                "args_desc": {},
                "examples": [],
                "group_tag": "GAIM",
                "font_color": u.rgb_to_hex(t.ALICE_BLUE),
                "back_color": u.rgb_to_hex(t.BLACK)
            },
            "save": {
                "name": "save",
                "usage": "'save'",
                "call_func": self.save_game,
                "lite_desc": f"Save a {game_name} game.",
                "full_desc": [],
                "possible_args": {},
                "args_desc": {},
                "examples": [],
                "group_tag": "GAIM",
                "font_color": u.rgb_to_hex(t.ALICE_BLUE),
                "back_color": u.rgb_to_hex(t.BLACK)
            },
            "stop": {
                "name": "stop",
                "usage": "'stop'",
                "call_func": self.stop_game,
                "lite_desc": f"Stop playing {game_name}.",
                "full_desc": [],
                "possible_args": {},
                "args_desc": {},
                "examples": [],
                "group_tag": "GAIM",
                "font_color": u.rgb_to_hex(t.ALICE_BLUE),
                "back_color": u.rgb_to_hex(t.BLACK)}
        }
        self.helper_commands = self.helper_commands | self.gaim_commands
        self.game_state = {}

    def new_game(self):
        self.txo.priont_string(f"Starting a new {self.game_name} game.")

    def save_game(self):
        """Save this profile progress of this gaim to a file."""
        game_state = self.game_state
        os.makedirs(SAVE_DIR, exist_ok=True)
        # filename = f"{sanitize_filename(self.game_name+'_'+game_state['player_name'])}.json"
        filename = f"{self.game_name+'_'+game_state['player_name']}.json"
        path = os.path.join(SAVE_DIR, filename)

        saveload = {
            "version": 1,
            "player_name": game_state['player_name'],
            "created_at": game_state.get('created_at', datetime.now().isoformat() + "Z"),
            "updated_at": datetime.now().isoformat() + "Z",
            "game_state": game_state
        }

        fd, tmp_path = tempfile.mkstemp(dir=SAVE_DIR)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(saveload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, path)
            self.txo.priont_string(f"Saved game to {path}.")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return path

    def load_game(self):
        player_name = self.txo.master.active_profile.username
        filename = f"{self.game_name}_{sanitize_filename(player_name)}.json"
        path = os.path.join(SAVE_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                game_state = json.load(f)
            return game_state["game_state"]
        else:
            self.txo.priont_string(f"No saved game found for {player_name}.")
            return None

    def welcome_message(self, welcoming_msgs: Optional[list] = None):
        """Generic welcoming message."""
        self.txo.clear_add_header(f"{self.game_name}")
        self.txo.priont_string(f'Welcome to {self.game_name}!')

    def display_help_message(self, group_tag: Optional[str] = None):
        """Generic help message."""
        super().display_help_message(group_tag)
        self.txo.priont_string("Using the 'commands' command will display a list of available commands.")
        self.txo.priont_string("Using the 'welcome' command will show the welcome message and some directions.")


    def display_available_commands(self):
        super().display_available_commands()

    def stop_game(self):
        txty = self.txo.master
        print("STOPPING", self.game_name)
        txty.default_mode()
        txty.active_helper_dict['GAIM'][0].current_gaim = None

def sanitize_filename(filename: str) -> str:
    return ''.join(c for c in filename if c.isalnum() or c in ("_", "-")).rstrip()