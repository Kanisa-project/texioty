import random
from pathlib import Path
from typing import List

import requests
from src.texioty.settings import utils as u
from src.texioty.helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from src.texioty.helpers.promptaires.tcg_lab.sourceTCG import SourceTCG

print_width_len = 36


YUGIOH_TEMPLATES = {
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
    "monster_cards": {
        "number": [],
        "lvl": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "ATK": [],
        "DEF": [],
        "type": []
    },
    "spell_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "rarity": [],
        "type": []
    },
    "trap_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "rarity": [],
        "type": []
    },
    "other_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "colour": [],
        "rarity": []
    }
}

class SourceYGO(SourceTCG):
    def __init__(self):
        super().__init__()
        self.tcg_title_name = 'yugioh'
        self.base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
        self._init_yugioh_database()

    def _init_yugioh_database(self):
        try:
            db_path = Path(__file__).resolve().parent / "databases" / "yugioh_cards.db"

            if not db_path.exists():
                self.db_helper = DatabaseHelper(str(db_path))
                self.db_helper.create_tables_from_templates(YUGIOH_TEMPLATES)
            else:
                self.db_helper = DatabaseHelper(str(db_path))
        except Exception as e:
            print(f"Error initializing YGO database: {e}")

        self.color_translation_dict = {
            'LIGHT': 'yellow',
            'DARK': 'purple',
            'FIRE': 'red',
            'WATER': 'blue',
            'WIND': 'green',
            'EARTH': 'brown',
            'DIVINE': 'white'
        }

    def add_card_local_database(self, new_card):
        """
        Adds a Yugioh card to the local database under the all_cards table and also the proper table.
        :param new_card: The card to add to the database.
        """
        all_card_insert_query = insert_table_statement_maker('all_cards',
                                                             ['number',
                                                              'name',
                                                              'colour',
                                                              'type'])[0]
        self.db_helper.execute_query(all_card_insert_query,
                                     [new_card['id'],
                                      new_card['name'],
                                      new_card.get('attribute', 'nOne'),
                                      new_card['type']])
        print('ADDCARD', new_card)
        if "Monster" in new_card['type']:
            self.add_monster_local_database(new_card)
        if "Spell" in new_card['type']:
            self.add_spell_local_database(new_card)
        if "Trap" in new_card['type']:
            self.add_trap_local_database(new_card)
        print(f"✓  Added {new_card['name']} to all_yugioh_cards.")

    def get_card_batch(self, card_criteria: dict) -> List[dict]:
        print("YUGI_CRITeria", card_criteria)
        if "Monster" in card_criteria.get('type', ''):
            return self.gather_monster_cards(card_criteria)
        if "Spell" in card_criteria.get('type', ''):
            return self.gather_spell_cards(card_criteria)
        if "Trap" in card_criteria.get('type', ''):
            return self.gather_trap_cards(card_criteria)
        return []

    def add_monster_local_database(self, new_card):
        monster_card_insert_query = insert_table_statement_maker('monster_cards',
                                                                 ['number',
                                                                  'lvl',
                                                                  'name',
                                                                  'colour',
                                                                  # 'rarity',
                                                                  'ATK',
                                                                  'DEF',
#                                                                   'type'
                                                                  ])[0]
        print("YUGO->  ", new_card)
        self.db_helper.execute_query(monster_card_insert_query,
                                     [new_card['id'],
                                      new_card['level'],
                                      new_card['name'],
                                      new_card['attribute'],
                                      # new_card['card_sets'][0]['set_rarity'],
                                      new_card['atk'],
                                      new_card['def'],
                                      # new_card['archetype']
                                      ])
        print(f"✓  Added {new_card['name']} to monster_cards.")

    def add_spell_local_database(self, new_card):
        spell_card_insert_query = insert_table_statement_maker('spell_cards',
                                                               ['number',
                                                                'effects',
                                                                'name',
                                                                'rarity',
                                                                'type'])[0]
        self.db_helper.execute_query(spell_card_insert_query,
                                     [new_card['id'],
                                      new_card['desc'],
                                      new_card['name'],
                                      new_card['card_sets'][0]['set_rarity'],
                                      new_card['type']])

    def add_trap_local_database(self, new_card):
        trap_card_insert_query = insert_table_statement_maker('trap_cards',
                                                              ['number',
                                                               'effects',
                                                               'name',
                                                               'rarity',
                                                               'type'])[0]
        self.db_helper.execute_query(trap_card_insert_query,
                                     [new_card['id'],
                                      new_card['desc'],
                                      new_card['name'],
                                      new_card['card_sets'][0]['set_rarity'],
                                      new_card['type']])

    def download_card_batch(self, batch: List[dict]):
        # print(batch)
        for i in range(3):
            card = random.choice(batch)
            print("DLCARD", card)
            self.add_card_local_database(card)

    # def gather_correct_cards(self, card_criteria: dict):
    #     search_criteria = {}
    #     # print("GATH", card_criteria)
    #     if 'name' in card_criteria:
    #         search_criteria['name'] = card_criteria['name']
    #     if 'color' in card_criteria:
    #         search_criteria['color'] = card_criteria['color']
    #     if 'type' in card_criteria:
    #         match card_criteria['type']:
    #             case 'Normal Monster':
    #                 return self.gather_monster_cards(card_criteria)
    #             case 'Spell Card':
    #                 print("WAT", search_criteria)
    #                 return self.gather_spell_cards(card_criteria)
    #             case 'Trap Card':
    #                 return self.gather_trap_cards(card_criteria)
    #             case 'Other Card':
    #                 return self.gather_other_cards(card_criteria)
    #             case _:
    #                 raise ValueError(f"Invalid card type: {card_criteria['type']}")
    #     return []

    def query_builder(self, query_dict: dict) -> str:
        use_url = self.base_url + "?"
        for key in list(query_dict.keys()):
            if "name" in key:
                query_dict[key] = query_dict[key].replace(" ", "_")
            use_url += f"{key.lower()}={query_dict[key].lower()}&"
        return use_url

    def gather_monster_cards(self, search_criteria):
        fetch_url = self.query_builder(search_criteria).replace(' ', "%20")
        print(fetch_url)
        monsters = requests.get(fetch_url)
        if 'data' in monsters.json():
            return monsters.json()['data']
        return []

    def gather_spell_cards(self, search_criteria):
        fetch_url = self.query_builder(search_criteria)
        spells = requests.get(fetch_url)
        if 'data' in spells.json():
            return spells.json()['data']
        return []

    def gather_trap_cards(self, search_criteria):
        fetch_url = self.query_builder(search_criteria)
        traps = requests.get(fetch_url)
        if 'data' in traps.json():
            return traps.json()['data']
        return []

    def gather_other_cards(self, search_criteria):
        pass

    def card_to_dict(self, yugicard: dict) -> dict:
        print("YUGid", yugicard)
        return {
            "source_tcg": "yugioh",
            "source_id": str(yugicard['id']),
            "name": yugicard['name'],
            "type": yugicard['type'],
            "rarity": yugicard['card_sets'][0]['set_rarity'],
            "color": yugicard.get('attribute', yugicard.get('humanReadableCardType', 'Unknown')),
            "artist": yugicard.get('artist', 'Unknown'),
            "set_code": yugicard['card_sets'][0]['set_code'],
            "image_url": f"https://images.ygoprodeck.com/images/cards/{yugicard['id']}.jpg",
        }
