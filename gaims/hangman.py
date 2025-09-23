import random

from gaims.gaim_runner import BaseGaim
import theme as t
PHRASE_LIST = ["You gave Sally a cheese wheel, she buried it under a tree.",
               "You helped Tom move a couch, he burned it on the porch.",
               "Shane kicked your shin after you gave him a flower.",
               "This is just a phrase, we'll go out of it soon."]

HANGMAN_TEXTMAN_LIST = ["  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱        \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤════╕   \n"
                        "  ║╱╱    ┇   \n"
                        "  ║╱     ◯   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║     ‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    /    \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    / \\ \n"
                        "  ║         \n"
                        "══╩═════════\n"
                        ]
missed_letters = []
gaim_phrase = "This is one two."
max_guesses = 0


class HangmanRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "Hangman")
        self.gaim_commands["guess"] = [self.guess_letter, "Displays a message of helping helpfulness.",
                                       {}, [], t.rgb_to_hex(t.MUSTARD_YELLOW), t.rgb_to_hex(t.BLACK)],
        self.gaim_commands["solve"] = [self.solve_phrase, "Displays a message of helping helpfulness.",
                                       {}, [], t.rgb_to_hex(t.MUSTARD_YELLOW), t.rgb_to_hex(t.BLACK)],
        self.txo.priont_string(random.choice(HANGMAN_TEXTMAN_LIST))
        self.gaim_phrase = random.choice(PHRASE_LIST)

    def new_game(self):
        super().new_game()


    def guess_letter(self):
        pass

    def solve_phrase(self):
        pass


    def check_hangman_letter(self, letter_to_check: str, hidden_dict: dict) -> dict:
        print(hidden_dict)
        if letter_to_check in self.gaim_phrase:
            for i in range(len(self.gaim_phrase)):
                if letter_to_check * (i + 1) in hidden_dict:
                    if hidden_dict[letter_to_check * (i + 1)] == "◙":
                        hidden_dict[letter_to_check * (i + 1)] = letter_to_check
        else:
            if letter_to_check in missed_letters:
                pass
            else:
                missed_letters.append(letter_to_check)
        return hidden_dict
