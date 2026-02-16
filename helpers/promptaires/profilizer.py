import os
import random
from typing import Callable, Any

from helpers.promptaires.prompt_helper import BasePrompt, QuestionType, ResponseType, \
    dict_to_question_prompt_factory

PROFILE_NAMING_KEYS = {
    "users": {
        "texioty": "username",
        "laser_tag": "tagger_name"
    },
    "foto_worx": {
        "printer": ["server_name", "table_number"],
        "friar": ["grease_temp", "basket_depth"],
        "slicer": [],
        "flatop": [],
        "extruder": []
    }
}

USER_PROFILE_DICT = {
    "texioty": {
        "username": {"": "username_string",
                     "question": "What's the username?",
                     "question_type": QuestionType.STRICT,
                     "default_response": "bluebeard",
                     "response_type": ResponseType.STRING},
        "password": {"": "password_string",
                     "question": "What to use for password?",
                     "question_type": QuestionType.STRICT,
                     "default_response": random.randint(1000, 9999),
                     "response_type": ResponseType.INT},
        "color_theme": {"": "color_theme_string",
                        "question": "What color theme to use?",
                        "question_type": QuestionType.DECISIONING,
                        "default_response": "bluebrrryy dark",
                        "response_type": ResponseType.DECISION,
                        "decision_choices": ["bluebrrryy dark", "bluebrrryy light", "bluebrrryy medium"]},
        "profile_name": {"": "profile_string",
                         "question": "What's to name the profile?",
                         "question_type": QuestionType.STRICT,
                         "default_response": "bluebeard",
                         "response_type": ResponseType.STRING}

    },
    "laser_tag": {
        "tagger_name": {"": "tagger_name_string",
                       "question": "What's the tagger name?",
                       "question_type": QuestionType.STRICT,
                       "default_response": "B1U3B34RD",
                        "response_type": ResponseType.STRING
                        },
        "profile_name": {"": "profile_string",
                         "question": "What's to name the profile?",
                         "question_type": QuestionType.STRICT,
                         "default_response": "B1U3B34RD",
                         "response_type": ResponseType.STRING}
    }
}

FOTO_WORX_PROFILE_DICT = {
    "printer": {
        "table_size": {"": "people_integer",
                       "question": "How many items will be printed on the image?",
                       "question_type": QuestionType.STRICT,
                       "default_response": "4",
                       "response_type": ResponseType.INT},
        "ticket_items": {"": "printer_items",
                         "question": "What text will be printing onto the image?",
                         "question_type": QuestionType.LOOSE,
                         "default_response": [],
                         "response_type": ResponseType.LIST},
        "ticket_time_in": {"": "time_in_float",
                           "question": "Top left corner for text placement.",
                           "question_type": QuestionType.STRICT,
                           "default_response": 1.7,
                           "response_type": ResponseType.FLOAT},
        "ticket_time_out": {"": "time_out_float",
                            "question": "Bottom right corner for text placement.",
                            "question_type": QuestionType.STRICT,
                            "default_response": 6.4,
                            "response_type": ResponseType.FLOAT},
        "table_number": {"": "table_integer",
                         "question": "Give an integer for the font size scale.",
                         "question_type": QuestionType.STRICT,
                         "default_response": 67,
                         "response_type": ResponseType.INT},
        "server_name": {"": "server_string",
                        "question": "What's server_name for the font?",
                        "question_type": QuestionType.STRICT,
                        "default_response": "Ginger",
                        "response_type": ResponseType.STRING},
        "profile_name": {"": "profile_string",
                         "question": "What's to name the profile?",
                         "question_type": QuestionType.STRICT,
                         "default_response": "Ginger_67",
                         "response_type": ResponseType.STRING}
    },
    "friar": {
        "is_frozen": {"":"frozen_bool",
                      "question":"Is the item being fried, frozen?",
                      "question_type":QuestionType.STRICT,
                      "default_response":True,
                      "response_type":ResponseType.BOOL},
        "grease_temp": {"":"temp_integer",
                        "question":"What temperature is the grease?",
                        "question_type":QuestionType.STRICT,
                        "default_response":471,
                        "response_type":ResponseType.INT},
        "basket_depth": {"":"depth_integer",
                         "question":"How deep is the basket?",
                         "question_type":QuestionType.STRICT,
                         "default_response":7,
                         "response_type":ResponseType.INT},
        "cook_timer": {"":"timer_float",
                       "question":"How long is the timer float?",
                       "question_type":QuestionType.STRICT,
                       "default_response":12.6,
                       "response_type":ResponseType.FLOAT},
        "profile_name": {"":"profile_string",
                         "question":"What's to name the profile?",
                         "question_type":QuestionType.STRICT,
                         "default_response":"471_7",
                         "response_type":ResponseType.STRING}
    },
    "slicer": {
        "slice_item": {"": "item_string",
                       "question": "What's the item to slice?",
                       "question_type": QuestionType.STRICT,
                       "default_response": "cheese",
                       "response_type": ResponseType.STRING},
        "slice_direction": {"": "direction_list",
                            "question": "What direction to slice the item?",
                            "question_type": QuestionType.STRICT,
                            "default_response": [0.2, 0.9],
                            "response_type": ResponseType.LIST},
        "thickness": {"": "thickness_float",
                      "question": "What thickness to slice the item?",
                      "question_type": QuestionType.STRICT,
                      "default_response": 0.5,
                      "response_type": ResponseType.FLOAT},
        "amount": {"": "amount_integer",
                   "question": "How much item to slice?",
                   "question_type": QuestionType.STRICT,
                   "default_response": 10,
                   "response_type": ResponseType.INT},
        "portion_amount": {"": "portion_integer",
                           "question": "How much item to weight?",
                           "question_type": QuestionType.STRICT,
                           "default_response": 10.268,
                           "response_type": ResponseType.INT},
        "profile_name": {"": "profile_string",
                         "question": "What's to name the profile?",
                         "question_type": QuestionType.STRICT,
                         "default_response": "cheese_0.5_10",
                         "response_type": ResponseType.STRING}

    },
    "flatop": {
        "spatula_slide": {"": "direction_list",
                          "question": "Which way to slide the spatula?",
                          "question_type": QuestionType.STRICT,
                          "default_response": [0.3, 0.89],
                          "response_type": ResponseType.LIST},
        "grill_weight": {"": "weight_box",
                         "question": "What weight to put on the grill?",
                         "question_type": QuestionType.STRICT,
                         "default_response": [0.2, 0.2, 0.8, 0.8],
                         "response_type": ResponseType.LIST},
        "steam_lid": {"": "steam_bool",
                      "question": "Should the item be steamed under the lid?",
                      "question_type": QuestionType.STRICT,
                      "default_response": True,
                      "response_type": ResponseType.BOOL},
        "profile_name": {"": "profile_string",
                         "question": "What's to name the profile?",
                         "question_type": QuestionType.STRICT,
                         "default_response": "flatop_left",
                         "response_type": ResponseType.STRING}
    }
}

class Profilizer(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.profile_to_make = "Texioty"
        self.word_gaims = [
            "hangman", "word_search", "candy_slinger", "boston_trail"
        ]
        # self.foto_worx_profiles = ["printer", "friar", "slicer", "flatop", "extruder"]


    def profile_make(self, profile_type: str):
        match profile_type:
            case 'users':
                self.decide_user_profile()
            case 'foto_worx':
                self.decide_fotoworx_profile()
            case 'tcg_lab':
                pass
            case 'word_gaims':
                self.decide_word_gaims_profile()

    def decide_fotoworx_profile(self):
        """
        Decides which foto worx profile to make and sets up the deciding function accordingly.
        """
        self.decide_decision("Which foto worx profile to make", list(FOTO_WORX_PROFILE_DICT.keys()))
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.prompt_foto_worx_profile

    def prompt_foto_worx_profile(self, worx_type: str="printer"):
        """
        Sets up the foto worx profile questions and starts the questionnaire.
        """
        question_dict = dict_to_question_prompt_factory(FOTO_WORX_PROFILE_DICT[worx_type])
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt(question_dict)

    def decide_user_profile(self):
        self.decide_decision("Which user profile to make", list(USER_PROFILE_DICT.keys()))
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.prompt_user_profile

    def prompt_user_profile(self, user_type: str="Texioty"):
        question_dict = dict_to_question_prompt_factory(USER_PROFILE_DICT[user_type])
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.start_question_prompt(question_dict)


    # def prompt_lasertag_profile(self):
    #     self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
    #     self.start_question_prompt({
    #         "profile_name": ["What to name the profile?", "", f"laser_master{random.randint(0, 9999)}"],
    #         "color_theme": ["Which color theme to use?", "", random.choice(['dark_moon', 'moon_light',
    #                                                                         'space_shot', 'red_blue'])],
    #         "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile],
    #     })

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