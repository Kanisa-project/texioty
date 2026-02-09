import os
from typing import List

import requests
import random
from dotenv import load_dotenv
from helpers import dbHelper
from helpers.apis.api_helper import BaseAPIHelper
from helpers.apis.base_tcg_api import TCGAPI

load_dotenv()


class SourceTCG(TCGAPI):
    def __init__(self):
        super().__init__()

    def gather_all_creature_cards(self, creature_criteria: dict) -> List[dict]:
        """
        Gather creature-styled cards to create a card batch. They match an offensive/defensive profile.
        :param creature_criteria: The criteria to match creature cards to.
        """
        pass

    def gather_all_resource_cards(self, resource_criteria: dict) -> List[dict]:
        """
        Gather resource-styled cards to create a card batch. They match an energy provision profile.
        :param resource_criteria: The criteria to match resource cards to.
        """
        pass

    def gather_all_permanent_cards(self, permanent_criteria: dict) -> List[dict]:
        """
        Gather permanent-styled cards to create a card batch. They match a battlefield static profile.
        :param permanent_criteria: The criteria to match permanent cards to.
        """
        pass

    def gather_all_temporary_cards(self, temporary_criteria: dict) -> List[dict]:
        """
        Gather temporary-styled cards to create a card batch. They match a battlefield effect profile.
        :param temporary_criteria: The criteria to match temporary cards to.
        """
        pass

    def endpoint_builder(self, endpoint_name: str, url_ending: str):
        self.previous_endpoint = f'{self.base_url}{endpoint_name}{url_ending}'
        return self.previous_endpoint

    def query_builder(self, query_dict: dict) -> str:
        query_str = ''
        for i, (k, v) in enumerate(query_dict.items()):
            query_str += f'{k}={v}&'
        # print('dict:  ', query_dict)
        return query_str

    # def get_random_psa_cert(self):
    #     rand_cert = random.randint(1, 99999999)
    #     rand_cert = f'{"0"*(8-len(str(rand_cert)))}{rand_cert}'
    #     print(self.endpoint_builder('cert', 'GetByCertNumber/70507261'))
    #     r = requests.get(self.endpoint_builder('cert', f'GetByCertNumber/70507261'), headers=self.headers)
    #     return r.json()

    # def download_card_batch(self, batch_config: dict):
    #     """
    #     Get batch information and then download accordingly.
    #     :param batch_config:
    #     :return:
    #     """
    #     self.batch_set_id = random.choice(batch_config['batch_set_ids'])
    #     self.batch_type = random.choice(batch_config['batch_types'])
    #     self.batch_size = batch_config['batch_size']
    #     self.batch_colors = ','.join(batch_config['batch_colors'])
    #     # display_title(self.tcg_title_name, False)
    #     print(f"Attempting to download {self.batch_size} {self.batch_type} cards..")
    #     print(f"Of {self.batch_colors} coloring from {self.batch_set_id} sets...")

    # def generate_random_deck(self, deck_config: dict):
    #     # number_of_cards = deck_config['number_of_cards']
    #     # self.deckster_list = []
    #     # for i in range(number_of_cards):
    #     #     self.deckster_list.append(i)
    #     pass

    # def download_card_image(self):
    #     """
    #     Grab a single card image and download it.
    #     :return:
    #     """
    #     pass

# if __name__ == "__main__":
#     based_helper = BaseAPIHelper()
#     print(based_helper.get_random_psa_cert())