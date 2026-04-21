from src.texioty.settings import themery as t, utils as u

from src.texioty.helpers.tex_helper import TexiotyHelper

from src.texioty.helpers.gaims.hangman import HangmanRunner
from src.texioty.helpers.gaims.casino import CasinoRunner
from src.texioty.helpers.gaims.candy_slinger import CandySlingerRunner
from src.texioty.helpers.gaims.boston_trail import BostonTrailRunner
from src.texioty.helpers.gaims.battleship import BattleshipRunner


class GaimRegistry(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_game = False
        self.available_games = {"hangman": HangmanRunner,
                                "casino": CasinoRunner,
                                "slinger": CandySlingerRunner,
                                "trailin": BostonTrailRunner,
                                "battleship": BattleshipRunner}
        self.helper_commands["start"] = {
                "name": "start",
                "usage": '"start [GAME_NAME]"',
                "call_func": self.start_game,
                "lite_desc": "Start a text based game.",
                "full_desc": ["Start a text based game."],
                "possible_args": self.available_games,
                "args_desc": {"[GAME_NAME]": "Name of the game engine to start."},
                "examples": ['start hangman', 'start slinger'],
                "group_tag": "GAIM",
                "font_color": u.rgb_to_hex(t.GREEN),
                "back_color": u.rgb_to_hex(t.BLACK)
        }
        self.current_gaim = None

    def reset_game_session(self):
        self.in_game = False
        self.current_gaim = None


    def start_game(self, args):
        print('start_args', args)
        if isinstance(args, list):
            args = args[0] if args else None

        if args not in self.available_games:
            self.txo.priont_string(f"Invalid game name: {args}")
            return

        if self.current_gaim is not None:
            self.txo.priont_string("A game is already in progress.")
            return
        self.in_game = True
        self.current_gaim = self.available_games[args](self.txo, self.txi)
        self.current_gaim.new_game()
        self.txo.master.change_current_mode(
            "Gaim",
            self.current_gaim.gaim_commands | self.current_gaim.helper_commands)
        print("Game started.")
