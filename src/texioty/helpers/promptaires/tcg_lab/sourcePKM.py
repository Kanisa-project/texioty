import random
from typing import List, Dict

import requests
from dotenv import load_dotenv

from src.texioty.helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from src.texioty.helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from src.texioty.settings import utils as u
from tcgdexsdk import TCGdex, Query, Card, SetResume
from pathlib import Path

load_dotenv()
width_len = 36
ENERGY_TYPES = ['grass', 'fire', 'water', 'lighting', 'psychic', 'fighting', 'darkness', 'metal']

POKEMON_TEMPLATES = {
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
    "energy_cards": {
        "source_id": [],
        "name": [],
        "special_effect": []
    },
    "pokemon_cards": {
        "source_id": [],
        "name": [],
        "hp": [],
        "level": [],
        "abilities": [],
        "attacks": [],
        "retreat_cost": [],
        "stage": []
    },
    "trainer_cards": {
        "source_id": [],
        "name": [],
        "trainer_type": [],
        "effect": []
    }
}


class SourcePKM(SourceTCG):
    """
    An API helper for Pokemon TCG depiction, puzzling and listering on the KanisaBot.
    """
    def __init__(self):
        super().__init__()
        self.tcg_title_name = 'pokemon'
        self.CARDTYPES = ["Energy", "Pokemon", "Trainer"]
        self.base_url = 'https://api.pokemontcg.io/v2/'

        self.color_translation_dict = {
            'grass': 'green',
            'fire': 'red',
            'water': 'blue',
            'lighting': 'yellow',
            'psychic': 'purple',
            'fighting': 'brown',
            'darkness': 'dark grey',
            'metal': 'light grey',
            'colorless': 'white'
        }
        self.sdk = TCGdex()
        self._init_pkm_database()

    def _init_pkm_database(self):
        try:
            db_path = Path(__file__).resolve().parent / "cards" / "databases" / "pokemon_cards.db"
            if not db_path.exists():
                self.db_helper = DatabaseHelper(str(db_path))
                self.db_helper.create_tables_from_templates(POKEMON_TEMPLATES)
            else:
                self.db_helper = DatabaseHelper(str(db_path))
        except Exception as e:
            print(f"Error initializing PKM database: {e}")

    def get_card_batch(self, card_criteria: Dict) -> List[Card]:
        if "Pokemon" in card_criteria.get('type'):
            return self.gather_pokemon_cards(card_criteria)
        if "Energy" in card_criteria.get('type'):
            return self.gather_energy_cards(card_criteria)
        if "Trainer" in card_criteria.get('type'):
            return self.gather_trainer_cards(card_criteria)
        else:
            return []

    def add_card_to_database(self, new_card: Card) -> bool:
        try:
            if not self.db_helper:
                print("Database not initialized")
                return False
            if not isinstance(new_card, dict):
                new_card = pkmcard_to_dict(new_card)
            return super().add_card_to_database(new_card)
        except Exception as e:
            print(f"Error adding card to database:--{e}")
            return False

    def add_card_local_database(self, new_card):
        all_card_insert_query = insert_table_statement_maker('all_cards', ['number', 'name', 'colour', 'type'])[0]
        new_card = self.sdk.card.getSync(new_card.id)
        self.db_helper.execute_query(all_card_insert_query, [new_card.id, new_card.name, ', '.join(new_card.types) if new_card.types else "None", new_card.category])
        print(f"✓  Added {new_card.name} to database.")
        match new_card.category:
            case "Pokemon":
                self.add_pokemon_local_database(new_card)
            case "Energy":
                self.add_energy_local_database(new_card)
            case "Trainer":
                self.add_trainer_local_database(new_card)

    def add_pokemon_local_database(self, new_card):
        tamer_card_insert_query = insert_table_statement_maker('pokemon_cards', ['number', 'hp', 'abilities', 'lvl', 'name', 'colour', 'rarity', 'stage', 'retreat_cost', 'attacks'])[0]
        new_card = self.sdk.card.getSync(new_card.id)
        print(new_card)
        self.db_helper.execute_query(tamer_card_insert_query,
                                     [new_card.id,
                                      new_card.hp,
                                      random.choice(new_card.abilities).name if new_card.abilities else "None",
                                      str(new_card.level),
                                      new_card.name,
                                      ', '.join(new_card.types),
                                      new_card.rarity,
                                      new_card.stage,
                                      new_card.retreat if new_card.retreat else "None",
                                      random.choice(new_card.attacks).name])
        print(f"✓  Added {new_card.name} to pokemon_cards.")

    def add_energy_local_database(self, new_card):
        """
        Add an energy card from the card batch to the local database.
        :new_card: The card to add to the database.
        """
        energy_card_insert_query = insert_table_statement_maker('energy_cards', ['number', 'name', 'colour', 'rarity', 'special_effect'])[0]
        new_card = self.sdk.card.getSync(new_card.id)
        print(new_card)
        self.db_helper.execute_query(energy_card_insert_query,
                                     [new_card.id,
                                             new_card.name,
                                             new_card.name.replace(" Energy", ""),
                                             new_card.rarity,
                                             str(new_card.effect)])
        print(f"✓  Added {new_card.name} to energy_cards.")

    def add_trainer_local_database(self, new_card):
        """
        Add a trainer card from the card batch.
        """
        trainer_card_insert_query = insert_table_statement_maker('trainer_cards', ['number', 'effects', 'name', 'rarity'])[0]
        new_card = self.sdk.card.getSync(new_card.id)
        print(new_card)
        self.db_helper.execute_query(trainer_card_insert_query,
                                     [new_card.id,
                                      new_card.effect if not None else "None",
                                      new_card.name,
                                      new_card.rarity])
        print(f"✓  Added {new_card.name} to trainer_cards.")



    def download_card_batch(self, batch):
        print("Downloading cards:")
        for _ in range(5):
            card = random.choice(batch)
            self.add_card_local_database(card)
            if card.image is not None:
                img_data = requests.get(f'{card.image}/high.png').content
                save_name = f"{card.id}_" + card.name.replace(" ", "_")
                # with open(f'helpers/promptaires/tcg_lab/cards/pokemon/{save_name}.png',
                with open(f'cards/{save_name}.png',
                          'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded {save_name}")


    def gather_correct_cards(self, card_criteria: dict):
        search_criteria = {}
        if 'name' in card_criteria:
            search_criteria['name'] = card_criteria['name']
        if 'color' in card_criteria:
            search_criteria['color'] = card_criteria['color']
        if 'rarity' in card_criteria:
            search_criteria['rarity'] = card_criteria['rarity']
        if 'artist' in card_criteria:
            search_criteria['artist'] = card_criteria['artist']
        if 'type' in card_criteria:
            match card_criteria['type']:
                case "Pokemon":
                    search_criteria['type'] = card_criteria['type']
                    return self.gather_pokemon_cards(search_criteria)
                case "Energy":
                    search_criteria['type'] = card_criteria['type']
                    return self.gather_energy_cards(search_criteria)
                case "Trainer":
                    search_criteria['type'] = card_criteria['type']
                    return self.gather_trainer_cards(search_criteria)
                case _:
                    return None
        return None

    def gather_pokemon_cards(self, creature_criteria):
        try:
            print(f"Trying to get pokemons with criteria: {creature_criteria}")
            pokemons = self.sdk.card.listSync(
                Query()
                .equal('name', creature_criteria.get('name', ''))
                .equal('category', 'Pokemon')
                # .equal('rarity', creature_criteria.get('rarity', ''))
                # .equal('types', creature_criteria.get('color', ''))
                # .equal('illustrator', creature_criteria.get('artist', ''))
            )
            print(f"Got {pokemons} pokemons")
        except Exception as e:
            print(f"Error gathering pokemon cards: {e}")
            pokemons = []
        return pokemons

    def gather_energy_cards(self, energy_criteria):
        try:
            energys = self.sdk.card.listSync(Query().equal('category', energy_criteria['type']))
            if energy_criteria.get('name'):
                energys = energys.listSync(Query().equal('name', energy_criteria['name']))
            if energy_criteria.get('type'):
                energys = energys.listSync(Query().equal('category', energy_criteria['type']))
            if energy_criteria.get('rarity'):
                energys = energys.listSync(Query().equal('rarity', energy_criteria['rarity']))
            if energy_criteria.get('color'):
                energys = energys.listSync(Query().equal('types', energy_criteria['color']))
            if energy_criteria.get('artist'):
                energys = energys.listSync(Query().equal('illustrator', energy_criteria['artist']))
            else:
                energys = []
        except Exception as e:
            print(f"Error gathering energy cards: {e}")
            energys = []
        print(energys)
        return energys

    def gather_trainer_cards(self, trainer_criteria):
        try:
            trainers = self.sdk.card.listSync(Query().equal('category', trainer_criteria['type']))
            if trainer_criteria.get('name'):
                trainers = trainers.listSync(Query().equal('name', trainer_criteria['name']))
            if trainer_criteria.get('rarity'):
                trainers = trainers.listSync(Query().equal('rarity', trainer_criteria['rarity']))
            if trainer_criteria.get('artist'):
                trainers = trainers.listSync(Query().equal('illustrator', trainer_criteria['artist']))
            if trainer_criteria.get('type'):
                trainers = trainers.listSync(Query().equal('category', trainer_criteria['type']))
            if trainer_criteria.get('color'):
                trainers = trainers.listSync(Query().equal('types', trainer_criteria['color']))
            else:
                trainers = []
        except Exception as e:
            print(f"Error gathering trainer cards: {e}")
            trainers = []
        return trainers

    def card_to_dict(self, pkmcard: Card) -> Dict:
        local_id = pkmcard.localId
        pkmcard = self.sdk.card.getSync(pkmcard.id)
        print("PKMCARD", pkmcard.id)
        return {
            'source_id': f"{pkmcard.id}",
            'name': pkmcard.name,
            'type': pkmcard.category,
            'rarity': pkmcard.rarity,
            'color': ', '.join(pkmcard.types) if isinstance(pkmcard.types, list) else pkmcard.types,
            'artist': pkmcard.illustrator,
            'set_code': pkmcard.set.id,
            'image_url': pkmcard.image,
            'number': local_id
        }

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
            with open(f'cards/{save_name}.png',
                      'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}")

if __name__ == "__main__":
    pkm = SourcePKM()
    batch_profile = u.retrieve_tcg_profiles('pokemons')["snorlax"]
    card_batch = pkm.gather_correct_cards(batch_profile['card_criteria'])
    pkm.download_card_batch(card_batch)
    # download_snorlaxes()

