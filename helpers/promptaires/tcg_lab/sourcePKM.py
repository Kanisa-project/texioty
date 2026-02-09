import os
import random
from typing import List

import requests
from dotenv import load_dotenv

from helpers.dbHelper import DatabaseHelper, insert_table_statement_maker
from helpers.promptaires.tcg_lab.sourceTCG import SourceTCG
from settings import themery as t, utils as u
from tcgdexsdk import TCGdex, Query, Card

load_dotenv()
width_len = 36
ENERGY_TYPES = ['grass', 'fire', 'water', 'lighting', 'psychic', 'fighting', 'darkness', 'metal']


POKEMON_TEMPLATES = {
    "all_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "type": []
    },
    "energy_cards": {
        "number": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "special_effect": []
    },
    "pokemon_cards": {
        "number": [],
        "hp": [],
        "abilities": [],
        "lvl": [],
        "name": [],
        "colour": [],
        "rarity": [],
        "stage": [],
        "retreat_cost": [],
        "attacks": []
    },
    "trainer_cards": {
        "number": [],
        "effects": [],
        "name": [],
        "rarity": []
    }
}


class SourcePKM(SourceTCG):
    """
    An API helper for Pokemon TCG depiction, puzzling and listering on the KanisaBot.
    """
    def __init__(self):
        super().__init__()
        self.CARDTYPES = ["Energy", "Pokemon", "Trainer"]
        self.base_url = 'https://api.pokemontcg.io/v2/'
        self.db_helper = DatabaseHelper('helpers/promptaires/tcg_lab/cards/databases/pokemon_cards.db')
        # self.db_helper = DatabaseHelper('cards/databases/pokemon_cards.db')
        self.db_helper.create_tables_from_templates(POKEMON_TEMPLATES)
        # self.endpoint_names = {'cards': [],
        #                        'sets': []}
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
        self.tcg_title_name = 'pokemon'

    def gather_all_creature_cards(self, creature_criteria: dict) -> List[dict]:
        # super().gather_all_creature_cards(creature_criteria)
        pass


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
                with open(f'helpers/promptaires/tcg_lab/cards/pokemon/{save_name}.png',
                # with open(f'cards/{save_name}.png',
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
        if "name" in creature_criteria:
            pokemons = self.sdk.card.listSync(Query().equal('name', creature_criteria['name']))
        print(pokemons)
        return pokemons

    def gather_energy_cards(self, energy_criteria):
        if "name" in energy_criteria:
            energys = self.sdk.card.listSync(Query().equal('name', energy_criteria['name']))
        elif "type" in energy_criteria:
            energys = self.sdk.card.listSync(Query().equal('category', energy_criteria['type']))
        else:
            energys = []
        print(energys)
        return energys

    def gather_trainer_cards(self, trainer_criteria):
        if "name" in trainer_criteria:
            trainers = self.sdk.card.listSync(Query().equal('name', trainer_criteria['name']))
        print(trainers)
        return trainers

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
    batch_profile = u.retrieve_tcg_profiles('pokemons')["snorlax_playmat_wordsearch"]
    card_batch = pkm.gather_correct_cards(batch_profile['card_criteria'])
    pkm.download_card_batch(card_batch)
    # download_snorlaxes()

