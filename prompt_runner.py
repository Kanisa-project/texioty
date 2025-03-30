import tkinter as tk

class PromptRunner(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)
        self.in_questionnaire_mode = False
        self.master = master
        self.question_prompt_dict = {}
        self.question_keys = []
        self.current_question_index = 0

    def start_question_prompt(self, question_dict: dict):
        """
        Checks if Textioty is already in a questionnaire prompt. If not, sets up the first question and starts the
        prompt to receive answers. Anything typed and sent in Texity will be saved as answers for the prompt questions.
        :param question_dict: Dictionary of questions, consider making a dataclass.
        :return:
        """
        self.texoty.clear_add_header()
        if not self.in_questionnaire_mode:
            self.question_prompt_dict = question_dict
            self.question_keys = list(question_dict.keys())
            self.in_questionnaire_mode = True
            self.current_question_index = 0
            self.display_question()
        else:
            self.texoty.priont_string("Already in a questionnaire prompt.")
            self.display_question()

    def display_question(self):
        """Displays a question from the loaded questionnaire prompt dictionary."""
        if self.current_question_index < len(self.question_keys):
            question_key = self.question_keys[self.current_question_index]
            question = self.question_prompt_dict[question_key][0]
            self.texoty.priont_string(question)
        else:
            self.end_question_prompt(self.question_prompt_dict)

    def end_question_prompt(self, question_dict: dict):
        self.texoty.priont_string("Prompt ended, here are the results: ")
        self.texoty.priont_dict(question_dict)
        self.in_questionnaire_mode = False

    def store_response(self, answer):
        """ Store the response in the questionnaire dictionary and advance to the next question."""
        question_key = self.question_keys[self.current_question_index]
        if answer == "":
            answer = self.question_prompt_dict[question_key][2]
            self.texoty.priont_string("|>  " + str(answer) + " (Default)")
        else:
            self.texoty.priont_string("|>  " + str(answer))
        self.question_prompt_dict[question_key][1] = answer

        self.current_question_index += 1
        self.display_question()
        # if question_key == "confirmation":
        #     if answer.startswith('y'):
        #         pass
        #     else:
        #         self.texoty.priont_string("Canceling, please restart the prompt.")
