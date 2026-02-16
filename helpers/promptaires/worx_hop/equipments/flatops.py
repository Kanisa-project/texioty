import random

from PIL import Image

def resize_foto(foto: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    """Resize a foto and return it."""
    new_size = (int(new_size[0]), int(new_size[1]))
    return foto.resize(new_size)


def crop_foto(foto: Image.Image, cropping: tuple[int, int, int, int]) -> Image.Image:
    """Crop a foto with the cropping and return it."""
    return foto.crop(cropping)


def steaming_lid(img: Image.Image, profile_dict: dict) -> Image.Image:
    """ - - """
    w, h = img.size
    return img

def grill_weight(img: Image.Image, weight_corners=(0.2, 0.2, 0.8, 0.8)) -> Image.Image:
    """Get a starting box and press it to make it larger."""
    w, h = img.size
    print(weight_corners, "CORNEREDWEIGHT")
    weight_shape = random.choice(["circle", "rectangle"])
    time_length = random.randint(1, 9)
    full_press = time_length * 3
    start_pos = (int(weight_corners[0]*w), int(weight_corners[1]*h))
    start_box = (int(start_pos[0]), int(start_pos[1]),
                 weight_corners[2]*w, weight_corners[3]*h)
    end_size = (start_box[2] + full_press, start_box[3] + full_press)
    weighted_image = crop_foto(img, start_box)
    pressed = resize_foto(weighted_image, end_size)
    img.paste(pressed, (start_pos[0], start_pos[1] + full_press))
    return img

def slide_spatula(img: Image.Image, slide_direction=(0.43, 0.19)) -> Image.Image:
    """Slide a box of a given size and direction."""
    w, h = img.size
    top_left = slide_direction
    if random.random() < 0.5:
        bottom_right = (1-slide_direction[0], 1-slide_direction[1])
    else:
        bottom_right = (slide_direction[0]+0.5, slide_direction[1]+0.5)
    sliding_box = (top_left[0]*w, top_left[1]*h,
                   bottom_right[1]*(w*2), bottom_right[0]*(h*2))
    sliding_img = crop_foto(img, sliding_box)
    for i in range(8):
        if random.randint(0, 100) % 2 == 0:
            direction = (slide_direction[0], slide_direction[1])
        else:
            direction = (slide_direction[1], slide_direction[0])
        img.paste(sliding_img, (int(direction[0]*(i*3)), int(direction[1]*(i*3))))
    return img

def flip_foto(img: Image.Image) -> Image.Image:
    """Flip the foto horizontally."""
    return img.transpose(Image.FLIP_LEFT_RIGHT)
