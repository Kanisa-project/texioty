import os
import random
from helpers.promptaires.prompt_helper import BasePrompt


class Profilizer(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.profile_to_make = "Texioty"


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