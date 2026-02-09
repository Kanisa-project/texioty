import os
import random
from typing import Callable, Any

from helpers.promptaires.prompt_helper import BasePrompt, Question, QuestionType

FOTO_WORX_PROFILE_DICT = {
    "printer": {
        "table_size": ["people_integer",
                       "How many people are in the table?",
                       QuestionType.STRICT, "4"],
        "ticket_items": ["printer_items",
                         "What text will be printing onto the image?",
                         QuestionType.STRICT, []],
        "ticket_time_in": ["time_in_float",
                           "Give a float for ticket_time_in.",
                           QuestionType.STRICT, 1.7],
        "ticket_time_out": ["time_out_float",
                            "Give a float for ticket_time_out.",
                            QuestionType.STRICT, 6.4],
        "table_number": ["table_integer",
                         "Give an integer for the table_number.",
                         QuestionType.STRICT, 67],
        "server_name": ["server_string",
                        "What's the server_name.",
                        QuestionType.STRICT, "Ginger"],
    },
    "friar": {
        "grease_temp": ["grease_temp_integer", "What temperature is the grease?", QuestionType.STRICT, 471],
        "basket_depth": ["basket_depth_integer", "How deep is the basket?", QuestionType.STRICT, 7],
        "cook_timer": ["cook_timer_float", "How long is the timer float?", QuestionType.STRICT, 12.6]
    }
}


def dict_to_question_prompt_factory(profile_dict: dict) -> dict[str, Question]:
    question_dict = {}
    for profile_key, profile_value in profile_dict.items():
        print(profile_key, profile_value)
        match len(profile_value):
            case 3:
                question_dict[profile_key] = Question(profile_value[0], profile_value[1], profile_value[2])
            case 4:
                question_dict[profile_key] = Question(profile_value[0], profile_value[1], profile_value[2], profile_value[3])
            case _:
                raise ValueError(f"Invalid profile_dict length: {len(profile_value)}")
    return question_dict


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
            case 'laser_tag':
                self.prompt_lasertag_profile()
            case 'foto_worx':
                self.prompt_foto_worx_profile()
            case 'tcg_lab':
                pass
            case 'word_gaims':
                self.decide_word_gaims_profile()

    def prompt_foto_worx_profile(self):
        question_dict = dict_to_question_prompt_factory(FOTO_WORX_PROFILE_DICT["printer"])
        print(question_dict)
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)

        self.start_question_prompt(question_dict)

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