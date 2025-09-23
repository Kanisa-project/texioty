import math
from mtgsdk import Card
from PIL import Image, ImageDraw
import random
import settings as s
import theme as t
import tex_helper


class SpellDepicter(tex_helper.TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.txo = None
        self.texioty_commands = {
            "depict_spell": [self.depict_mtg_spell, "Depicts a spell from MTG.",
                             {}, [], s.rgb_to_hex(t.INDIAN_RED), s.rgb_to_hex(t.BLACK)], }

    def depict_mtg_spell(self, args):
        self.txo.priont_string(f"Depicting the '{args[0].title()}' spell.")
        spell_card = Card.where(name=args[0].title()).all()[0]
        spell_dict = build_spell_dict(spell_card)
        new_spell_img = Image.new("RGBA", (960, 960), (127, 127, 127))
        depict_spell(new_spell_img, spell_dict)
        new_spell_img.save(f"depictions/{spell_card.name}.png")


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def plan_angled_line(x, y, angle, length, width, color, img_size):
    endx = x + length * math.cos(math.radians(angle + 180)) * -1
    endy = y + length * math.sin(math.radians(angle + 180)) * -1
    return (clamp(x, 0, img_size[0]),
            clamp(y, 0, img_size[1]),
            clamp(endx, 0, img_size[0]),
            clamp(endy, 0, img_size[1])), width, color


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


def depict_spell(img: Image, spell_info_dict: dict):
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


def create_depiction(img: Image, spell_dict: dict):
    depicted_spell = depict_spell(new_spell_img, spell_dict)
    card_name = spell_dict['spell_name']
    save_name = "_".join(card_name.split())
    save_path = f"depictions/{save_name.split('_//_')[0]}.png"
    img.save(save_path)

