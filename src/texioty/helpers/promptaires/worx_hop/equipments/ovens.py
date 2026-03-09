import glob
import random
from PIL import Image

def preheat_oven(img: Image.Image, oven_temp: int) -> Image.Image:
    return img

def setup_sheet_pan(img: Image.Image, sheet_pan_size: dict) -> Image.Image:

    return img

def insert_sheet_pan(img: Image.Image, oven_time: float) -> Image.Image:
    return img

def remove_sheet_pan(img: Image.Image) -> Image.Image:
    return img

def dutch_up_foto(img: Image.Image, oven_profile: dict) -> Image.Image:
    pan_width = oven_profile['sheet_pan_size']['width']
    pan_length = oven_profile['sheet_pan_size']['length']
    item_spacing = oven_profile['sheet_pan_size']['spacing']
    oven_temp = oven_profile['oven_temp']
    oven_timer = oven_profile['oven_timer']
    prepped_img_paths = glob.glob('helpers/promptaires/worx_hop/fotoes/prepped/*.png')
    random_prepped_paths = random.sample(prepped_img_paths, int(oven_timer))
    for i, path in enumerate(random_prepped_paths):
        for j in range(int(oven_timer)):
            prep_size = (img.width//pan_width//2, img.height//pan_length//2)
            resized_prep = Image.open(path).resize(prep_size)
            prep_placed = pan_width*item_spacing*i*2, pan_length*item_spacing*j*2
            img.paste(resized_prep, prep_placed)
    return img