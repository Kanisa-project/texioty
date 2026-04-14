import logging
import os
from typing import List, Dict, Optional
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from src.texioty.helpers import dbHelper

from src.texioty.helpers.apis.api_helper import BaseAPIHelper

load_dotenv()
logger = logging.getLogger(__name__)

class TCGAPIError(Exception):
    pass

class TCGAPI(BaseAPIHelper):
    """
    Base class for TCG API helpers and interactions.
    Handles authentication, endpoint building and database stuff.
    """
    def __init__(self, api_name: str = 'psa', timeout: int = 10):
        """
        Initializes the TCG API helper with specified API name and timeout.
        """
        super().__init__()
        # self.tcg_title_name = api_name
        self.timeout = timeout
        self.base_url = 'https://api.psacard.com/publicapi/'

        self.api_token = os.getenv('PSACARD_API_TOKEN')
        if not self.api_token:
            logger.warning("No PSA API token found. Please set the PSACARD_API_TOKEN environment variable.")

        self.headers = {
            'Authorization': f'bearer {self.api_token}' if self.api_token else 'bearer invalid_token',
        }

        self.previous_endpoint = ''
        self.endpoint_names = {
            'cert': [
                'GetByCertNumber',
                'GetByCertNumberForFileAppend',
                'GetImagesByCertNumber'
            ],
            'order': [
                'GetProgress',
                'GetSubmissionProgress'
            ],
            'pop': [
                'GetPSASpecPopulation'
            ]
        }
        self.color_translation_dict: Dict[str, str] = {}
        self.db_helper: dbHelper.DatabaseHelper

    def endpoint_builder(self, endpoint_name: str, url_ending: str = '') -> str:
        if not endpoint_name:
            raise ValueError("Invalid endpoint name.")

        endpoint_url = f'{self.base_url}{endpoint_name}{url_ending}'
        logger.debug(f"Endpoint URL: {endpoint_url}")
        return endpoint_url

    def query_builder(self, query_dict: dict) -> str:
        if not query_dict:
            return ''
        try:
            query_string = urlencode(query_dict)
            logger.debug(f"Query string: {query_string}")
            return query_string
        except Exception as er:
            logger.error(f"Error constructing query string: {er}")
            raise TCGAPIError(f"Error constructing query string: {er}")


    def add_card_to_database(self, new_card: Dict) -> bool:
        if not self.db_helper:
            logger.warning("Database not initialized. Returning False.")
            return False

        try:
            required_fields = ['name', 'rarity', 'color', 'artist', 'type', 'set_code']
            if not all(field in new_card for field in required_fields):
                raise ValueError(f"Card missing required fields: {', '.join(required_fields)}. \nCard data: {new_card}")

            insert_query = dbHelper.insert_table_statement_maker(
                'all_cards',
                [
                    'source_tcg',
                    'source_id',
                    'name',
                    'type',
                    'rarity',
                    'color',
                    'artist',
                    'set_code',
                    'image_url',
                    'local_image_path',
                    'raw_data'
                ]
            )[0]

            self.db_helper.execute_query(
                insert_query,
                [
                    new_card.get('source_tcg', 'unknown'),
                    new_card.get('source_id', 'unknown'),
                    new_card['name'],
                    new_card['type'],
                    new_card['rarity'],
                    new_card['color'],
                    new_card['artist'],
                    new_card['set_code'],
                    new_card.get('image_url', 'unknown'),
                    new_card.get('local_image_path', 'unknown'),
                    str(new_card.get('raw_data', 'unknown'))
                ]
            )
            logger.info(f"Added card {new_card['name']} to database.")
            return True
        except Exception as e_:
            logger.error(f"Error adding card to database:-{e_}")
            return False

    def fetch_card_by_id(self, card_id: str) -> Optional[Dict]:
        try:
            endpoint = self.endpoint_builder('cert', f'/GetByCertNumber')
            query_params = self.query_builder({'': card_id})
            full_endpoint = f'{endpoint}/{query_params}'

            logger.debug(f"Fetching card from endpoint: {full_endpoint}")

            response = requests.get(
                full_endpoint,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            card_data = response.json()
            logger.info(f"Fetched card data for ID {card_id}: {card_data}")
            return card_data

        except Exception as e:
            logger.error(f"Error fetching card by ID {card_id}: {e}")
            return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    tcg = TCGAPI(api_name='psa')

    try:
        card = tcg.fetch_card_by_id('130782441')
        print(card)
    except Exception as e:
        print(e)