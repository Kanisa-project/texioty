import settings as s
import tex_helper
import theme as t


class BaseGaim(tex_helper.TexiotyHelper):
    def __init__(self, txo, txi, game_name: str):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.game_name = game_name
        self.gaim_commands = {
            "new": [self.new_game, f"Create a new game of {game_name}.",
                      {}, [], s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)],
            "load": [self.load_game, f"Load a {game_name} saved game.",
                      {}, [], s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)],
            "save": [self.save_game, f"Save a {game_name} game.",
                      {}, [], s.rgb_to_hex(t.ALICE_BLUE), s.rgb_to_hex(t.BLACK)]
        }
        self.texioty_commands = {}

    def new_game(self):
        pass

    def load_game(self):
        pass

    def save_game(self):
        pass


class GaimRegistry(tex_helper.TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_game = False
        self.available_games = {}
        self.texioty_commands = {
            "start": [self.start_game, "Start a text based game.",
                      {"hangman": "Play hangman.",
                       "casino": "Play casino games.",
                       "slinger": "Play candy slinger."},
                      [], s.rgb_to_hex(t.GREEN), s.rgb_to_hex(t.BLACK)],
            "stop": [self.stop_game, "Stop the current text based game.",
                     {},[], s.rgb_to_hex(t.RED), s.rgb_to_hex(t.BLACK)]
        }

    def add_available_game(self, game_name: str, gaim_object: BaseGaim):
        pass

    def start_game(self, args):
        pass

    def stop_game(self, args):
        pass