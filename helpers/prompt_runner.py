import os
import random
import tkinter as tk
from typing import Callable

from helpers import tex_helper
import texity
import texoty
from settings import themery as t, utils as u

MAIN_OPTIONS = ["launcher>Gaim",
                "Discord.botty",
                "laser%tag$RUN",
                "TCG__[labrat]",
                "foto(FUNCS{})",
                "Profile/-make"]

GAIM_OPTIONS = ['PyLanes', 'kPaint', 'ThurBo', 'Othaido', 'spaceDits']
KBOT_OPTIONS = ['Config', 'Launch']
LASERTAG_OPTIONS = ['Start lobby', 'Edit config']
TCG_OPTIONS = ['Magic the Gathering', 'Pokemon', 'Lorcana', 'Yu-Gi-Oh', 'Digimon', 'All']

LAB_OPTIONS = ['Depictinator{}',
               'Card%Puzzler()',
               'TC-Blender 690',
               'Card-0wn1oad3r',
               'RanDexter-2110']

FUNCFOTO_OPTIONS = ['Flatop_XT 2200',
                    'S/p/licer R0T8',
                    'Deep-friar 420',
                    'Pixtruderer V3']

PROFILE_OPTIONS = ['kanisa',
                   'texioty',
                   'laser_tag',
                   'view_profiles']



class PromptRunner(tex_helper.TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.in_questionnaire_mode = False
        self.in_decisioning_mode = False
        self.question_prompt_dict = {}
        self.response_dict = {}
        self.question_keys = []
        self.current_question_index = 0
        self.helper_commands = {
            "tcg_lab": [self.tcg_lab_functions, "Enter the TCG lab.",
                        {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)],
            "foto_worx": [self.foto_worxhop, "Work in the foto hop.",
                          {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)],
            "profile_make": [self.profile_maker, "Make some type of profile.",
                             {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)]}

    def tcg_lab_functions(self):
        self.decide_decision("What lab would you like to work in", LAB_OPTIONS, 'tcg_lab')
        if self.txo.master.deciding_function is None:
            self.txo.master.deciding_function = self.laboratory

    def laboratory(self, lab_funcs: str):
        self.decide_decision("Which TCG for experimenting", TCG_OPTIONS, lab_funcs.lower())
        match lab_funcs:
            case 'Depictinator{}':
                self.decide_decision("Which profile to depict with ", TCG_OPTIONS, 'depict')
                if self.txo.master.deciding_function is None:
                    self.txo.master.deciding_function = self.depictinator
            case 'Card%Puzzler()':
                pass
            case 'TC-Blender 690':
                pass
            case 'Card-0wn1oad3r':
                pass
            case 'RanDexter-2110':
                pass

    def depictinator(self, tcg_choice: str):
        self.decide_decision(f"Which profile to use for depiction", [], tcg_choice)
        if self.txo.master.deciding_function is None:
            self.txo.master.deciding_function = self.create_depiction

    def create_depiction(self, profile_dict: dict):
        pass

    def foto_worxhop(self):
        self.decide_decision("What lab would you like to work in", FUNCFOTO_OPTIONS, 'foto_worxhop')

    def profile_maker(self):
        self.display_title('profile_make')

    def start_question_prompt(self, question_dict: dict, clear_txo=False):
        """
        Checks if Textioty is already in a questionnaire prompt. If not, sets up the first question and starts the
        prompt to receive answers. Anything typed and sent in Texity will be saved as answers for the prompt questions.
        :param question_dict: Dictionary of questions, consider making a dataclass.
        :param clear_txo: Clears the Texioty header before starting the questionnaire prompt.
        :return:
        """
        if clear_txo:
            self.txo.clear_add_header()
        if not self.in_questionnaire_mode:
            self.question_prompt_dict = question_dict
            self.response_dict = question_dict
            self.question_keys = list(question_dict.keys())
            self.in_questionnaire_mode = True
            self.current_question_index = 0
            self.display_question()
        else:
            self.txo.priont_string("Already in a questionnaire prompt.")
            self.display_question()

    def display_option_question(self, entitled: str, question: str, avail_options: list):
        """
        Display a question with a list of options.

        """
        self.in_decisioning_mode = True
        self.txo.master.change_current_mode("Decisioning", self.helper_commands)
        self.txo.clear_no_header()
        self.txi.current_possible_options = avail_options
        for i in range(self.txo.texoty_h-len(avail_options)):
            self.txo.priont_string(' '*(self.txo.texoty_w-2)+'\n')
        self.display_title(entitled, False)
        for i, option in enumerate(avail_options):
            self.txo.priont_string(f"{i} - {option}")
        self.txo.priont_string(question)
        self.txi.bind_new_options(avail_options)
        return 0

    def display_question(self, options=()):
        """Displays a question from the loaded questionnaire prompt dictionary."""
        if self.current_question_index < len(self.question_keys):
            question_key = self.question_keys[self.current_question_index]
            question = self.question_prompt_dict[question_key][0]
            for i in range(self.txo.texoty_h-3):
                self.txo.priont_string(' -')
            self.txo.insert(tk.END, question)
            self.txo.priont_string(f"[{self.question_prompt_dict[question_key][2]}]")
            # self.txi.command_string_var.set(f"[{self.question_prompt_dict[question_key][2]}]  ›")
            self.txi.icursor(tk.END)
        else:
            self.end_question_prompt(self.response_dict)
            self.txo.master.default_mode()

    def end_question_prompt(self, question_dict: dict) -> dict:
        """End the questionnaire prompt and return the results."""
        self.txo.priont_string("Prompt ended, here are the results: ")
        self.txo.priont_dict(question_dict)
        self.in_questionnaire_mode = False
        # self.response_dict = question_dict
        print(self.response_dict)
        self.response_dict['confirming_function'][3](self.response_dict['confirming_function'][1])
        return question_dict

    def store_response(self, answer: str):
        """ Store the response in the questionnaire dictionary and advance to the next question."""
        question_key = self.question_keys[self.current_question_index]
        if answer == "":
            answer = self.question_prompt_dict[question_key][2]
            self.txo.priont_string("|>  " + answer + " (Default)")
        else:
            self.txo.priont_string("|>  " + answer)
        self.response_dict[question_key][1] = answer

        self.current_question_index += 1
        self.display_question()

    def prompt_texioty_profile(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt(
                {"profile_name": [f"What to name the profile?", "", os.getcwd().split('/')[2]],
                 "password": [f"What to use for password?", "", str(random.randint(1000, 9999))],
                 "color_theme": ["Which color theme to use?", "", random.choice(['bluebrrryy dark', 'bluebrrryy light',
                                                                                 'nulbrrryyy dark', 'nulbrrryyy light'])],
                 "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile]},
                clear_txo=True)

    def decide_decision(self, input_question: str, possible_options: list, titled='basic'):
        """
        List each item in possible_options with its number for usage.
        :param titled:
        :param input_question: Question to make a decision on.
        :param possible_options: All options for the question.
        :return: String
        """
        self.txi.isDecidingDecision = True
        self.display_option_question(titled,
                                     input_question + f", (0-{len(possible_options) - 1})? ",
                                     possible_options)

