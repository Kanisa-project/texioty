from typing import Callable

from src.texioty.core import texity, texoty
from src.texioty.helpers.apis.arc_api import ArcApi
from src.texioty.helpers.kanisa_wallet import KanisaWallet
from src.texioty.helpers.promptaires.beep_boop.beep_boops import BeepBoops
from src.texioty.helpers.promptaires.tcg_lab.tcg_labby import TCGLabby
from src.texioty.helpers.tex_helper import TexiotyHelper
from src.texioty.helpers.promptaires.worx_hop.foto_worx import FotoWorxHop
from src.texioty.helpers.promptaires.profilizer import Profilizer
from src.texioty.helpers.registries.command_definitions import (TEXIOTY_COMMANDS, PROMPT_COMMANDS, DIRY_COMMANDS,
                                                                bind_commands, merge_command_groups)

LAB_OPTIONS = ['Depictinator{}',
               'Card%Puzzler(]',
               'TC-Blender 690',
               'Card-0wn1oad3r',
               'RanDexter-2110']

FUNCFOTO_OPTIONS = ['Flatop_XT 2200',
                    'S/p/licer R0T8',
                    'Deep-friar 420',
                    'Pixtruderer V3',
                    'Tix>Prit C.R.1',
                    '[)UtchOven 650',
                    'Mix-n-Stir 816']

PROFILIZER_OPTIONS = ['users',
                      'foto_worx',
                      'tcg_lab',
                      'beop_boeps',
                      'word_gaims']

class PromptRegistry(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.tcg_lab = TCGLabby(txo, txi)
        self.foto_worx = FotoWorxHop(txo, txi)
        self.profilemake = Profilizer(txo, txi)
        self.k_wallet = KanisaWallet(txo, txi)
        self.arc_api = ArcApi(txo, txi)
        self.beep_boops = BeepBoops(txo, txi)
        all_prompt_commands = merge_command_groups(PROMPT_COMMANDS, DIRY_COMMANDS, TEXIOTY_COMMANDS)
        self.helper_commands = bind_commands(all_prompt_commands,{
            'welcome': self.welcome_message,
            'help': self.display_help_message,
            'commands': self.display_all_available_commands,
            'tcg_lab': self.start_tcg_lab_prompt,
            'foto_worx': self.start_worxhop_prompt,
            'profile_make': self.start_profiler_prompt
        })
        self.in_questionnaire_mode = False
        self.current_prompt = "N/A"

    def start_tcg_lab_prompt(self):
        self.tcg_lab.decide_decision("What lab would you like to work in", LAB_OPTIONS, 'tcg_lab')
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.tcg_lab.laboratory

    def start_worxhop_prompt(self):
        self.foto_worx.decide_decision("What station to work in", FUNCFOTO_OPTIONS, 'worx_hop')
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.foto_worx.worxhop_stations

    def start_profiler_prompt(self):
        self.profilemake.decide_decision("What kind of profile to make", PROFILIZER_OPTIONS, "profilizer")
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.profilemake.profile_make
