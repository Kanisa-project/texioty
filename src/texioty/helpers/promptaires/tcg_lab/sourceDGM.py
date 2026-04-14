from typing import List, Optional

import requests
import random

from src.texioty.helpers.dbHelper import DatabaseHelper
from src.texioty.helpers.dbHelper import insert_table_statement_maker
from src.texioty.helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from src.texioty.settings import utils as u
from pathlib import Path

base_url = "https://digimoncard.io/api-public/"

DIGIMON_TEMPLATES = {
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
    "digiegg_cards": {
        "number": [],
        "lvl": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "form": [],
        "type": [],
        "inherited_effect": []
    },
    "digimon_cards": {
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
    "tamer_cards": {
        "number": [],
        "play_cost": [],
        "effects": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "security_effect": [],
    },
    "option_cards": {
        "number": [],
        "play_cost": [],
        "effects": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "security_effect": []
    }
}

class SourceDGM(SourceTCG):
    def __init__(self):
        super().__init__()
        self.tcg_title_name = 'digimon'
        self._init_digimon_database()
        self.color_translation_dict = {
            "Red": "red",
            "Blue": "blue",
            "Yellow": "yellow",
            "Green": "green",
            "Black": "black",
            "Purple": "purple",
            "White": "white"
        }

    def _init_digimon_database(self):
        try:
            db_path = Path(__file__).resolve().parent / "databases" / "digimon_cards.db"
            if not db_path.exists():
                self.db_helper = DatabaseHelper(str(db_path))
                self.db_helper.create_tables_from_templates(DIGIMON_TEMPLATES)
            else:
                self.db_helper = DatabaseHelper(str(db_path))
        except Exception as e:
            print(f"Error initializing DGM database: {e}")

    def fetch_digiegg_cards(self, egg_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(egg_criteria)
        digieggs = requests.get(fetch_url)
        return digieggs.json()

    def fetch_tamer_cards(self, tamer_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(tamer_criteria)
        tamers = requests.get(fetch_url)
        return tamers.json()

    def fetch_digimon_cards(self, creature_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(creature_criteria)
        print(fetch_url)
        digimons = requests.get(fetch_url)
        return digimons.json()

    def fetch_option_cards(self, option_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(option_criteria)
        print(fetch_url)
        options = requests.get(fetch_url)
        return options.json()

    def query_builder(self, query_dict: dict) -> str:
        use_url = base_url + "search?"
        for key, value in query_dict.items():
            if key == "name":
                use_url += f"n={value.lower()}&"
            else:
                use_url += f"{key.lower()}={query_dict[key].lower()}&"
        print(use_url)
        return use_url

    def get_card_batch(self, card_criteria: dict) -> List[dict]:
        print("DGM_CRITeria", card_criteria)
        if "Digimon" in card_criteria.get('type', ''):
            return self.fetch_digimon_cards(card_criteria)
        if "Tamer" in card_criteria.get('type', ''):
            return self.fetch_tamer_cards(card_criteria)
        if "Digiegg" in card_criteria.get('type', ''):
            return self.fetch_digiegg_cards(card_criteria)
        if "Option" in card_criteria.get('type', ''):
            return self.fetch_option_cards(card_criteria)
        return []

    def card_to_dict(self, card: dict) -> dict:
        return {
            "source_tcg": "digimon",
            "source_id": card['id'],
            "name": card['name'],
            "type": card['type'],
            "rarity": card['rarity'],
            "color": card['color'],
            "artist": card['artist'],
            "set_code": card['set_name'],
            "pretty_url": card['pretty_url'],
        }

    def add_digiegg_local_database(self, new_card):
        tamer_card_insert_query = insert_table_statement_maker('digiegg_cards', ['number', 'name', 'colour', 'lvl', 'rarity', 'form', 'type', 'inherited_effect'])[0]
        self.db_helper.execute_query(tamer_card_insert_query,
                                     [new_card['id'],
                                      new_card['name'],
                                      new_card['color'],
                                      new_card['level'],
                                      new_card['rarity'],
                                      new_card['form'],
                                      new_card['type'],
                                      new_card['main_effect']])
        print(f"✓  Added {new_card['name']} to digiegg_cards.")

    def add_digimon_local_database(self, new_card):
        tamer_card_insert_query = insert_table_statement_maker('digimon_cards', ['number', 'digimon_power', 'play_cost', 'effects', 'lvl', 'name', 'colour', 'digivolution_conditions', 'rarity', 'form', 'attribute', 'type', 'inherited_effect'])[0]
        self.db_helper.execute_query(tamer_card_insert_query,
                                     [new_card['id'],
                                      new_card['dp'],
                                      new_card['play_cost'],
                                      new_card['main_effect'],
                                      new_card['level'],
                                      new_card['name'],
                                      new_card['color'],
                                      new_card['id'],
                                      new_card['rarity'],
                                      str(new_card['form']),
                                      new_card['attribute'],
                                      new_card['type'],
                                      new_card['source_effect']])
        print(f"✓  Added {new_card['name']} to digimon_cards.")

    def add_option_local_database(self, new_card):
        tamer_card_insert_query = insert_table_statement_maker('option_cards', ['number', 'effects', 'name', 'colour', 'play_cost', 'rarity', 'security_effect'])[0]
        self.db_helper.execute_query(tamer_card_insert_query,
                                     [new_card['id'],
                                      new_card['main_effect'],
                                      new_card['name'],
                                      new_card['color'],
                                      new_card['play_cost'],
                                      new_card['rarity'],
                                      new_card['source_effect']])
        print(f"✓  Added {new_card['name']} to option_cards.")

    def add_tamer_local_database(self, new_card):
        tamer_card_insert_query = insert_table_statement_maker('tamer_cards', ['number', 'effects', 'name', 'colour', 'play_cost', 'rarity', 'security_effect'])[0]
        self.db_helper.execute_query(tamer_card_insert_query,
                                     [new_card['id'],
                                      new_card['main_effect'],
                                      new_card['name'],
                                      new_card['color'],
                                      new_card['play_cost'],
                                      new_card['rarity'],
                                      new_card['source_effect']])
        print(f"✓  Added {new_card['name']} to tamer_cards.")
