import random
from pathlib import Path
from settings import themery as t, alphanumers as a, utils as u
from PIL import Image, ImageDraw



class TcgDepicter:
    def __init__(self):
        self.card_datadict = {}
        self.depiction_preset = {}
        self.color_translation_dict = {}
        self.depiction_type = "default"

    def create_color_palette(self, card_colors: str) -> list:
        print(self.color_translation_dict[card_colors], "COLORD_CARds")
        if ', ' in card_colors:
            card_colors = random.choice(card_colors.split(', '))
        match self.color_translation_dict[card_colors]:
            case "red":
                return [
                    t.ARC_RED, t.FIREBRICK, t.INDIAN_RED, t.PALE_VIOLET_RED, t.FREE_SPEECH_RED,
                    t.RANDOM_RED, t.DARK_RED, t.CRIMSON, t.RED, t.DARK_SALMON,
                ]
            case "blue":
                return [
                    t.ARC_BLUE, t.LOOPRING_BLUE, t.SKY_BLUE, t.CADET_BLUE, t.CONTINENTAL_BLUE,
                    t.ROYAL_BLUE, t.BLUE, t.MEDIUM_BLUE, t.DARK_BLUE, t.NAVY_BLUE
                ]
            case "green":
                return [
                    t.ARC_GREEN, t.LIGHT_GREEN, t.DARK_GREEN, t.MEDIUM_SPRING_GREEN, t.PALE_GREEN,
                    t.RANDOM_GREEN, t.DARK_SEA_GREEN, t.GREEN, t.LIME, t.SAGE_GREEN
                ]
            case "yellow":
                return [
                    t.ARC_YELLOW, t.MUSTARD_YELLOW, t.YELLOW, t.LIGHT_GOLDENROD, t.GOLDENROD,
                    t.DARK_GOLDENROD, t.OLIVE, t.YELLOW_GREEN, t.MEDIUM_GOLDENROD, t.ZENYTE_YELLOW
                ]
            case "white":
                return [
                    t.WHITE_SMOKE, t.WHITE, t.GHOST_WHITE, t.SNOW, t.EGGSHELL_WHITE,
                    t.IVORY, t.LINEN, t.QUARTZ, t.FLORAL_WHITE, t.ANTIQUE_WHITE
                ]
            case "black":
                return [
                    t.BLACK, t.SPACE_GREY, t.DARK_GREY, t.SUPER_DARK_GREY, t.X_RAY_GRAY,
                    t.DARK_SLATE_GREY, t.GREY50, t.GREY25, t.FREE_SPEECH_GREY, t.MIDNIGHT_BLUE
                ]
            case "purple":
                return [
                    t.PURPLE, t.FREE_SPEECH_MAGENTA, t.DARK_VIOLET, t.DARK_PURPLE, t.PALE_VIOLET_RED,
                    t.UBE_PURPLE, t.DRS_PURPLE, t.MAGENTA, t.IMMUTABLE_PURPLE, t.MEDIUM_PURPLE
                ]
            case "pink":
                return [
                    t.PINK, t.MISTY_ROSE, t.FLESH, t.LIGHT_CORAL, t.LIGHT_PINK,
                    t.NEON_PINK, t.HOT_PINK, t.SPICY_PINK, t.DEEP_PINK, t.LIGHT_RED
                ]
            case "brown":
                return [
                    t.BROWN, t.SANDY_BROWN, t.DARK_BROWN, t.SEMI_SWEET_CHOCOLATE, t.BURLYWOOD,
                    t.SIENNA, t.ROSY_BROWN, t.SADDLE_BROWN, t.PERU, t.CHOCOLATE
                ]
            case _:
                return t.RANDOM_COLORS

    def build_card_datadict(self, card_data) -> dict:
        print("CARD_DATA", card_data)
        card_datadict = {
            'name': card_data.get('name', 'R4nd0m'),
            'type': card_data.get('type', 'Sorcery'),
            'rarity': card_data.get('rarity', 'Common'),
            'id': card_data.get('id', 'SOAD-420')
        }
        self.card_datadict = card_datadict
        return card_datadict

    def depict_card(self, card_source_id: str):
        print("depict_set", self.depiction_preset)
        img = Image.new('RGBA',
                        self.depiction_preset.get('image_size', (365, 365)),
                        tuple(self.depiction_preset.get('background', (0, 0, 0, 255)))
                    )
        name_points = self.pointify_name()
        type_points = self.pointify_type()
        id_points = self.pointify_id()
        rarity_points = self.pointify_rarity()
        pointlist_dict = {"name_points": name_points,
                          "type_points": type_points,
                          "id_points": id_points,
                          "rarity_points": rarity_points
                        }
        img = self.draw_depiction(img, pointlist_dict)
        self.save_depiction(img, card_source_id)

    def save_depiction(self, img: Image.Image, card_source_id: str):
        save_name = f"{card_source_id}"
        save_path = Path(f"filesOutput/tcg_lab/depictions") / self.depiction_type / f"{save_name}.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path)
        print(f"Depiction saved to {save_path}")

    def draw_depiction(self, img: Image.Image, card_pointlists: dict) -> Image.Image:
        draw = ImageDraw.Draw(img)
        color_list = self.create_color_palette(self.card_datadict['color'])
        # print(card_pointlists['type_points'], "TYPEPOOINT")
        for n_point in card_pointlists["name_points"]:
            draw.line([(n_point[0][0], n_point[0][1]),
                       (n_point[0][2], n_point[0][3])],
                      fill=tuple(random.choice(color_list)))
        for t_point in card_pointlists['type_points']:
            for tn_point in u.polypointlist(len(self.card_datadict['type']), 30,
                                          t_point[0], t_point[1], 69):
                draw.line((tn_point, (t_point[0], t_point[1])), fill=random.choice(color_list), width=2)
        for i_point in card_pointlists["id_points"]:
            draw.line([(0, i_point[0][1]),
                       (img.size[0], i_point[0][1])],
                      fill=tuple(random.choice(color_list)))
            draw.line([(i_point[0][2], 0),
                       (i_point[0][2], img.size[1])],
                      fill=tuple(random.choice(color_list)))
        for r_point in card_pointlists["rarity_points"]:
            draw.line([(0, r_point[0][1]),
                       (r_point[0][1], 0)],
                      fill=tuple(random.choice(color_list)))
            draw.line([(r_point[0][2], 0),
                       (0, r_point[0][2])],
                      fill=tuple(random.choice(color_list)))
        return img

    def pointify_name(self) -> list:
        name_len = len(self.card_datadict['name'])
        image_size = self.depiction_preset.get('image_size', (365, 365))
        planned_name_lines = []
        for x in range(0, image_size[0], 3):
            planned_name_lines.append(
                u.plan_angled_line(x, 0, 90, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
            planned_name_lines.append(
                u.plan_angled_line(x, image_size[1], 270, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
        for y in range(0, image_size[1], 3):
            planned_name_lines.append(
                u.plan_angled_line(0, y, 0, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
            planned_name_lines.append(
                u.plan_angled_line(image_size[0], y, 180, name_len, 1, t.BLUE_2, (image_size[0], image_size[1])))
        return planned_name_lines

    def pointify_type(self) -> list:
        type_name_len = len(self.card_datadict['type'])
        image_size = self.depiction_preset.get('image_size', (365, 365))
        card_type_pointlist = u.polypointlist(type_name_len, 0, image_size[0] // 2, image_size[1] // 2, 69)
        return card_type_pointlist

    def pointify_rarity(self) -> list:
        card_rarity = u.string_to_morse(self.card_datadict['rarity'])
        rarity_lstring = u.lsystem_string_maker(card_rarity, a.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(rarity_lstring)
        return lsystem_points

    def pointify_id(self) -> list:
        card_id = u.string_to_morse(self.card_datadict['source_id'])
        id_lstring = u.lsystem_string_maker(card_id, a.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(id_lstring)
        return lsystem_points

    def depict_coloring(self) -> list:
        card_coloring = u.string_to_morse(self.card_datadict['color'])
        coloring_lstring = u.lsystem_string_maker(card_coloring, a.MORSE_CODE_AXIOMS, 2)
        lsystem_points = u.lsystem_morse_coder(coloring_lstring)
        return lsystem_points
