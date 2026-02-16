import random

from PIL import Image, ImageDraw


def pixel_sorter(img: Image.Image, noodleBase="flour") -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    gravity = len(noodleBase) % 4
    for y in range(0, h):
        sorted_rgb_list = []
        for x in range(w):
            sorted_rgb_list.append(rgb_img.getpixel((x, y)))
        sorted_rgb_list.sort(key=lambda c: c[0] + c[1] + c[2], reverse=bool(gravity))
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

def pixel_streaker(img: Image.Image, streak_length=5, thickness=4) -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    number_of_pixels = (thickness+1) * (streak_length+1) * 10
    # streak_len = streak_length
    direction = (1, 0)
    for i in range(number_of_pixels):
        ran_x = random.randint(0, 1) * w//2
        ran_y = random.randint(0, h-1)
        for strk_len in range(w//2):
            x_strk = direction[0]*strk_len
            y_strk = direction[1]*strk_len
            draw.point((ran_x+x_strk, ran_y+y_strk), fill=rgb_img.getpixel((ran_x, ran_y)))
    return img

def pixel_encircler(img: Image.Image, isSpiral=False, noodleBase="flour") -> Image.Image:
    w, h = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    number_of_pixels = (len(noodleBase)+1) * 10
    circle_size = 5 if isSpiral else 22
    for i in range(number_of_pixels):
        ran_x = random.randint(0, w-1)
        ran_y = random.randint(0, h-1)
        r, g, b = rgb_img.getpixel((ran_x, ran_y))
        draw.circle((ran_x, ran_y), 10, fill=(r, g, b), width=circle_size)
    return img
