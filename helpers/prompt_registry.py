import os
import random
import tkinter as tk
from typing import Callable

import texity
import texoty
from helpers.tex_helper import TexiotyHelper
from settings import themery as t, utils as u
from question_prompts.tcg_labby import TCGLabratory
from question_prompts.foto_worx import FotoWorxHop
from question_prompts.profilizer import Profilizer

LAB_OPTIONS = ['Depictinator{}',
               'Card%Puzzler()',
               'TC-Blender 690',
               'Card-0wn1oad3r',
               'RanDexter-2110']

FUNCFOTO_OPTIONS = ['Flatop_XT 2200',
                    'S/p/licer R0T8',
                    'Deep-friar 420',
                    'Pixtruderer V3']

PROFILIZER_OPTIONS = ['texioty',
                      'laser-tag',
                      'fotofuncs',
                      'tcg_lab']

class PromptRegistry(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_questionnaire_mode = False
        self.current_prompt = "N/A"
        self.tcg_lab = TCGLabratory(txo, txi)
        self.foto_worx = FotoWorxHop(txo, txi)
        self.profilemake = Profilizer(txo, txi)
        self.helper_commands = {
            "tcg_lab": {"name": "tcg_lab",
                        "usage": '"tcg_lab"',
                        "call_func": self.tcg_lab_prompt,
                        "lite_desc": "Enter the TCG lab.",
                        "full_desc": ["Enter the TCG lab.",
                                      "Can be used in Texioty mode only."],
                        "possible_args": {' - ': 'No arguments available.'},
                        "args_desc": {' - ': 'No arguments available.'},
                        "examples": ['tcg_lab'],
                        "group_tag": "PRUN",
                        "font_color": u.rgb_to_hex(t.KHAKI),
                        "back_color": u.rgb_to_hex(t.BLACK)},
            "foto_worx": {"name": "foto_worx",
                          "usage": '"foto_worx"',
                          "call_func": self.worxhop_prompt,
                          "lite_desc": "Work in the foto hop.",
                          "full_desc": ["Work in the foto hop.",],
                          "possible_args": {' - ': 'No arguments available.'},
                          "args_desc": {' - ': 'No arguments available.'},
                          "examples": ['foto_worx'],
                          "group_tag": "PRUN",
                          "font_color": u.rgb_to_hex(t.KHAKI),
                          "back_color": u.rgb_to_hex(t.BLACK)},
            "profile_make": {"name": "profile_make",
                             "usage": '"profile_make"',
                             "call_func": self.profiler_prompt,
                             "lite_desc": "Make some type of profile.",
                             "full_desc": ["Make some type of profile.",],
                             "possible_args": {' - ': 'No arguments available.'},
                             "args_desc": {' - ': 'No arguments available.'},
                             "examples": ['profile_make'],
                             "group_tag": "PRUN",
                             "font_color": u.rgb_to_hex(t.KHAKI),
                             "back_color": u.rgb_to_hex(t.BLACK)}}

    def tcg_lab_prompt(self):
        self.tcg_lab.decide_decision("What lab would you like to work in", LAB_OPTIONS, 'tcg_lab')
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.tcg_lab.laboratory

    def worxhop_prompt(self):
        self.foto_worx.decide_decision("What station to work in", FUNCFOTO_OPTIONS, 'worxhop_fotoes')
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.foto_worx.worxhop

    def profiler_prompt(self):
        self.display_title('profile_make')
