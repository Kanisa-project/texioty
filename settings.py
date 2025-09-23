import glob
import json
import math
from dataclasses import dataclass
import random
import theme

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


ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyz0123456789"
MIN_CREATION_UTC = 1119553200
MAX_CREATION_UTC = 1633120253

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
                            (rgb_to_hex(theme.DARK_BROWN),
                             rgb_to_hex(theme.SAGE_GREEN),
                             rgb_to_hex(theme.LIGHT_GOLDENROD_YELLOW))),
    "bluebeard": TexiotyProfile("Bluebeard", "p455",
                                (rgb_to_hex(theme.DARK_SLATE_BLUE),
                                 rgb_to_hex(theme.LIGHT_SLATE_BLUE),
                                 rgb_to_hex(theme.GHOST_WHITE)))
}
for profile in glob.glob(".profiles/*.json"):
    with open(profile, "r") as f:
        profile_data = json.load(f)
        print(profile_data)
        available_profiles[profile_data['texioty']["username"]] = TexiotyProfile(
            profile_data['texioty']["username"],
            profile_data['texioty']["password"],
            (profile_data['texioty']["color_theme"]["background"],
             profile_data['texioty']["color_theme"]["foreground"],
             profile_data['texioty']["color_theme"]["accent"])
        )
LOADING_TERMS = ["Downloading", "Updating", "Executing", "Finding", "Searching for", "Deleting",
                 "Creating", "Mixing", "Baking", "Loading", "Uploading", "Rolling", "Planting",
                 "Growing", "Typing", "Brewing", "Shopping for", "Fishing for", "Stashing", "Formatting",
                 "Coiling", "Breaking", "Toasting", "Meowing", "Pouring"]
MID_TERMS = ["a", "all the", "some", "the most", "that", "this", "many", "the entire", "the empty"]
LOADED_TERMS = ["cookie", "cache", "chip", "lock", "keyboard", "logic", "code", "math", "cereal",
                "vape", "water", "juice", "rug", "cord", "port", "puppy", "kitten", "gaim", "key",
                "phone", "table", "mouse", "coffee", "tea", "python", "java", "screen", "virus",
                "bread", "toast", "ball", "cloud", "recycling bin", "mug", "desk"]
LOADING_BRACKETS = ["⁅⁆", "[]", "()", "<>", "‹›", "«»", "⎡⎦", "❲❳", "⸂⸃", "｢｣", "〚〛"]


def random_loading_phrase() -> str:
    mid_term = random.choice(MID_TERMS)
    bracks = random.choice(LOADING_BRACKETS)
    phrase = bracks[0] + random.choice("•⌂×¤±") + bracks[1]
    phrase += '  ' + random.choice(LOADING_TERMS)
    phrase += " " + mid_term + " "
    if mid_term in ["some", "all the", "the most", "many"]:
        phrase += random.choice(LOADED_TERMS) + "'s"
    else:
        phrase += random.choice(LOADED_TERMS)
    return phrase + ("." * random.randint(2, 5))
