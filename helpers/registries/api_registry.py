from helpers.apis.arc_api import ArcApi
from helpers.apis.digimon_api import DigimonAPIHelper
from helpers.apis.lorcana_api import LorcanaAPIHelper
from helpers.apis.mtg_api import MagicAPIHelper
from helpers.apis.poketcg_api import PokeAPIHelper
from helpers.apis.yugioh_api import YugiohAPIHelper
from helpers.registries.base_registry import BaseRegistry
from settings import utils as u, themery as t

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

        self.helper_commands['get_arc'] = {
                'name': 'get_arc',
                'usage': '"get_arc"',
                'call_func': self.get_arc_prompt,
                'lite_desc': 'Prompt for getting ARC raiders info.',
                'full_desc': ['Begins a prompt for acquiring and displaying ARC raiders info.'],
                'possible_args': {' - ': 'No arguments available.'},
                'args_desc': {' - ': ['No arguments available.', None]},
                'examples': ['get_arc'],
                'group_tag': 'HAPI',
                'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
                'back_color': u.rgb_to_hex(t.BLACK)
        }

    def get_arc_prompt(self):
        pass