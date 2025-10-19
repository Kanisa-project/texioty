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
            "tcg_lab": [self.tcg_lab_prompt, "Enter the TCG lab.",
                        {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)],
            "foto_worx": [self.worxhop_prompt, "Work in the foto hop.",
                          {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)],
            "profile_make": [self.profiler_prompt, "Make some type of profile.",
                             {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)]}

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
