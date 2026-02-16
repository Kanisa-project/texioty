import random

from PIL import ImageDraw, Image

from settings.utils import get_random_font, get_font_server_name, polypointlist, clamp, get_point_delta
from settings import alphanumers as a

def get_server_font(serverName="Kyle", table_number=67):
    possible_fonts = []
    for letter in serverName:
        possible_fonts.append(a.ALPHANUMERIC_FONTS[letter.lower()])
    return get_font_server_name(possible_fonts, table_number)


def print_on_image(img: Image.Image, printing_profile: dict) -> Image.Image:
    draw = ImageDraw.Draw(img)
    img_x, img_y = img.size
    table_items = printing_profile['ticket_items']
    table_size = printing_profile['table_size']
    font_size = printing_profile['table_number']
    font = get_server_font(printing_profile['server_name'], font_size)
    table_points = polypointlist(table_size, 0, img_x//2, img_y//2, 107)
    for i, point in enumerate(table_points):
        text = table_items[clamp(i, 0, len(table_items)-1)]
        delta = get_point_delta(point, (img_x//2, img_y//2))
        for j, letter in enumerate(text):
            point = (point[0]+((delta[0]//img_x)*font_size), point[1]+((delta[1]//img_y)*font_size))
            draw.text(point, text=letter, font=font, fill=(0, 0, 0))
    return img



def server_stamper(img: Image.Image, serverName="Kyle") -> Image.Image:
    draw = ImageDraw.Draw(img)
    # stamp_phrase = profile_dict['phrase']
    font_size = 22
    font_list = []
    for i in range(3):
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
    for i, letter in enumerate(serverName.split()):
        draw.text((start_point[0]+(i*x_dir*font_size), start_point[1]+(i*y_dir*font_size)), text=letter, font=random.choice(font_list), fill=(0, 0, 0))

    return img


def print_ticket_items(img, items_on_ticket=('seat1', 'seattoo')) -> Image.Image:
    # add_word = profile_dict['word']
    # direction = profile_dict['direction']
    font_size = 26
    draw = ImageDraw.Draw(img)
    font_list = []
    for i in range(3):
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
    for word_item in items_on_ticket:
        for i, letter in enumerate(word_item):
            draw.text((start_point[0]+(i*x_dir*font_size), start_point[1]+(i*y_dir*font_size)), text=letter, font=random.choice(font_list), fill=(0, 0, 0))

    return img