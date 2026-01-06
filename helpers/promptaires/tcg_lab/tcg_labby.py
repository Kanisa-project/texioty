import math
from typing import Callable

from mtgsdk import Card
from PIL import Image, ImageDraw
import random

from helpers.promptaires.prompt_helper import BasePrompt
# from src.widgets.basik_widget import BasikWidget
from settings import themery as t, alphanumers as s, utils as u, konfig as k

TCG_OPTIONS = ['Magic the Gathering',
               'Pokemon',
               'Lorcana',
               'Yu-Gi-Oh',
               'Digimon',
               'All']

# class TCGLaboratory(BasikWidget):
#     def __init__(self, txo, txi):
#         super().__init__(txo, txi)
#         self.current_tcg = None


class TCGLabby(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_tcg = None
        self.opts_to_profs_map = {
            'Magic the Gathering': 'magics',
            'Pokemon': 'pokemons',
            'Lorcana': 'lorcanas',
            'Yu-Gi-Oh': 'yugiohs',
            'Digimon': 'digimons'
        }

    def laboratory(self, lab_funcs: str):
        match lab_funcs:
            case 'Depictinator{}':
                self.decide_decision("Which card game to depict with", TCG_OPTIONS, 'depict')
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.depictinator
                    self.txo.priont_string(f"Now depicting {self.txo.master.deciding_function}")
            case 'Card%Puzzler(]':
                self.decide_decision("Which card game to puzzle with", TCG_OPTIONS, 'puzzler')
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.card_puzzler
                    self.txo.priont_string("Now puzzlering ")
            case 'TC-Blender 690':
                pass
            case 'Card-0wn1oad3r':
                self.decide_decision("What game to downloaded cards from", TCG_OPTIONS, '0wn1oad3r')
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.card_downloader
            case 'RanDexter-2110':
                self.decide_decision("Which card game to generate a deck for", TCG_OPTIONS, 'deckster')
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.deck_generator

    def depictinator(self, tcg_choice: str):
        """
        Depicts an abstract artistical image from the tcg_choice.
        :param tcg_choice: TCG_OPTIONS
        """
        self.current_tcg = tcg_choice
        depiction_profiles = u.retrieve_tcg_profiles(self.opts_to_profs_map[tcg_choice])
        # print("depiction_profs", depiction_profiles)
        self.decide_decision(f"Which profile to use for depiction", list(depiction_profiles.keys()), tcg_choice.lower())
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            print("Creating depicting")
            self.txo.master.deciding_function = self.create_depictions

    def card_puzzler(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        puzzler_profiles = u.retrieve_tcg_profiles(self.opts_to_profs_map[tcg_choice])
        self.decide_decision(f"Which profile to make a puzzle with", list(puzzler_profiles.keys()), tcg_choice.lower())
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.create_puzzles

    def card_downloader(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        download_profiles = u.retrieve_lab_profiles('downloaders')
        self.decide_decision("Which downloader profile to use", download_profiles)

    def deck_generator(self, tcg_choice: str):
        self.current_tcg = tcg_choice
        deckster_profiles = u.retrieve_lab_profiles('decksters')
        self.decide_decision("Which deck profile to use", list(deckster_profiles.keys()), tcg_choice.lower())
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.generate_decks

    def create_depictions(self, profile_name: str):
        self.txo.priont_string(f"Depicting a {self.current_tcg} {profile_name}..")
        card_profile_dict = u.retrieve_tcg_profiles(self.opts_to_profs_map[self.current_tcg])[profile_name]
        self.txo.priont_dict(card_profile_dict)
        profile_keys = list(card_profile_dict.keys())[:1]
        print("PROFKEYS", profile_keys)
        for depiction in profile_keys:
            create_depiction(card_profile_dict, card_profile_dict)

    def create_puzzles(self, profile_name: str):
        self.txo.priont_string(f"Puzzling a {self.current_tcg} {profile_name}....")
        match profile_name:
            case "word_search":
                pass
            case "fill_in":
                self.txo.priont_string("┌─┐")
                self.txo.priont_string("│a│")
                self.txo.priont_string("└─┘")

    def generate_decks(self, profile_name: str):
        deck_profile = u.retrieve_lab_profiles('decksters')
        self.txo.priont_dict(deck_profile)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def polypointlist(sides: int, offset: int, cx: int, cy: int, radius: int) -> list:
    step = 2 * math.pi / sides
    offset = math.radians(offset)
    pointlist = [(radius * math.cos(step * n + offset) + cx, radius * math.sin(step * n + offset) + cy) for n in
                 range(0, int(sides) + 1)]
    return pointlist


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
        if MORSE_CODE_RULES[c.lower()].startswith("ANGLE"):
            angle += int(MORSE_CODE_RULES[c.lower()].split("ANGLE")[1])
            angle = clamp(angle, -360, 360)
        if MORSE_CODE_RULES[c.lower()].startswith("LINE"):
            length = int(MORSE_CODE_RULES[c.lower()].split("LINE")[1])
        line_tuple = plan_angled_line(prev_line_tuple[0][2], prev_line_tuple[0][3],
                                      angle, length, width,
                                      color, (w, h))
        line_points_list.append(line_tuple)
        prev_line_tuple = line_tuple
    # color = random.choice(t.RANDOM_COLORS)
    return line_points_list

def depict_card(img: Image.Image, card_info_dict: dict):
    # for criteria in ['name', 'type', 'rarity', 'color', 'artist']:
    print(card_info_dict)
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


def depict_spell(img: Image.Image, spell_info_dict: dict):
    spell_name = spell_info_dict['spell_name']
    spell_cmc = spell_info_dict['spell_cmc']
    spell_type = spell_info_dict['spell_type']
    print(spell_info_dict)
    name_points = depict_name(spell_name)
    cmc_points = depict_cmc(spell_cmc)
    type_points = depict_type(spell_type)
    polypoint_dict = {"name_points": name_points,
                      "cmc_points": cmc_points,
                      "type_points": type_points}
    draw_depiction(img, polypoint_dict, spell_info_dict)


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


def lsystem_depiction(img: Image, spell_llines: dict, spell_info_dict: dict):
    pass


def draw_depiction(img: Image, spell_polypoints: dict, spell_info_dict: dict):
    draw = ImageDraw.Draw(img)
    a = 5
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


def depict_cmc(spell_cmc: int) -> list:
    cmc_pointlist = polypointlist(spell_cmc + 3, spell_cmc * 60, 480, 480, spell_cmc * 19)
    return cmc_pointlist


def build_card_info_dict(tcg: str, card_info) -> dict:
    match tcg:
        case "Magic the Gathering":
            pass
        case "Pokemon":
            pass
        case "Lorcana":
            pass
        case "Digimon":
            pass
        case "YuGiOh":
            pass
    return {}


def build_mtg_card_dict(card: Card):
    return {"card_name": card.name,
            "card_cmc": card.cmc,
            "card_type": card.type.replace('\u2014', '-'),
            "card_colors": card.colors,
            "card_mana_cost": card.mana_cost[::-1]}


def build_spell_dict(spell_card):
    if isinstance(spell_card, Card):
        return {"spell_name": spell_card.name,
                "spell_cmc": spell_card.cmc,
                "spell_type": spell_card.type.replace('\u2014', '-'),
                "spell_colors": spell_card.colors,
                "spell_mana_cost": spell_card.mana_cost[::-1]}
    elif isinstance(spell_card, list):
        spell_dict_list = []
        for spell in spell_card:
            spell_dict_list.append({"spell_name": spell.name,
                                    "spell_cmc": spell.cmc,
                                    "spell_type": spell.type.replace('\u2014', '-'),
                                    "spell_colors": spell.colors,
                                    "spell_mana_cost": spell.mana_cost})
        return spell_dict_list
    return None


def create_depiction(depict_dict: dict, card_dict: dict):
    img_size = depict_dict.get('image_size', (320, 320))
    bg_color = depict_dict.get('background', (125, 52, 210, 99))
    # color_list = depict_dict['palette']
    new_img = Image.new('RGBA', img_size, tuple(bg_color))
    print("CDD: DD", depict_dict)
    print("CDD: CD", card_dict)
    depict_card(new_img, card_dict)
    card_name = card_dict['card_name']
    save_name = "_".join(card_name.split())
    save_path = f"filesOutput/depictions/{save_name.split('_//_')[0]}.png"
    new_img.save(save_path)
    print(f"saved to {save_path}")

# def create_depiction(spell_dict: dict):
#     new_spell_img = Image.new("RGBA", (320, 320), t.KHAKI)
#     depict_spell(new_spell_img, spell_dict)
#     card_name = spell_dict['spell_name']
#     save_name = "_".join(card_name.split())
#     save_path = f"filesOutput/depictions/{save_name.split('_//_')[0]}.png"
#     new_spell_img.save(save_path)
#     print(f"saved to {save_path}")


def playmat_depiction(profile_name: str):
    prof_dict = u.retrieve_lab_profiles('depicters')[profile_name]
    img_size = prof_dict['image_size']
    bg_color = prof_dict['background']
    color_list = prof_dict['palette']
    new_img = Image.new('RGBA', img_size, tuple(bg_color))
    print(prof_dict)
    create_depiction(prof_dict['spell_dict'])


class TcgDepicter:
    def __init__(self, config_dict: dict):
        self.select_choices = ["Name a card.", "Random card.", "Cards batch."]

        self.single_card_queries = {"name": 'What name would you like to find? ',
                                    "type": 'What type of card is it? ',
                                    "coloring": 'What colors are the card? '}

        self.batch_cards_queries = {"set_code": 'What is the setcode for the batch? ',
                                    "batch_size": 'How many cards to batch? ',
                                    "batch_types": 'What type is each card in the batch? '}
        self.card_datadict = {}
        self.config = config_dict

    def build_card_datadict(self, card_data) -> dict:
        """
        Fetch the card_id from the tcg_name's library of cards and creates a datadict to be
        depicted and drawn.
        :param card_data: The card data directly from the API.
        :return:
        """
        print("CARD_DATA", card_data)
        card_datadict = {
            'name': 'R4nd0m',
            'type': 'Sorcery',
            'rarity': 'Common',
            'id': 'SOAD-420'
        }
        self.card_datadict = card_datadict
        return card_datadict

    def depict_card(self, datadict: dict) -> Image.Image:
        print(self.config)
        print(datadict)
        img = Image.new('RGBA', self.config["image_size"], tuple(self.config["background"]))
        name_points = self.depict_name()
        type_points = self.depict_type()
        id_points = self.depict_id()
        rarity_points = self.depict_rarity()
        # self.depict_coloring()
        pointlist_dict = {"name_points": name_points,
                          "type_points": type_points,
                          "id_points": id_points,
                          "rarity_points": rarity_points}
        self.draw_depiction(img, pointlist_dict)
        return img

    def draw_depiction(self, img: Image.Image, card_pointlists: dict):
        draw = ImageDraw.Draw(img)
        color_list = self.config['palette']
        print(color_list)
        for n_point in card_pointlists["name_points"]:
            draw.line([(n_point[0][0], n_point[0][1]),
                       (n_point[0][2], n_point[0][3])],
                      fill=tuple(random.choice(color_list)))
        for i_point in card_pointlists["id_points"]:
            draw.line([(0, i_point[0][1]),
                       (img.size[0], i_point[0][1])],
                      fill=tuple(random.choice(color_list)))
            draw.line([(i_point[0][2], 0),
                       (i_point[0][2], img.size[1])],
                      fill=tuple(random.choice(color_list)))

    def depict_name(self) -> list:
        name_len = len(self.card_datadict['name'])
        image_size = self.config['image_size']
        planned_name_lines = []
        for x in range(0, image_size[0], 3):
            planned_name_lines.append(
                u.plan_angled_line(x, 0, 90, name_len, 1, s.BLUE_2, (image_size[0], image_size[1])))
            planned_name_lines.append(
                u.plan_angled_line(x, image_size[1], 270, name_len, 1, s.BLUE_2, (image_size[0], image_size[1])))
        for y in range(0, image_size[1], 3):
            planned_name_lines.append(
                u.plan_angled_line(0, y, 0, name_len, 1, s.BLUE_2, (image_size[0], image_size[1])))
            planned_name_lines.append(
                u.plan_angled_line(image_size[0], y, 180, name_len, 1, s.BLUE_2, (image_size[0], image_size[1])))
        return planned_name_lines

    def depict_type(self) -> list:
        card_type = u.string_to_morse(self.card_datadict['type'])
        type_lstring = lsystem_string_maker(card_type, s.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(type_lstring)
        return lsystem_points

    def depict_rarity(self) -> list:
        card_rarity = u.string_to_morse(self.card_datadict['rarity'])
        rarity_lstring = lsystem_string_maker(card_rarity, s.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(rarity_lstring)
        return lsystem_points

    def depict_id(self) -> list:
        card_id = u.string_to_morse(self.card_datadict['id'])
        id_lstring = lsystem_string_maker(card_id, s.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(id_lstring)
        return lsystem_points

    def depict_coloring(self) -> list:
        card_coloring = u.string_to_morse(self.card_datadict['coloring'])
        coloring_lstring = lsystem_string_maker(card_coloring, s.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(coloring_lstring)
        return lsystem_points
