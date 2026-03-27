import glob
import os
import tkinter
from pathlib import Path
from typing import Callable

from src.texioty.helpers.promptaires.prompt_helper import BasePrompt
from src.texioty.settings import utils as u
from PIL import Image
from src.texioty.helpers.promptaires.worx_hop.equipments import friars, flatops, extruders, ovens, mixers, slicers, \
    printers


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
            case '[)UtchOven 650':
                self.current_equipment = "ovens"
                self.equipt_saved_name = "backed"
            case 'Mix-n-Stir 816':
                self.current_equipment = "mixers"
                self.equipt_saved_name = "micksed"
        self.decide_image_for_cook()

    def _base_image_dirs(self) -> list[Path]:
        candidate_dirs = [
            Path(u.input_path("foto_worx", "fotoes")),
            Path(u.input_path("foto_worx", "images")),
            Path(u.asset_path("foto_worx", "fotoes")),
            Path(u.asset_path("images", "foto_worx")),
            Path("src/texioty/helpers/promptaires/worx_hop/fotoes"),
        ]

        seen = set()
        unique_dirs = []
        for directory in candidate_dirs:
            normalized = os.path.normpath(str(directory))
            if normalized not in seen:
                seen.add(normalized)
                unique_dirs.append(directory)

        return unique_dirs

    def _base_image_options(self) -> list[str]:
        image_options = []

        for foto_dir in self._base_image_dirs():
            if not foto_dir.exists():
                continue

            for pattern in ("base_img*.jpeg", "base_img*.png", "base_img*.jpg"):
                image_options.extend(sorted(str(path) for path in foto_dir.glob(pattern)))

        seen = set()
        unique_options = []
        for image_path in image_options:
            normalized = os.path.normpath(image_path)
            if normalized not in seen:
                seen.add(normalized)
                unique_options.append(image_path)

        return unique_options

    def decide_image_for_cook(self):
        image_options = self._base_image_options()
        self.decide_foto_decision("What image to cook with", image_options, "foto_opt")
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.image_to_station


    def image_to_station(self, image_path):
        self.cook_image = Image.open(image_path)
        try:
            profiles = u.retrieve_worx_profiles(self.current_equipment)
        except FileNotFoundError as exc:
            self.txo.update_header_status(bottom_status="Profile file not found.")
            print(exc)
            self.txo.master.deciding_function = None
            return
        self.decide_decision("At the station", list(profiles.keys()))
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
            case "ovens":
                self.create_foto_iterations(dutched_foto)
            case "mixers":
                self.create_foto_iterations(stirmix_foto)

    def create_foto_iterations(self, equipment_func: Callable):
        self.order_up_images = []
        for i in range(5):
            save_name = f"{self.equipt_saved_name}{i}.png"
            serving_name = f"serving_{i}.png"

            foto_output_path = u.ensure_parent_dir(
                u.output_path("foto_worx", "exports", self.current_equipment, save_name)
            )
            serving_output_path = u.ensure_parent_dir(
                u.cache_path("foto_worx", self.current_equipment, serving_name)
            )

            foto = equipment_func(self.cook_image, self.foto_profile_dict)
            foto_serving = resize_foto(foto, (128, 128))

            foto.save(foto_output_path)
            foto_serving.save(serving_output_path)

            self.order_up_images.append(tkinter.PhotoImage(file=serving_output_path))
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
    return slicers.slice_up_image(img, profile_dict)

def deepfry_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """
    Deep fryer meets color shifting/manipulations.
    :param img:
    :param profile_dict:
    :return:
    """
    return friars.deep_fry_image(img, profile_dict)

def pixtrude_foto(img: Image.Image, profile_dict: dict) -> Image.Image:
    """Pasta extruder meets pixel manipulations."""
    return extruders.extrude_noodle(img, profile_dict)

def dutched_foto(img: Image.Image, profile_dict) -> Image.Image:
    return ovens.dutch_up_foto(img, profile_dict)

def stirmix_foto(img: Image.Image, profile_dict) -> Image.Image:
    return mixers.mix_it(img, profile_dict)