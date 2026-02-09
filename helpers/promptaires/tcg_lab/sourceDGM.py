from typing import List

import requests
import random

from helpers.dbHelper import DatabaseHelper
from helpers.dbHelper import insert_table_statement_maker
from helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from settings import themery as t, utils as u

base_url = "https://digimoncard.io/api-public/"

DIGIMON_TEMPLATES = {
    "all_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "type": []
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
        # self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/cards/databases/digimon_cards.db')
        self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/digimon_cards.db')
        self.db_helper.create_tables_from_templates(DIGIMON_TEMPLATES)

    def gather_correct_cards(self, card_criteria: dict):
        search_criteria = {}
        if 'name' in card_criteria:
            search_criteria['n'] = card_criteria['name']
        if 'color' in card_criteria:
            search_criteria['color'] = card_criteria['color']
        if 'rarity' in card_criteria:
            search_criteria['rarity'] = card_criteria['rarity']
        if 'artist' in card_criteria:
            search_criteria['artist'] = card_criteria['artist']
        if 'type' in card_criteria:
            match card_criteria['type']:
                case "Digi-Egg":
                    pass
                case "Digimon":
                    search_criteria['type'] = card_criteria['type']
                    return self.gather_digimon_cards(search_criteria)
                case "Option":
                    pass
                case "Tamer":
                    search_criteria['type'] = card_criteria['type']
                    return self.gather_tamer_cards(search_criteria)
                case _:
                    raise ValueError(f"Invalid card type: {card_criteria['type']}")
        return self.gather_digimon_cards(search_criteria)

    def gather_tamer_cards(self, tamer_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(tamer_criteria)
        tamers = requests.get(fetch_url)
        return tamers.json()

    def gather_digimon_cards(self, creature_criteria: dict) -> List[dict]:
        fetch_url = self.query_builder(creature_criteria)
        digimons = requests.get(fetch_url)
        return digimons.json()

    def query_builder(self, query_dict: dict) -> str:
        use_url = base_url + "search.php?"
        for key in list(query_dict.keys()):
            use_url += f"{key.lower()}={query_dict[key].lower()}&"
        print(use_url)
        return use_url

    def get_card_database(self, card_type="Digimon"):
        pass

    def add_card_local_database(self, new_card):
        all_card_insert_query = insert_table_statement_maker('all_cards',
                                                             ['name',
                                                              'colour',
                                                              'type',
                                                              'number'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card['name'],
                                                             new_card['color'],
                                                             new_card['type'],
                                                             new_card['id']])
        match new_card['type']:
            case "Digi-Egg":
                self.add_digiegg_local_database(new_card)
            case "Digimon":
                self.add_digimon_local_database(new_card)
            case "Tamer":
                self.add_tamer_local_database(new_card)
            case "Option":
                self.add_option_local_database(new_card)
        print(f"✓  Added {new_card['name']} to all_digimon_cards.")

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

    def download_card_batch(self, batch: List[dict]):
        for i in range(3):
            card = random.choice(batch)
            # print("DLCARD", card)
            self.add_card_local_database(card)
            print(f"{card['attribute']}    {card['id']}")
            if card['id'] is not None:
                img_data = requests.get(f'https://images.digimoncard.io/images/cards/{card['id']}.jpg').content
                save_name = f"{card['id']}_" + card['name'].replace(" ", "_")
                with open(f'helpers/promptaires/tcg_lab/cards/digimon/{save_name}.jpg',
                # with open(f'cards/{save_name}.jpg',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /fotoes/cardsDigimon")


if __name__ == "__main__":
    dgm = SourceDGM()
    batch_profile = u.retrieve_tcg_profiles('digimons')["augumon_sleeves_fillin"]
    card_batch = dgm.gather_correct_cards(batch_profile['card_criteria'])
    dgm.download_card_batch(card_batch)

