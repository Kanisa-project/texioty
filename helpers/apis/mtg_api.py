import math

import mtgsdk
import requests

# from config import settings as s
from mtgsdk import Card
from PIL import Image, ImageDraw
import random

# from question_prompts.spell_depicter import TcgDepicter
from helpers.apis.base_tcg_api import TCGAPI
from helpers import dbHelper
# from helpers.promptaires.tcg_labby import TcgDepicter
from settings.alphanumers import MORSE_CODE_RULES
from settings.utils import clamp
from settings import themery as t

COLOR_DICT = {
    "R": {},
    "G": {},
    "U": {},
    "W": {},
    "B": {},
    "P": {},
    "1": {},
    "2": {}
}


def plan_angled_line(x, y, angle, length, width, color, img_size):
    endx1 = x
    endy1 = y
    endx2 = x + length * math.cos(math.radians(angle + 180)) * -1
    endy2 = y + length * math.sin(math.radians(angle + 180)) * -1
    return (clamp(endx1, 0, img_size[0]),
            clamp(endy1, 0, img_size[1]),
            clamp(endx2, 0, img_size[0]),
            clamp(endy2, 0, img_size[1])), width, color


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


def lsystem_morse_coder(lstring: str, start_point=(320, 320), start_length=32,
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
    # color = random.choice(s.RANDOM_COLORS)
    return line_points_list


def download_goblins():
    random_goblins = Card.where(subtypes="goblin").all()
    random_goblins = random.sample(random_goblins, 6)
    for card in random_goblins:
        print(f'{card.name}  {card.image_url}')
        print(f'{card.power}  {card.toughness}')
        print(f'{card.set}')
        if card.image_url is not None:
            img_data = requests.get(f'{card.image_url}').content
            save_name = f"{card.set.upper()}_" + card.name.replace(" ", "_")
            with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsMagic/{save_name}.png',
                      'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}")


# def depict_playmat(spell_name: str) -> (Image, str):
#     nim = Image.new("RGBA", (1920, 1120), (0, 0, 0, 0))
#     spellCard = random.choice(Card.where(name=spell_name).all())
#     save_name = spellCard.name.replace(" ", "_")
#     imaj: Image = depict_spell(nim, build_spell_dict(spellCard))
#     imaj.save(f"tcg_lab\\playmats\\{save_name}.png")
#     return imaj, save_name


def depict_spell(img: Image, spell_info_dict: dict) -> Image:
    spell_name = spell_info_dict['spell_name']
    spell_cmc = spell_info_dict['spell_cmc']
    spell_colors = spell_info_dict['spell_colors']
    spell_type = spell_info_dict['spell_type']
    print("spell_info ", spell_info_dict)
    name_points = depict_name(spell_name, img.size)
    cost_points = depict_cost(spell_cmc, img.size)[1:]
    type_points = depict_type(spell_type, img.size)
    polypoint_dict = {"name_points": name_points,
                      "cost_points": cost_points,
                      "type_points": type_points}
    draw_depiction(img, polypoint_dict, spell_info_dict, spell_colors)
    # img.save(f"tcg_lab\\{spell_name}.png")
    return img


def get_colors_from_mana(mana_letter: str) -> dict:
    mana_symbol_color_dict = {
        'light': (),
        'medium': (),
        'dark': ()
    }
    if len(mana_letter) == 1:
        if mana_letter == "R":
            red_base = average_the_colors(Image.open('../config/src_imgs/mountain_box.png'), 'red')
            mana_symbol_color_dict['light'] = (179, 206, 234)
            mana_symbol_color_dict['medium'] = red_base
            mana_symbol_color_dict['dark'] = (14, 104, 171)
        if mana_letter == "U":
            blue_base = average_the_colors(Image.open('../config/src_imgs/island_box.png'), 'blue')
            mana_symbol_color_dict['light'] = (179, 206, 234)
            mana_symbol_color_dict['medium'] = blue_base
            mana_symbol_color_dict['dark'] = (14, 104, 171)
    return mana_symbol_color_dict


def build_mana_color_dict(spell_mana_cost: str) -> dict:
    casting_cost_color_dict = {}
    dark_mana_colors = []
    avg_mana_colors = []
    light_mana_colors = []
    mana_symbols = spell_mana_cost.split('{')
    num_of_slots = len(mana_symbols[1:])
    cost_index = 0
    if spell_mana_cost is None:
        spell_mana_cost = "L"
    for color_symbol in mana_symbols[1:]:
        color_symbol = color_symbol.removesuffix('}')
        color_symbol = color_symbol.split('/')
        alpha_lvl = 255
        if color_symbol == '':
            continue
        for i in range(0, 16):
            if str(i) in color_symbol:
                colorless_lvl = i
                alpha_lvl = (16 - colorless_lvl) * 16
                light_mana_colors.append((137, 137, 137, alpha_lvl))
                avg_mana_colors.append((127, 127, 127, alpha_lvl))
                dark_mana_colors.append((117, 117, 117, alpha_lvl))
            elif "X" in color_symbol:
                colorless_lvl = random.randint(0, 16)
                alpha_lvl = (16 - colorless_lvl) * 16
                light_mana_colors.append((137, 137, 137, alpha_lvl))
                avg_mana_colors.append((127, 127, 127, alpha_lvl))
                dark_mana_colors.append((117, 117, 117, alpha_lvl))
            else:
                # colorless_lvl = 0
                # alpha_lvl = (16 - colorless_lvl) * 16
                pass

        if "U" in color_symbol:
            blue_img = Image.open('../config/src_imgs/island_box.png')
            light_mana_colors.append((179, 206, 234, alpha_lvl))
            avg_mana_colors.append(average_the_colors(blue_img, 'blue') + (alpha_lvl, ))
            dark_mana_colors.append((14, 104, 171, alpha_lvl))
        if "R" in color_symbol:
            red_img = Image.open('../config/src_imgs/mountain_box.png')
            light_mana_colors.append((235, 159, 130, alpha_lvl))
            avg_mana_colors.append(average_the_colors(red_img, 'red') + (alpha_lvl, ))
            dark_mana_colors.append((211, 32, 42, alpha_lvl))
        if "G" in color_symbol:
            green_img = Image.open('../config/src_imgs/forest_box.png')
            light_mana_colors.append((196, 211, 202, alpha_lvl))
            avg_mana_colors.append(average_the_colors(green_img, 'green') + (alpha_lvl, ))
            dark_mana_colors.append((0, 115, 62, alpha_lvl))
        if "B" in color_symbol:
            black_img = Image.open(f'../config/src_imgs/swamp_box.png')
            light_mana_colors.append((166, 159, 157, alpha_lvl))
            avg_mana_colors.append(average_the_colors(black_img, 'black') + (alpha_lvl, ))
            dark_mana_colors.append((21, 11, 0, alpha_lvl))
        if "W" in color_symbol:
            white_img = Image.open('../config/src_imgs/plains_box.png')
            light_mana_colors.append((248, 231, 185, alpha_lvl))
            avg_mana_colors.append(average_the_colors(white_img, 'white') + (alpha_lvl, ))
            dark_mana_colors.append((249, 250, 244, alpha_lvl))
        if "P" in color_symbol:
            phyrex_img = Image.open('../config/src_imgs/test3.png')
            light_mana_colors.append((255, 255, 0, alpha_lvl))
            avg_mana_colors.append(average_the_colors(phyrex_img, 'phyrexian') + (alpha_lvl, ))
            dark_mana_colors.append((0, 255, 255, alpha_lvl))
        if "L" in color_symbol:
            land_img = Image.open('../config/src_imgs/test.png')
            light_mana_colors.append((255, 255, 255))
            avg_mana_colors.append(average_the_colors(land_img, 'colorless') + (alpha_lvl, ))
            dark_mana_colors.append((0, 0, 0))
        mana_symbol_color_dict = {
            'light': light_mana_colors,
            'medium': avg_mana_colors,
            'dark': dark_mana_colors
        }
        casting_cost_color_dict[f'cost_slot_{cost_index}'] = mana_symbol_color_dict
        if cost_index != num_of_slots:
            cost_index += 1
        else:
            continue
        light_mana_colors = []
        avg_mana_colors = []
        dark_mana_colors = []
    # print("Full cost", spell_mana_cost, mana_symbols)
    # for cost in casting_cost_color_dict:
    #     print(f'{cost}- ')
    #     for shade in casting_cost_color_dict[cost]:
    #         print(f'{" "*(len(cost)-2)}{shade}- ')
    #         for color in casting_cost_color_dict[cost][shade]:
    #             print(f'{" " * (len(cost)+len(shade)-4)} {color}')
    return casting_cost_color_dict


def average_the_colors(src_img: Image, color_name: str) -> tuple:
    colors = src_img.getcolors(maxcolors=300000)
    r_avg = 0
    g_avg = 0
    b_avg = 0
    a_avg = 0
    ttl_colos = 1
    match color_name:
        case 'red':
            for colo in colors:
                if colo[1][0] >= colo[1][1] + colo[1][2]:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'green':
            for colo in colors:
                if colo[1][1] >= colo[1][0] + colo[1][2]:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'blue':
            for colo in colors:
                if colo[1][2] >= colo[1][0] + colo[1][1]:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'white':
            for colo in colors:
                if colo[1][0] >= 220 and colo[1][1] >= 220 and colo[1][2] >= 220:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'black':
            for colo in colors:
                if colo[1][0] <= 35 and colo[1][1] <= 35 and colo[1][2] <= 35:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'colorless':
            for colo in colors:
                if 85 <= colo[1][0] <= 170 and 85 <= colo[1][1] <= 170 and 85 <= colo[1][2] <= 170:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
        case 'phyrexian':
            for colo in colors:
                if 85 >= colo[1][0] >= 170 and 85 >= colo[1][1] >= 170 and 85 >= colo[1][2] >= 170:
                    r_avg += colo[1][0]
                    g_avg += colo[1][1]
                    b_avg += colo[1][2]
                    a_avg += colo[1][3]
                    ttl_colos += 1
    return r_avg // ttl_colos, g_avg // ttl_colos, b_avg // ttl_colos


def draw_depiction(img: Image, spell_polypoints: dict, spell_info_dict: dict, spell_colors: list):
    draw = ImageDraw.Draw(img)
    mana_cost_color_dict = build_mana_color_dict(spell_info_dict['spell_mana_cost'])
    # print("avg colors ", avg_mana)

    # Border the whole thing with the name depiction.
    for n_point in spell_polypoints["name_points"]:
        rand_cast_slot = mana_cost_color_dict[f'cost_slot_{random.randint(0, len(mana_cost_color_dict)-1)}']

        draw.line([(n_point[0][0], n_point[0][1]),
                   (n_point[0][2], n_point[0][3])],
                  fill=random.choice(rand_cast_slot[random.choice(['medium', 'dark'])]))

    # Encircle the color identity and mana cost with the type of spell.
    for t_point in spell_polypoints['type_points']:
        rand_cast_slot = mana_cost_color_dict[f'cost_slot_{random.randint(0, len(mana_cost_color_dict)-1)}']
        tn_polypoints = polypointlist(int(spell_info_dict['spell_cmc']), 0, t_point[0], t_point[1], 69)
        for tn_point in tn_polypoints:
            draw.line((tn_point, t_point), fill=random.choice(rand_cast_slot[random.choice(['light', 'medium', 'dark'])]),
                      width=int(spell_info_dict['spell_cmc']))

    # Color spikes representing full casting cost.
    for cost_point in spell_polypoints['cost_points']:
        try:
            cost_slot = mana_cost_color_dict[f'cost_slot_{spell_polypoints["cost_points"].index(cost_point)}']
        except KeyError as e:
            cost_slot = mana_cost_color_dict[f'cost_slot_0']
        for color in cost_slot['medium']:
            # print('cmc_point', f'{color} + {cost_point}')
            draw.line((cost_point, (img.size[0] // 2, img.size[1] // 2)),
                      fill=color,
                      width=int(spell_info_dict['spell_cmc']) + (
                              7 - (clamp(cost_slot['medium'].index(color), 0, len(cost_slot['medium']) - 1) * 4)))
    #
    # # Depict color identity for the big circle in the center.
    if spell_colors is None:
        spell_colors = []
    for colo in spell_colors:
        color = get_id_color(colo)
        # colors = mana_cost_color_dict[f'cost_slot_{s.s.clamp(spell_colors.index(colo), 0, len(mana_cost_color_dict)-1, True)}']
        # print("COLOR", colors)
        size_factor = 65 - (spell_colors.index(colo) * 12)
        draw.ellipse((img.size[0] // 2 - size_factor, img.size[1] // 2 - size_factor,
                      img.size[0] // 2 + size_factor, img.size[1] // 2 + size_factor),
                     fill=color, outline=color)


def get_id_color(color_id: str) -> tuple|None:
    if "R" in color_id:
        return t.CRIMSON
    if "G" in color_id:
        return t.FOREST_GREEN
    if "U" in color_id:
        return t.NAVY_BLUE
    if "W" in color_id:
        return t.GHOST_WHITE
    if "B" in color_id:
        return t.BLACK
    return None


def depict_name(spell_name: str, image_size: tuple) -> list:
    name_len = len(spell_name)
    planned_name_lines = []
    for x in range(0, image_size[0], 3):
        planned_name_lines.append(plan_angled_line(x, 0, 90, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
        planned_name_lines.append(
            plan_angled_line(x, image_size[1], 270, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
    for y in range(0, image_size[1], 3):
        planned_name_lines.append(plan_angled_line(0, y, 0, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
        planned_name_lines.append(
            plan_angled_line(image_size[0], y, 180, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
    return planned_name_lines


def depict_type(spell_type: str, image_size: tuple) -> list:
    if "Enchantment" in spell_type:
        type_pointlist = polypointlist(64, 0, image_size[0] // 2, image_size[1] // 2, 350)
    elif "Sorcery" in spell_type:
        type_pointlist = polypointlist(48, 0, image_size[0] // 2, image_size[1] // 2, 300)
    elif "Instant" in spell_type:
        type_pointlist = polypointlist(32, 0, image_size[0] // 2, image_size[1] // 2, 180)
    elif "Artifact" in spell_type:
        type_pointlist = polypointlist(44, 0, image_size[0] // 2, image_size[1] // 2, 220)
    elif "Creature" in spell_type:
        type_pointlist = polypointlist(54, 0, image_size[0] // 2, image_size[1] // 2, 350)
    else:
        type_pointlist = polypointlist(48, 0, image_size[0] // 2, image_size[1] // 2, 320)
    return type_pointlist


def depict_cost(cmc: int, image_size: tuple) -> list:
    """
    Depict the mana cost of the spell, using the cmc and fmc.
    :param cmc: Converted Mana Cost
    :param image_size: Size of the image being depicted
    :return:
    """
    if cmc == 0:
        cost_pointlist = polypointlist(3, random.randint(0, 360), image_size[0] // 2, image_size[1] // 2, 10)
    else:
        cost_pointlist = polypointlist(cmc, random.randint(0, 360), image_size[0] // 2, image_size[1] // 2, 107)
    return cost_pointlist


def build_spell_dict(spell_card):
    if isinstance(spell_card, Card):
        return {"spell_name": spell_card.name,
                "spell_set": spell_card.set,
                "spell_cmc": spell_card.cmc,
                "spell_layout": spell_card.layout,
                "spell_type": spell_card.type.replace('\u2014', '-'),
                "spell_colors": spell_card.color_identity,
                "spell_mana_cost": spell_card.mana_cost}
    elif isinstance(spell_card, list):
        spell_dict_list = []
        for spell in spell_card:
            spell_dict_list.append({"spell_name": spell.name,
                                    "spell_set": spell.set,
                                    "spell_cmc": spell.cmc,
                                    "spell_layout": spell.layout,
                                    "spell_type": spell.type.replace('\u2014', '-'),
                                    "spell_colors": spell.colors,
                                    "spell_mana_cost": spell.mana_cost})
        return spell_dict_list
    return None


# def create_depiction(img: Image, depicted_dict: dict):
#     depicted_spell = depict_spell(img, depicted_dict)
#     save_name = depicted_dict['spell_name'].replace(" ", "_")
#     if os.path.isdir(f"tcg_lab/{depicted_dict['spell_set'].upper()}/"):
#         save_path = f"tcg_lab/{depicted_dict['spell_set'].upper()}/{save_name}.png"
#     else:
#         os.mkdir(f"tcg_lab/{depicted_dict['spell_set'].upper()}")
#         save_path = f"tcg_lab/{depicted_dict['spell_set'].upper()}/{save_name}.png"
#     depicted_spell.save(save_path)


def run_depicter_from_script(depict_config_dict: dict):
    depicter = MtgDepicter(depict_config_dict)
    rando_card = random.choice(Card.where(name="Ultimatum").all())
    card_datadict = depicter.build_card_datadict(rando_card)
    depicted_card = depicter.depict_card(card_datadict)
    save_name = depicter.card_datadict['name'].replace(' ', '_')
    depicted_card.save(f"depictions/{save_name}.png")
    print(f"Saved {save_name}")


class MagicAPIHelper(TCGAPI):
    def __init__(self):
        super().__init__()
        self.tcg_title_name = 'magic'
        self.creature_races = ['Goblin', 'Elf', 'Human', 'Horror', 'Hydra', 'Bird', 'Spider', 'Troll', 'Beast',
                               'Turtle', 'Cat']
        self.creature_jobs = ['Cleric', 'Wizard', 'Ninja', 'Samurai', 'Warrior', 'Rogue', 'Pirate']
        self.color_translation_dict = {
            'R': 'red',
            'G': 'green',
            'U': 'blue',
            'W': 'white',
            'B': 'black',
            'C': 'dark grey',
            'L': 'light grey',
        }

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        if self.db_helper.execute_query(all_card_insert_query, [new_card.name, new_card.rarity, new_card.type, "Magic the Gathering", new_card.set+'-'+new_card.number]) is None:
            print(f"✕  Could not add {new_card.name}, probably already exists.")
        else:
            print(f"✓  Added {new_card.name} to database.")

    def download_card_batch(self, batch_config: dict):
        # super().download_card_batch(batch_config)
        print(batch_config)
        current_cards = []
        for set_code in batch_config["batch_set_ids"]:
            for card in mtgsdk.Card.where(set=set_code).all():
                for mtg_type in batch_config["batch_types"]:
                    if mtg_type in card.type:
                        for color_id in batch_config["batch_colors"]:
                            if card.color_identity is not None:
                                if color_id in card.color_identity:
                                    current_cards.append(card)
                                    self.add_card_database(card)
        try:
            chosen_cards = random.sample(current_cards, self.batch_size)
        except ValueError as e:
            # print(e)
            chosen_cards = random.sample(current_cards, len(current_cards))

        for card in chosen_cards:
            if card.image_url is not None:
                img_data = requests.get(f'{card.image_url}').content
                save_name = f"{card.set.upper()}_" + card.name.replace(" ", "_")
                with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsMagic/{save_name}.png',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /fotoes/cardsMagic")
            else:
                print(f"✕  Card '{card.name}' has no image to download.")



    def download_card_image(self):
        pass


# class MtgDepicter(TcgDepicter):
#     def __init__(self, depict_settings: dict):
#         super().__init__(depict_settings)
#
#     def build_card_datadict(self, card_data) -> dict:
#         card_datadict = {
#             'name': card_data.name,
#             'type': card_data.type,
#             'rarity': card_data.rarity,
#             'id': f"{card_data.set}-{card_data.number}"
#         }
#         self.card_datadict = card_datadict
#         return card_datadict


def run_puzzler_from_script(param):
    return None