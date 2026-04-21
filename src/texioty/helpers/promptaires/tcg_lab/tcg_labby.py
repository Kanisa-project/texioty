import glob
import math
from pathlib import Path
from mtgsdk import Card
from PIL import Image, ImageDraw
import random

from helpers.promptaires.tcg_lab.tcg_depicter import TcgDepicter
from src.texioty.helpers.promptaires.prompt_helper import BasePrompt
from src.texioty.helpers.promptaires.tcg_lab.sourceDGM import SourceDGM
from src.texioty.helpers.promptaires.tcg_lab.sourceLRCNA import SourceLRCNA
from src.texioty.settings import themery as t, alphanumers as a, utils as u
from src.texioty.helpers.promptaires.tcg_lab.sourceMTG import SourceMTG
from src.texioty.helpers.promptaires.tcg_lab.sourcePKM import SourcePKM
from src.texioty.helpers.promptaires.tcg_lab.sourceYGO import SourceYGO

from src.texioty.helpers.gaims.wordsearch import create_wordsearch
from src.texioty.helpers.gaims.hangman import generate_hidden_dictionary

TCG_OPTIONS = [
    'Magic the Gathering',
    'Pokemon',
    'Lorcana',
    'Yu-Gi-Oh',
    'Digimon'
]

LAB_PROFILE_ROOT = Path("src/texioty/helpers/promptaires/tcg_lab/lab_presets")
TCG_PROFILE_ROOT = Path("src/texioty/helpers/promptaires/tcg_lab/tcg_profiles")


class TCGLabby(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_tcg: str | None = None
        self.current_lab: str | None = None
        self.current_lab_profile_name: str | None = None
        self.depicter = TcgDepicter()

        self.sources = {
            'magic': SourceMTG(),
            'pokemon': SourcePKM(),
            'yugioh': SourceYGO(),
            'lorcana': SourceLRCNA(),
            'digimon': SourceDGM()
        }

    def get_source_for_tcg(self, tcg_name: str):
        source = self.sources.get(tcg_name)
        if source is None:
            raise ValueError(f"Unsupported TCG: {tcg_name}")
        return source

    def ingest_cards_for_profile(self, tcg_name: str|None, profile_name: str):
        source = self.get_source_for_tcg(self._tcg_tag(tcg_name))
        profile = self.load_tcg_profile(tcg_name, profile_name)
        card_criteria = profile.get("card_criteria", profile)
        print(card_criteria, "card CRIT")
        raw_cards = source.get_card_batch(card_criteria)
        # print(raw_cards, "RAW CARDS")
        if raw_cards is None:
            raw_cards = []

        if not isinstance(raw_cards, list):
            raise TypeError(f"Expected a list of cards, got {type(raw_cards)}")

        output_dir = f"filesOutput/tcg_lab/cards/{source.tcg_title_name}"
        print(output_dir, "OPOUT")
        ingested_count = 0
        for raw_card in raw_cards:
            raw_card = source.card_to_dict(raw_card)
            source.ingest_card(raw_card, tcg_name, output_dir)
            ingested_count += 1
            # self.txo.priont_string(f"Ingested card: {raw_card['name']} - {raw_card['source_id']}")

        self.txo.update_header_status(bottom_status=f"Ingested {ingested_count} cards for {tcg_name}/{profile_name}")

    def download_cards(self, profile_name: str):
        self.current_lab_profile_name = profile_name
        self.txo.priont_string(f"Ingesting {self.current_tcg} {profile_name}....")
        self.ingest_cards_for_profile(self.current_tcg, profile_name)

    def laboratory(self, lab_name: str):
        self.current_lab = lab_name

        match lab_name:
            case 'Depictinator{}':
                self.decide_decision("Which card game to depict from", TCG_OPTIONS, 'depict')
                self.txo.master.deciding_function = self.depictinator
            case 'Card%Puzzler(]':
                self.decide_decision("Which card game to puzzle with", TCG_OPTIONS, 'puzzler')
                self.txo.master.deciding_function = self.card_puzzler
            case 'TC-Blender 690':
                self.decide_decision("Which card games to blend together", TCG_OPTIONS, 'tc_blender')
                self.txo.master.deciding_function = self.tc_blender_690
            case 'Card-0wn1oad3r':
                self.decide_decision("What game to download cards from", TCG_OPTIONS, '0wn1oad3r')
                self.txo.master.deciding_function = self.card_0wn1oad3r
            case 'RanDexter-2110':
                self.decide_decision("Which card game to generate a deck for", TCG_OPTIONS, 'deckster')
                self.txo.master.deciding_function = self.randexter_2110
            case _:
                self.txo.update_header_status(bottom_status="Unknown LAB: " + lab_name)
                self.txo.master.deciding_function = None

    def get_lab_profile_names(self, lab_choice: str) -> list[str]:
        lab_tag = self._lab_tag(lab_choice)
        profile_dir = LAB_PROFILE_ROOT / lab_tag
        if profile_dir.exists():
            profiles = sorted([p.stem for p in profile_dir.glob("*.json")])
            if profiles:
                return profiles

        try:
            profiles = u.retrieve_lab_profiles(lab_tag)
            return sorted(list(profiles.keys()))
        except FileNotFoundError:
            return []

    def get_tcg_profile_names(self, tcg_choice: str) -> list[str]:
        tcg_tag = self._tcg_tag(tcg_choice)
        profile_dir = TCG_PROFILE_ROOT / tcg_tag
        if profile_dir.exists():
            profiles = sorted([p.stem for p in profile_dir.glob("*.json")])
            if profiles:
                return profiles

        try:
            profiles = u.retrieve_tcg_profiles(tcg_tag)
            return sorted(list(profiles.keys()))
        except FileNotFoundError:
            return []

    def load_lab_profile(self, lab_name: str | None, profile_name: str) -> dict:
        if lab_name is None:
            lab_name = self.current_lab
        lab_tag = self._lab_tag(lab_name)
        profile_path = TCG_PROFILE_ROOT / lab_tag / f"{profile_name}.json"
        if profile_path.exists():
            return u.read_json_file(profile_path)

        try:
            profiles = u.retrieve_lab_profiles(lab_tag)
        except FileNotFoundError:
            raise FileNotFoundError(f"No profile found: {lab_name}/{profile_name}")

        if profile_name in profiles:
            return profiles[profile_name]

        raise FileNotFoundError(f"No profile found: {lab_name}/{profile_name}")

    def load_tcg_profile(self, tcg_name: str|None, profile_name: str) -> dict:
        tcg_tag = self._tcg_tag(tcg_name)
        profile_path = TCG_PROFILE_ROOT / tcg_tag / f"{profile_name}.json"
        if profile_path.exists():
            return u.read_json_file(profile_path)

        try:
            profiles = u.retrieve_tcg_profiles(tcg_tag)
        except FileNotFoundError:
            raise FileNotFoundError(f"No profile found: {tcg_name}/{profile_name}")

        if profile_name in profiles:
            return profiles[profile_name]

        raise FileNotFoundError(f"No profile found: {tcg_name}/{profile_name}")

    def depictinator(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        profiles = self.get_lab_profile_names(self._lab_tag(self.current_lab))
        self.decide_decision(f"Which depiction profile to use", profiles, tcg_choice.lower())
        self.txo.master.deciding_function = self.setup_depiction

    def card_puzzler(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        profiles = self.get_tcg_profile_names(tcg_choice)
        self.decide_decision(f"Which puzzle profile to use", profiles, tcg_choice.lower())
        self.txo.master.deciding_function = self.create_puzzles

    def tc_blender_690(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        profiles = self.get_tcg_profile_names(tcg_choice)
        self.decide_decision("Which blend profile to use", profiles, tcg_choice.lower())
        self.txo.master.deciding_function = self.blend_cards

    def card_0wn1oad3r(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        profiles = self.get_tcg_profile_names(tcg_choice)

        if not profiles:
            self.txo.update_header_status(bottom_status=f"No profiles found for {self.sources[tcg_choice].tcg_title_name}")
            return
        self.decide_decision("Which download profile to use", profiles, tcg_choice.lower())
        self.txo.master.deciding_function = self.download_cards

    def randexter_2110(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        profiles = self.get_tcg_profile_names(tcg_choice)
        self.decide_decision("Which deck profile to use", profiles, tcg_choice.lower())
        self.txo.master.deciding_function = self.generate_decks

    def setup_depiction(self, profile_name: str):
        self.current_lab_profile_name = profile_name
        self.txo.priont_string(f"Depicting a {self.current_tcg} {profile_name}....")

        source = self.get_source_for_tcg(self._tcg_tag(self.current_tcg))
        # profile = self.load_lab_profile(self.current_lab, profile_name)
        # source.chosen_lab_profile_dict = profile

        cards = source.get_card_database()

        if not cards:
            self.txo.update_header_status(bottom_status=f"No cards found for {self.current_tcg}/{profile_name}")
            return

        # chosen_card = random.choice(cards)
        card_options = [f"{card.get('name', 'Unknown')} - {card.get('source_id', 'Unknown')}" for card in cards]
        self.decide_decision("Which card to use", card_options)
        self._set_deciding_function(self.depict_depiction)

    def depict_depiction(self, card_source_id: str):
        source = self.get_source_for_tcg(self._tcg_tag(self.current_tcg))
        self.depicter.card_datadict = source.get_card_database(filters={"source_id": card_source_id})[0]
        self.depicter.depiction_preset = self.load_lab_profile(self.current_lab, self.current_lab_profile_name)
        self.depicter.depiction_type = self.current_lab_profile_name
        self.depicter.color_translation_dict = source.color_translation_dict
        self.depicter.depict_card(card_source_id)

    def create_puzzles(self, profile_name: str):
        self.current_lab_profile_name = profile_name
        self.txo.priont_string(f"Creating a {self.current_tcg} {profile_name}....")

        source = self.get_source_for_tcg(self.current_tcg)
        profile = self.load_tcg_profile(self.current_tcg, profile_name)
        cards = source.get_card_database(filters=profile.get("card_criteria", profile))

        if not cards:
            self.txo.update_header_status(bottom_status=f"No cards found for {self.current_tcg}/{profile_name}")
            return

        puzzle_profile = profile.get("puzzle", profile)
        if "wordsearch" in profile_name:
            self.generate_wordsearch(puzzle_profile)
        elif "hangman" in profile_name:
            self.generate_hangman(puzzle_profile)
        else:
            self.txo.update_header_status(bottom_status=f"No puzzle profile found for {self.current_tcg}/{profile_name}")

    def blend_cards(self):
        self.txo.update_header_status(bottom_status=f"Blending cards isn't working yet.")

    def generate_decks(self, profile_name: str):
        self.current_lab_profile_name = profile_name
        self.txo.priont_string(f"Building decks for {self.current_tcg} {profile_name}....")

        source = self.get_source_for_tcg(self.current_tcg)
        deck_profile = self.load_tcg_profile(self.current_tcg, profile_name)
        deck_config = deck_profile.get("deck", deck_profile)

        cards = source.get_card_database(filters=deck_profile.get("card_criteria", deck_profile))
        if not cards:
            self.txo.update_header_status(bottom_status=f"No cards found for {self.current_tcg}/{profile_name}")
            return

        deck_size = int(deck_config.get("deck_size", 60))
        selected_cards = random.sample(cards, min(deck_size, len(cards)))
        self.txo.priont_list(
            [f"{card.get('name', 'Unknown')} - {card.get('type', 'Unknown')}" for card in selected_cards],
            numbered=True
        )


    def generate_wordsearch(self, card_profile: dict):
        self.txo.priont_dict(card_profile)
        for row in create_wordsearch(["one", "thee", "kanisa"], 13):
            self.txo.priont_string(' '.join(row))

    def generate_hangman(self, card_profile: dict):
        self.txo.priont_dict(card_profile.get("hangman", {"difficulty": 2, "phrase": "hangman"}))
        self.txo.priont_dict(generate_hidden_dictionary("This is a phrase."))

    # def create_depiction(self, card_source_id: str):
    #     source = self.get_source_for_tcg(self._tcg_tag(self.current_tcg))
    #     print(source.chosen_lab_profile_dict, "LABDICT")
    #     source.chosen_card_dict = source.get_card_database(filters={"source_id": card_source_id})[0]
    #     print(source.chosen_card_dict, "CARDDICT")
    #     img_size = tuple(source.chosen_lab_profile_dict.get("image_size", (320, 320)))
    #     bg_color = tuple(source.chosen_lab_profile_dict.get("background", (125, 52, 210, 255)))
    #     new_img = Image.new("RGBA", img_size, bg_color)
    #     self.depict_card(new_img, source.chosen_card_dict)
    #     card_name = source.chosen_card_dict.get('name', 'unknown_card')
    #     save_name = "_".join(str(card_name).split())
    #     save_path = Path(f"filesOutput/tcg_lab/depictions/{self.current_lab_profile_name}") / f"{save_name}.png"
    #     save_path.parent.mkdir(parents=True, exist_ok=True)
    #     new_img.save(save_path)
    #     self.txo.priont_string(f"Depiction saved to {save_path}")

    @staticmethod
    def depict_card(img: Image.Image, card_info_dict: dict):
        draw = ImageDraw.Draw(img)

        name = str(card_info_dict.get('name', 'unknown_name'))
        card_type = str(card_info_dict.get('type', 'unknown_type'))
        rarity = str(card_info_dict.get('rarity', 'unknown_rarity'))
        source_tcg = str(card_info_dict.get('source_tcg', 'unknown_source_tcg'))

        draw.rectangle([(8, 8), (img.size[0] - 8, img.size[1] - 8)], fill=(255, 255, 255, 255), width=2)
        draw.text((16, 16), source_tcg, fill=(5, 55, 125, 255))
        draw.text((16, 48), name, fill=(5, 55, 125, 255))
        draw.text((16, 80), card_type, fill=(5, 55, 125, 255))
        draw.text((16, 112), rarity, fill=(5, 55, 125, 255))

    @staticmethod
    def _lab_tag(lab_choice: str | None) -> str:
        mapping = {
            'Card-0wn1oad3r': "downloaders",
            'Depictinator{}': "depicters",
            'Card%Puzzler(]': "puzzlers",
            'TC-Blender 690': "blenders",
            'RanDexter-2110': "decksters"
        }
        if lab_choice is None:
            return str(lab_choice)
        return mapping.get(lab_choice, lab_choice.lower())

    @staticmethod
    def _tcg_tag(tcg_choice: str | None) -> str:
        mapping = {
            "Magic the Gathering": "magic",
            "Pokemon": "pokemon",
            "Lorcana": "lorcana",
            "Yu-Gi-Oh": "yugioh",
            "Digimon": "digimon"
        }
        if tcg_choice is None:
            return str(tcg_choice)
        return mapping.get(tcg_choice, tcg_choice.lower())


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def polypointlist(sides: int, offset: float, cx: int, cy: int, radius: int) -> list:
    step = 2 * math.pi / sides
    print("OSep", step)
    offset = math.radians(offset)
    print(offset, "OFFS")
    pointlist = [(radius * math.cos(step * n + offset) + cx, radius * math.sin(step * n + offset) + cy) for n in
                 range(0, int(sides) + 1)]
    return pointlist


# def lsystem_string_maker(axioms: str, rules: dict, iterations: int) -> str:
#     for _ in range(iterations):
#         new_axioms = ''
#         for axiom in axioms:
#             if axiom in rules:
#                 new_axioms += rules[axiom]
#             else:
#                 new_axioms += axiom
#             axioms = new_axioms
#     return axioms


def blend_cards(img1, img2, param) -> Image.Image:
    return img1


def tc_blender(tcg1: str, tcg2: str) -> Image.Image:
    """Blend a TCG card from two different card games."""
    print(tcg1, tcg2)
    src1_img_list = glob.glob(f'config/cards{tcg1.split(" ")[0]}/*.*')
    src2_img_list = glob.glob(f'config/cards{tcg2.split(" ")[0]}/*.*')
    img1 = Image.open(random.choice(src1_img_list))
    img2 = Image.open(random.choice(src2_img_list))
    if img1.mode == "P":
        img1 = img1.convert("RGBA")
    img2 = img2.convert(img1.mode).resize(img1.size)
    blended = blend_cards(img1, img2, 0.5)
    return blended



def lsystem_dual_mana_decoder(lstring: str, start_point=(480, 480), start_length=32,
                              start_width=1, start_color=(22, 143, 212)):
    angle = 0
    length = start_length
    w, h = (960, 960)
    width = start_width
    color = start_color
    prev_line_tuple = ((start_point[0], start_point[1], start_point[0], start_point[1]), width, color)
    line_points_list = [prev_line_tuple]

    for c in lstring:
        if a.MORSE_CODE_RULES[c.lower()].startswith("ANGLE"):
            angle += int(a.MORSE_CODE_RULES[c.lower()].split("ANGLE")[1])
            angle = clamp(angle, -360, 360)
        if a.MORSE_CODE_RULES[c.lower()].startswith("LINE"):
            length = int(a.MORSE_CODE_RULES[c.lower()].split("LINE")[1])
        line_tuple = u.plan_angled_line(prev_line_tuple[0][2], prev_line_tuple[0][3],
                                      angle, length, width,
                                      color, (w, h))
        line_points_list.append(line_tuple)
        prev_line_tuple = line_tuple
    # color = random.choice(t.RANDOM_COLORS)
    return line_points_list

def depict_card(img: Image.Image, card_info_dict: dict):
    # for criteria in ['name', 'type', 'rarity', 'color', 'artist']:
    print(card_info_dict)
    card_name = card_info_dict.get('name', "N0ne")
    card_rarity = card_info_dict.get('rarity', "Rar3")
    card_artist = card_info_dict.get('artist', "Ar7")
    card_set = card_info_dict.get('set', "5et")
    card_type = card_info_dict.get('type', 'C4rd')
    name_points = depict_name(card_name)
    rarity_points = depict_name(card_rarity)
    artist_points = depict_name(card_artist)
    set_points = depict_name(card_set)
    type_points = depict_type(card_type)
    polypoint_dict = {"name_points": name_points,
                      "rarity_points": rarity_points,
                      "artist_points": artist_points,
                      "set_points": set_points,
                      "type_points": type_points}
    draw_depiction(img, polypoint_dict, card_info_dict)

def build_mana_color_dict(spell_mana_cost: str) -> dict:
    mana_colors = {
        "light_colors": [],
        "dark_colors": [],
        "strong_colors": []
    }
    print(spell_mana_cost)
    if spell_mana_cost is None:
        spell_mana_cost = "L"
    for color in spell_mana_cost:
        if color == "U":
            mana_colors["light_colors"].append((179, 206, 234))
            mana_colors["dark_colors"].append((14, 104, 171))
            mana_colors["strong_colors"].append((0, 0, 255))
        elif color == "R":
            mana_colors["light_colors"].append((235, 159, 130))
            mana_colors["dark_colors"].append((211, 32, 42))
            mana_colors["strong_colors"].append((255, 0, 0))
        elif color == "G":
            mana_colors["light_colors"].append((196, 211, 202))
            mana_colors["dark_colors"].append((0, 115, 62))
            mana_colors["strong_colors"].append((0, 255, 0))
        elif color == "B":
            mana_colors["light_colors"].append((166, 159, 157))
            mana_colors["dark_colors"].append((21, 11, 0))
            mana_colors["strong_colors"].append((0, 0, 0))
        elif color == "W":
            mana_colors["light_colors"].append((248, 231, 185))
            mana_colors["dark_colors"].append((249, 250, 244))
            mana_colors["strong_colors"].append((255, 255, 255))
        elif color == "L":
            mana_colors["light_colors"].append((77, 77, 77))
            mana_colors["dark_colors"].append((62, 62, 62))
            mana_colors["strong_colors"].append((62, 62, 62))

        elif color not in ['/', '{', '}', 'X'] and int(color) in range(0, 25):
            if int(color) == 0 or color == "X":
                mana_colors["light_colors"].append((0, 0, 0))
                mana_colors["dark_colors"].append((25, 171, 212))
                mana_colors["strong_colors"].append((12, 86, 106))
            for i in range(int(color)):
                mana_colors['light_colors'].append((147, 147, 147))
                mana_colors['dark_colors'].append((213, 213, 213))
                mana_colors['strong_colors'].append((180, 180, 180))
    return mana_colors


def draw_depiction(img: Image.Image, spell_polypoints: dict, spell_info_dict: dict):
    draw = ImageDraw.Draw(img)
    a = 5
    print(spell_polypoints)
    print(spell_info_dict)
    mana_colors = build_mana_color_dict(spell_info_dict['spell_mana_cost'])
    light_colors = mana_colors['light_colors']
    dark_colors = mana_colors['dark_colors']
    strong_colors = mana_colors['strong_colors']
    print("manaColors", mana_colors)
    for n_point in spell_polypoints["name_points"]:
        for nn_point in polypointlist(len(spell_info_dict['spell_name']),
                                      0, n_point[0], n_point[1], 241):
            draw.line((n_point, nn_point), fill=random.choice(light_colors))
            draw.line([(n_point[0] - a, n_point[1] - a),
                       (n_point[0] + a, n_point[1] + a)], fill=random.choice(light_colors))
            draw.ellipse([(nn_point[0] - a, nn_point[1] - a),
                          (nn_point[0] + a, nn_point[1] + a)], fill=random.choice(strong_colors))

    for t_point in spell_polypoints['type_points']:
        for tn_point in polypointlist(spell_info_dict['spell_cmc'] + 3, 0,
                                      t_point[0], t_point[1], 69):
            draw.line((tn_point, t_point), fill=random.choice(dark_colors), width=int(spell_info_dict['spell_cmc']) + 2)
        #draw.ellipse([(t_point[0]-7, t_point[1]-3),
        #			  (t_point[0]+7, t_point[1]+3)], fill=random.choice(mana_colors))
        #draw.ellipse([(tn_point[0]-7, tn_point[1]-3),
        #			  (tn_point[0]+7, tn_point[1]+3)], fill=random.choice(mana_colors))

    for c_point in spell_polypoints['cmc_points']:
        for ct_point in polypointlist(len(spell_info_dict['spell_type']), 30, c_point[0], c_point[1], 99):
            draw.line((c_point, ct_point), fill=random.choice(dark_colors), width=int(spell_info_dict['spell_cmc']) + 2)
            draw.line((ct_point[1], ct_point[1]), fill=random.choice(light_colors),
                      width=int(spell_info_dict['spell_cmc']) + 2)
        #draw.polygon(spell_polypoints['cmc_points'], fill=mana_colors[1], outline=random.choice(mana_colors))


def depict_name(spell_name: str) -> list:
    name_len = len(spell_name)
    name_polypoints = polypointlist(name_len, 0, 480, 480, name_len * 2)
    #morse_str = lsystem_string_maker(spell_name.lower(), MORSE_CODE_AXIOMS, 1)
    #print(morse_str)
    #name_polypoints = lsystem_morse_coder(morse_str)
    return name_polypoints


def depict_type(spell_type: str) -> list:
    type_pointlist = []
    if "Enchantment" in spell_type:
        type_pointlist = polypointlist(5, 0, 480, 480, 147)
    elif "Sorcery" in spell_type:
        type_pointlist = polypointlist(3, 0, 480, 480, 147)
    elif "Instant" in spell_type:
        type_pointlist = polypointlist(42, 0, 480, 480, 147)
    elif "Artifact" in spell_type:
        type_pointlist = polypointlist(10, 0, 480, 480, 147)
    elif "Creature" in spell_type:
        type_pointlist = polypointlist(6, 0, 480, 480, 147)
    else:
        type_pointlist = polypointlist(4, 0, 480, 480, 147)
    return type_pointlist


# def depict_cmc(spell_cmc: int) -> list:
#     cmc_pointlist = polypointlist(spell_cmc + 3, spell_cmc * 60, 480, 480, spell_cmc * 19)
#     return cmc_pointlist


# def build_card_info_dict(tcg: str, card_info) -> dict:
#     match tcg:
#         case "Magic the Gathering":
#             pass
#         case "Pokemon":
#             pass
#         case "Lorcana":
#             pass
#         case "Digimon":
#             pass
#         case "YuGiOh":
#             pass
#     return {}


# def build_mtg_card_dict(card: Card):
#     return {"card_name": card.name,
#             "card_cmc": card.cmc,
#             "card_type": card.type.replace('\u2014', '-'),
#             "card_colors": card.colors,
#             "card_mana_cost": card.mana_cost[::-1]}


# def build_spell_dict(spell_card):
#     if isinstance(spell_card, Card):
#         return {"spell_name": spell_card.name,
#                 "spell_cmc": spell_card.cmc,
#                 "spell_type": spell_card.type.replace('\u2014', '-'),
#                 "spell_colors": spell_card.colors,
#                 "spell_mana_cost": spell_card.mana_cost[::-1]}
#     elif isinstance(spell_card, list):
#         spell_dict_list = []
#         for spell in spell_card:
#             spell_dict_list.append({"spell_name": spell.name,
#                                     "spell_cmc": spell.cmc,
#                                     "spell_type": spell.type.replace('\u2014', '-'),
#                                     "spell_colors": spell.colors,
#                                     "spell_mana_cost": spell.mana_cost})
#         return spell_dict_list
#     return None

# class TcgDepicter:
#     def __init__(self):
#         self.card_datadict = {}
#
#     def build_card_datadict(self, card_data) -> dict:
#         print("CARD_DATA", card_data)
#         card_datadict = {
#             'name': 'R4nd0m',
#             'type': 'Sorcery',
#             'rarity': 'Common',
#             'id': 'SOAD-420'
#         }
#         self.card_datadict = card_datadict
#         return card_datadict
#
#     def depict_card(self, card_source_id: str):
#         img = Image.new('RGBA',
#                         (640, 640),
#                         (32, 36, 123))
#         name_points = self.pointify_name()
#         type_points = self.pointify_type()
#         id_points = self.pointify_id()
#         rarity_points = self.pointify_rarity()
#         pointlist_dict = {"name_points": name_points,
#                           "type_points": type_points,
#                           "id_points": id_points,
#                           "rarity_points": rarity_points}
#         img = self.draw_depiction(img, pointlist_dict)
#         save_name = f"{card_source_id}"
#         save_path = Path(f"filesOutput/tcg_lab/depictions") / f"{save_name}.png"
#         save_path.parent.mkdir(parents=True, exist_ok=True)
#         img.save(save_path)
#         print(f"Depiction saved to {save_path}")
#
#     def draw_depiction(self, img: Image.Image, card_pointlists: dict) -> Image.Image:
#         draw = ImageDraw.Draw(img)
#         color_list = t.RANDOM_COLORS
#         print(color_list)
#         for n_point in card_pointlists["name_points"]:
#             draw.line([(n_point[0][0], n_point[0][1]),
#                        (n_point[0][2], n_point[0][3])],
#                       fill=tuple(random.choice(color_list)))
#         for t_point in card_pointlists['type_points']:
#             print(t_point, "TPOIN")
#             for tn_point in polypointlist(3, 30,
#                                           t_point[0][0], t_point[0][1], 69):
#                 draw.line((tn_point, (t_point[0][0], t_point[0][1])), fill=random.choice(color_list), width=2)
#         for i_point in card_pointlists["id_points"]:
#             draw.line([(0, i_point[0][1]),
#                        (img.size[0], i_point[0][1])],
#                       fill=tuple(random.choice(color_list)))
#             draw.line([(i_point[0][2], 0),
#                        (i_point[0][2], img.size[1])],
#                       fill=tuple(random.choice(color_list)))
#         for r_point in card_pointlists["rarity_points"]:
#             draw.line([(r_point[0][0], r_point[0][1]),
#                        (r_point[0][2], r_point[0][3])],
#                       fill=tuple(random.choice(color_list)))
#         return img
#
#     def pointify_name(self) -> list:
#         # print("POINTYNAEM", self.card_datadict)
#         name_len = len(self.card_datadict['name'])
#         image_size = (365, 365)
#         planned_name_lines = []
#         for x in range(0, image_size[0], 3):
#             planned_name_lines.append(
#                 u.plan_angled_line(x, 0, 90, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
#             planned_name_lines.append(
#                 u.plan_angled_line(x, image_size[1], 270, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
#         for y in range(0, image_size[1], 3):
#             planned_name_lines.append(
#                 u.plan_angled_line(0, y, 0, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
#             planned_name_lines.append(
#                 u.plan_angled_line(image_size[0], y, 180, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
#         return planned_name_lines
#
#     def pointify_type(self) -> list:
#         card_type = u.string_to_morse(self.card_datadict['type'])
#         type_lstring = lsystem_string_maker(card_type, a.MORSE_CODE_AXIOMS, 2)
#         lsystem_points = u.lsystem_morse_coder(type_lstring)
#         return lsystem_points
#
#     def pointify_rarity(self) -> list:
#         card_rarity = u.string_to_morse(self.card_datadict['rarity'])
#         rarity_lstring = lsystem_string_maker(card_rarity, a.MORSE_CODE_AXIOMS, 2)
#         lsystem_points = u.lsystem_morse_coder(rarity_lstring)
#         return lsystem_points
#
#     def pointify_id(self) -> list:
#         card_id = u.string_to_morse(self.card_datadict['source_id'])
#         id_lstring = lsystem_string_maker(card_id, a.MORSE_CODE_AXIOMS, 2)
#         lsystem_points = u.lsystem_morse_coder(id_lstring)
#         return lsystem_points
#
#     def depict_coloring(self) -> list:
#         card_coloring = u.string_to_morse(self.card_datadict['color'])
#         coloring_lstring = lsystem_string_maker(card_coloring, a.MORSE_CODE_AXIOMS, 2)
#         lsystem_points = u.lsystem_morse_coder(coloring_lstring)
#         return lsystem_points
