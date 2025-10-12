import glob
import random
from math import ceil

from settings import utils as u, themery as t, alphanumers as a
from PIL import Image, ImageDraw, ImageFont



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
    print(tile_xnum, tile_ynum)
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
    start_box = (percent_box[0]*w, percent_box[1]*h,
                 percent_box[2]*w, percent_box[3]*h)
    end_size = (start_box[2] + full_press, start_box[3] + full_press)
    pressed = crop_foto(img, start_box)
    pressed = resize_foto(pressed, end_size)
    img.paste(pressed, (random.randint(0, w), random.randint(0, h)))
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
        sdraw.rectangle((0, 0, 13, 13), fill=t.BLACK)
        sdraw.text((0, 0), str(sliced_images.index(simg)))
        if sliced_images.index(simg) == len(sliced_images)-1:
            simg.paste(Image.new("RGB", (simg.size[0], simg.size[1]), color=t.MAGENTA))
        simg.save(f".temp/{sliced_images.index(simg)}.png")
        shuf_img_pos_list.remove(picked_pos)
    return img


def hsb_filter(img: Image.Image, kre8dict: dict) -> Image.Image:
    """
    Applies a hue, saturation, brightness filter to the provided image.

    :param img:
    :param kre8dict:
    :return:
    """
    hsb_im = img.convert('HSV')
    hsb_list = kre8dict["HSB"]
    h, a, b = hsb_im.split()
    h = h.point(lambda p: p + hsb_list[0])
    a = a.point(lambda p: p * (hsb_list[1] // 10))
    b = b.point(lambda p: p * (hsb_list[2] // 10))
    img = Image.merge('HSV', (h, a, b))
    return img


def rgb_filter(img: Image.Image, kre8dict: dict) -> Image.Image:
    """
    Applies a red, green, blue filter to the provided image.

    :param img: Image to be used in masterpiece.
    :param kre8dict: Dictionary with instructions on how to make a masterpiece.
    :return:
    """
    rgb_im = img.convert('RGB')
    rgb_list = kre8dict["RGB"]
    r, g, b = rgb_im.split()
    r = r.point(lambda p: p + rgb_list[0])
    g = g.point(lambda p: p + rgb_list[1])
    b = b.point(lambda p: p + rgb_list[2])
    img = Image.merge('RGB', (r, g, b))
    return img

def text_stamper(img: Image.Image, profile_dict: dict) -> Image.Image:
    draw = ImageDraw.Draw(img)
    font_size = 32
    font1 = ImageFont.truetype(random.choice(glob.glob('config/fonts/*.ttf')), size=32)
    font2 = ImageFont.truetype(random.choice(glob.glob('config/fonts/*.ttf')), size=32)
    font3 = ImageFont.truetype(random.choice(glob.glob('config/fonts/*.ttf')), size=32)
    start_point = (random.randint(font_size, img.size[0]-font_size), random.randint(font_size, img.size[1]-font_size))
    x_thirds = img.size[0]//3
    y_thirds = img.size[1]//3
    stamp_word = "GAMESTOP"
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
    for i, letter in enumerate(stamp_word):
        draw.text((start_point[0]+(i*x_dir*font_size), start_point[1]+(i*y_dir*font_size)), text=letter, font=random.choice([font1, font2, font3]), fill=(0, 0, 0))

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

def color_drainer(img: Image.Image, profile_dict: dict) -> Image.Image:
    pass



def solidify_tiles(img, profile_dict: dict) -> Image.Image:
    solidify_chance = profile_dict["chance"]
    solidify_color = profile_dict["color"]
    shuffled = profile_dict["shuffled"]
    for img_tile in glob.glob(".temp/*.png"):
        r_c = img_tile.removeprefix(".temp/").removesuffix(".png").split("_")
        solid_hit = random.random()
        print(r_c, solid_hit)
        if solid_hit < solidify_chance:
            print(img_tile)
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
    if 'HSB' in prof_keys:
        profile_dict['HSB'] = hsb_adjustment(profile_dict['HSB'])
        img = hsb_filter(img, profile_dict)
    if 'RGB' in prof_keys:
        profile_dict['RGB'] = rgb_adjustment(profile_dict['RGB'])
        img = rgb_filter(img, profile_dict)
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

def rgb_adjustment(rgb_list: list) -> list:
    """
    Normalizes RGB values and clamps between 0 and 255.
    :param rgb_list: Red, Green, Blue values.
    :return:
    """
    r = u.clamp(rgb_list[0], 1, 127)
    g = u.clamp(rgb_list[1], 1, 127)
    b = u.clamp(rgb_list[2], 1, 127)
    r = u.clamp(random.randint(127-r, 127+r), 0, 255)
    g = u.clamp(random.randint(127-g, 127+g), 0, 255)
    b = u.clamp(random.randint(127-b, 127+b), 0, 255)
    return [r, g, b]

def hsb_adjustment(hsb_list: list) -> list:
    """
    Normalizes the HSB values and clamps between 0 and 360 for Hue,
    or between 0 and 100 for Saturation and Brightness.
    :param hsb_list:
    :return:
    """
    h = u.clamp(hsb_list[0], 1, 180)
    v = u.clamp(hsb_list[1], 1, 50)
    b = u.clamp(hsb_list[2], 1, 50)
    h = u.clamp(random.randint(180-h, 180+h), 0, 360)
    v = u.clamp(random.randint(50-v, 50+v), 0, 100)
    b = u.clamp(random.randint(50-b, 50+b), 0, 100)
    return [h, v, b]

def blend_tcg(deep_fried: bool, tcg1='Pokemon', tcg2='Magic') -> Image.Image:
    print(tcg1, tcg2)
    src1_img_list = glob.glob(f'config/cards{tcg1.split(" ")[0]}/*.*')
    src2_img_list = glob.glob(f'config/cards{tcg2.split(" ")[0]}/*.*')
    img1 = Image.open(random.choice(src1_img_list))
    img2 = Image.open(random.choice(src2_img_list))
    if img1.mode == "P":
        img1 = img1.convert("RGBA")
    img2 = img2.convert(img1.mode).resize(img1.size)
    blended = blend_foto(img1, img2, 0.5)
    if deep_fried:
        blended = hsb_filter(blended, {
            "foto": {
                "HSB": [random.randint(0, 360), random.randint(0, 100), random.randint(0, 100)]
            }
        })
        blended = rgb_filter(blended, {
            'foto': {
                "RGB": [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]}})
    return blended