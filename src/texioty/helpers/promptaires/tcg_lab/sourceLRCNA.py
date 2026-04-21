import random
from typing import List

import requests

from src.texioty.helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from src.texioty.helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from src.texioty.settings import utils as u
from pathlib import Path
# from tcg_api.sourceTCG import BaseAPIHelper
# from src.utils import dbHelper

print_width_len = 36
base_url = 'https://api.lorcana-api.com'

LORCANA_TEMPLATES = {
    "all_cards": {
        "source_id": [],
        "source_tcg": [],
        "name": [],
        "type": [],
        "rarity": [],
        "color": [],
        "artist": [],
        "set_code": [],
        "image_url": [],
        "local_image_path": [],
        "raw_data": []
    },
    "character_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "type": []
    },
    "action_cards": {
        "number": [],
        "play_cost": [],
        "digimon_power": [],
        "digivolution_conditions": [],
        "effects": [],
        "lvl": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "form": [],
        "attribute": [],
        "type": [],
        "inherited_effect": []
    },
    "item_cards": {
        "number": [],
        "play_cost": [],
        "effects": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "security_effect": [],
    },
    "location_cards": {
        "number": [],
        "play_cost": [],
        "effects": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "security_effect": []
    }
}

class SourceLRCNA(SourceTCG):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.lorcana-api.com'
        self.tcg_title_name = 'lorcana'
        self._init_lorcana_database()
        self.color_translation_dict = {
            "Amber": "yellow",
            "Amethyst": "purple",
            "Emerald": "green",
            "Ruby": "red",
            "Sapphire": "blue",
            "Steel": "gray",
        }

    def _init_lorcana_database(self):
        try:
            db_path = Path(__file__).resolve().parent / "databases" / "lorcana_cards.db"
            if not db_path.exists():
                self.db_helper = DatabaseHelper(str(db_path))
                self.db_helper.create_tables_from_templates(LORCANA_TEMPLATES)
            else:
                self.db_helper = DatabaseHelper(str(db_path))
        except Exception as e:
            print(f"Error initializing LRCNA database: {e}")


    def add_card_local_database(self, new_card):
        all_card_insert_query = insert_table_statement_maker('all_cards',
                                                             ['number',
                                                              'name',
                                                              'colour',
                                                              'type'])[0]
        self.db_helper.execute_query(all_card_insert_query,
                                     [new_card['Set_ID']+'-'+str(new_card['Card_Num']),
                                      new_card['Name'],
                                      new_card['Color'],
                                      new_card['Type']])
        print(new_card)
        match new_card['Type']:
            case "Character":
                self.add_character_local_database(new_card)
            case "Action":
                self.add_action_local_database(new_card)
            case "Item":
                self.add_item_local_database(new_card)
            case "Location":
                self.add_location_local_database(new_card)

        print(f"✓  Added {new_card['Name']} to local database.")

    def add_character_local_database(self, new_card):
        character_card_insert_query = insert_table_statement_maker('character_cards',
                                                                   ['number',
                                                                    'lvl',
                                                                    'name',
                                                                    'colour',
                                                                    'rarity',
                                                                    'form',
                                                                    'type',
                                                                    'inherited_effect'])[0]
        self.db_helper.execute_query(character_card_insert_query,
                                     [new_card['Unique_ID'],
                                      new_card['Cost'],
                                      new_card['Name'],
                                      new_card['Color'],
                                      new_card['Rarity'],
                                      new_card['Classifications'],
                                      new_card['Type'],
                                      new_card['Inkable']])

    def add_action_local_database(self, new_card):
        pass

    def add_item_local_database(self, new_card):
        pass

    def add_location_local_database(self, new_card):
        pass

    def download_card_batch(self, batch: List[dict]):
        for i in range(3):
            card = random.choice(batch)
            if 'Character' in card['Type']:
                # print(f"{card['Image']}    {card['Strength']}/{card['Willpower']}")
                pass
            else:
                # print(f"{card['Name']} - {card['Rarity']}")
                pass
            if card['Image'] is not None:
                self.add_card_local_database(card)
                img_data = requests.get(f'{card['Image']}').content
                save_name = f"{card['Set_Num']}_" + card['Name'].replace(" ", "_")
                with open(f'cards/{save_name}.png',
                # with open(f'helpers/promptaires/tcg_lab/cards/lorcana/{save_name}.png',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /fotoes/cardsLorcana")


    def fetch_cards_url(self, query_dict: dict) -> str:
        use_url = self.base_url + "/cards/fetch?search="
        for key in list(query_dict.keys()):
            if key == 'name':
                use_url += f"{key.lower()}~{query_dict[key].lower()};"
            elif key == 'set':
                use_url += f"set_id={query_dict[key]};"
            else:
                use_url += f"{key.lower()}={query_dict[key].lower()};"
        print("fetching  " + use_url)
        return use_url

    def get_card_batch(self, card_criteria: dict) -> List[dict]:
        print("LORCriterisa", card_criteria)
        if "Character" in card_criteria.get('type', ''):
            return self.fetch_character_cards(card_criteria)
        return []

    def fetch_character_cards(self, card_criteria) -> list:
        fetch_url = self.fetch_cards_url(card_criteria)
        return requests.get(fetch_url).json()

    def card_to_dict(self, card: dict) -> dict:
        print(card, "DECODODOlorcononono")
        return {
            "source_tcg": "lorcana",
            "source_id": card['Unique_ID'],
            "name": card['Name'],
            "set": card['Set_Name'],
            "type": card['Type'],
            "artist": card['Artist'],
            "color": card['Color'],
            "rarity": card['Rarity'],
            "image_url": card['Image'],
            "set_number": card['Set_Num'],
            "number": card['Card_Num'],
        }