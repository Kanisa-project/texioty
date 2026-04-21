import json
import math
import os
import glob
import random
from dataclasses import dataclass
from typing import List

# from pytube import YouTube

import requests
from PIL import ImageFont, Image

# from dotenv import load_dotenv
from src.texioty.settings import themery as t, alphanumers as a

# load_dotenv()

PRO_TIPS = ["Double click the click-commands to bring focus back to Texity.",
            "'welcome' 'commands' 'help' are three helpful commands to welcome a user.",
            "Arguments in square brackets [] are required, and arguments in parentheses () are optional."]


def input_path(*parts: str) -> str:
    return os.path.join(input_root(), *parts)

def output_path(*parts: str) -> str:
    return os.path.join(output_root(), *parts)

def cache_path(*parts: str) -> str:
    return os.path.join(output_root(), "cache", *parts)

def prepped_dir(*parts: str) -> str:
    return os.path.join(cache_path("foto_worx", "prepped"), *parts)

def prepped_path(*parts: str) -> str:
    return ensure_parent_dir(prepped_dir(*parts))

def save_prepped_image(image, *parts: str, **save_kwargs) -> str:
    save_path = prepped_path(*parts)
    image.save(save_path, **save_kwargs)
    return save_path

def list_prepped_images(*parts: str, pattern: str = "*.png") -> list[str]:
    directory = prepped_dir(*parts)
    if not os.path.isdir(directory):
        return []
    return sorted(glob.glob(os.path.join(directory, pattern)))

def load_prepped_image(*parts: str) -> Image.Image:
    return Image.open(prepped_path(*parts))

def asset_path(*parts: str) -> str:
    return os.path.join(project_root(), "assets", *parts)

PROFILE_ROOT_BUILDERS = (
    output_path,
    input_path,
    asset_path,
)

PROFILE_LOCATIONS = {
    "lab": (
        ("helpers", "promptaires", "tcg_lab", "lab_presets"),
        ("tcg_lab", "lab_presets"),
    ),
    "tcg": (
        ("helpers", "promptaires", "tcg_lab", "tcg_profiles"),
        ("tcg_lab", "tcg_presets"),

    ),
    "worx": (
        ("foto_worx", "worx_profiles"),
        ("helpers", "promptaires", "worx_hop", "worx_profiles"),
        ("worx_hop", "worx_profiles"),
    ),
    "user": (
        (".profiles",),
    ),
}

def _candidate_profile_paths(profile_group: str, profile_name: str) -> list[str]:
    file_name = f"{profile_name}.json"
    candidate_paths = []

    for root_builder in PROFILE_ROOT_BUILDERS:
        for relative_dir in PROFILE_LOCATIONS[profile_group]:
            candidate_paths.append(root_builder(*relative_dir, file_name))

    fallback_dirs = {
        "lab": (("helpers", "promptaires", "tcg_lab", "lab_presets"),),
        "tcg": (("tcg_lab",),),
        "worx": (("helpers", "promptaires", "worx_hop", "worx_profiles"),),
    }

    for relative_dir in fallback_dirs.get(profile_group, ()):
        candidate_paths.append(os.path.join(project_root(), *relative_dir, file_name))

    seen = set()
    unique_paths = []
    for path in candidate_paths:
        normalized = os.path.normpath(path)
        if normalized not in seen:
            seen.add(normalized)
            unique_paths.append(path)
    return unique_paths

def _candidate_profile_dirs(profile_group: str) -> list[str]:
    candidate_dirs = []

    for root_builder in PROFILE_ROOT_BUILDERS:
        for relative_dir in PROFILE_LOCATIONS[profile_group]:
            candidate_dirs.append(root_builder(*relative_dir))

    fallback_dirs = {
        "user": (("filesOutput", ".profiles"),),
    }

    for relative_dir in fallback_dirs.get(profile_group, ()):
        candidate_dirs.append(os.path.join(project_root(), *relative_dir))

    seen = set()
    unique_dirs = []
    for path in candidate_dirs:
        normalized = os.path.normpath(path)
        if normalized not in seen:
            seen.add(normalized)
            unique_dirs.append(path)

    return unique_dirs

def check_file_exists(path: str) -> bool:
    """Use glob to check if a file exists."""
    if glob.glob(path):
        return True
    return False

def project_root() -> str:
    return os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    )

def output_root() -> str:
    """
    Root folder for generated/output files. Adjust as needed.
    """
    return os.path.join(project_root(), "filesOutput")

def input_root() -> str:
    """
    Root folder for input files, such as fonts, sounds or images. Adjust as needed.
    """
    return os.path.join(project_root(), "filesInput")


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


def polypointlist(sides: int, ophset: int, cx: int, cy: int, radius: int) -> list:
    step = 2 * math.pi / sides
    offset = math.radians(ophset)
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

def get_point_delta(point1, point2) -> tuple:
    return point2[0] - point1[0], point2[1] - point1[1]

def get_random_font(font_size: int):
    return ImageFont.truetype(random.choice(glob.glob('src/texioty/assets/fonts/*.ttf')), size=font_size)

def get_font_server_name(server_fonts: List[str], font_size: int):
    font_name = random.choice(server_fonts)
    print(font_name)
    return ImageFont.truetype(f'src/texioty/assets/fonts/{font_name}', size=font_size)

@dataclass
class TexiotyProfile:
    username: str
    password: str
    color_theme: tuple

def _default_available_profiles() -> dict[str, TexiotyProfile]:
    return {
        "guest": TexiotyProfile("Guest", "p455",
                                (rgb_to_hex(t.DARK_BROWN),
                                 rgb_to_hex(t.SAGE_GREEN),
                                 rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW))),
        "bluebeard": TexiotyProfile("Bluebeard", "p455",
                                    (rgb_to_hex(t.DARK_SLATE_BLUE),
                                     rgb_to_hex(t.LIGHT_SLATE_BLUE),
                                     rgb_to_hex(t.GHOST_WHITE)))
    }

def _iter_profile_json_files(profile_group: str) -> list[str]:
    profile_files = []

    for directory in _candidate_profile_dirs(profile_group):
        if not os.path.isdir(directory):
            continue

        profile_files.extend(sorted(glob.glob(os.path.join(directory, "*.json"))))

    seen = set()
    unique_files = []
    for path in profile_files:
        normalized = os.path.normpath(path)
        if normalized not in seen:
            seen.add(normalized)
            unique_files.append(path)

    return unique_files


def _load_available_profiles() -> dict[str, TexiotyProfile]:
    profiles = _default_available_profiles()

    for profile_path in _iter_profile_json_files("user"):
        file_name = os.path.basename(profile_path)

        with open(profile_path, "r") as profile_file:
            profile_data = json.load(profile_file)

        texioty_data = profile_data.get('texioty')
        if not texioty_data:
            continue

        username = texioty_data.get('username')
        profiles[username] = TexiotyProfile(
            username,
            texioty_data.get('password'),
            (texioty_data["color_theme"]["background"],
             texioty_data["color_theme"]["foreground"],
             texioty_data["color_theme"]["accent"])
        )
    return profiles

available_profiles = _load_available_profiles()

def string_to_morse(reg_str: str) -> str:
    morse_str = ''
    print(reg_str)
    for letter in reg_str:
        morse_str += a.MORSE_CODE_AXIOMS[letter.lower()]
    return morse_str


def lsystem_string_maker(axioms: str, rules: dict, iterations: int) -> str:
    for _ in range(iterations):
        new_axioms = ''
        for axiom in axioms:
            if axiom in rules:
                new_axioms += rules[axiom]
            else:
                new_axioms += axiom
            axioms = new_axioms
    return axioms


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

def _load_profile_json(profile_group: str, profile_name: str) -> dict:
    searched_paths = []

    for path in _candidate_profile_paths(profile_group, profile_name):
        searched_paths.append(path)
        if os.path.exists(path):
            with open(path, "r") as profile_file:
                return json.load(profile_file)

    searched_paths_text = "\n".join(searched_paths)
    print(searched_paths_text)
    raise FileNotFoundError(
        f"Profile file not found in any of the following paths:\n{searched_paths_text}"
    )

def retrieve_lab_profiles(lab_to_get: str) -> dict:
    return _load_profile_json('lab', lab_to_get)

def retrieve_tcg_profiles(tcg_to_get: str) -> dict:
    return _load_profile_json("tcg", tcg_to_get)

def retrieve_worx_profiles(equipment: str) -> dict:
    return _load_profile_json("worx", equipment)


def read_json_file(profile_path):
    return None