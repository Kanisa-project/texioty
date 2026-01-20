from typing import Callable

import texity
import texoty
from helpers.apis.arc_api import ArcApi
from helpers.kanisa_wallet import KanisaWallet
from helpers.promptaires.beep_boop.beep_boops import BeepBoops
from helpers.promptaires.tcg_lab.tcg_labby import TCGLabby
from helpers.tex_helper import TexiotyHelper
from settings import themery as t, utils as u
from helpers.promptaires.worx_hop.foto_worx import FotoWorxHop
from helpers.promptaires.profilizer import Profilizer

LAB_OPTIONS = ['Depictinator{}',
               'Card%Puzzler(]',
               'TC-Blender 690',
               'Card-0wn1oad3r',
               'RanDexter-2110']

FUNCFOTO_OPTIONS = ['Flatop_XT 2200',
                    'S/p/licer R0T8',
                    'Deep-friar 420',
                    'Pixtruderer V3',
                    'Tix>Prit C.R.1']

PROFILIZER_OPTIONS = ['texioty',
                      'laser-tag',
                      'fotofuncs',
                      'tcg_lab',
                      'beop_boeps'
                      'word_gaims']

ARC_API_OPTIONS = ['items',
                   'quests',
                   'enemies']

class PromptRegistry(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_questionnaire_mode = False
        self.current_prompt = "N/A"
        self.tcg_lab = TCGLabby(txo, txi)
        self.foto_worx = FotoWorxHop(txo, txi)
        self.profilemake = Profilizer(txo, txi)
        self.k_wallet = KanisaWallet(txo, txi)
        self.arc_api = ArcApi(txo, txi)
        self.beep_boops = BeepBoops(txo, txi)
        self.helper_commands = self.helper_commands | self.beep_boops.helper_commands | self.arc_api.helper_commands
        # self.promptaire_dict = {
        #     'tcg_lab': self.tcg_lab,
        #     'foto_worx': self.foto_worx,
        #     'prof_make': self.profilemake,
        #     'ka_wallet': self.k_wallet,
        #     'arc_api': self.arc_api,
        #     'beep_boops': self.beep_boops
        # }
        self.helper_commands["tcg_lab"] = {"name": "tcg_lab",
                        "usage": '"tcg_lab"',
                        "call_func": self.start_tcg_lab_prompt,
                        "lite_desc": "Enter the TCG lab.",
                        "full_desc": ["Enter the TCG lab.",
                                      "Can be used in Texioty mode only."],
                        "possible_args": {' - ': 'No arguments available.'},
                        "args_desc": {' - ': ['No arguments available.', None]},
                        "examples": ['tcg_lab'],
                        "group_tag": "PRUN",
                        "font_color": u.rgb_to_hex(t.KHAKI),
                        "back_color": u.rgb_to_hex(t.BLACK)}
        self.helper_commands["foto_worx"] = {"name": "foto_worx",
                          "usage": '"foto_worx"',
                          "call_func": self.start_worxhop_prompt,
                          "lite_desc": "Work in the foto hop.",
                          "full_desc": ["Work in the foto hop.",],
                          "possible_args": {' - ': 'No arguments available.'},
                          "args_desc": {' - ': ['No arguments available.', None]},
                          "examples": ['foto_worx'],
                          "group_tag": "PRUN",
                          "font_color": u.rgb_to_hex(t.KHAKI),
                          "back_color": u.rgb_to_hex(t.BLACK)}
        self.helper_commands["profile_make"] = {"name": "profile_make",
                             "usage": '"profile_make"',
                             "call_func": self.start_profiler_prompt,
                             "lite_desc": "Make some type of profile.",
                             "full_desc": ["Make some type of profile.",],
                             "possible_args": {' - ': 'No arguments available.'},
                             "args_desc": {' - ': ['No arguments available.', None]},
                             "examples": ['profile_make'],
                             "group_tag": "PRUN",
                             "font_color": u.rgb_to_hex(t.KHAKI),
                             "back_color": u.rgb_to_hex(t.BLACK)}

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
