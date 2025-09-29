import settings as s
import tex_helper
import theme as t

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

    def new_game(self, args):
        self.txo.priont_string(f"Starting a new {self.game_name} game.")

    def load_game(self, args):
        pass

    def save_game(self, args):
        pass

    def welcome_message(self, args):
        self.txo.clear_add_header(f"{self.game_name}")
        self.txo.priont_string(f'Welcome to {self.game_name}!')

    def display_help_message(self, args):
        pass

    def display_available_commands(self, args):
        super().display_available_commands(args)

    def stop_game(self, args):
        txty = self.txo.master
        print("STOPPING")
        txty.default_mode()
        txty.helper_dict['GAIM'][0].current_gaim = None
