from settings import themery as t, utils as u

from helpers.tex_helper import TexiotyHelper

from gaims.hangman import HangmanRunner
from gaims.casino import CasinoRunner
from gaims.candy_slinger import CandySlingerRunner


class GaimRegistry(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_game = False
        self.available_games = {"hangman": HangmanRunner,
                                "casino": CasinoRunner,
                                "slinger": CandySlingerRunner}
        self.helper_commands = {
            "start": [self.start_game, "Start a text based game.",
                      self.available_games, "GAIM",
                      u.rgb_to_hex(t.GREEN), u.rgb_to_hex(t.BLACK)]
        }
        self.current_gaim = None

    def start_game(self, *args):
        if args[0] in list(self.available_games.keys()) and self.current_gaim is None:
            self.in_game = True
            self.current_gaim = self.available_games[args[0]](self.txo, self.txi)
            self.current_gaim.new_game()
            # help_symb = self.available_games[args[0]][1]
            self.txo.master.change_current_mode("Gaim",
                                                self.current_gaim.gaim_commands | self.current_gaim.helper_commands)
