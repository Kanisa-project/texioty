import random

from gaims.gaim_runner import BaseGaim

suits = "♠♥♣♦"
card_vals = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_DECK = {
    "♠": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    "♥": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    "♣": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    "♦": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
}
CARD_TEMPLATE = "┌———┐\n" \
                "│ NS│\n" \
                "└———┘\n"
FACE_DOWN_TEMPLATE = "╔╦╦╦╗\n" \
                     "╠╬╬╬╣\n" \
                     "╚╩╩╩╝\n"

DIE_TEMPLATE = "⚀ ⚁ ⚂ ⚃ ⚄ ⚅"
dealer_hand_value = 0

class CasinoRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "Casino")


def draw_a_card() -> (str, int):
    ran_suit = random.choice(suits)
    ran_val_letter = random.choice(CARD_DECK[ran_suit])
    CARD_DECK[ran_suit].remove(ran_val_letter)
    if len(CARD_DECK[ran_suit]) <= 0:
        replenish_deck()
    else:
        pass
    if ran_val_letter in ['J', 'Q', 'K']:
        ran_val = 10
    elif ran_val_letter == 'A':
        ran_val = 11
    else:
        ran_val = str(ran_val_letter)
    return str(ran_val_letter) + ran_suit, int(ran_val)


def replenish_deck():
    for suit in suits:
        for val in card_vals:
            CARD_DECK[suit].append(val)


def apply_card_template(card_digits) -> str:
    if len(card_digits) == 3:
        return CARD_TEMPLATE.replace(" N", str(card_digits[:2])).replace("S", str(card_digits[2]))
    else:
        return CARD_TEMPLATE.replace("N", str(card_digits[0])).replace("S", str(card_digits[1]))


def take_dealer_turn():
    pass


def dealer_hit():
    pass


def dealer_stay():
    pass


def gaim_outcome():
    pass
