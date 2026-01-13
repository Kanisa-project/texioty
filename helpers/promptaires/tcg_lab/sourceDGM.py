import requests
import random

from helpers import dbHelper
from helpers.promptaires.tcg_lab.sourceTCG import BaseAPIHelper, TCGAPIHelper
# from helpers.promptaires.tcg_lab.tcg_labby import TcgDepicter

base_url = "https://digimoncard.io/api-public/"

class DigimonAPIHelper(TCGAPIHelper):
    def __init__(self):
        super().__init__()
        self.tcg_title_name = 'digimon'

    def get_card_database(self, card_type="Digimon"):
        pass

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card['name'], new_card['rarity'], new_card['type'], new_card['series'], new_card['id']])
        print(f"✓  Added {new_card['name']} to database.")

    def download_card_batch(self, batch_config: dict):
        # super().download_card_batch(batch_config)
        chosen_color = random.choice(self.batch_colors.split(','))
        fetch_url = fetch_cards_url({'color': chosen_color,
                                                       'pack': self.batch_set_id,
                                                       'type': self.batch_type})
        print(fetch_url)
        random_digimon = requests.get(fetch_url)
        print(random_digimon)
        for i in range(batch_config['pack_size']):
            card = random.choice(random_digimon.json())
            # self.add_card_database(card)
            print(f"{card['attribute']}    {card['id']}")
            if card['id'] is not None:
                img_data = requests.get(f'https://images.digimoncard.io/images/cards/{card['id']}.jpg').content
                save_name = f"{card['id']}_" + card['name'].replace(" ", "_")
                with open(f'helpers/promptaires/tcg_lab/cards/digimon/{save_name}.jpg',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /fotoes/cardsDigimon")




def fetch_cards_url(query_dict: dict) -> str:
    use_url = base_url + "search.php?"
    for key in list(query_dict.keys()):
        use_url += f"{key.lower()}={query_dict[key].lower()}&"
    # print(use_url)
    return use_url

def download_digimon():
    random_digimon = requests.get(fetch_cards_url({'color': 'purple',
                                                   'evocolor': 'blue',
                                                   'type': 'digimon'}))
    for card in random_digimon.json():
        print(f"{card['attribute']}    {card['id']}")
        if card['id'] is not None:
            img_data = requests.get(f'https://images.digimoncard.io/images/cards/{card['id']}.jpg').content
            save_name = f"{card['id']}_" + card['name'].replace(" ", "_")
            with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/fotoes/cardsDigimon/{save_name}.jpg',
                      'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}")

# class DgmDepicter(TcgDepicter):
#     def __init__(self, config_dict):
#         super().__init__(config_dict)

# def run_depicter_from_script(depict_config_dict: dict):
#     depicter = DgmDepicter(depict_config_dict)
#     dapi = DigimonAPIHelper()
#     rando_card = random.choice(Card.where(name="Ultimatum").all())
#     card_datadict = depicter.build_card_datadict(rando_card)
#     depicted_card = depicter.depict_card(card_datadict)
#     save_name = depicter.card_datadict['name'].replace(' ', '_')
#     depicted_card.save(f"tcg_lab/{save_name}.png")
#     print(f"Saved {save_name}")