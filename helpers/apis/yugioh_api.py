import random

import requests
import yugioh

from helpers import dbHelper
from helpers.apis.base_tcg_api import TCGAPI
# from utils import dbHelper

# from helpers.promptaires.tcg_labby import TcgDepicter

# from utils.glythed import TcgDepicter

print_width_len = 36

def print_some_toons():
    cards = yugioh.get_cards_by_name(keyword='toon')
    random_cards = random.sample(cards.list, 6)
    for card_name in random_cards:
        random_toon = yugioh.get_card(card_name=card_name)
        try:
            print(random_toon.name)
            print(random_toon.attack, random_toon.defense, random_toon.attribute)
        except AttributeError as e:
            pass



# class YgoDepicter(TcgDepicter):
#     def __init__(self, depict_settings: dict):
#         super().__init__(depict_settings)


class YugiohAPIHelper(TCGAPI):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
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

    def fetch_single_card(self) -> dict:
        r = requests.get(self.endpoint_builder('?', self.query_builder({'cardset': random.choice(self.batch_set_ids)})))
        print("JSONDADA", r.json()['data'])
        random_card = random.choice(r.json()['data'])
        return random_card

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card['name'], new_card['card_sets'][0]['set_rarity'], new_card['type'], "Yu-Gi-Oh", new_card['id']])
        print(f"✓  Added {new_card['name']} to database")

    def download_card_batch(self, batch_config: dict):
        super().download_card_batch(batch_config)
        r = requests.get(self.endpoint_builder('?', self.query_builder({'type': self.batch_type})))
        random_cards = random.sample(r.json()['data'], self.batch_size)
        for card_dict in random_cards:
            self.add_card_database(card_dict)
            try:
                img_data = requests.get(f'https://images.ygoprodeck.com/images/cards/{card_dict["id"]}.jpg').content
                save_name = card_dict['name'].replace(" ", "_")
                with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsYuGiOh/{save_name}.jpg',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓|  Downloaded {save_name} into /fotoes/cardsYuGiOh")
            except AttributeError as e:
                print(e)
            except FileNotFoundError as e:
                print(e)


if __name__ == "__main__":
    pass


def run_depicter_from_script(depict_config_dict: dict):
    depicter = YgoDepicter(depict_config_dict)
    yapi = YugiohAPIHelper()
    ygo_card = yapi.fetch_single_card()
    card_datadict = depicter.build_card_datadict(ygo_card)
    depicted_card = depicter.depict_card(card_datadict)
    depicted_card.save(f"depictions/{depicter.card_datadict['name']}.png")


def run_puzzler_from_script(puzzle_config_dict: dict):
    pass