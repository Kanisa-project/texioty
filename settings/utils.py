import json
import math
import os
import glob
import random
from dataclasses import dataclass

# from pytube import YouTube

import requests
# from dotenv import load_dotenv
from settings import themery as t, alphanumers as a

# load_dotenv()

PRO_TIPS = ["Double click the click-commands to bring focus back to Texity.",
            "'welcome' 'commands' 'help' are three helpful commands to welcome a user."]


def check_file_exists(path: str) -> bool:
    """Use glob to check if a file exists."""
    if glob.glob(path):
        return True
    return False

def project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def asset_path(*parts: str) -> str:
    return os.path.join(project_root(), "..", "assets", *parts)

def output_root() -> str:
    """
    Root folder for generated/output files. Adjust as needed.
    """
    return os.path.join(project_root(), "filesOutput")

def input_root() -> str:
    """
    Root folder for input files, such as fonts, sounds or images. Adjust as needed.
    """
    return os.path.join(project_root(), "..", "filesInput")

def output_path(*parts: str) -> str:
    """
    Build a path inside the output directory.
    """
    return os.path.join(output_root(), *parts)

def ensure_parent_dir(file_path: str) -> str:
    """
    Ensure the parent directory of file_path exists. Return the original file_path.
    """
    parent = os.path.dirname(file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    return file_path

def safe_filename(name: str, replacement: str = "_") -> str:
    """
    Sanitize a filename or path segment by replacing common invalid characters.
    Keeps it simple and cross-platform friendly.
    """
    invalid = '<>:"/\\|?*\n\r\t'
    return "".join((c if c not in invalid else replacement) for c in name).strip()

def get_stock_price(ticker):
    try:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={ticker}"
        response = requests.get(url, headers={"X-Api-Key": os.getenv("API_NINJAS")})
        data = response.json()
    finally:
        data = {}
    return data

def clamp(n, minn, maxn) -> int:
    return max(min(maxn, n), minn)


def set_masterpiece_size(image_size: str) -> tuple[int, int]:
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


def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])


@dataclass
class TexiotyProfile:
    username: str
    password: str
    color_theme: tuple



available_profiles = {
    "guest": TexiotyProfile("Guest", "p455",
                            (rgb_to_hex(t.DARK_BROWN),
                             rgb_to_hex(t.SAGE_GREEN),
                             rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW))),
    "bluebeard": TexiotyProfile("Bluebeard", "p455",
                                (rgb_to_hex(t.DARK_SLATE_BLUE),
                                 rgb_to_hex(t.LIGHT_SLATE_BLUE),
                                 rgb_to_hex(t.GHOST_WHITE)))
}
for profile in glob.glob("filesOutput/.profiles/*.json"):
    if "trevor2" in profile:
        continue
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

def string_to_morse(reg_str: str) -> str:
    morse_str = ''
    print(reg_str)
    for letter in reg_str:
        morse_str += s.MORSE_CODE_AXIOMS[letter.lower()]
    return morse_str


def lsystem_morse_coder(lstring: str, start_point=(320, 320), start_length=32, start_width=1, start_color=t.ORANGE) -> list:
    """
    Parses the lstring into a dictionary of line_tuples which contain 2 points, a width and color.

    :param lstring: L-System string to apply rules from.
    :param start_point: Beginning point of a whole line.
    :param start_length: Starting length to move forward.
    :param start_width: Width of a whole line to start at.
    :param start_color: Color of the first line portion.
    :return: list
    """
    angle = 0
    length = start_length
    w, h = (640, 640)
    width = start_width
    color = start_color
    prev_line_tuple = ((start_point[0], start_point[1], start_point[0], start_point[1]), width, color)
    # point_list = [prev_line_tup]
    line_points_list = [prev_line_tuple]

    for c in lstring:
        if a.MORSE_CODE_RULES[c.lower()].startswith("ANGLE"):
            angle += int(a.MORSE_CODE_RULES[c.lower()].split("ANGLE")[1])
            angle = clamp(angle, -360, 360)
        if a.MORSE_CODE_RULES[c.lower()].startswith("LINE"):
            length = int(a.MORSE_CODE_RULES[c.lower()].split("LINE")[1])
        line_tuple = plan_angled_line(prev_line_tuple[0][2], prev_line_tuple[0][3],
                                      angle, length, width,
                                      color, (w, h))
        line_points_list.append(line_tuple)
        prev_line_tuple = line_tuple
        # color = random.choice(RANDOM_COLORS)
    return line_points_list

def plan_angled_line(x, y, angle, length, width, color, img_size):
    endx = x + length * math.cos(math.radians(angle + 180)) * -1
    endy = y + length * math.sin(math.radians(angle + 180)) * -1
    return (clamp(x, 0, img_size[0]),
            clamp(y, 0, img_size[1]),
            clamp(endx, 0, img_size[0]),
            clamp(endy, 0, img_size[1])), width, color

def retrieve_lab_profiles(lab_to_get: str) -> dict:
    with open(f'helpers/promptaires/tcg_lab/lab_profiles/{lab_to_get}.json') as labbed_tcg:
        data = json.load(labbed_tcg)
        return data

def retrieve_tcg_profiles(tcg_to_get: str) -> dict:
    with open(f'helpers/promptaires/tcg_lab/tcg_profiles/{tcg_to_get}.json') as labbed_tcg:
        data = json.load(labbed_tcg)
        return data

def retrieve_worx_profiles(equipment: str) -> dict:
    with open(f'helpers/promptaires/worx_hop/equipments/{equipment}.json') as json_equip:
        data = json.load(json_equip)
        return data