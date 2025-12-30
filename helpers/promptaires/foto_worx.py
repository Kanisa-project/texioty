import glob
import random
from math import ceil
from typing import Callable

from helpers.promptaires.prompt_helper import BasePrompt
from settings import utils as u
from PIL import Image, ImageDraw, ImageFont


class FotoWorxHop(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_equipment = None
        self.foto_profile_dict = None
        self.equipt_saved_name = None
        self.equipment_func = None

    def worxhop(self, equipment: str):
        match equipment:
            case 'Flatop_XT 2200':
                self.current_equipment = "flatops"
                self.equipt_saved_name = "flatopped"
                self.decide_decision("What's going on the flat top", list(u.retrieve_worx_profiles("flatops").keys()), equipment.lower())
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.set_foto_profile_dict
            case 'S/p/licer R0T8':
                self.current_equipment = "slicers"
                self.equipt_saved_name = "pliced"
                self.decide_decision("What are we slicing", list(u.retrieve_worx_profiles("slicers").keys()), equipment.lower())
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.set_foto_profile_dict
            case 'Deep-friar 420':
                self.current_equipment = "friars"
                self.equipt_saved_name = "fried"
                self.decide_decision("What kind of deep fry", list(u.retrieve_worx_profiles("friars").keys()), equipment.lower())
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.set_foto_profile_dict
            case 'Pixtruderer V3':
                self.current_equipment = "extruders"
                self.equipt_saved_name = "truded"
                self.decide_decision("What to extrude pixel-wise", list(u.retrieve_worx_profiles("extruders").keys()), equipment.lower())
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.set_foto_profile_dict
            case 'Tix>Prit C.R.1':
                self.current_equipment = "printers"
                self.equipt_saved_name = "ticked"
                self.decide_decision("What to ticket print", list(u.retrieve_worx_profiles("printers").keys()), equipment.lower())
                if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
                    self.txo.master.deciding_function = self.set_foto_profile_dict


    def set_foto_profile_dict(self, profile_name: str) -> None:
        """Set the foto profile dict."""
        self.foto_profile_dict = u.retrieve_worx_profiles(self.current_equipment)[profile_name]
        self.txo.priont_string(f"foto_profile_dict is now..")
        self.txo.priont_dict(self.foto_profile_dict)
        match self.current_equipment:
            case "flatops":
                self.create_foto_iterations(flatop_foto)
            case "slicers":
                self.create_foto_iterations(s_p_licer_foto)
            case "friars":
                self.create_foto_iterations(deepfry_foto)
            case "extruders":
                self.create_foto_iterations(pixtrude_foto)
            case "printers":
                self.create_foto_iterations(ticket_print_foto)

    def create_foto_iterations(self, equipment_func: Callable):
        for i in range(self.foto_profile_dict["iterations"]):
            save_name = self.equipt_saved_name + str(i) + ".png"
            foto = Image.open(f"helpers/promptaires/worxhop_fotoes/base_img.jpeg")
            foto = equipment_func(foto, self.foto_profile_dict)
            foto.save(f"helpers/promptaires/worxhop_fotoes/{save_name}")

def resize_foto(foto: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    """Resize a foto and return it."""
    new_size = (int(new_size[0]), int(new_size[1]))
    return foto.resize(new_size)


def crop_foto(foto: Image.Image, cropping: tuple[int, int, int, int]) -> Image.Image:
    """Crop a foto with the cropping and return it."""
    return foto.crop(cropping)


def blend_foto(foto: Image.Image, foto2: Image.Image, blend_percent: float) -> Image.Image:
    """Blend the two foto_worxhop and return the one."""
    return Image.blend(foto, foto2, blend_percent)

def tile_slice_number(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Tile the foto and return it."""
    img_w, img_h = img.size
    num_x, num_y = profile_dict["num_tuple"]
    tile_xsize = img_w // num_x if num_x > 0 else img_w
    tile_ysize = img_h // num_y if num_y > 0 else img_h
    tile_xnum = num_x if num_x > 0 else ceil(img_w / tile_xsize)
    tile_ynum = num_y if num_y > 0 else ceil(img_h / tile_ysize)
    for r in range(tile_ynum):
        for c in range(tile_xnum):
            left = c * tile_xsize
            top = r * tile_ysize
            if c == tile_xnum - 1:
                right = img_w
            else:
                right = min(left + tile_xsize, img_w)
            if r == tile_ynum - 1:
                bottom = img_h
            else:
                bottom = min(top + tile_ysize, img_h)
            crop_foto(img, (left, top, right, bottom)).save(f".temp/{r}_{c}.png")
    return img


def tile_slice_size(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Tile the foto and return it."""
    img_w, img_h = img.size
    slice_w, slice_h = profile_dict["size_tuple"]
    tile_xnum = ceil(img_w / slice_w)
    tile_ynum = ceil(img_h / slice_h)
    for r in range(tile_ynum):
        for c in range(tile_xnum):
            left = c * slice_w
            top = r * slice_h
            right = min(left + slice_w, img_w)
            bottom = min(top + slice_h, img_h)
            crop_foto(img, (left, top, right, bottom)).save(f".temp/{r}_{c}.png")
    return img

def steaming_lid(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Get a starting box and press it to make it larger."""
    w, h = img.size
    return img

def press_spatula(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Get a starting box and press it to make it larger."""
    w, h = img.size
    percent_box = profile_dict["start_box_percents"]
    strength = profile_dict["strength"]
    jiggle_amount = profile_dict["jiggle_amount"]
    full_press = strength * int(jiggle_amount * strength)
    start_pos = (int(percent_box[0]*w), int(percent_box[1]*h))
    start_box = (int(start_pos[0]), int(start_pos[1]),
                 percent_box[2]*w, percent_box[3]*h)
    end_size = (start_box[2] + full_press, start_box[3] + full_press)
    pressed = crop_foto(img, start_box)
    pressed = resize_foto(pressed, end_size)
    img.paste(pressed, (start_pos[0], start_pos[1] + full_press))
    return img

def slide_spatula(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Slide a box of a given size and direction."""
    w, h = img.size
    percent_box = profile_dict["box_size_percents"]
    direction = profile_dict["direction"]
    droppings = profile_dict["droppings"]
    sliding_box = (percent_box[0]*w, percent_box[1]*h,
                   percent_box[2]*w, percent_box[3]*h)
    sliding_img = crop_foto(img, sliding_box)
    for i in range(droppings):
        if random.randint(0, 100) % 2 == 0:
            direction = (direction[0], direction[1])
        else:
            direction = (direction[1], direction[0])
        img.paste(sliding_img, (direction[0]*(i*3), direction[1]*(i*3)))
    return img


def shuffle_foto(img: Image.Image, kre8dict: dict) -> Image.Image:
    """
    Slice and shuffle the provided image.

    :param img:
    :param kre8dict:
    :return:
    """
    crop_window_list = []
    sliced_images = []
    shuf_img_pos_list = []
    num_of_tiles = "4x4"
    if "Shuffle Size" in kre8dict:
        num_of_tiles = kre8dict["Shuffle Size"]
    w, h = img.size
    x_tiles = int(num_of_tiles.split("x")[0])
    y_tiles = int(num_of_tiles.split("x")[1])
    tile_xsize = w // x_tiles
    tile_ysize = h // y_tiles
    for x in range(0, w, tile_xsize):
        for y in range(0, h, tile_ysize):
            shuf_img_pos_list.append((x + 0, y + 0))
    for r in range(x_tiles):
        for c in range(y_tiles):
            x, y = c * tile_xsize, r * tile_ysize
            w, h = tile_xsize + x, tile_ysize + y
            crop_window_list.append((x, y, w, h))
            sliced_images.append(crop_foto(img, (x, y, w, h)))
    for simg in sliced_images:
        picked_pos = random.choice(shuf_img_pos_list)
        img.paste(simg, picked_pos)
        sdraw = ImageDraw.Draw(simg)
        sdraw.rectangle((0, 0, 13, 13), fill=s.BLACK)
        sdraw.text((0, 0), str(sliced_images.index(simg)))
        if sliced_images.index(simg) == len(sliced_images)-1:
            simg.paste(Image.new("RGB", (simg.size[0], simg.size[1]), color=s.MAGENTA))
        simg.save(f".temp/{sliced_images.index(simg)}.png")
        shuf_img_pos_list.remove(picked_pos)
    return img


def hsb_filter(img: Image.Image, profile_dict: dict) -> Image.Image:
    """
    Applies a hue, saturation, brightness filter to the provided image.

    :param profile_dict:
    :param img:
    :return:
    """
    hsb_im = img.convert('HSV')
    hsb_dict = profile_dict["hsb_ranges"]
    h_adjust = random.randint(hsb_dict['hue'][0], hsb_dict['hue'][1])
    s_adjust = random.randint(hsb_dict['saturation'][0], hsb_dict['saturation'][1])
    b_adjust = random.randint(hsb_dict['brightness'][0], hsb_dict['brightness'][1])
    h, a, b = hsb_im.split()
    h = h.point(lambda p: p + h_adjust)
    a = a.point(lambda p: p * (s_adjust // 10))
    b = b.point(lambda p: p * (b_adjust // 10))
    img = Image.merge('HSV', (h, a, b))
    return img

def pal_filter(img: Image.Image, profile_dict: dict) -> Image.Image:
    pal_range = profile_dict["pal_ranges"]["palette"]
    palet_num = random.randint(pal_range[0], pal_range[1])
    palet_src = Image.open(f"palettes/palette_{palet_num}.png")
    altitude_int = profile_dict["pal_ranges"]["altitude"]
    ligma_factor = random.choice(profile_dict["pal_ranges"]["ligma"])
    print(ligma_factor, palet_num)
    num_of_colors = clamp(altitude_int, 1, 256)
    img = img.quantize(colors=num_of_colors)
    img = img.remap_palette(list(range(256)), palet_src.tobytes())
    return img


def rgb_filter(img: Image.Image, profile_dict: dict) -> Image.Image:
    """
    Applies a red, green, blue filter to the provided image.

    :param profile_dict:
    :param img: Image to be used in masterpiece.
    :return:
    """
    rgb_im = img.convert('RGB')
    rgb_dict = profile_dict["rgb_ranges"]
    r_adjust = random.randint(rgb_dict['red'][0], rgb_dict['red'][1])
    g_adjust = random.randint(rgb_dict['green'][0], rgb_dict['green'][1])
    b_adjust = random.randint(rgb_dict['blue'][0], rgb_dict['blue'][1])
    r, g, b = rgb_im.split()
    r = r.point(lambda p: p + r_adjust)
    g = g.point(lambda p: p + g_adjust)
    b = b.point(lambda p: p + b_adjust)
    img = Image.merge('RGB', (r, g, b))
    return img

def pixel_sorter(img: Image.Image, profile_dict: dict) -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    dark_left = profile_dict['dark_left']
    for y in range(0, h):
        sorted_rgb_list = []
        for x in range(w):
            sorted_rgb_list.append(rgb_img.getpixel((x, y)))
        sorted_rgb_list.sort(key=lambda c: c[0] + c[1] + c[2], reverse=not dark_left)
        for x in range(w):
            draw.point((x, y), fill=sorted_rgb_list[x])
    return img

def box_borderer(img: Image.Image, profile_dict: dict) -> Image.Image:
    w, h = img.size
    edge_depth = profile_dict['edge_depth']
    edge_tup = tuple(map(int, edge_depth.split("x")))
    draw = ImageDraw.Draw(img)
    return img

def pixel_borderer(img: Image.Image, profile_dict: dict) -> Image.Image:
    width, height = img.size
    rgb_img = img.convert('RGB')
    edge_depth = profile_dict['edge_depth']
    edge_tup = tuple(map(int, edge_depth.split("x")))
    draw = ImageDraw.Draw(img)

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = rgb_img.getpixel((x, y))
            if y == edge_tup[1]:
                use_color = (r, g, b)
                for i in range(0, edge_tup[1]):
                    draw.point((x, y-i), fill=use_color)
            elif x == edge_tup[0]:
                use_color = (r, g, b)
                for i in range(0, edge_tup[0]):
                    draw.point((x-i, y), fill=use_color)
            elif y == height - edge_tup[1]:
                use_color = (r, g, b)
                for i in range(0, edge_tup[1]):
                    draw.point((x, y+i), fill=use_color)
            elif x == width - edge_tup[0]:
                use_color = (r, g, b)
                for i in range(0, edge_tup[0]):
                    draw.point((x+i, y), fill=use_color)
    return img

def pixel_streaker(img: Image.Image, profile_dict: dict) -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    number_of_pixels = profile_dict['amount']
    streak_len = profile_dict['length']
    direction = profile_dict['direction']
    for i in range(number_of_pixels):
        ran_x = random.randint(0, w-1)
        ran_y = random.randint(0, h-1)
        for strk_len in range(streak_len):
            x_strk = direction[0]*strk_len
            y_strk = direction[1]*strk_len
            draw.point((ran_x+x_strk, ran_y+y_strk), fill=rgb_img.getpixel((ran_x, ran_y)))
    return img

def pixel_encircler(img: Image.Image, profile_dict: dict) -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    number_of_pixels = profile_dict['amount']
    circle_size = profile_dict['size']
    for i in range(number_of_pixels):
        ran_x = random.randint(0, w-1)
        ran_y = random.randint(0, h-1)
        r, g, b = rgb_img.getpixel((ran_x, ran_y))
        draw.circle((ran_x, ran_y), 10, fill=(r, g, b), width=circle_size)
    return img

def tc_blender(tcg1: str, tcg2: str) -> Image.Image:
    """Blend a TCG card from two different card games."""
    print(tcg1, tcg2)
    src1_img_list = glob.glob(f'config/cards{tcg1.split(" ")[0]}/*.*')
    src2_img_list = glob.glob(f'config/cards{tcg2.split(" ")[0]}/*.*')
    img1 = Image.open(random.choice(src1_img_list))
    img2 = Image.open(random.choice(src2_img_list))
    if img1.mode is "P":
        img1 = img1.convert("RGBA")
    img2 = img2.convert(img1.mode).resize(img1.size)
    blended = blend_foto(img1, img2, 0.5)
    return blended

def solidify_tiles(img, profile_dict: dict) -> Image.Image:
    solidify_chance = profile_dict["chance"]
    solidify_color = profile_dict["color"]
    shuffled = profile_dict["shuffled"]
    for img_tile in glob.glob(".temp/*.png"):
        r_c = img_tile.removeprefix(".temp/").removesuffix(".png").split("_")
        solid_hit = random.random()
        if solid_hit < solidify_chance:
            solid_tile = Image.open(img_tile)
            w, h = solid_tile.size
            tile_draw = ImageDraw.Draw(solid_tile)
            tile_draw.rectangle((0, 0, w, h), fill=u.rgb_to_hex(solidify_color))
            solid_tile.save(img_tile)
        else:
            solid_tile = Image.open(img_tile)
            w, h = solid_tile.size
        try:
            img.paste(solid_tile, (int(r_c[1])*w, int(r_c[0])*h))
        except ValueError as e:
            print(e)
    return img

def flatop_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    prof_keys = list(profile_dict.keys())
    if "spatula_press" in prof_keys:
        img = press_spatula(img, profile_dict["spatula_press"])
    if "spatula_slide" in prof_keys:
        img = slide_spatula(img, profile_dict["spatula_slide"])
    if "steam_lid" in prof_keys:
        img = steaming_lid(img, profile_dict["steam_lid"])
    if "bordered" in prof_keys:
        img = box_borderer(img, profile_dict["bordered"])
    return img

def get_random_font(font_size: int):
    return ImageFont.truetype(random.choice(glob.glob('config/fonts/*.ttf')), size=font_size)

def phrase_stamper(img: Image.Image, profile_dict: dict) -> Image.Image:
    draw = ImageDraw.Draw(img)
    stamp_phrase = profile_dict['phrase']
    font_size = profile_dict['font_size']
    font_list = []
    for i in range(profile_dict['num_of_fonts']):
        font_list.append(get_random_font(font_size))
    start_point = (random.randint(font_size, img.size[0]-font_size), random.randint(font_size, img.size[1]-font_size))
    x_thirds = img.size[0]//3
    y_thirds = img.size[1]//3
    if start_point[0] < x_thirds:
        x_dir = 1
    elif x_thirds < start_point[0] < 2*x_thirds:
        x_dir = 1
    else:
        x_dir = -1
    if start_point[1] < y_thirds:
        y_dir = 1
    elif y_thirds < start_point[1] < 2*y_thirds:
        y_dir = -1
    else:
        y_dir = -1
    for i, letter in enumerate(stamp_phrase.split()):
        draw.text((start_point[0]+(i*x_dir*font_size), start_point[1]+(i*y_dir*font_size)), text=letter, font=random.choice(font_list), fill=(0, 0, 0))

    return img


def ticket_single_word(img, profile_dict: dict) -> Image.Image:
    add_word = profile_dict['word']
    direction = profile_dict['direction']
    font_size = profile_dict['font_size']
    draw = ImageDraw.Draw(img)
    font_list = []
    for i in range(profile_dict['num_of_fonts']):
        font_list.append(get_random_font(font_size))
    start_point = (random.randint(font_size, img.size[0]-font_size), random.randint(font_size, img.size[1]-font_size))
    x_thirds = img.size[0]//3
    y_thirds = img.size[1]//3
    if start_point[0] < x_thirds:
        x_dir = 1
    elif x_thirds < start_point[0] < 2*x_thirds:
        x_dir = 1
    else:
        x_dir = -1
    if start_point[1] < y_thirds:
        y_dir = 1
    elif y_thirds < start_point[1] < 2*y_thirds:
        y_dir = -1
    else:
        y_dir = -1
    for i, letter in enumerate(add_word):
        draw.text((start_point[0]+(i*x_dir*font_size), start_point[1]+(i*y_dir*font_size)), text=letter, font=random.choice(font_list), fill=(0, 0, 0))

    return img


def ticket_print_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Print some words/emojis/numbers on the img."""
    prof_keys = list(profile_dict.keys())
    if "single_word" in prof_keys:
        img = ticket_single_word(img, profile_dict["single_word"])
    if "short_phrase" in prof_keys:
        img = phrase_stamper(img, profile_dict["short_phrase"])
    return img

def s_p_licer_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    prof_keys = list(profile_dict.keys())
    if "slice_numbers" in prof_keys:
        img = tile_slice_number(img, profile_dict["slice_numbers"])
    if "slice_size" in prof_keys:
        img = tile_slice_size(img, profile_dict["slice_size"])
    if "solid_splice" in prof_keys:
        img = solidify_tiles(img, profile_dict["solid_splice"])
    return img

def deepfry_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """
    Deep fryer meets color shifting/manipulations.
    :param img:
    :param profile_dict:
    :return:
    """
    prof_keys = list(profile_dict.keys())
    if 'hsb_ranges' in prof_keys:
        img = hsb_filter(img, profile_dict)
    if 'rgb_ranges' in prof_keys:
        img = rgb_filter(img, profile_dict)
    if 'pal_ranges' in prof_keys:
        img = pal_filter(img, profile_dict)
    img = img.convert('RGB')
    return img

def pixtrude_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Pasta extruder meets pixel manipulations."""
    prof_keys = list(profile_dict.keys())
    if "sorted" in prof_keys:
        img = pixel_sorter(img, profile_dict['sorted'])
    if "raindrops" in prof_keys:
        img = pixel_streaker(img, profile_dict['raindrops'])
    if "encircled" in prof_keys:
        img = pixel_encircler(img, profile_dict['encircled'])
    if "bordered" in prof_keys:
        img = pixel_borderer(img, profile_dict['bordered'])
    return img