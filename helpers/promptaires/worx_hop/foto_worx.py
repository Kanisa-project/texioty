import glob
import random
import tkinter
from math import ceil
from typing import Callable

from helpers.promptaires.prompt_helper import BasePrompt
from settings import utils as u, themery as t
from PIL import Image, ImageDraw, ImageFont
from helpers.promptaires.worx_hop.equipments import slicers, printers, friars, extruders, flatops


class FotoWorxHop(BasePrompt):
    """
    The worxhop for fotoes. You can put an image on the flatop, through the slicer, in the deep friar.
    """
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_equipment = None
        self.foto_profile_dict = None
        self.equipt_saved_name = None
        self.equipment_func = None
        self.cook_image = None
        self.order_up_images = []
        self.base_images = []

    def worxhop_stations(self, equipment: str):
        match equipment:
            case 'Flatop_XT 2200':
                self.current_equipment = "flatops"
                self.equipt_saved_name = "flatopped"
            case 'S/p/licer R0T8':
                self.current_equipment = "slicers"
                self.equipt_saved_name = "pliced"
            case 'Deep-friar 420':
                self.current_equipment = "friars"
                self.equipt_saved_name = "fried"
            case 'Pixtruderer V3':
                self.current_equipment = "extruders"
                self.equipt_saved_name = "truded"
            case 'Tix>Prit C.R.1':
                self.current_equipment = "printers"
                self.equipt_saved_name = "ticked"
        self.decide_image_for_cook()

    def decide_image_for_cook(self):
        self.decide_foto_decision("What image to cook with", glob.glob('helpers/promptaires/worx_hop/fotoes/base_img*.jpeg'), "foto_opt")
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.image_to_station


    def image_to_station(self, image_path):
        if image_path not in ['<pg', 'pg>']:
            self.cook_image = Image.open(image_path)
        self.decide_decision("At the station", list(u.retrieve_worx_profiles(self.current_equipment).keys()))
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.set_foto_profile_dict

    def set_foto_profile_dict(self, profile_name: str) -> None:
        """Set the foto profile dict."""
        self.foto_profile_dict = u.retrieve_worx_profiles(self.current_equipment)[profile_name]

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
        self.order_up_images = []
        save_path = f"helpers/promptaires/worx_hop/fotoes/"
        for i in range(5):
            save_name = f"{self.equipt_saved_name}{i}.png"
            serving_name = f"serving_{i}.png"
            foto = equipment_func(self.cook_image, self.foto_profile_dict)
            foto_serving = resize_foto(foto, (128, 128))
            foto.save(save_path + save_name)
            foto_serving.save(save_path + serving_name)
            self.order_up_images.append(tkinter.PhotoImage(file=save_path + serving_name))
            self.txo.image_create(tkinter.END, image=self.order_up_images[i])

def resize_foto(foto: Image.Image, new_size: tuple[int, int]) -> Image.Image:
    """Resize a foto and return it."""
    new_size = (int(new_size[0]), int(new_size[1]))
    return foto.resize(new_size)


def flatop_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    prof_keys = list(profile_dict.keys())
    if "grill_weight" in prof_keys:
        img = flatops.grill_weight(img, profile_dict['grill_weight'])
    if "spatula_slide" in prof_keys:
        img = flatops.slide_spatula(img, profile_dict['spatula_slide'])
    if "steam_lid" in prof_keys:
        img = flatops.steaming_lid(img, profile_dict['steam_lid'])
    return img


def ticket_print_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Print some words/emojis/numbers on the img."""
    return printers.print_on_image(img, profile_dict)

def s_p_licer_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    prof_keys = list(profile_dict.keys())
    if "slice_item" in prof_keys:
        img = slicers.tile_slice_number(img, profile_dict["slice_item"])
    if "thickness" in prof_keys and "slice_direction" in prof_keys:
        img = slicers.tile_slice_size(img, profile_dict["thickness"], profile_dict["slice_direction"])
    if "amount" in prof_keys and "portion_amount" in prof_keys:
        img = slicers.portion_out(img, profile_dict["amount"], profile_dict['portion_amount'])
    return img

def deepfry_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """
    Deep fryer meets color shifting/manipulations.
    :param img:
    :param profile_dict:
    :return:
    """
    prof_keys = list(profile_dict.keys())
    if 'basket_depth' in prof_keys:
        img = friars.drop_basket(img, profile_dict['basket_depth'])
    if 'grease_temp' in prof_keys:
        img = friars.oil_boil(img, profile_dict['grease_temp'])
    if 'cook_timer' in prof_keys:
        img = friars.timed_cook(img, profile_dict['cook_timer'])
    img = img.convert('RGB')
    return img

def pixtrude_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Pasta extruder meets pixel manipulations."""
    prof_keys = list(profile_dict.keys())
    if "noodle_base" in prof_keys:
        img = extruders.pixel_sorter(img, profile_dict['noodle_base'])
    if "length" in prof_keys and "thickness" in prof_keys:
        img = extruders.pixel_streaker(img, profile_dict['length'], profile_dict['thickness'])
    if "is_spiral" in prof_keys and "noodle_base" in prof_keys:
        img = extruders.pixel_encircler(img, profile_dict['is_spiral'], profile_dict['noodle_base'])
    return img