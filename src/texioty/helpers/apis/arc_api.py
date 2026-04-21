import random

import requests
from typing import Callable
from src.texioty.helpers.apis.api_helper import BaseAPIHelper
from src.texioty.helpers.promptaires.prompt_helper import BasePrompt
from src.texioty.settings import themery as t, utils as u


class ArcApi(BasePrompt, BaseAPIHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.base_url = 'https://ardb.app/api'
        self.headers = {'Accept': 'application/json'}
        self.endpoint_names = {'items': ['/items'],
                               'quests': ['/quests'],
                               'enemies': ['/arc-enemies']}
        self.helper_commands["get_arc"] = {
            "name": "get_arc",
            "usage": '"get_arc"',
            "call_func": self.get_arc_prompt,
            "lite_desc": "Get some data from the arc api.",
            "full_desc": ["Get some data from the arc api.",],
            "possible_args": {},
            "args_desc": {},
            "examples": ['get_arc'],
            "group_tag": "PRUN",
            "font_color": u.rgb_to_hex(t.KHAKI),
            "back_color": u.rgb_to_hex(t.BLACK)}

    def get_arc_prompt(self):
        self.display_title('get_arc')
        self.decide_decision("What are you looking for, raider?", list(self.endpoint_names.keys()), "arc_api")
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.get_random_arc


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

