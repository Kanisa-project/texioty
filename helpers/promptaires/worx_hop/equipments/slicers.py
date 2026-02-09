from math import ceil

from PIL import Image

from helpers.promptaires.worx_hop.foto_worx import crop_foto


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
