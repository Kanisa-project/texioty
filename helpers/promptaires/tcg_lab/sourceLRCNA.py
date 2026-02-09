import random
from typing import List
from unittest import case

import requests

from helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from settings import themery as t, utils as u

# from tcg_api.sourceTCG import BaseAPIHelper
# from src.utils import dbHelper

print_width_len = 36
base_url = 'https://api.lorcana-api.com'

LORCANA_TEMPLATES = {
    "all_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "type": []
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
        self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/lorcana_cards.db')
        # self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/lorcana_cards.db')
        self.db_helper.create_tables_from_templates(LORCANA_TEMPLATES)
        self.tcg_title_name = 'lorcana'

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
        action_card_insert_query = insert_table_statement_maker('action_cards',
                                                                [])

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


    # def download_card_batch(self, batch_config: dict):
    #     # super().download_card_batch(batch_config)
    #     random_color_types = requests.get(self.fetch_cards_url({'type': self.batch_type,
    #                                                         'color': random.choice(self.batch_colors.split(','))}))
    #     for i in range(batch_config['pack_size']):
    #         card = random.choice(random_color_types.json())
    #         # self.add_card_database(card)
    #         if 'Character' in card['Type']:
    #             # print(f"{card['Image']}    {card['Strength']}/{card['Willpower']}")
    #             pass
    #         else:
    #             # print(f"{card['Name']} - {card['Rarity']}")
    #             pass
    #         if card['Image'] is not None:
    #             self.add_card_local_database(card)
    #             img_data = requests.get(f'{card['Image']}').content
    #             save_name = f"{card['Set_Num']}_" + card['Name'].replace(" ", "_")
    #             with open(f'cards/{save_name}.png',
    #             # with open(f'helpers/promptaires/tcg_lab/cards/lorcana/{save_name}.png',
    #                       'wb') as handler:
    #                 handler.write(img_data)
    #             print(f"✓  Downloaded {save_name} into /fotoes/cardsLorcana")
    #

    def fetch_cards_url(self, query_dict: dict) -> str:
        use_url = self.base_url + "/cards/fetch?search="
        for key in list(query_dict.keys()):
            if key == 'name':
                use_url += f"{key.lower()}~{query_dict[key].lower()};"
            else:
                use_url += f"{key.lower()}={query_dict[key].lower()};"
        print("fetching  " + use_url)
        return use_url

    # def download_character(self):
    #     random_jasmine = requests.get(self.fetch_cards_url({'name': 'jasmine'}))
    #     for card in random_jasmine.json():
    #         if 'Character' in card['Type']:
    #             print(f"{card['Image']}    {card['Strength']}/{card['Willpower']}")
    #         else:
    #             print(f"{card['Name']} - {card['Rarity']}")
    #         if card['Image'] is not None:
    #             img_data = requests.get(f'{card['Image']}').content
    #             save_name = f"{card['Set_Num']}_" + card['Name'].replace(" ", "_")
    #             with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsLorcana/{save_name}.png',
    #                       'wb') as handler:
    #                 handler.write(img_data)
    #             print(f"Downloaded {save_name}")

    def gather_correct_cards(self, card_criteria: dict):
        search_criteria = {}
        if 'name' in card_criteria:
            search_criteria['name'] = card_criteria['name']
        if 'color' in card_criteria:
            search_criteria['color'] = card_criteria['color']
        if 'type' in card_criteria:
            search_criteria['type'] = card_criteria['type']
        return requests.get(self.fetch_cards_url(search_criteria)).json()


if __name__ == "__main__":
    lrca = SourceLRCNA()
    batch_profile = u.retrieve_tcg_profiles('lorcanas')["mickey_playmat_sleeves"]
    card_batch = lrca.gather_correct_cards(batch_profile['card_criteria'])
    lrca.download_card_batch(card_batch)
