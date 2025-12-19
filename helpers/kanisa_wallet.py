import os
import random
from typing import Optional

import requests

from helpers.api_helper import BaseAPIHelper
from question_prompts.base_prompt import BasePrompt
from settings import utils as u, themery as t

class KanisaWallet(BasePrompt, BaseAPIHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.base_url = 'https://api.sandbox.immutable.com'
        self.headers = {'Accept': 'application/json',
                        'X-API-Key': os.getenv('IMX_API_KEY')}
        self.endpoint_names = {
            'list_erc20': ['v1', 'chains', 'imtbl-zkevm-testnet', 'tokens']
        }
        self.helper_commands["list_erc20"] = {"name": "list_erc20",
                                              "usage": '"list_erc20 (CHAIN_NAME)"',
                                              "call_func": self.priont_erc20_list,
                                              "lite_desc": "List all ERC20 tokens of a chain.",
                                              "full_desc": ["List all ERC20 tokens of a chain.",],
                                              "possible_args": {' - ': 'No arguments available.'},
                                              "args_desc": {'(CHAIN_NAME)': 'The name of the chain to get the list..'},
                                              'examples': ['list_erc20'],
                                              "group_tag": "KWAL",
                                              "font_color": u.rgb_to_hex(t.IMMUTABLE_PURPLE),
                                              "back_color": u.rgb_to_hex(t.BLACK)}

    def build_endpoint(self, path_list: list):
        self.previous_endpoint = f'{self.base_url}/{path_list[0]}/{path_list[1]}/{path_list[2]}/{path_list[3]}'
        return self.previous_endpoint

    def priont_erc20_list(self, chain_name: Optional[str] = None):
        if chain_name:
            endpoint = self.build_endpoint(['v1', 'chains', chain_name, 'tokens'])
        else:
            endpoint = self.build_endpoint(['v1', 'chains', 'imtbl-zkevm-testnet', 'tokens'])
        response = requests.get(endpoint, headers=self.headers)
        self.txo.priont_dict(response.json())