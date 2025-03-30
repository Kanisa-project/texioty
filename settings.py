import math
import random
import tkinter as tk
import tkinter.font as tkfont
from dataclasses import dataclass
import random
import os
import configparser

config = configparser.ConfigParser()
config.read(".env")


def set_masterpiece_size(image_size: str) -> (int, int):
    """
    Set the size of the masterpiece from animal to pixels.
    @param image_size:
    @return:
    """
    size = (0, 0)
    if image_size == "Chicken":
        size = (320, 320)
    elif image_size == "Dog":
        size = (640, 640)
    elif image_size == "Camel":
        size = (960, 960)
    elif image_size == "avatar":
        size = (500, 500)
    elif image_size == "tile":
        size = (500, 700)
    elif image_size == "banner":
        size = (1500, 500)
    return size


def polypointlist(sides: int, offset: int, cx: int, cy: int, radius: int) -> list:
    step = 2 * math.pi / sides
    offset = math.radians(offset)
    pointlist = [(radius * math.cos(step * n + offset) + cx, radius * math.sin(step * n + offset) + cy) for n in
                 range(0, int(sides) + 1)]
    return pointlist


def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def get_monospace_font():
    return tkfont.Font(family="Consolas", size=10, weight="normal")


ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyz0123456789"
MIN_CREATION_UTC = 1119553200
MAX_CREATION_UTC = 1633120253

# PRIMARY COLORS
LIGHT_RED = (230, 173, 216)
LIGHT_GREEN = (216, 230, 173)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (79, 47, 47)
DARK_GREEN = (47, 79, 47)
DARK_BLUE = (47, 47, 79)

# SHADES
BLACK = (0, 0, 0)
SPACE_GREY = (22, 22, 22)
# SPACE_GREY = (22, 22, 22, 69)
DARK_GREY = (60, 60, 60)
SUPER_DARK_GREY = (40, 40, 40)
DARK_SLATE_GREY = (47, 79, 79)
DIM_GREY = (105, 105, 105)
FREE_SPEECH_GREY = (99, 86, 136)
GREY = (190, 190, 190)
GREY25 = (64, 64, 64)
GREY50 = (127, 127, 127)
GREY75 = (191, 191, 191)
GREY99 = (252, 252, 252)
LIGHT_GREY = (211, 211, 211)
SLATE_GREY = (112, 128, 144)
VERY_LIGHT_GREY = (205, 205, 205)
WHITE = (255, 255, 255)
EGGSHELL_WHITE = (240, 234, 214)
X_RAY_GRAY = (90, 111, 106)

# BLUES
ALICE_BLUE = (240, 248, 255)
AQUA = (0, 255, 255)
LOOPRING_BLUE = (46, 126, 254)
AQUAMARINE = (127, 255, 212)
AZURE = (240, 255, 255)
BLUE_2 = (0, 0, 238)
BLUE_3 = (0, 0, 205)
BLUE_4 = (0, 0, 139)
BLUE_VIOLET = (138, 43, 226)
CADET_BLUE = (95, 159, 159)
CORN_FLOWER_BLUE = (66, 66, 111)
CYAN = (0, 255, 255)
DARK_SLATE_BLUE = (36, 24, 130)
DARK_TURQUOISE = (112, 147, 219)
DEEP_SKY_BLUE = (0, 191, 255)
DODGER_BLUE = (30, 144, 255)
FREE_SPEECH_BLUE = (65, 86, 197)
LIGHT_CYAN = (224, 255, 255)
LIGHT_SKY_BLUE = (135, 206, 250)
LIGHT_SLATE_BLUE = (132, 112, 255)
LIGHT_STEEL_BLUE = (176, 196, 222)
MEDIUM_BLUE = (0, 0, 205)
MEDIUM_SLATE_BLUE = (123, 104, 238)
MEDIUM_TURQUOISE = (72, 209, 204)
MIDNIGHT_BLUE = (25, 25, 112)
NAVY = (0, 0, 128)
NAVY_BLUE = (0, 0, 128)
NEON_BLUE = (77, 77, 255)
NEW_MIDNIGHT_BLUE = (0, 0, 156)
PALE_TURQUOISE = (187, 255, 255)
POWDER_BLUE = (176, 224, 230)
RICH_BLUE = (89, 89, 171)
ROYAL_BLUE = (65, 105, 225)
SKY_BLUE = (135, 206, 235)
SLATE_BLUE = (131, 111, 255)
STEEL_BLUE = (70, 130, 180)
SUMMER_SKY = (56, 176, 222)
TEAL = (0, 128, 128)
TRUE_IRIS_BLUE = (3, 180, 204)
TURQUOISE = (64, 224, 208)
LIGHT_GREY_BLUE = (22, 22, 249)
DARK_GREY_BLUE = (241, 241, 250)

# BROWNS
BAKERS_CHOCOLATE = (92, 51, 23)
BEIGE = (245, 245, 220)
BROWN = (166, 42, 42)
BURLYWOOD = (222, 184, 135)
CHOCOLATE = (210, 105, 30)
DARK_BROWN = (92, 64, 51)
DARK_TAN = (151, 105, 79)
DARK_WOOD = (133, 94, 66)
LIGHT_WOOD = (133, 99, 99)
MEDIUM_WOOD = (166, 128, 100)
NEW_TAN = (235, 199, 158)
PERU = (205, 133, 63)
ROSY_BROWN = (188, 143, 143)
SADDLE_BROWN = (139, 69, 19)
SANDY_BROWN = (244, 164, 96)
SEMI_SWEET_CHOCOLATE = (107, 66, 38)
SIENNA = (142, 107, 35)
TAN = (219, 147, 112)
VERY_DARK_BROWN = (92, 64, 51)

# GREENS
CHARTREUSE = (127, 255, 0)
DARK_GREEN_COPPER = (74, 118, 110)
DARK_KHAKI = (189, 183, 107)
DARK_OLIVE_GREEN = (85, 107, 47)
DARK_SEA_GREEN = (143, 188, 143)
FOREST_GREEN = (34, 139, 34)
FREE_SPEECH_GREEN = (9, 249, 17)
GREEN_YELLOW = (173, 255, 47)
KHAKI = (240, 230, 140)
LAWN_GREEN = (124, 252, 0)
LIGHT_SEA_GREEN = (32, 178, 170)
LIME = (0, 255, 0)
MEDIUM_SEA_GREEN = (60, 179, 113)
MEDIUM_SPRING_GREEN = (0, 250, 154)
MINT_CREAM = (245, 255, 250)
OLIVE = (128, 128, 0)
OLIVE_DRAB = (107, 142, 35)
PALE_GREEN = (152, 251, 152)
SEA_GREEN = (46, 139, 87)
SPRING_GREEN = (0, 255, 127)
YELLOW_GREEN = (154, 205, 50)
SAGE_GREEN = (157, 193, 131)
ARMY_GREEN = (75, 83, 32)
JUNGLE_GREEN = (30, 56, 33)

# ORANGES
BISQUE = (255, 228, 196)
CORAL = (255, 127, 0)
DARK_ORANGE = (255, 140, 0)
DARK_SALMON = (233, 150, 122)
HONEYDEW = (240, 255, 240)
LIGHT_CORAL = (240, 128, 128)
LIGHT_SALMON = (255, 160, 122)
MANDARIN_ORANGE = (142, 35, 35)
ORANGE = (255, 165, 0)
ORANGE_RED = (255, 36, 0)
PEACH_PUFF = (255, 218, 185)
SALMON = (250, 128, 114)

# RED/PINK
DEEP_PINK = (255, 20, 147)
CRIMSON = (153, 0, 0)
DUSTY_ROSE = (133, 99, 99)
FIREBRICK = (178, 34, 34)
FELDSPAR = (209, 146, 117)
FLESH = (245, 204, 176)
FREE_SPEECH_MAGENTA = (227, 91, 216)
FREE_SPEECH_RED = (192, 0, 0)
HOT_PINK = (255, 105, 180)
INDIAN_RED = (205, 92, 92)
LIGHT_PINK = (255, 182, 193)
MEDIUM_VIOLET_RED = (199, 21, 133)
MISTY_ROSE = (255, 228, 225)
PALE_VIOLET_RED = (219, 112, 147)
PINK = (255, 192, 203)
SCARLET = (140, 23, 23)
SPICY_PINK = (255, 28, 174)
TOMATO = (255, 99, 71)
VIOLET_RED = (208, 32, 144)

# PURPLE/PINK
DARK_ORCHID = (153, 50, 204)
DARK_PURPLE = (135, 31, 120)
DRS_PURPLE = (147, 24, 108)
DARK_VIOLET = (148, 0, 211)
FUCHSIA = (255, 0, 255)
IMMUTABLE_PURPLE = (224, 158, 248)
LAVENDER = (230, 230, 250)
LAVENDER_BLUSH = (255, 240, 245)
MAGENTA = (255, 0, 255)
MAROON = (176, 48, 96)
MEDIUM_ORCHID = (186, 85, 211)
MEDIUM_PURPLE = (147, 112, 219)
NEON_PINK = (255, 110, 199)
ORCHID = (218, 112, 214)
PLUM = (221, 160, 221)
PURPLE = (160, 32, 240)
THISTLE = (216, 191, 216)
VIOLET = (238, 130, 238)
VIOLET_BLUE = (159, 95, 159)
UBE_PURPLE = (136, 120, 195)

# YELLOWS/GOLDS
BLANCHED_ALMOND = (255, 235, 205)
DARK_GOLDENROD = (184, 134, 11)
LEMON_CHIFFON = (255, 250, 205)
LIGHT_GOLDENROD = (238, 221, 130)
LIGHT_GOLDENROD_YELLOW = (250, 250, 210)
LIGHT_YELLOW = (255, 255, 224)
PALE_GOLDENROD = (238, 232, 170)
PAPAYA_WHIP = (255, 239, 213)
CORNSILK = (255, 248, 220)
GOLDENROD = (218, 165, 32)
MOCCASIN = (255, 228, 181)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
MEDIUM_GOLDENROD = (234, 234, 174)
MUSTARD_YELLOW = (254, 220, 86)
BURNT_YELLOW = ()
ZENYTE_YELLOW = (218, 132, 25)

# WHITES/OFF-WHITES
ANTIQUE_WHITE = (250, 235, 215)
FLORAL_WHITE = (255, 250, 240)
GHOST_WHITE = (248, 248, 255)
NAVAJO_WHITE = (255, 222, 173)
OLD_LACE = (253, 245, 230)
WHITE_SMOKE = (245, 245, 245)
GAINSBORO = (220, 220, 220)
IVORY = (255, 255, 240)
LINEN = (250, 240, 230)
SEASHELL = (255, 245, 238)
SNOW = (255, 250, 250)
WHEAT = (245, 222, 179)
QUARTZ = (217, 217, 243)

RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
RANDOM_COLOR2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
RANDOM_COLOR3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

RANDOM_RED = (random.randint(185, 255), random.randint(0, 125), random.randint(0, 125))
RANDOM_GREEN = (random.randint(0, 125), random.randint(185, 255), random.randint(0, 125))
RANDOM_BLUE = (random.randint(0, 125), random.randint(0, 125), random.randint(185, 255))

RANDOM_COLORS = [RANDOM_COLOR, RANDOM_COLOR2, RANDOM_COLOR3, RANDOM_BLUE, RANDOM_GREEN, RANDOM_RED]

ALPHANUMERIC_AXIOMS = {
    " ": " ",
    ":": ":",
    "-": "-",
    "_": "_",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "a": "b3",
    "b": "a4",
    "c": "c1",
    "d": "do",
    "e": "el",
    "f": "f9",
    "g": "gg",
    "h": "h9",
    "i": "il",
    "j": "jo",
    "k": "ke",
    "l": "l0",
    "m": "ma",
    "n": "ne",
    "o": "wl",
    "p": "0n",
    "q": "qi",
    "r": "rt",
    "s": "sn",
    "t": "tp",
    "u": "ui",
    "v": "va",
    "w": "w1",
    "x": "xy",
    "y": "yi",
    "z": "ze"
}

MORSE_CODE_AXIOMS = {
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--.."
}
PUNCTUATION_COORDS = {
    ",": [(1, 1), (0, 5), (0, 0)],
    "'": [(2, 0), (1, 2), (4, 1)],
    " ": [(0, 2), (2, 2), (7, 3)],
    ":": [(1, 0), (3, 4), (8, 4)],
    "-": [(0, 0), (4, 6), (1, 5)],
    "_": [(2, 3), (5, 5), (2, 6)],
    "!": [(2, 0), (6, 8), (4, 7)],
    ".": [(3, 1), (7, 7), (5, 8)],
    "?": [(1, 0), (8, 3), (5, 9)],
    ";": [(0, 2), (9, 5), (6, 0)],
    "*": [(2, 0), (0, 9), (9, 1)],
    "\"": [(2, 0), (6, 8), (4, 7)],
    "=": [(3, 1), (7, 7), (5, 8)],
    "/": [(1, 0), (8, 3), (5, 9)],
    "+": [(0, 2), (9, 5), (6, 0)],
    "&": [(2, 0), (0, 9), (9, 1)]
}

ALPHANUMERIC_COORDS = {
    " ": [(1, 1), (0, 5), (0, 0)],
    ":": [(2, 0), (1, 2), (4, 1)],
    "_": [(0, 2), (2, 2), (7, 3)],
    "0": [(1, 0), (3, 4), (8, 4)],
    "1": [(0, 0), (4, 6), (1, 5)],
    "2": [(2, 3), (5, 5), (2, 6)],
    "3": [(2, 0), (6, 8), (4, 7)],
    "4": [(3, 1), (7, 7), (5, 8)],
    "5": [(1, 0), (8, 3), (5, 9)],
    "6": [(0, 2), (9, 5), (6, 0)],
    "7": [(2, 0), (0, 9), (9, 1)],
    "8": [(2, 2), (1, 6), (6, 2)],
    "9": [(1, 3), (2, 5), (3, 3)],
    "a": [(2, 1), (3, 1), (3, 4)],
    "b": [(0, 3), (4, 0), (6, 5)],
    "c": [(2, 0), (5, 2), (5, 6)],
    "d": [(0, 2), (6, 0), (2, 7)],
    "e": [(2, 2), (7, 1), (5, 8)],
    "f": [(0, 2), (8, 2), (2, 9)],
    "g": [(2, 1), (9, 7), (1, 0)],
    "h": [(3, 0), (0, 4), (1, 1)],
    "i": [(1, 2), (1, 5), (1, 2)],
    "j": [(1, 3), (2, 8), (4, 3)],
    "k": [(1, 1), (3, 1), (1, 4)],
    "l": [(0, 3), (4, 2), (4, 5)],
    "m": [(0, 3), (5, 2), (7, 6)],
    "n": [(2, 1), (6, 3), (7, 7)],
    "o": [(2, 0), (7, 6), (8, 8)],
    "p": [(2, 2), (8, 9), (9, 9)],
    "q": [(1, 0), (9, 3), (5, 0)],
    "r": [(0, 2), (0, 6), (3, 1)],
    "s": [(2, 3), (1, 2), (6, 2)],
    "t": [(3, 1), (2, 0), (5, 3)],
    "u": [(0, 1), (3, 3), (2, 4)],
    "v": [(1, 0), (4, 6), (2, 5)],
    "w": [(1, 2), (5, 9), (0, 6)],
    "x": [(1, 3), (6, 1), (1, 7)],
    "y": [(2, 1), (7, 4), (4, 8)],
    "z": [(0, 2), (8, 3), (0, 2)]
}


ALPHANUMERIC_NOTE_PATTERNS = {
    " ": ["..+.", "-+-=", "=..="],
    ":": ["..-+", "+--=", "__//"],
    "-": [".._.", "+==+", "--=="],
    "_": ["..=.", "=-++", "/---"],
    "0": ["../.", "-++=", "///="],
    "1": [".++.", "//==", "++.."],
    "2": [".--+", "/==/", "-+-+"],
    "3": [".__+", "=/=+", "/=/="],
    "4": [".==-", "._=+", "-+//"],
    "5": [".//-", "__.+", "/-_-"],
    "6": [".+-.", "+=._", "__=="],
    "7": [".+_+", "-_.=", "_./="],
    "8": [".+=+", "=+/+", "___="],
    "9": [".+/=", "-=/+", "...="],
    "a": [".-+=", "--/_", "=_=="],
    "b": [".---", "=-/_", "_..-"],
    "c": [".-=+", "/_/-", "-+-+"],
    "d": [".-/+", "--/.", ".+-+"],
    "e": ["._++", "==/_", "/-_/"],
    "f": ["._--", "-=/-", "-.-_"],
    "g": ["._-=", ".//=", "_._."],
    "h": ["._-/", "//=/", "._.-"],
    "i": [".=-+", "/_//", "__.."],
    "j": [".=_-", "_+//", "=+=="],
    "k": [".=__", "+==/", "+==="],
    "l": [".=_/", ".=/_", "==+="],
    "m": ["./+-", "_/+=", "===+"],
    "n": ["._/-", "==_/", "...="],
    "o": [".-/_", "=+=/", "_-_="],
    "p": ["._/=", "+=/_", "==__"],
    "q": ["__//", "+//=", "=_-="],
    "r": ["/-_=", "./.+", "=-_="],
    "s": [".+--", "+/._", "=++="],
    "t": ["-+._", "_..=", "=-+="],
    "u": ["/-._", "//+-", "=+-="],
    "v": ["./__", "=._=", "_=_="],
    "w": ["_-/.", "+.=-", "=_=-"],
    "x": [".__/", "+._+", "=--="],
    "y": ["+_-.", "=-==", "/./."],
    "z": [".=_+", "-=++", "././"],
}

LAYER_DICT = {
    "None": {
        "rounded": [10],
        "sparkles": [10],
        "shell": [10],
        "decor": [10]
    },
    "Alien": {
        "body": [10, "ALEEN"],
        "eyes": [10],
        "mouth": [10],
        "tentacles": [10],
    },
    "Asteroid": {
        "core": [10, "ASTROID"],
        "metal": [10],
        "rock": [10],
        "shell": [10],
    },
    "Ball": {
        "base": [10, "OKAY"],
        "casing": [10],
        "shade": [10],
        "sparkles": [10],
    },
    "Portal": {
        "casing": [10],
        "cover": [10],
        "decor": [10],
        "metal": [10],
        "shell": [10],
    },
    # "Ball": {
    #     "base": ["Ants", "Bacteria", "Cave", "Dots", "Eye", "Glitched", "Shines", "Snow", "Spots", "Termites"],
    #     "casing": ["Compass", "Dstar", "Eth", "Jacobs", "Ladder", "Minus", "Spider", "Wall", "Web", "Xhair"],
    #     "shade": ["Cloud", "Crab", "Frog", "Jelly", "Low", "Moon", "Night", "Noon", "Open", "Tree"],
    #     "sparkles": ["Blank", "Check", "Lots", "Milky", "None", "Round", "Shadow", "Split", "Stars", "Trip"],
    # },
    "Medallion": {
        "base": [10],
        "cover": [10],
        "triangle": [10],
        "decor": [10],
    },
    "Platform": {
        "Emoji": [10],
        "Mandel": [10],
        "Vertical": [10],
        "Horizontal": [10],
    },
    "Ship": {
        "nose": [10],
        "body": [10],
        "wings": [10],
        "engine": [10],
    },
    "Sword": {
        "handle": [10],
        "hilt": [10],
        "blade": [10],
        "charm": [10],
    },
    "Tribloc": {
        "block": [10],
        "lepht": [10],
        "rhite": [10],
        "taup": [10],
    },
    "RTJ": {
        "violent_hand": [10],
        "peaceful_hand": [10],
        "pointing": [10],
        "holding": [10],
    },
    "Boat": {
        "bowsprit": [10],
        "hull": [10],
        "masts": [10],
        "rudder": [10]
    },
    "Goal": {
        "arrive": [10],
        "kill": [10],
        "survive": [10],
        "collect": [10]
    }
}

PUNCTUATION_COLORS = {
    ",": LAWN_GREEN,
    "'": BLANCHED_ALMOND,
    " ": FREE_SPEECH_MAGENTA,
    ":": VIOLET_RED,
    "-": SAGE_GREEN,
    "_": DARK_ORANGE,
    "!": WHEAT,
    ".": SEMI_SWEET_CHOCOLATE,
    "?": BLACK,
    ";": PURPLE,
    "*": POWDER_BLUE,
    "\"": FELDSPAR,
    "=": PEACH_PUFF,
    "+": PAPAYA_WHIP,
    "/": DEEP_PINK,
    "&": BAKERS_CHOCOLATE
}

ALPHANUMERIC_COLORS = {
    " ": SNOW,
    ":": LINEN,
    "-": WHEAT,
    "_": GREY,
    "0": GREY75,
    "1": GREY25,
    "2": PURPLE,
    "3": DARK_GREEN_COPPER,
    "4": MINT_CREAM,
    "5": DARK_RED,
    "6": FELDSPAR,
    "7": MEDIUM_PURPLE,
    "8": SEMI_SWEET_CHOCOLATE,
    "9": MOCCASIN,
    # "a": BLACK,
    # "b": YELLOW,
    # "c": BLACK,
    # "d": MUSTARD_YELLOW,
    # "e": ZENYTE_YELLOW,
    # "f": LIGHT_GOLDENROD_YELLOW,
    "a": AQUA,
    "b": BROWN,
    "c": CORNSILK,
    "d": DARK_WOOD,
    "e": EGGSHELL_WHITE,
    "f": FLESH,
    "g": GOLD,
    "h": HONEYDEW,
    "i": IVORY,
    "j": JUNGLE_GREEN,
    "k": KHAKI,
    "l": LAVENDER,
    "m": MAGENTA,
    "n": NAVAJO_WHITE,
    "o": OLIVE,
    "p": PURPLE,
    "q": QUARTZ,
    "r": RED,
    "s": SKY_BLUE,
    "t": TAN,
    "u": UBE_PURPLE,
    "v": VIOLET,
    "w": WHEAT,
    "x": X_RAY_GRAY,
    "y": YELLOW,
    "z": ZENYTE_YELLOW
}

PUNCTUATION_WORD_LISTS = {
    ",": ["comma", "coma", "kona", "players", "right", "turtle", "look", "please", "feel", "less"],
    "'": ["apostrophe", "trophy", "post", "apostle", "hustle", "bussin", "combine", "pretty", "if", "you"],
    " ": ["space", "blank", "empty", "nope", "paris", "almost", "copper", "whole", "world", "ice"],
    ":": ["colon", "dots", "top", "heart", "frankfurt", "star", "silver", "try", "too", "hard"],
    "-": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "_": ["under", "line", "bottom", "score", "moscow", "over", "gold", "why", "do", "I"],
    "!": ["comma", "coma", "kona", "players", "right", "turtle", "look", "please", "feel", "less"],
    ".": ["apostrophe", "trophy", "post", "apostle", "hustle", "bussin", "combine", "pretty", "if", "you"],
    "?": ["space", "blank", "empty", "nope", "paris", "almost", "copper", "whole", "world", "ice"],
    ";": ["colon", "dots", "top", "heart", "frankfurt", "star", "silver", "try", "too", "hard"],
    "*": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "\"": ["under", "line", "bottom", "score", "moscow", "over", "gold", "why", "do", "I"],
    "=": ["colon", "dots", "top", "heart", "frankfurt", "star", "silver", "try", "too", "hard"],
    "+": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "/": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "&": ["under", "line", "bottom", "score", "moscow", "over", "gold", "why", "do", "I"]
}
MORSE_CODE_RULES = {
    "-": "ANGLE+36",
    ".": "LINE+30"
}
ALPHANUMERIC_RULES = {
    " ": "PUSH+1",
    ":": "PUSH+2",
    "-": "POP-1",
    "_": "POP-2",
    "0": "ANGLE-120",
    "1": "ANGLE-90",
    "2": "ANGLE-60",
    "3": "ANGLE-45",
    "4": "ANGLE-12",
    "5": "ANGLE+12",
    "6": "ANGLE+45",
    "7": "ANGLE+60",
    "8": "ANGLE+90",
    "9": "ANGLE+120",
    "a": "LINE+8",
    "b": "LINE+8",
    "c": "LINE+8",
    "d": "LINE+6",
    "e": "LINE+8",
    "f": "LINE+8",
    "g": "LINE-36",
    "h": "LINE-1",
    "i": "LINE+8",
    "j": "LINE+8",
    "k": "LINE-8",
    "l": "LINE-45",
    "m": "LINE-8",
    "n": "LINE+12",
    "o": "LINE+8",
    "p": "LINE-1",
    "q": "LINE+8",
    "r": "LINE+45",
    "s": "LINE+8",
    "t": "LINE-8",
    "u": "LINE+1",
    "v": "LINE+8",
    "w": "LINE-1",
    "x": "LINE+8",
    "y": "LINE+8",
    "z": "LINE-8",
}

ALPHANUMERIC_WORD_LISTS = {
    ",": ["comma", "coma", "kona", "players", "right", "turtle", "look", "please", "feel", "less"],
    "'": ["apostrophe", "trophy", "post", "apostle", "hustle", "bussin", "combine", "pretty", "if", "you"],
    " ": ["space", "blank", "empty", "nope", "paris", "almost", "copper", "whole", "world", "ice"],
    ":": ["colon", "dots", "top", "heart", "frankfurt", "star", "silver", "try", "too", "hard"],
    "-": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "_": ["under", "line", "bottom", "score", "moscow", "over", "gold", "why", "do", "I"],
    "0": ["zero", "none", "hero", "villain", "beijing", "eye", "platinum", "yeah", "baby", "ever"],
    "1": ["one", "lonely", "win", "juan", "tokyo", "hand", "sapphire", "run", "the", "jewels"],
    "2": ["two", "too", "lose", "to", "madagascar", "foot", "emerald", "render", "final", "fantasy"],
    "3": ["three", "tree", "charm", "triangle", "chicago", "knee", "ruby", "crash", "hit", "wall"],
    "4": ["four", "fore", "core", "square", "seattle", "ear", "diamond", "in", "right", "now"],
    "5": ["five", "high", "hive", "pentagon", "miami", "hair", "opal", "need", "miracle", "stranded"],
    "6": ["six", "sticks", "chicks", "angle", "detroit", "finger", "jade", "let", "down", "around"],
    "7": ["seven", "heaven", "Kevin", "shovel", "mesa", "toe", "topaz", "head", "died", "hole"],
    "8": ["eight", "straight", "infinite", "ate", "youngstown", "bones", "quartz", "call", "name", "side"],
    "9": ["nine", "no", "max", "final", "akron", "teeth", "onyx", "headphone", "window", "door"],
    "a": ["alpha", "after", "aloha", "all", "atlanta", "aisle", "amber", "ape", "apple", "acura"],
    "b": ["bravo", "being", "bang", "bunny", "buffalo", "banquet", "blue", "bat", "broccoli", "bently"],
    "c": ["charlie", "cold", "climb", "cow", "cleveland", "concert", "cerulean", "cat", "cauliflower", "car"],
    "d": ["delta", "dinner", "drink", "dead", "denver", "diner", "dandelion", "dog", "dragonfruit", "dodge"],
    "e": ["echo", "evening", "east", "eat", "ellensburg", "elegant", "ecru", "elephant", "eggplant", "elantra"],
    "f": ["foxtrot", "fire", "flint", "flower", "flynt", "ferocious", "firebrick", "fox", "fennel", "ford"],
    "g": ["golf", "grass", "golden", "game", "georgia", "giant", "green", "gorilla", "grape", "golfcart"],
    "h": ["hotel", "hurried", "hungry", "humble", "houston", "hurling", "hotpink", "hippopotamus", "honeydew", "honda"],
    "i": ["india", "in", "ice", "into", "idaho", "icicle", "indigo", "iguana", "iceberg", "illicit"],
    "j": ["juliette", "just", "jump", "Jessica", "jamestown", "jungle", "jade", "jaguar", "jalapenos", "jetplane"],
    "k": ["kilo", "killed", "knight", "kindle", "kentucky", "kingly", "khaki", "kangaroo", "kale", "kudi"],
    "l": ["lima", "last", "long", "list", "london", "lost", "lavender", "llama", "legumes", "lincoln"],
    "m": ["mike", "month", "mass", "moon", "massachusetts", "more", "magenta", "monkey", "mushroom", "minivan"],
    "n": ["november", "near", "noble", "noon", "nashville", "never", "navyblue", "newt", "napa", "nas"],
    "o": ["oscar", "open", "opera", "out", "oakland", "optic", "orchid", "orangutan", "orange", "october"],
    "p": ["papa", "punch", "prince", "penelope", "philadelphia", "pan", "periwinkle", "platypus", "potato", "poptart"],
    "q": ["quebec", "queen", "quest", "quilt", "queens", "question", "quicksilver", "quail", "quinoa", "quack"],
    "r": ["romeo", "really", "random", "rake", "reno", "ranch", "red", "rhinoceros", "radish", "reel"],
    "s": ["sierra", "sold", "simple", "sake", "scranton", "sacred", "saffron", "snake", "spinach", "soil"],
    "t": ["tango", "time", "topple", "take", "tuscaloosa", "ton", "tawny", "turkey", "taro", "taser"],
    "u": ["uniform", "until", "under", "utility", "ukraine", "ultra", "ube", "unicorn", "ugli", "up"],
    "v": ["victor", "very", "vixen", "vampire", "vienna", "violence", "violet", "vulture", "vanilla", "voss"],
    "w": ["whiskey", "wise", "west", "well", "wuhan", "well", "white", "whale", "watermelon", "wet"],
    "x": ["x-ray", "x-men", "Xena", "xylophone", "xi'an", "xacto", "xanadu", "xenops", "ximenia", "xoom"],
    "y": ["yankee", "yelled", "yip", "yuck", "yakima", "yarn", "yellow", "yak", "yam", "yup"],
    "z": ["zulu", "zebra", "zoinks", "zealand", "zhengzhou", "zombie", "zaffre", "zebra", "zucchini", "zoom"]
}
email_domains = [
    "gmail.com", "yahoo.com", "outlook.com", "aol.com", "icloud.com", "protonmail.com",
    "gmx.com", "zoho.com", "mail.com", "lycos.com", "inbox.com",
    "yandex.com", "tutanota.com", "fastmail.com", "hushmail.com", "mailfence.com",
    "rackspace.com", "runbox.com", "posteo.net", "disroot.org"
]
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen"
]
last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
    "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
    "Moore", "Martin", "Jackson", "Thompson", "White"
]
business_abbreviations = [
    "LLC", "Inc.", "Co.", "Corp.", "Ltd.", "Ltda.", "LLP", "PLLC", "PLC", "LLLP"
]
sub_clients = [
    "Mila", "Maxwell", "Tucker", "Toby", "Frick", "Frack", "Snowball", "Kora", "Church", "Henry", "Ollie", "Luna",
    "Bruiser", "Pearl", "Panther"
]
animal_sounds = [
    "Bark", "Meow", "Quack", "BaAa", "Moo", "Oink", "Chirp", "Neigh", "Ribbit", "Hiss", "Roar"
]


@dataclass
class TexiotyProfile:
    username: str
    password: str
    color_theme: tuple


available_profiles = {
    "guest": TexiotyProfile("Guest", "p455",
                            (rgb_to_hex(DARK_BROWN),
                             rgb_to_hex(SAGE_GREEN),
                             rgb_to_hex(LIGHT_GOLDENROD_YELLOW))),
    "bluebeard": TexiotyProfile("Bluebeard", "p455",
                                (rgb_to_hex(DARK_SLATE_BLUE),
                                 rgb_to_hex(LIGHT_SLATE_BLUE),
                                 rgb_to_hex(GHOST_WHITE)))
}

LOADING_TERMS = ["Downloading", "Updating", "Executing", "Finding", "Searching for", "Deleting",
                 "Creating", "Mixing", "Baking", "Loading", "Uploading", "Rolling", "Planting",
                 "Growing", "Typing", "Brewing", "Shopping for", "Fishing for", "Stashing", "Formatting",
                 "Coiling", "Breaking", "Toasting", "Meowing", "Pouring"]
MID_TERMS = ["a", "all the", "some", "the most", "that", "this", "many", "the entire", "the empty"]
LOADED_TERMS = ["cookie", "cache", "chip", "lock", "keyboard", "logic", "code", "math", "cereal",
                "vape", "water", "juice", "rug", "cord", "port", "puppy", "kitten", "gaim", "key",
                "phone", "table", "mouse", "coffee", "tea", "python", "java", "screen", "virus",
                "bread", "toast", "ball", "cloud", "recycling bin", "mug", "desk"]
LOADING_BRACKETS = ["{}", "[]", "()", "<>", "‹›", "«»", "↻↺"]


def random_loading_phrase() -> str:
    mid_term = random.choice(MID_TERMS)
    bracks = random.choice(LOADING_BRACKETS)
    phrase = random.choice(LOADING_TERMS)
    phrase += " " + mid_term + " "
    if mid_term in ["some", "all the", "the most", "many"]:
        phrase += random.choice(LOADED_TERMS) + "'s"
    else:
        phrase += random.choice(LOADED_TERMS)
    # phrase += " " + random.choice("•⌂×¤±")
    # phrase += bracks[0] + random.choice(".,_") + random.choice("-=+") + random.choice("^`*") + bracks[1]
    return phrase + ("." * random.randint(2, 5))
    # return phrase


# @dataclass
# class DisplayComponent:
#     """
#     Display some text as a label widget or edit some text as an entry widget.
#     """
#     default_value: str
#     var: tk.StringVar = None
#     label_widget: tk.Widget = None
#     new_entry_widget: tk.Widget = None
#     edit_entry_widget: tk.Widget = None
#
#     def set_var(self, new_var: str):
#         """
#         Set the StringVar of this display component.
#         :param new_var: String of info.
#         :return:
#         """
#         self.var.set(new_var)
