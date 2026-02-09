import random
from typing import List

import requests
import yugioh
from settings import themery as t, utils as u
from helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from helpers.promptaires.tcg_lab.sourceTCG import SourceTCG

print_width_len = 36


YUGIOH_TEMPLATES = {
    "all_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "type": []
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

# def print_some_toons():
#     cards = yugioh.get_cards_by_name(keyword='toon')
#     random_cards = random.sample(cards.list, 6)
#     for card_name in random_cards:
#         random_toon = yugioh.get_card(card_name=card_name)
#         try:
#             print(random_toon.name)
#             print(random_toon.attack, random_toon.defense, random_toon.attribute)
#         except AttributeError as e:
#             pass


class SourceYGO(SourceTCG):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
        # self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/cards/databases/yugioh_cards.db')
        self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/yugioh_cards.db')
        self.db_helper.create_tables_from_templates(YUGIOH_TEMPLATES)
        self.color_translation_dict = {
            'light': 'yellow',
            'dark': 'purple',
            'fire': 'red',
            'water': 'blue',
            'wind': 'green',
            'earth': 'brown',
            'divine': 'white'
        }
        self.tcg_title_name = 'yugioh'

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



    # def download_card_batch(self, batch_config: dict):
    #     # super().download_card_batch(batch_config)
    #     print(batch_config)
    #     endpoint = self.endpoint_builder('?', self.query_builder({'type': random.choice(batch_config['type'])}))
    #     r = requests.get(endpoint)
    #     # print(r.json(), endpoint)
    #     random_cards = random.sample(r.json()['data'], batch_config['pack_size'])
    #     for card_dict in random_cards:
    #         self.add_card_local_database(card_dict)
    #         # self.add_card_database(card_dict)
    #         try:
    #             img_data = requests.get(f'https://images.ygoprodeck.com/images/cards/{card_dict["id"]}.jpg').content
    #             save_name = card_dict['name'].replace(" ", "_")
    #             with open(f'cards/{save_name}.jpg',
    #             # with open(f'helpers/promptaires/tcg_lab/cards/yugioh/{save_name}.jpg',
    #                       'wb') as handler:
    #                 handler.write(img_data)
    #             print(f"✓|  Downloaded {save_name} into /fotoes/cardsYuGiOh")
    #         except AttributeError as e:
    #             print(e)
    #         except FileNotFoundError as e:
    #             print(e)

    def gather_correct_cards(self, card_criteria: dict):
        search_criteria = {}
        print("GATH", card_criteria)
        if 'name' in card_criteria:
            search_criteria['name'] = card_criteria['name']
        if 'color' in card_criteria:
            search_criteria['color'] = card_criteria['color']
        if 'type' in card_criteria:
            match card_criteria['type']:
                case 'Normal Monster':
                    return self.gather_monster_cards(card_criteria)
                case 'Spell Card':
                    print("WAT", search_criteria)
                    return self.gather_spell_cards(card_criteria)
                case 'Trap Card':
                    return self.gather_trap_cards(card_criteria)
                case 'Other Card':
                    return self.gather_other_cards(card_criteria)
                case _:
                    raise ValueError(f"Invalid card type: {card_criteria['type']}")
        return []

    def query_builder(self, query_dict: dict) -> str:
        use_url = self.base_url + "?"
        for key in list(query_dict.keys()):
            use_url += f"{key.lower()}={query_dict[key].lower()}&"
        return use_url

    def gather_monster_cards(self, search_criteria):
        fetch_url = self.query_builder(search_criteria)
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


if __name__ == "__main__":
    ygo = SourceYGO()
    batch_profile = u.retrieve_tcg_profiles('yugiohs')["slimetoad_playmat_fillin_sleeves"]
    card_batch = ygo.gather_correct_cards(batch_profile['card_criteria'])
    for card in card_batch:
        print(card['name'], card_batch.index(card) + 1)
    ygo.download_card_batch(card_batch)