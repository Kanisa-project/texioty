import random

from gaims.base_gaim import BaseGaim
import theme as t

PHRASE_LIST = ["You gave Sally a cheese wheel, she buried it under a tree.",
               "You helped Tom move a couch, he burned it on the porch.",
               "Shane kicked your shin after you gave him a flower.",
               "This is just a phrase, we'll go out of it soon."]

HANGMAN_TEXTMAN_LIST = ["  ╔╤╤═══╕   \n"
                        "  ║     ┇   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤════╕   \n"
                        "  ║╱╱    ┇   \n"
                        "  ║      ◯   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ◯   \n"
                        "  ║     ‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    /    \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    / \\ \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    / \\ \n"
                        "══╩═════════\n"
                        ]

class HangmanRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "Hangman")
        self.gaim_commands["guess"] = [self.guess_letter, "Guess a single letter or number.",
                                       {}, "HMAN", t.rgb_to_hex(t.MUSTARD_YELLOW), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["solve"] = [self.guess_phrase, "Guess the entire phrase.",
                                       {}, "HMAN", t.rgb_to_hex(t.MUSTARD_YELLOW), t.rgb_to_hex(t.BLACK)]
        self.gaim_prefix = "guess "
        self.gaim_phrase = random.choice(PHRASE_LIST)
        self.hidden_dict = {'t': "◙", 'h': "◙", 'i': "◙", 's': "◙"}
        self.missed_letters = []
        self.correct_letters = []

    def new_game(self, args):
        super().new_game(args)
        self.missed_letters = []
        self.correct_letters = []
        self.pick_new_phrase()
        self.welcome_message([])
        self.gaim_prefix = 'guess '

    def display_man(self):
        """Display the progress of the man being hanged."""
        if len(self.missed_letters) <= len(HANGMAN_TEXTMAN_LIST)-2:
            self.txo.priont_string(HANGMAN_TEXTMAN_LIST[len(self.missed_letters)])
            self.txo.priont_list(self.missed_letters, parent_key="Missed letters:")
        else:
            self.txo.priont_string(HANGMAN_TEXTMAN_LIST[len(HANGMAN_TEXTMAN_LIST)-1])
            self.txo.priont_string("Sorry, you guessed too many wrong letters.\n\n")
            self.txo.priont_string(self.gaim_phrase)
            self.gaim_prefix = random.choice(['new ', 'stop '])

    def display_phrase(self):
        """Display the progress of the phrase discovered so far."""
        hidden_phrase = ''.join(self.hidden_dict.values())
        self.txo.priont_string(hidden_phrase)
        if "◙" not in hidden_phrase:
            self.txo.priont_string("CONGRATS! YOU WIN!")
            self.gaim_prefix = random.choice(['new ', 'stop '])

    def pick_new_phrase(self):
        """Pick a new phrase and generate it into a hidden dictionary as well."""
        self.hidden_dict = {}
        self.gaim_phrase = random.choice(PHRASE_LIST)
        self.generate_hidden_dictionary()

    def generate_hidden_dictionary(self):
        """Generate a dictionary to solve by guessing one letter at a time."""
        for c in self.gaim_phrase:
            hide_it = "◙"
            if c in [' ', '.', ',', '\'']:
                hide_it = c
            while c in self.hidden_dict:
                c += c[0]
            self.hidden_dict[c] = hide_it

    def welcome_message(self, args):
        super().welcome_message(args)
        self.txo.priont_string("")
        self.txo.priont_string("Hangman is where you guess a single letter at a time, in an attempt to solve a hidden phrase.")
        self.txo.priont_string("Every wrongly guessed letter will add another body part to the man being hanged.")
        self.txo.priont_string("Guess too many wrong letters and uh-oh, the man gets hanged.")
        self.txo.priont_string("")
        self.display_man()
        self.display_phrase()

    def save_game(self, args):
        self.game_state = {
            "player_name": self.txo.master.active_profile.username,
            "missed_letters": self.missed_letters,
            "correct_letters": self.correct_letters,
            "gaim_phrase": self.gaim_phrase,
            "hidden_dict": self.hidden_dict
        }
        super().save_game([self.game_state])

    def load_game(self, args):
        self.game_state = super().load_game([self.txo.master.active_profile.username])
        self.missed_letters = self.game_state['missed_letters']
        self.correct_letters = self.game_state['correct_letters']
        self.gaim_phrase = self.game_state['gaim_phrase']
        self.hidden_dict = self.game_state['hidden_dict']
        self.welcome_message([])

    def guess_letter(self, guessed_letter: str):
        """
        Guess if the letter is in the phrase.
        """
        if len(guessed_letter) == 1:
            self.txo.priont_string(f"Guessing: {guessed_letter}")
            self.check_hangman_letter(guessed_letter[0])
        else:
            self.txo.priont_string("Guess only one letter at a time.")
        self.welcome_message([])

    def guess_phrase(self, guessed_phrase: str):
        if self.gaim_phrase.lower() == guessed_phrase.lower():
            pass
        else:
            self.txo.priont_string(guessed_phrase)
            self.txo.priont_string(f"  ....is incorrect")

    def check_hangman_letter(self, letter: str):
        if letter in self.gaim_phrase and letter not in self.correct_letters:
            self.correct_letters.append(letter)
            self.update_hidden_dict(letter)
        else:
            self.missed_letters.append(letter)
            self.txo.priont_string(f"Sorry {letter} is not in this phrase.")

    def update_hidden_dict(self, checked_letter: str):
        """Update the hidden dictionary with a checked correct letter."""
        for i in range(len(self.gaim_phrase)):
            if checked_letter * (i + 1) in self.hidden_dict:
                if self.hidden_dict[checked_letter * (i + 1)] == "◙":
                    self.hidden_dict[checked_letter * (i + 1)] = checked_letter

    def display_help_message(self, args):
        super().display_help_message(args)

    def display_available_commands(self, args):
        super().display_available_commands(args)

    def stop_game(self, args):
        super().stop_game(args)