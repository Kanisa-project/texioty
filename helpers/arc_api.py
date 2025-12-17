import random

import requests

from helpers.api_helper import BaseAPIHelper
from question_prompts.base_prompt import BasePrompt
from settings import utils as u, themery as t

class ArcApi(BasePrompt, BaseAPIHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.base_url = 'https://ardb.app/api'
        self.headers = {'Accept': 'application/json'}
        self.endpoint_names = {'items': ['/items'],
                               'quests': ['/quests'],
                               'enemies': ['/arc-enemies']}
        self.helper_commands["arc"] = {
            "name": "arc",
            "usage": '"arc [items/quests/enemies] [id]"',
            "call_func": self.find_arc_id,
            "lite_desc": "Find an arc id.",
            "full_desc": ["Get info about items/quests/enemies from the arc api."],
            "possible_args": {'[items/quests/enemies]': "What type of id you want to find.",
                              "[id]": "The id of the object or quest you want to find."},
            "args_desc": {'[items/quests/enemies]': 'The type of arc info to find.'},
            'examples': ['arc items', 'arc quests', 'arc enemies'],
            "group_tag": "PRUN",
            'font_color': u.rgb_to_hex(t.KHAKI),
            'back_color': u.rgb_to_hex(t.BLACK)
        }

    def find_arc_id(self, desired_info: str, desired_id: str):
        self.txo.priont_string(f"Finding {desired_info} with id {desired_id}...")
        endpoint_path = self.endpoint_builder(f'/{desired_info}/', desired_id)
        print(endpoint_path)
        response = requests.get(endpoint_path, headers=self.headers)
        self.txo.priont_dict(response.json())

    def get_random_arc(self, desired_info: str):
        endpoint_path = self.endpoint_builder('', self.endpoint_names[desired_info][0])
        response = requests.get(endpoint_path, headers=self.headers)
        match desired_info:
            case "items":
                rando_item = random.choice(response.json())
                self.txo.priont_string(f"You found {rando_item['name']}!")
            case "quests":
                rando_quest = random.choice(response.json())
                print(rando_quest, type(rando_quest))
                self.txo.priont_dict(rando_quest)
            case "enemies":
                rando_enemy = random.choice(response.json())
                print(rando_enemy, type(rando_enemy))
                self.txo.priont_dict(rando_enemy)

