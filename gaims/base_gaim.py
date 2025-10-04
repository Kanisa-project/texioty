import settings as s
from helpers import tex_helper
import theme as t
import json
import os
import tempfile
from datetime import datetime

SAVE_DIR = "gaims/gaim_saves"

class BaseGaim(tex_helper.TexiotyHelper):
    def __init__(self, txo, txi, game_name: str):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.game_name = game_name
        self.gaim_prefix = ''
        self.gaim_commands = {
            "new": [self.new_game, f"Create a new game of {game_name}.",
                      {}, "GAIM", s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)],
            "load": [self.load_game, f"Load a {game_name} saved game.",
                      {}, "GAIM", s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)],
            "save": [self.save_game, f"Save a {game_name} game.",
                      {}, "GAIM", s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)],
            "stop": [self.stop_game, f"Stop playing {game_name}.",
                      {}, "GAIM", s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)]
        }
        self.texioty_commands = {}
        self.game_state = {}

    def new_game(self, args):
        self.txo.priont_string(f"Starting a new {self.game_name} game.")
        if '--new' in args:
            pass
        else:
            self.txo.priont_string("Are you sure you want to start a new game?")

    def save_game(self, args):
        """Save this profile progress of this gaim to a file."""
        game_state = args[0]
        os.makedirs(SAVE_DIR, exist_ok=True)
        filename = f"{sanitize_filename(self.game_name+'_'+game_state['player_name'])}.json"
        path = os.path.join(SAVE_DIR, filename)

        payload = {
            "version": 1,
            "player_name": game_state['player_name'],
            "created_at": game_state.get('created_at', datetime.now().isoformat() + "Z"),
            "updated_at": datetime.now().isoformat() + "Z",
            "game_state": game_state
        }

        fd, tmp_path = tempfile.mkstemp(dir=SAVE_DIR)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, path)
            self.txo.priont_string(f"Saved game to {path}.")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return path

    def load_game(self, args):
        player_name = args[0]
        filename = f"{self.game_name}_{sanitize_filename(player_name)}.json"
        path = os.path.join(SAVE_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                game_state = json.load(f)
            return game_state["game_state"]
        else:
            self.txo.priont_string(f"No saved game found for {player_name}.")
            return None

    def welcome_message(self, args):
        """Generic welcoming message."""
        self.txo.clear_add_header(f"{self.game_name}")
        self.txo.priont_string(f'Welcome to {self.game_name}!')

    def display_help_message(self, args):
        """Generic help message."""
        self.txo.priont_string("Using the 'commands' command will display a list of available commands.")
        self.txo.priont_string("Using the 'welcome' command will show the welcome message and some directions.")


    def display_available_commands(self, args):
        super().display_available_commands(args)

    def stop_game(self, args):
        txty = self.txo.master
        print("STOPPING")
        txty.default_mode()
        txty.active_helper_dict['GAIM'][0].current_gaim = None

def sanitize_filename(filename: str) -> str:
    return ''.join(c for c in filename if c.isalnum() or c in ("_", "-")).rstrip()