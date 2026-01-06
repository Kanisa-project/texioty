import os
import requests
import random
from dotenv import load_dotenv
from helpers import dbHelper
from helpers.apis.api_helper import BaseAPIHelper

load_dotenv()


class TCGAPIHelper(BaseAPIHelper):
    def __init__(self):
        super().__init__()
        self.db_helper = dbHelper.DatabaseHelper('utils/tcg_cards.db')
        self.base_url = 'https://api.psacard.com/publicapi/'
        self.previous_endpoint = ''
        self.endpoint_names = {'cert': ['GetByCertNumber', 'GetByCertNumberForFileAppend', 'GetImagesByCertNumber'],
                               'order': ['GetProgress', 'GetSubmissionProgress'],
                               'pop': ['GetPSASpecPopulation']}
        self.headers = {
            'Authorization': 'bearer ' + 'psa_access_token_fake'
        }
        self.color_translation_dict = {}
        self.batch_set_id = ''
        self.batch_type = ''
        self.batch_size = 0
        self.batch_colors = ''
        self.tcg_title_name = 'psa'

    def get_card_database(self, card_type="R4ND0M") -> dict:
        pass

    def add_card_database(self, new_card):
        # all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        # self.db_helper.execute_query(all_card_insert_query, [new_card.name, new_card.rarity, new_card.type, new_card.set, new_card.number])
        pass

    def endpoint_builder(self, endpoint_name: str, url_ending: str):
        self.previous_endpoint = f'{self.base_url}{endpoint_name}{url_ending}'
        return self.previous_endpoint

    def query_builder(self, query_dict: dict) -> str:
        # print('previous endpoint', self.previous_endpoint)
        query_str = ''
        for i, (k, v) in enumerate(query_dict.items()):
            query_str += f'{k}={v}&'
        # print('dict:  ', query_dict)
        return query_str

    def get_random_psa_cert(self):
        rand_cert = random.randint(1, 99999999)
        rand_cert = f'{"0"*(8-len(str(rand_cert)))}{rand_cert}'
        print(self.endpoint_builder('cert', 'GetByCertNumber/70507261'))
        r = requests.get(self.endpoint_builder('cert', f'GetByCertNumber/70507261'), headers=self.headers)
        return r.json()

    def download_card_batch(self, batch_config: dict):
        """
        Get batch information and then download accordingly.
        :param batch_config:
        :return:
        """
        self.batch_set_id = random.choice(batch_config['batch_set_ids'])
        self.batch_type = random.choice(batch_config['batch_types'])
        self.batch_size = batch_config['batch_size']
        self.batch_colors = ','.join(batch_config['batch_colors'])
        # display_title(self.tcg_title_name, False)
        print(f"Attempting to download {self.batch_size} {self.batch_type} cards..")
        print(f"Of {self.batch_colors} coloring from {self.batch_set_id} sets...")


    def download_card_image(self):
        """
        Grab a single card image and download it.
        :return:
        """
        pass

# if __name__ == "__main__":
#     based_helper = BaseAPIHelper()
#     print(based_helper.get_random_psa_cert())