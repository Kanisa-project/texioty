import random
from question_prompts.base_prompt import BasePrompt


class Profilizer(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)


    def prompt_texioty_profile(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt(
                {"profile_name": [f"What to name the profile?", "", os.getcwd().split('/')[2]],
                 "password": [f"What to use for password?", "", str(random.randint(1000, 9999))],
                 "color_theme": ["Which color theme to use?", "", random.choice(['bluebrrryy dark', 'bluebrrryy light',
                                                                                 'nulbrrryyy dark', 'nulbrrryyy light'])],
                 "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile]},
                clear_txo=True)
