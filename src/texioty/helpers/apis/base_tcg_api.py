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
        self.tcg_title_name = api_name
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
        try:
            self.db_helper = dbHelper.DatabaseHelper(
                'alldata_base.db'
                # 'helpers/promptaires/tcg_lab/cards/databases/alldata_base.db'
            )
        except Exception as e_:
            logger.error(f"Error initializing database: {e_}")
            self.db_helper = None

    def endpoint_builder(self, endpoint_name: str, url_ending: str = '') -> str:
        """
        Constructs a full endpoint string by combining the base URL with the given endpoint name
        and optional URL ending.

        Args:
            endpoint_name (str): The name of the endpoint to be appended to the base URL.
            url_ending (str, optional): An additional string to be appended after the endpoint name.
                Defaults to an empty string.

        Returns:
            str: The constructed full endpoint URL.
        """
        if not endpoint_name:
            raise ValueError("Invalid endpoint name.")

        endpoint_url = f'{self.base_url}{endpoint_name}{url_ending}'
        logger.debug(f"Endpoint URL: {endpoint_url}")
        return endpoint_url

    def query_builder(self, query_dict: dict) -> str:
        """
        Constructs a query string from a dictionary of key-value pairs.

        Args:
            query_dict (dict): A dictionary containing query parameters.

        Returns:
            str: The constructed query string.
        """
        if not query_dict:
            return ''
        try:
            query_string = urlencode(query_dict)
            logger.debug(f"Query string: {query_string}")
            return query_string
        except Exception as er:
            logger.error(f"Error constructing query string: {er}")
            raise TCGAPIError(f"Error constructing query string: {er}")

    def get_card_database(self, card_type: str = 'all', limit: Optional[str] = None) -> List[Dict]:
        """
        Retrieve cards from the local database.

        Args:
            card_type (str, optional): The type of cards to retrieve. Defaults to 'all'.
            limit (int, optional): The maximum number of cards to retrieve. Defaults to None (no limit).

        Returns:
            List[Dict]: A list of card dictionaries.
        """
        if not self.db_helper:
            logger.warning("Database not initialized. Returning empty list.")
            return []

        try:
            query = "SELECT * FROM all_cards"
            if card_type != 'all':
                query += f" WHERE card_type = ?"
                params = [card_type]
            else:
                params = []

            if limit:
                query += f" LIMIT ?"
                params.append(limit)

            results = self.db_helper.execute_query(query, params)
            logger.info(f"Retrieved {len(results) if results else 0} cards from database.")
            return results if results else []
        except Exception as e_:
            logger.error(f"Error retrieving cards from database: {e_}")
            return []

    def add_card_to_database(self, new_card: Dict) -> bool:
        """
        Add a single card to the local database.

        Args:
            new_card (Dict): Card dictionary with keys: name, rarity, color, artist, type, set

        Returns:
            bool: True if the card was successfully added, False otherwise.
        """
        if not self.db_helper:
            logger.warning("Database not initialized. Returning False.")
            return False

        try:
            required_fields = ['name', 'rarity', 'color', 'artist', 'type', 'set_code']
            if not all(field in new_card for field in required_fields):
                raise ValueError(f"Card missing required fields: {', '.join(required_fields)}. \nCard data: {new_card}")

            insert_query = dbHelper.insert_table_statement_maker(
                'all_cards',
                ['name', 'rarity', 'color', 'artist', 'type', 'set_code']
            )[0]

            self.db_helper.execute_query(
                insert_query,
                [new_card['name'], new_card['rarity'], new_card['color'], new_card['artist'], new_card['type'], new_card['set_code']]
            )
            logger.info(f"Added card {new_card['name']} to database.")
            return True
        except Exception as e_:
            logger.error(f"Error adding card to database:-{e_}")
            return False

    def fetch_card_by_id(self, card_id: str) -> Optional[Dict]:
        """
        Fetch a card from the local database by its ID.

        Args:
            card_id (int): The ID of the card to fetch.

        Returns:
            Optional[Dict]: The card dictionary if found, None otherwise.
        """
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