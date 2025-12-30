from helpers.apis.arc_api import ArcApi
from helpers.apis.digimon_api import DigimonAPIHelper
from helpers.apis.lorcana_api import LorcanaAPIHelper
from helpers.apis.mtg_api import MagicAPIHelper
from helpers.apis.poketcg_api import PokeAPIHelper
from helpers.apis.yugioh_api import YugiohAPIHelper
from helpers.registries.base_registry import BaseRegistry


class ApiRegistry(BaseRegistry):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_catalog = {
            "YGO": YugiohAPIHelper,
            "MTG": MagicAPIHelper,
            "PKM": PokeAPIHelper,
            "DGM": DigimonAPIHelper,
            "LCA": LorcanaAPIHelper,
            "ARC": ArcApi
        }