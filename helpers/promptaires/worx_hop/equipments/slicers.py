import glob
import random
from math import ceil

from PIL import Image, ImageDraw

from settings import utils as u, themery as t


def crop_foto(foto: Image.Image, cropping: tuple[int, int, int, int]) -> Image.Image:
    """Crop a foto with the cropping and return it."""
    return foto.crop(cropping)

def tile_slice_number(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Tile the foto and return it."""
    img_w, img_h = img.size
    num_x, num_y = (4, 7)
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


def tile_slice_size(img: Image.Image, thickness=0.123, slice_direction=(1, 0)) -> Image.Image:
    """Tile the foto and return it."""
    img_w, img_h = img.size
    slice_w, slice_h = (int(img_w*thickness),
                        int(img_h*thickness))
    # slice_w, slice_h = profile_dict["size_tuple"]
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

def portion_out(img, slice_amount=9, portion_amount=1.1) -> Image.Image:
    solidify_chance = portion_amount/10
    solidify_color = random.choice(t.RANDOM_COLORS)
    # shuffled = profile_dict["shuffled"]
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
