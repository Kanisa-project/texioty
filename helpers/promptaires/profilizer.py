import os
import random
from typing import Callable

from helpers.promptaires.prompt_helper import BasePrompt


class Profilizer(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.profile_to_make = "Texioty"
        self.word_gaims = [
            "hangman", "word_search", "candy_slinger", "boston_trail"
        ]


    def profile_make(self, profile_type: str):
        match profile_type:
            case 'texioty':
                self.prompt_texioty_profile()
            case 'laser-tag':
                self.prompt_lasertag_profile()
            case 'fotofuncs':
                pass
            case 'tcg_lab':
                pass
            case 'word_gaims':
                self.decide_word_gaims_profile()


    def prompt_texioty_profile(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt(
                {"profile_name": [f"What to name the profile?", "", os.getcwd().split('/')[2]],
                 "password": [f"What to use for password?", "", str(random.randint(1000, 9999))],
                 "color_theme": ["Which color theme to use?", "", random.choice(['bluebrrryy dark', 'bluebrrryy light',
                                                                                 'nulbrrryyy dark', 'nulbrrryyy light'])],
                 "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile]},
                clear_txo=True)

    def prompt_lasertag_profile(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt({
            "profile_name": ["What to name the profile?", "", f"laser_master{random.randint(0, 9999)}"],
            "color_theme": ["Which color theme to use?", "", random.choice(['dark_moon', 'moon_light',
                                                                            'space_shot', 'red_blue'])],
            "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile],
        })

    def decide_word_gaims_profile(self):
        self.decide_decision("Which word gaim for a new make", self.word_gaims)
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.prompt_word_gaim_profile

    def prompt_word_gaim_profile(self, word_gaim: str):
        match word_gaim:
            case "crossword":
                pass
            case "word_search":
                pass
            case "candy_slinger":
                pass
            case "hangman":
                self.prompt_new_hangman()


    def prompt_new_hangman(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt({
            "phrase_length": ["How long is this new phrase for hangman?", "", random.choice(['short_phrase', 'long_phrase', 'single_word'])],
            "category": ["What category would you categorize the new phrase?", "", random.choice(["sports", "vehicles", "plants"])],
            "new_phrase": ["What is the new phrase to add?", "", "new"*random.randint(5, 10)],
            "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.save_new_hangman],
        })

    def save_new_hangman(self, yesno: str):
        pass