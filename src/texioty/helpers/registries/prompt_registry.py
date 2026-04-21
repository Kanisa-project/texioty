from typing import Callable

from src.texioty.core import texity, texoty
from src.texioty.helpers.apis.arc_api import ArcApi
from src.texioty.helpers.promptaires.tcg_lab.tcg_labby import TCGLabby
from src.texioty.helpers.tex_helper import TexiotyHelper
from src.texioty.helpers.promptaires.worx_hop.foto_worx import FotoWorxHop
from src.texioty.helpers.promptaires.profilizer.profilizer import Profilizer
from src.texioty.helpers.registries.command_definitions import (TEXIOTY_COMMANDS, PROMPT_COMMANDS, DIRY_COMMANDS,
                                                                bind_commands, merge_command_groups)

LAB_OPTIONS = ['Card-0wn1oad3r',
               'Depictinator{}',
               'Card%Puzzler(]',
               'TC-Blender 690',
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
    """
    A registry of promptaires for many different tasks grouped by a common theme/goal.
    """
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.tcg_lab = TCGLabby(txo, txi)
        self.foto_worx = FotoWorxHop(txo, txi)
        self.profilemake = Profilizer(txo, txi)
        self.arc_api = ArcApi(txo, txi)
        all_prompt_commands = merge_command_groups(PROMPT_COMMANDS, DIRY_COMMANDS, TEXIOTY_COMMANDS)
        self.helper_commands = bind_commands(all_prompt_commands,{
            'tcg_lab': self.decide_tcg_lab,
            'foto_worx': self.start_worxhop_prompt,
            'profile_make': self.start_profiler_prompt
        })
        self.in_questionnaire_mode = False
        self.current_prompt = "N/A"

    def _set_deciding_function(self, func: Callable) -> None:
        if self.txo.master.deciding_function is None or callable(self.txo.master.deciding_function):
            self.txo.master.deciding_function = func

    def decide_tcg_lab(self):
        self.tcg_lab.decide_decision("What lab would you like to work in", LAB_OPTIONS, 'tcg_lab')
        self._set_deciding_function(self.tcg_lab.laboratory)

    def start_worxhop_prompt(self):
        self.foto_worx.decide_decision("What station to work in", FUNCFOTO_OPTIONS, 'worx_hop')
        self._set_deciding_function(self.foto_worx.worxhop_stations)

    def start_profiler_prompt(self):
        self.profilemake.decide_decision("What kind of profile to make", PROFILIZER_OPTIONS, "profilizer")
        self._set_deciding_function(self.profilemake.profile_make)
