import os
import random
import tkinter as tk
import tex_helper
import texity
import texoty

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
LAB_OPTIONS = ['Card%Puzzler()',
               'Card-0wn1oad3r',
               'RanDexter-2110']
FUNCFOTO_OPTIONS = ['Depictinator{}',
                    'TC-Blender 690',
                    'Deep-friar 420']
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
        self.question_prompt_dict = {}
        self.response_dict = {}
        self.question_keys = []
        self.current_question_index = 0
        self.texioty_commands = {}

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
            # for key in self.question_keys:
            #     self.response_dict[key] = [None, None, None, question_dict[key][3]]
            self.in_questionnaire_mode = True
            self.current_question_index = 0
            self.display_question()
        else:
            self.txo.priont_string("Already in a questionnaire prompt.")
            self.display_question()

    def display_option_question(self, avail_options: list):
        for i in range(self.txo.texoty_h-len(avail_options)):
            self.txo.priont_string(' '*(self.txo.texoty_w-2)+'\n')
        for i, option in enumerate(avail_options):
            self.txo.priont_string(f"{i} - {option}")

    def display_question(self, options=[]):
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

    def run_skrypto(self, args):
        self.display_option_question(MAIN_OPTIONS)

    def prompt_texioty_profile(self):
        self.start_question_prompt(
                {"profile_name": [f"What to name the profile?", "", os.getcwd().split('/')[2]],
                 "password": [f"What to use for password?", "", str(random.randint(1000, 9999))],
                 "color_theme": ["Which color theme to use?", "", random.choice(['bluebrrryy dark', 'bluebrrryy light',
                                                                                 'nulbrrryyy dark', 'nulbrrryyy light'])],
                 "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile]},
                clear_txo=True)

    def check_question_confirmation(self, answer: str):
        if self.response_dict['confirming_function'][1] == 'yes':
            pass