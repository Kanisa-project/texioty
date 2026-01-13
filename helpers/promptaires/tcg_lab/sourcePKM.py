import os
import random

import requests
from dotenv import load_dotenv

from helpers import dbHelper
from helpers.promptaires.tcg_lab.sourceTCG import BaseAPIHelper, TCGAPIHelper
# from helpers.promptaires.tcg_lab.tcg_labby import TcgDepicter

from tcgdexsdk import TCGdex, Query
# from tcg_api.sourceTCG import BaseAPIHelper
# from src.utils import dbHelper, glythed
# from src.utils.glythed import TcgDepicter

load_dotenv()
width_len = 36
ENERGY_TYPES = ['grass', 'fire', 'water', 'lighting', 'psychic', 'fighting', 'darkness', 'metal']


# class PkmnDepicter(TcgDepicter):
#     def __init__(self, depict_settings: dict):
#         super().__init__(depict_settings)
#
#     def build_card_datadict(self, card_data) -> dict:
#         card_datadict = {
#             'name': card_data.name,
#             'type': ''.join(card_data.types),
#             'rarity': card_data.rarity,
#             'id': card_data.id
#         }
#         self.card_datadict = card_datadict
#         return card_datadict


class PokeAPIHelper(TCGAPIHelper):
    """
    An API helper for Pokemon TCG depiction, puzzling and listering on the KanisaBot.
    """
    def __init__(self):
        super().__init__()
        self.CARDTYPES = ["Energy", "Pokemon", "Trainer"]
        self.base_url = 'https://api.tcgdex.net/v2/en/'
        self.endpoint_names = {'cards': [],
                               'sets': []}
        self.color_translation_dict = {
            'grass': 'green',
            'fire': 'red',
            'water': 'blue',
            'lighting': 'yellow',
            'psychic': 'purple',
            'fighting': 'brown',
            'darkness': 'dark grey',
            'metal': 'light grey'
        }
        self.sdk = TCGdex()
        self.tcg_title_name = 'pokemon'

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card.name, new_card.rarity, new_card.category, "Pokemon TCG", new_card.id])
        print(f"✓  Added {new_card.name} to database.")


    def download_card_batch(self, batch_config: dict):
        endpoint = self.endpoint_builder('cards?', self.query_builder({'category': random.choice(batch_config["card_types"])}))
        r = requests.get(self.endpoint_builder('cards?', self.query_builder({'category': random.choice(batch_config["card_types"])})))
        print(endpoint, r.json())
        try:
            r.raise_for_status()
        except Exception as e:
            print(f"Error: {e} (status {getattr(r, 'status_code', 'unknown')})")
            return

        try:
            payload = r.json()
        except ValueError:
            print("Invalid JSON received.")
            return

        if isinstance(payload, dict):
            cards = None
            for possible_key in ('cards', 'data', 'results', 'items'):
                if possible_key in payload and isinstance(payload[possible_key], list):
                    cards = payload[possible_key]
                    break
            if cards is None:
                for v in payload.values():
                    if isinstance(v, list):
                        cards = v
                        break
            if cards is None:
                print(f"API returned an object and no card list was found: {list(payload.keys())}")
        elif isinstance(payload, list):
            cards = payload
        else:
            print(f"API returned an object of unknown type: {type(payload)}")
            return

        chosen_count = min(batch_config.get('pack_size', 1), len(cards))
        chosen_cards = random.sample(cards, chosen_count) if chosen_count <= len(cards) else [random.choice(cards) for _ in range(batch_config.get('batch_size', 1))]

        for card in chosen_cards:
            if isinstance(card, dict):
                image_field = card.get('image') or card.get('image_url') or card.get('images')
                if isinstance(image_field, dict):
                    img_url = image_field.get('high') or image_field.get('png') or image_field.get('large')
                else:
                    img_url = image_field
                name = card.get('name') or card.get('title') or 'unknown card'
                set_info = card.get('set') or card.get('set_name') or {}
                set_id = set_info.get('id') if isinstance(set_info, dict) else getattr(set_info, 'id', 'unknown')
            else:
                img_url = getattr(card, 'image', None)
                name = getattr(card, 'name', 'unknown card')
                set_id = getattr(getattr(card, 'set', None), 'id', 'unknown')

            if not img_url or img_url in ("None", "none"):
                print(f"Skipping {name} because it has no image.")
                continue

            if img_url.endswith('/high.png') or img_url.endswith('.png'):
                final_url = img_url if img_url.endswith('.png') else img_url + '.png'
            else:
                final_url = img_url + '/high.png'

            try:
                img_data = requests.get(final_url).content
            except Exception as e:
                print(f"Failed to download {name} from {img_url}: {e}")
                continue
            print(card, "PKMNCard")
            save_name = f"{(set_id or 'UNK').upper()}_" + card['name'].replace(" ", "_")
            out_path = os.path.join('helpers/promptaires/tcg_lab/cards/pokemon', f'{save_name}.png')
            try:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, 'wb') as handler:
                    handler.write(img_data)
                print(f"✓  Downloaded {save_name} into /worx_hop/cardsPokemon")
            except Exception as e:
                print(f"Failed to write image to {out_path}: {e}")


def download_snorlaxes():
    sdk = TCGdex()
    snorlax_cards = sdk.card.listSync(Query().equal('name', 'Snorlax'))
    random_snorlaxes = random.sample(snorlax_cards, 6)
    for card in random_snorlaxes:
        card = sdk.card.getSync(card.id)
        print(f'{card.name}  {card.image}/high.png')
        print(f'{card.rarity}  {card.hp}')
        print(f'{card.set.name}')
        if card.image is not None:
            img_data = requests.get(f'{card.image}/high.png').content
            save_name = f"{card.set.id.upper()}_" + card.name.replace(" ", "_")
            with open(f'/worx_hop/cardsPokemon/{save_name}.png',
                      'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}")

if __name__ == "__main__":
    # download_energy_set()
    download_snorlaxes()


def run_depicter_from_script(depict_config_dict: dict):
    depicter = PkmnDepicter(depict_config_dict)
    sdk = TCGdex()
    rando_card = random.choice(sdk.card.listSync(Query().equal('name', 'Snorlax')))
    pkmn_card = sdk.card.getSync(rando_card.id)
    card_datadict = depicter.build_card_datadict(pkmn_card)
    depicted_card = depicter.depict_card(card_datadict)
    depicted_card.save(f"depictions/{depicter.card_datadict['name']}.png")


def run_puzzler_from_script(puzzle_config_dict: dict):
    pass