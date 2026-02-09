import math
from typing import List

import mtgsdk
import requests

from mtgsdk import Card
from PIL import Image, ImageDraw
import random

from helpers import dbHelper
from helpers.dbHelper import DatabaseHelper
from helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from settings.utils import clamp, polypointlist, plan_angled_line
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


MAGIC_TEMPLATES = {
    "all_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "type": []
    },
    "land_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "special_effect": []
    },
    "creature_cards": {
        "number": [],
        "hp": [],
        "abilities": [],
        "lvl": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "stage": [],
        "retreat_cost": [],
        "attacks": []
    },
    "enchantment_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "rarity": []
    },
    "instant_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "rarity": []
    }
}


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


def depict_spell(img: Image.Image, spell_info_dict: dict) -> Image.Image:
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
    return casting_cost_color_dict


def average_the_colors(src_img: Image.Image, color_name: str) -> tuple:
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


def draw_depiction(img: Image.Image, spell_polypoints: dict, spell_info_dict: dict, spell_colors: list):
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


def gather_all_creature_cards(creature_criteria: dict) -> List[Card]:
    set_code = creature_criteria['set_codes']
    colors = creature_criteria['colors']
    creature_cards = mtgsdk.Card.where(set=set_code).where(colors=colors).where(type="Creature").all()
    return creature_cards

def gather_all_resource_cards(resource_criteria: dict) -> List[Card]:
    set_code = resource_criteria['set_codes']
    colors = resource_criteria['colors']
    land_cards = mtgsdk.Card.where(set=set_code).where(color_id=colors).where(type="Land").all()
    return land_cards

def gather_all_temporary_cards(temporary_criteria: dict) -> List[Card]:
    set_code = temporary_criteria['set_codes']
    colors = temporary_criteria['colors']
    sorcery_cards = mtgsdk.Card.where(set=set_code).where(color_identity=colors).where(type="Sorcery").all()
    instant_cards = mtgsdk.Card.where(set=set_code).where(color_identity=colors).where(type="Instant").all()
    return sorcery_cards + instant_cards

def gather_all_permanent_cards(permanent_criteria: dict) -> List[Card]:
    set_code = permanent_criteria['set_codes']
    colors = permanent_criteria['colors']
    artifact_cards = mtgsdk.Card.where(set=set_code).where(color_identity=colors).where(type="Artifact").all()
    enchantment_cards = mtgsdk.Card.where(set=set_code).where(color_identity=colors).where(type="Enchantment").all()
    return artifact_cards + enchantment_cards


class SourceMTG(SourceTCG):
    def __init__(self):
        super().__init__()

        self.tcg_title_name = 'magic'
        self.creature_races = ['Goblin', 'Elf', 'Human', 'Horror', 'Hydra', 'Bird', 'Spider', 'Troll', 'Beast',
                               'Turtle', 'Cat']
        self.creature_jobs = ['Cleric', 'Wizard', 'Ninja', 'Samurai', 'Warrior', 'Rogue', 'Pirate']
        self.enchantment_types = ['Aura', 'Curse', 'Quest']
        # self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/cards/databases/magic_cards.db')
        self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/magic_cards.db')
        self.db_helper.create_tables_from_templates(MAGIC_TEMPLATES)
        self.color_translation_dict = {
            'R': 'red',
            'G': 'green',
            'U': 'blue',
            'W': 'white',
            'B': 'black',
            'C': 'dark grey',
            'L': 'light grey',
        }

    def get_card_batch(self, card_criteria):
        creatures = gather_all_creature_cards(card_criteria)
        resources = gather_all_resource_cards(card_criteria)
        temps = gather_all_temporary_cards(card_criteria)
        perms = gather_all_permanent_cards(card_criteria)
        return creatures + resources + temps + perms

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        if self.db_helper.execute_query(all_card_insert_query, [new_card.name, new_card.rarity, new_card.type, "Magic the Gathering", new_card.set+'-'+new_card.number]) is None:
            print(f"✕  Could not add {new_card.name}, probably already exists.")
        else:
            print(f"✓  Added {new_card.name} to database.")

    def download_card_batch(self, batch):
        for i in range(3):
            card = random.choice(batch)
            img_data = requests.get(f'{card.image_url}').content
            save_name = f"{card.set.upper()}_" + card.name.replace(" ", "_")
            proper_save_name = save_name.replace("_//_", "-")
            with open(f'cards/{proper_save_name}.png', 'wb') as handler:
                handler.write(img_data)

    #
    # def download_card_batch(self, batch_config: dict):
    #     # super().download_card_batch(batch_config)
    #     print(batch_config)
    #     total_cards = []
    #     current_cards = []
    #     for set_code in batch_config["pack_sets"]:
    #         for card_in_set in mtgsdk.Card.where(set=set_code).all():
    #             total_cards.append(card_in_set)
    #
    #     for card in total_cards:
    #         print(card, 'card')
    #         try:
    #             for color_id in card.color_identity:
    #                 if color_id not in batch_config['pack_colors']:
    #                     print(card.color_identity, "-", batch_config['pack_colors'])
    #                     try:
    #                         total_cards.remove(card)
    #                     except ValueError:
    #                         continue
    #         except TypeError:
    #             pass
    #
    #         for card_type in batch_config['card_types']:
    #             if card_type not in card.type:
    #                 print(card.type, "-", card_type)
    #                 try:
    #                     total_cards.remove(card)
    #                 except ValueError:
    #                     continue
    #
    #         for rarity in batch_config['rarities']:
    #             if rarity not in card.rarity:
    #                 print(card.rarity, "-", batch_config['rarities'])
    #                 try:
    #                     total_cards.remove(card)
    #                 except ValueError:
    #                     continue
    #     try:
    #         chosen_cards = random.sample(total_cards, batch_config['pack_size'])
    #     except ValueError as e:
    #         # print(e)
    #         chosen_cards = random.sample(total_cards, len(total_cards))
    #
    #     for card in chosen_cards:
    #         if card.image_url is not None:
    #             self.add_card_local_database(card)
    #             img_data = requests.get(f'{card.image_url}').content
    #             save_name = f"{card.set.upper()}_" + card.name.replace(" ", "_")
    #             proper_save_name = save_name.replace("_//_", "-")
    #             with open(f'cards/{proper_save_name}.png',
    #             # with open(f'helpers/promptaires/tcg_lab/cards/magic/{proper_save_name}.png',
    #                       'wb') as handler:
    #                 handler.write(img_data)
    #             print(f"✓  Downloaded {save_name} into /fotoes/cardsMagic")
    #         else:
    #             print(f"✕  Card '{card.name}' has no image to download.")

    def generate_random_deck(self, deck_config: dict) -> List[Card]:
        num_of_cards = deck_config['deck_size']
        creature_base_number = num_of_cards * (deck_config['creature_portion']/100)
        resource_base_number = num_of_cards * (deck_config['resource_portion']/100)
        permanent_base_number = num_of_cards * (deck_config['permanent_portion']/100)
        temporary_base_number = num_of_cards * (deck_config['temporary_portion']/100)
        creature_base = random.sample(gather_all_creature_cards({'set': "ZEN", "colors": "R"}), int(creature_base_number))
        resource_base = random.sample(gather_all_resource_cards({'set': "ZEN", "colors": "R"}), int(resource_base_number))
        permanent_base = random.sample(gather_all_temporary_cards({'set': "ZEN", "colors": "R"}), int(temporary_base_number))
        temporary_base = random.sample(gather_all_permanent_cards({'set': "ZEN", "colors": "R"}), int(permanent_base_number))
        deck_list = []
        for creature in creature_base:
            deck_list.append(creature.name + f" -{creature.type}")
        deck_list.append("---------")
        for resource in resource_base:
            deck_list.append(resource.name + f" -{resource.type}")
        deck_list.append("---------")
        for permanent in permanent_base:
            deck_list.append(permanent.name + f" -{permanent.type}")
        deck_list.append("---------")
        for temporary in temporary_base:
            deck_list.append(temporary.name + f" -{temporary.type}")
        deck_list.append("---------")
        return deck_list


if __name__ == '__main__':
    mtg = SourceMTG()
    mtg.download_card_batch({'pack_sets': ['ZEN'], 'pack_colors': ['R'], 'card_types': ['Creature'], 'rarities': ['Basic'], 'pack_size': 10})
