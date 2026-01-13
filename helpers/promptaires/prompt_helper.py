import texity
import texoty
from helpers.tex_helper import TexiotyHelper
from tkinter import END


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
        self.display_title(entitled, False)
        self.priont_available_options_by_page([avail_options])

        self.txo.priont_string(question)
        self.txi.bind_new_options(avail_options)
        return 0

    def priont_available_options_by_page(self, paged_options: list):
        current_options = paged_options[self.current_options_page]
        for i, option in enumerate(current_options):
            self.txo.priont_string(f"{i} - {option}")

    def display_question(self):
        """Displays a question from the loaded questionnaire prompt dictionary."""
        if self.current_question_index < len(self.question_keys):
            question_key = self.question_keys[self.current_question_index]
            question = self.question_prompt_dict[question_key][0]
            for i in range(self.txo.texoty_h-3):
                self.txo.priont_string(' -')
            self.txo.insert(END, question)
            self.txo.priont_string(f"[{self.question_prompt_dict[question_key][2]}]")
            # self.txi.command_string_var.set(f"[{self.question_prompt_dict[question_key][2]}]  ›")
            self.txi.icursor(END)
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

def pagify_available_options(available_options: list) -> list:
    paged_options = []
    if len(available_options) <= 10:
        paged_options.append(available_options)
    elif len(available_options) > 10:
        pass
    return paged_options