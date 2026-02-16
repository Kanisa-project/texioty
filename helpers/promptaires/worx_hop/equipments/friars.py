import random

from PIL import Image
from settings import themery as t

def oil_boil(img: Image.Image, grease_temp=377) -> Image.Image:
    """
    Applies a red, green, blue filter to the provided image.

    :param grease_temp:
    :param img:
    :return:
    """
    rgb_im = img.convert('RGB')
    rgb_dict = {
        'red': [0, grease_temp//3],
        'green': [0, grease_temp//3],
        'blue': [0, grease_temp//3]
    }
    r_adjust = random.randint(rgb_dict['red'][0], rgb_dict['red'][1])
    g_adjust = random.randint(rgb_dict['green'][0], rgb_dict['green'][1])
    b_adjust = random.randint(rgb_dict['blue'][0], rgb_dict['blue'][1])
    r, g, b = rgb_im.split()
    r = r.point(lambda p: p + r_adjust)
    g = g.point(lambda p: p + g_adjust)
    b = b.point(lambda p: p + b_adjust)
    img = Image.merge('RGB', (r, g, b))
    return img

def drop_basket(img: Image.Image, basket_depth=3) -> Image.Image:
    rgb_im = img.convert('RGBA')
    pixels = rgb_im.load()
    old_color = t.RANDOM_COLOR
    new_color = t.RANDOM_COLOR2
    basket_depth = random.randint(basket_depth, int(basket_depth*1.5))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b, a = pixels[x, y]
            if (abs(r - old_color[0]) <= basket_depth and
            abs(g - old_color[1]) <= basket_depth and
            abs(b - old_color[2]) <= basket_depth):
                pixels[x, y] = new_color + (a,)
    return rgb_im


def timed_cook(img: Image.Image, cook_timer=2.7) -> Image.Image:
    """
    Applies a hue, saturation, brightness filter to the provided image.

    :param cook_timer:
    :param img: Image to be used in masterpiece.
    :return:
    """
    hsb_im = img.convert('HSV')
    hsb_dict = {
        "hue": [0, int(36*cook_timer)],
        "saturation": [0, int(10*cook_timer)],
        "brightness": [0, int(10*cook_timer)]
    }
    h_adjust = random.randint(hsb_dict['hue'][0], hsb_dict['hue'][1])
    s_adjust = random.randint(hsb_dict['saturation'][0], hsb_dict['saturation'][1])
    b_adjust = random.randint(hsb_dict['brightness'][0], hsb_dict['brightness'][1])
    h, a, b = hsb_im.split()
    h = h.point(lambda p: p + h_adjust)
    a = a.point(lambda p: p * (s_adjust // 10))
    b = b.point(lambda p: p * (b_adjust // 10))
    img = Image.merge('HSV', (h, a, b))
    return img
