import random

import requests

from helpers.apis.base_tcg_api import TCGAPI
from helpers import dbHelper
print_width_len = 36
base_url = 'https://api.lorcana-api.com'

class LorcanaAPIHelper(TCGAPI):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.lorcana-api.com'
        self.tcg_title_name = 'lorcana'

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card['Name'], new_card['Rarity'], new_card['Type'], "Lorcana TCG", new_card['Set_ID']+'-'+str(new_card['Card_Num'])])
        print(f"✓  Added {new_card['Name']} to database.")

    def download_card_batch(self, batch_config: dict):
        super().download_card_batch(batch_config)
        random_color_types = requests.get(self.fetch_cards_url({'type': self.batch_type,
                                                            'color': random.choice(self.batch_colors.split(','))}))
        for i in range(batch_config['batch_size']):
            card = random.choice(random_color_types.json())
            self.add_card_database(card)
            if 'Character' in card['Type']:
                # print(f"{card['Image']}    {card['Strength']}/{card['Willpower']}")
                pass
            else:
                # print(f"{card['Name']} - {card['Rarity']}")
                pass
            if card['Image'] is not None:
                img_data = requests.get(f'{card['Image']}').content
                save_name = f"{card['Set_Num']}_" + card['Name'].replace(" ", "_")
                with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsLorcana/{save_name}.png',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /fotoes/cardsLorcana")


    def fetch_cards_url(self, query_dict: dict) -> str:
        use_url = self.base_url + "/cards/fetch?search="
        for key in list(query_dict.keys()):
            if key == 'name':
                use_url += f"{key.lower()}~{query_dict[key].lower()};"
            else:
                use_url += f"{key.lower()}={query_dict[key].lower()};"
        return use_url

    def download_character(self):
        random_jasmine = requests.get(self.fetch_cards_url({'name': 'jasmine'}))
        for card in random_jasmine.json():
            if 'Character' in card['Type']:
                print(f"{card['Image']}    {card['Strength']}/{card['Willpower']}")
            else:
                print(f"{card['Name']} - {card['Rarity']}")
            if card['Image'] is not None:
                img_data = requests.get(f'{card['Image']}').content
                save_name = f"{card['Set_Num']}_" + card['Name'].replace(" ", "_")
                with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsLorcana/{save_name}.png',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded {save_name}")

if __name__ == "__main__":
    lrca = LorcanaAPIHelper()
    # r = requests.get(lrca.fetch_cards_url({'name': 'jasmine'}))
    lrca.download_character()


def run_depicter_from_script(config_dict):
    return None