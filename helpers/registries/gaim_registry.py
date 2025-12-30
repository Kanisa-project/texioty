from settings import themery as t, utils as u, konfig as k

from helpers.tex_helper import TexiotyHelper

from helpers.gaims.hangman import HangmanRunner
from helpers.gaims.casino import CasinoRunner
from helpers.gaims.candy_slinger import CandySlingerRunner
from helpers.gaims.boston_trail import BostonTrail


class GaimRegistry(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_game = False
        self.available_games = {"hangman": HangmanRunner,
                                # "casino": CasinoRunner,
                                "slinger": CandySlingerRunner,
                                "trailin": BostonTrail}
        self.helper_commands = {
            "start": {"name": "start",
                      "usage": '"start [GAME_NAME]"',
                      "call_func": self.start_game,
                      "lite_desc": "Start a text based game.",
                      "full_desc": ["Start a text based game."],
                      "possible_args": self.available_games,
                      "args_desc": {"[GAME_NAME]": "Name of the game engine to start."},
                      "examples": ['start hangman', 'start slinger'],
                      "group_tag": "GAIM",
                      "font_color": u.rgb_to_hex(t.GREEN),
                      "back_color": u.rgb_to_hex(t.BLACK)}
        }
        self.current_gaim = None

    def start_game(self, args):
        print('start_args', args)
        if args in list(self.available_games.keys()) and self.current_gaim is None:
            self.in_game = True
            print('in_game', self.in_game, self.current_gaim)
            self.current_gaim = self.available_games[args](self.txo, self.txi)
            print('current_gaim', self.current_gaim)
            self.current_gaim.new_game()
            # help_symb = self.available_games[args[0]][1]
            k.UNLOCKED_HELPERS.append("HMAN")
            self.txo.master.change_current_mode("Gaim",
                                                self.current_gaim.gaim_commands | self.current_gaim.helper_commands)
        print("Game started.")
