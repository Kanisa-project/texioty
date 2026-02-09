from enum import Enum
from typing import Optional, List, Callable, Tuple
from dataclasses import dataclass

from PIL import Image

import texity
import texoty
from helpers.tex_helper import TexiotyHelper
from tkinter import END, PhotoImage
from settings import utils as u, themery as t

class ResponseType(Enum):
    DECISION = 'decision'
    DEFAULT = 'default'
    STRING = 'string'
    FLOAT = 'float'
    BOOL = 'bool'
    LIST = 'list'
    DICT = 'dict'
    NONE = 'none'
    INT = 'int'

@dataclass
class UserResponse:
    question_key: str
    response_type: ResponseType
    float_response: Optional[float] = None
    list_response: Optional[list] = None
    bool_response: Optional[bool] = None
    str_response: Optional[str] = None
    int_response: Optional[int] = None


class QuestionType(Enum):
    DECISIONING = 'decision'
    STRICT = 'strict'
    LOOSE = 'loose'

@dataclass
class Question:
    key: str
    question: str
    question_type: QuestionType = QuestionType.LOOSE
    # response_type: ResponseType = ResponseType.DEFAULT
    default_response: Optional[str] = None
    decision_choices: Optional[List[str]] = None
    validation_func: Optional[Callable[[str], Tuple[bool, Optional[str]]]] = None
    user_response: Optional[UserResponse] = None

    def __post_init__(self):
        if not self.key or not self.key.strip():
            raise ValueError("Question key cannot be empty or whitespace")
        if not self.question or not self.question.strip():
            raise ValueError("Question cannot be empty or whitespace")
        # if self.default_response and self.decision_choices:
        #     print(self.default_response, self.decision_choices)
        #     if self.default_response not in self.decision_choices:
        #         raise ValueError(f"Default response '{self.default_response}' is not in possible choices")

    def validate_response(self, response: str) -> Tuple[bool, Optional[str]]:
        if not response and not self.default_response:
            return False, "No response provided."
        if self.decision_choices and response not in self.decision_choices:
            return False, f"Response '{response}' is not in possible choices."
        if self.validation_func:
            return self.validation_func(response)
        return True, None

    def is_required(self) -> bool:
        return self.default_response is None

    def is_multiple_choice(self) -> bool:
        return self.decision_choices is not None and len(self.decision_choices) > 1

class BasePrompt(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY, prompt_name: str = "BasePrompt"):
        super().__init__(txo, txi)
        self.in_questionnaire_mode = None
        self.in_decisioning_mode = None
        self.txo = txo
        self.txi = txi
        self.prompt_name = prompt_name
        self.question_prompt_dict = {}
        self.response_dict = {}
        self.question_keys = []
        self.current_question_index = 0
        self.current_options_page = 0
        self.decision_images = []
        self.helper_commands['page'] = {
            'name': 'page',
            'usage': '"page [PAGE_NUMBER]"',
            'call_func': self.decisioning_page_next,
            'lite_desc': 'Store the response and advance to the next question.',
            'full_desc': ['Store the response and advance to the next question.'],
            'possible_args': {'[PAGE_NUMBER]': 'The page number of options to view.'},
            'args_desc': {'[PAGE_NUMBER]': ['The page number of options to view.', int]},
            'examples': ['page 0', 'page 3', 'page +', 'page -'],
            'group_tag': 'PRUN',
            'font_color': u.rgb_to_hex(t.BLANCHED_ALMOND),
            'back_color': u.rgb_to_hex(t.BLACK)
        }

    def display_loose_question(self):
        pass

    def display_strict_question(self):
        pass

    def display_decision_question(self):
        pass

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
            # self.response_dict['confirming_function'] = self.txo.master.create_profile
            self.question_keys = list(question_dict.keys())
            self.in_questionnaire_mode = True
            self.current_question_index = 0
            self.display_question()
        else:
            self.txo.priont_string("Already in a questionnaire prompt.")
            self.display_question()

    def display_foto_option_question(self, question: str, avail_options: list, titled: str = "basic"):
        self.in_decisioning_mode = True
        self.txo.master.change_current_mode("Decisioning", self.helper_commands)
        self.txo.clear_no_header()
        # self.txi.current_possible_options = avail_options
        for i in range(self.txo.texoty_h-len(avail_options)):
            self.txo.priont_string(' '*(self.txo.texoty_w-2)+'\n')
        self.display_title(titled, False)
        available_opts = pagify_available_options(avail_options)
        self.priont_available_fotoes_by_page(available_opts)

        self.txo.priont_string(question)
        # self.txi.bind_new_options(avail_options)
        return 0

    def display_option_question(self, titled: str, question: str, avail_options: list):
        """
        Print a header/title of the question being decided, then
        a list of options, each assigned to a single digit number, and finally
        the specific question to be decided upon.

        """
        self.in_decisioning_mode = True
        self.txo.master.change_current_mode("Decisioning", self.helper_commands)
        self.txo.clear_no_header()
        self.txi.current_possible_options = avail_options
        for i in range(self.txo.texoty_h-len(avail_options)):
            self.txo.priont_string(' '*(self.txo.texoty_w-2)+'\n')
        self.display_title(titled, False)
        self.priont_available_options_by_page([avail_options])

        self.txo.priont_string(question)
        self.txi.bind_new_options(avail_options)
        return 0

    def priont_available_options_by_page(self, paged_options: list):
        current_options = paged_options[self.current_options_page]
        for i, option in enumerate(current_options):
            self.txo.priont_string(f"{i} - {option}")

    def priont_available_fotoes_by_page(self, paged_options: list):
        current_options = paged_options[self.current_options_page]
        print("CUROPTS", current_options)
        self.decision_images = []
        self.txi.bind_new_options(current_options)

        for i, save_path in enumerate(current_options):
            save_name = "foto_opt_" + str(i) + ".png"
            foto_name = save_path.split("/")[-1]
            foto = Image.open(save_path)
            save_path = f"helpers/promptaires/worx_hop/fotoes/{save_name}"
            foto_option = resize_foto(foto, (64, 64))
            foto_option.save(save_path)
            self.decision_images.append(PhotoImage(file=save_path))
            print(self.decision_images[i], "DECISION IMG")
            self.txo.priont_foto_option(i, foto_name, self.decision_images[i])

    def display_question(self):
        """Displays a question from the loaded questionnaire prompt dictionary."""
        if self.current_question_index < len(self.question_keys):
            question_key = self.question_keys[self.current_question_index]
            question = self.question_prompt_dict[question_key].question
            for i in range(self.txo.texoty_h-3):
                # self.txo.priont_break_line()
                self.txo.priont_string('')
            self.txo.insert(END, question)
            self.txo.priont_string(f"[{self.question_prompt_dict[question_key].default_response}]")
            # self.txi.command_string_var.set(f"[{self.question_prompt_dict[question_key][2]}]  ›")
            self.txi.icursor(END)
        else:
            self.end_question_prompt(self.response_dict)
            self.txo.master.default_mode()

    # def display_question(self):
    #     """Displays a question from the loaded questionnaire prompt dictionary."""
    #     if self.current_question_index < len(self.question_keys):
    #         question_key = self.question_keys[self.current_question_index]
    #         question = self.question_prompt_dict[question_key][0]
    #         for i in range(self.txo.texoty_h-3):
    #             self.txo.priont_string(' -')
    #         self.txo.insert(END, question)
    #         self.txo.priont_string(f"[{self.question_prompt_dict[question_key][2]}]")
    #         # self.txi.command_string_var.set(f"[{self.question_prompt_dict[question_key][2]}]  ›")
    #         self.txi.icursor(END)
    #     else:
    #         self.end_question_prompt(self.response_dict)
    #         self.txo.master.default_mode()

    def end_question_prompt(self, question_dict: dict) -> dict:
        """End the questionnaire prompt and return the results."""
        self.txo.priont_string("Prompt ended, here are the results: ")
        self.txo.priont_dict(question_dict)
        self.in_questionnaire_mode = False
        # self.response_dict = question_dict
        print(self.response_dict)
        self.response_dict['confirming_function'][3](self.response_dict['confirming_function'][1])
        return question_dict

    # def end_question_prompt(self, question_dict: dict) -> dict:
    #     """End the questionnaire prompt and return the results."""
    #     self.txo.priont_string("Prompt ended, here are the results: ")
    #     self.txo.priont_dict(question_dict)
    #     self.in_questionnaire_mode = False
    #     # self.response_dict = question_dict
    #     print(self.response_dict)
    #     self.response_dict['confirming_function'][3](self.response_dict['confirming_function'][1])
    #     return question_dict

    def store_response(self, answer: str):
        """ Store the response in the questionnaire dictionary and advance to the next question."""
        question_key = self.question_keys[self.current_question_index]
        if answer == "":
            answer = self.question_prompt_dict[question_key].default_response
            self.txo.priont_string("|>  " + str(answer) + " (Default)")
        else:
            self.txo.priont_string("|>  " + answer)
        self.response_dict[question_key].user_response = UserResponse(question_key, self.question_prompt_dict[question_key].response_type, answer)

        self.current_question_index += 1
        self.display_question()

    # def store_response(self, answer: str):
    #     """ Store the response in the questionnaire dictionary and advance to the next question."""
    #     question_key = self.question_keys[self.current_question_index]
    #     if answer == "":
    #         answer = self.question_prompt_dict[question_key][2]
    #         self.txo.priont_string("|>  " + answer + " (Default)")
    #     else:
    #         self.txo.priont_string("|>  " + answer)
    #     self.response_dict[question_key][1] = answer
    #
    #     self.current_question_index += 1
    #     self.display_question()

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

    def decide_foto_decision(self, input_question: str, possible_options: list, titled='basic'):
        self.txi.isDecidingDecision = True
        self.display_foto_option_question(input_question + f", (0-{len(possible_options) - 1})? ", possible_options, titled)

    def decisioning_page_prev(self):
        self.current_options_page -= 1

    def decisioning_page_next(self):
        self.current_options_page += 1


def pagify_available_options(available_options: list) -> list:
    """
    Take in all options and return a list of lists for all options.
    :param available_options: Entire list of options
    """
    paged_options = []
    if len(available_options) <= 10:
        return [available_options]
    while len(available_options) > 10:
        page = []
        while len(page) < 10:
            page.append(available_options[0])
            available_options.remove(available_options[0])
        paged_options.append(page)
    paged_options.append(available_options)
    print("PAG", paged_options)
    return paged_options


def resize_foto(foto: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    """Resize a foto and return it."""
    new_size = (int(new_size[0]), int(new_size[1]))
    return foto.resize(new_size)
