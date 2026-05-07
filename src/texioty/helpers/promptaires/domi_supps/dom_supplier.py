import random
import sqlite3
from typing import Optional, Any, Dict

import pandas as pd

from helpers.dbHelper import DatabaseHelper
from helpers.promptaires.prompt_helper import BasePrompt, Question, dict_to_question_prompt_factory, ResponseType

PRICE_RANGE_QUESTION_DICT = {
    "low_price": {
        "question": "What should the lowest price be?",
        "question_type": "STRICT",
        "default_response": 2,
        "response_type": ResponseType.INT
    },
    "high_price": {
        "question": "What should the highest price be?",
        "question_type": "STRICT",
        "default_response": 8,
        "response_type": ResponseType.INT
    }
}

class DominionSupplier(BasePrompt, DatabaseHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.db_path = "filesOutput/dominion_cards_base/domi_cards.db"
        self.initialize_card_database()
        self.card_rules = ['+X Card', '+$X', '+X Action']
        self.supply_setup = {
            'card_types': [],
            'cost_range': [],
            'set_groups': []
        }
        self.supply_setup_category = None
        self.types_to_include = []
        self.cost_range = []
        self.set_groups = []

        self.price_range_questions = dict_to_question_prompt_factory(
            PRICE_RANGE_QUESTION_DICT
        )
        self.SET_NAMES = [
            'Promo',
            'Dominion',
            'Intrigue',
            'Seaside',
            'Alchemy',
            'Prosperity',
            'Cornucopia',
            'Hinterlands',
            'Base Cards',
            'Dark Ages',
            'Guilds',
            'Adventures',
            'Empires',
            'Nocturne',
            'Renaissance'
        ]
        self.basic_card_types = ['Action', 'Treasure', 'Victory', 'Curse']
        self.multi_expansion_types = ['Attack', 'Duration', 'Reaction', 'Command']
        self.labeled_piles = ['Augur', 'Castle', 'Clash', 'Fort', 'Knight',
                              'Loot', 'Crier', 'Ruins']

        self.all_types = self.basic_card_types + self.multi_expansion_types + self.labeled_piles

    def initialize_card_database(self):
        DatabaseHelper.__init__(self, self.db_path)
        dominion_csv_data = pd.read_csv('filesInput/imports/dominion_cards.csv')
        prev_table_name = ""
        table_name = "Base Cards"
        with sqlite3.connect(self.db_path) as conn:
            for row in dominion_csv_data.itertuples():
                if row.set_name == "Promo":
                    dominion_csv_data.to_sql(row.set_name, conn, if_exists='delete_rows', index=False)
                print("initddb", row.set_name)

    def domi_supplier(self, profile_type: str):
        match profile_type:
            case "Setup Kingdom":
                self.setup_kingdom_rules()
            case "Check Kingdom":
                self.check_kingdom_rules()
            case "Reset Kingdom":
                self.reset_kingdom_rules()
            case "Create Kingdom":
                self.generate_supply_list()

    def reset_kingdom_rules(self):
        self.supply_setup = {
            'card_types': [],
            'cost_range': [],
            'set_groups': []
        }

    def fetch_cards_by_filters(self, filters: dict, limit: Optional[int] = None):
        domi_query = f"""
        SELECT
            card_name,
            set_name,
            type,
            is_kingdom_card,
            cost,
            card_text
        FROM {filters['set_name']}
        WHERE 1=1
        """
        params: list[Any] = []

        for key, value in filters.items():
            if value is None:
                continue
            if isinstance(value, list):
                domi_query += f" AND {key} IN ({','.join(['?'] * len(value))})"
                params.extend(value)
            else:
                domi_query += f" AND {key} = ?"
                params.append(value)

        domi_query += "ORDER BY card_name COLLATE NOCASE"

        if limit is not None:
            domi_query += " LIMIT ?"
            params.append(int(limit))

        return self.fetch_all(domi_query, params)

    def setup_kingdom_rules(self):
        self.decide_decision("What supply category to adjust?", list(self.supply_setup.keys()))
        self._set_deciding_function(self.set_supply_setup_category)

    def set_supply_setup_category(self, new_category: str):
        self.supply_setup_category = new_category
        match new_category:
            case "card_types":
                self.decide_decision("What type of card to add", self.basic_card_types)
                self._set_deciding_function(self.add_card_type_ruleset)
            case "cost_range":
                self.question_keys = list(PRICE_RANGE_QUESTION_DICT.keys())
                print(self.question_keys)
                self.start_question_prompt(self.price_range_questions)
            case "set_groups":
                pass

    def start_question_prompt(self, question_dict: Dict[str, Question], clear_txo=False):
        super().start_question_prompt(question_dict, clear_txo)

    def store_response(self, answer: str):
        super().store_response(answer)

    def end_question_prompt(self, question_dict: dict) -> dict:
        self.finalize_price_range(self.question_prompt_dict)
        return super().end_question_prompt(question_dict)

    # def set_low_price_range(self, low_price):
    #     self.supply_setup['cost_range'][0] = int(low_price)
    #     self.display_int_req_question("What should the highest price be")
    #     self._set_deciding_function(self.set_high_price_range)
    #
    # def set_high_price_range(self, high_price):
    #     self.supply_setup['cost_range'][1] = int(high_price)

    def add_card_type_ruleset(self, new_card_type: str):
        self.supply_setup['card_types'].append(new_card_type)
        self.decide_decision("Would you like to add another type", ['Yes', 'No'])
        self._set_deciding_function(self.add_another_card_type)

    def add_another_card_type(self, yesno: str):
        match yesno:
            case "Yes":
                self.set_supply_setup_category("card_types")
            case "No":
                self.txo.priont_dict(self.supply_setup)

    def check_kingdom_rules(self):
        self.txo.priont_dict(self.supply_setup)

    def generate_supply_list(self):
        full_card_list = []
        supply_list = []
        print("Generating with", self.supply_setup)
        if len(self.supply_setup['card_types']) > 0:
            for card in self.gather_cards_by_type(self.supply_setup['card_types']):
                full_card_list.append(card)
        # elif len(self.supply_setup['set_groups']) > 0:
        #     for card in self.gather_cards_by_set(self.supply_setup['set_groups']):
        #         full_card_list.append(card)
        elif len(self.supply_setup['cost_range']) == 2:
            print(self.supply_setup['cost_range'])
            cost_range_list = [i for i in range(
                self.supply_setup['cost_range'][0],
                self.supply_setup['cost_range'][1]+1
            )]
            print('CRANG', cost_range_list, self.gather_cards_by_cost(cost_range_list))
            for card in self.gather_cards_by_cost(cost_range_list):
                print(card['card_name'], card['cost'], card['type'])
                full_card_list.append(card)
        else:
            full_card_list = self.fetch_cards_by_filters({})
        random.shuffle(full_card_list)
        for i in range(10):
            if len(full_card_list) > 0:
                card = random.choice(full_card_list)
                full_card_list.remove(card)
                if card['type'] in self.supply_setup['card_types']:
                    supply_list.append(f"{card['card_name']} - {card['type']} - {card['cost']}")

        self.txo.priont_string("Supply list┓")
        self.txo.priont_list(supply_list, parent_key='Supply list')

    def gather_cards_by_type(self, card_types: list) -> list:
        return self.fetch_cards_by_filters({
            'type': card_types,
            'set_name': "Renaissance"
        })

    def gather_cards_by_set(self, sets: list) -> list:
        if len(sets) == 0:
            return self.fetch_cards_by_filters({})
        return self.fetch_cards_by_filters({
            'set_name': sets
        })

    def gather_cards_by_cost(self, costs: list) -> list:
        priced_cards = []
        for cost in costs:
            for card in self.fetch_cards_by_filters({
                'cost': f"${cost}",
                'set_name': 'Renaissance'
            }):
#                 print(card, "SCARDS")
                priced_cards.append(card)
        return priced_cards

    def finalize_price_range(self, question_prompt_dict: dict) -> None:
        self.supply_setup['cost_range'] = [
            question_prompt_dict['low_price'].user_response.int_response,
            question_prompt_dict['high_price'].user_response.int_response
        ]