from typing import List, Optional, Dict, Callable
from enum import Enum

from dotenv import load_dotenv
from helpers.apis.base_tcg_api import TCGAPI

load_dotenv()

class CardGameType(Enum):
    MAGIC_THE_GATHERING = 'Magic the Gathering'
    POKEMON = 'Pokemon'
    LORCANA = 'Lorcana'
    YUGIOH = 'Yu-Gi-Oh'
    DIGIMON = 'Digimon'

class CardTypeCategory(Enum):
    CREATURE = 'creature'
    RESOURCE = 'resource'
    PERMANENT = 'permanent'
    TEMPORARY = 'temporary'


class SourceTCG(TCGAPI):
    """
    Gathers and normalizes cards from a TCG source.
    """
    def __init__(self, tcg_type: Optional[str] = None):
        super().__init__()
        self.default_tcg_type = tcg_type
        self.decoders: Dict[str, Callable] = {
            CardGameType.MAGIC_THE_GATHERING.value: self._decode_mtg,
            CardGameType.POKEMON.value: self._decode_pokemon,
            CardGameType.LORCANA.value: self._decode_lorcana,
            CardGameType.DIGIMON.value: self._decode_digimon,
            CardGameType.YUGIOH.value: self._decode_yugioh
        }

    def decode_card(self, raw_card_data: dict, tcg_type: str) -> dict:
        """
        Decodes raw card data for a specific trading card game (TCG) type and returns a
        formatted dictionary containing metadata and attributes specific to the card.

        Args:
            raw_card_data (dict): The raw card data containing unformatted attributes
                retrieved from an external source.
            tcg_type (str): The type of trading card game (e.g., "Yu-Gi-Oh", "Magic",
                etc.) to ensure correct field formatting.

        Returns:
            dict: Normalized card metadata and attributes.
        """
        decoder = self.decoders.get(tcg_type)
        if not decoder:
            raise ValueError(f"No decoder found for TCG type: {tcg_type}")
        return decoder(raw_card_data)

    def _decode_mtg(self, card_data: dict) -> dict:
        """
        Decode Magic the Gathering card data into normalized schema
        """
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('color'),
            'artist': card_data.get('artist'),
            'set': card_data.get('set'),
            'source_tcg': CardGameType.MAGIC_THE_GATHERING.value,
            'raw_data': card_data
        })

    def _decode_pokemon(self, card_data: dict) -> dict:
        """
        Decode Pokémon card data into normalized schema
        """
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('energyType'),
            'artist': card_data.get('illustrator'),
            'set': card_data.get('set'),
            'source_tcg': CardGameType.POKEMON.value,
            'raw_data': card_data
        })

    def _decode_lorcana(self, card_data: dict) -> dict:
        """
        Decode Lorcana card data into normalized schema
        """
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('ink'),
            'artist': card_data.get('artist'),
            'set': card_data.get('set'),
            'source_tcg': CardGameType.LORCANA.value,
            'raw_data': card_data
        })

    def _decode_digimon(self, card_data: dict) -> dict:
        """
        Decode Digimon card data into normalized schema
        """
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('card_type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('attribute'),
            'artist': card_data.get('creator'),
            'set': card_data.get('set_number'),
            'source_tcg': CardGameType.DIGIMON.value,
            'raw_data': card_data
        })

    def _decode_yugioh(self, card_data: dict) -> dict:
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('color'),
            'artist': card_data.get('artist'),
            'set': card_data.get('set'),
            'source_tcg': CardGameType.YUGIOH.value,
            'raw_data': card_data
        })

    @staticmethod
    def _normalize_card(card_dict: dict) -> dict:
        """
        Apply final normalization steps to a card dictionary and return the normalized card metadata.
        """
        required_fields = ["name", "type", "rarity", "color", "artist", "set_code", "source_tcg"]
        for field in required_fields:
            if field not in card_dict or card_dict[field] is None:
                card_dict[field] = "Unknown"
        return card_dict

    @staticmethod
    def _filter_by_criteria(cards: List[dict], criteria: dict) -> List[dict]:
        """
        Filter a list of cards based on given criteria.
        """
        filtered = cards
        for key, value in criteria.items():
            if value is None:
                continue
            if isinstance(value, list):
                filtered = [c for c in filtered if c.get(key) in value]
            else:
                filtered = [c for c in filtered if c.get(key) == value]
        return filtered


    def gather_all_creature_cards(self, creature_criteria: dict,
                                  tcg_type: Optional[str] = None) -> List[dict]:
        """
        Gather creature-styled cards to create a card batch. They match an offensive/defensive profile.
        :param creature_criteria: The criteria to match creature cards to.
        :param tcg_type: Optional type of TCG to filter by. If None, all types are considered.
        """
        criteria = {'type': 'creature'} if 'type' not in creature_criteria else creature_criteria
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [c for c in cards if c.get('source_tcg') == tcg_type]
        return self._filter_by_criteria(cards, criteria)

    def gather_all_resource_cards(self, resource_criteria: dict,
                                  tcg_type: Optional[str] = None) -> List[dict]:
        """
        Gather resource-styled cards to create a card batch. They match an energy provision profile.
        :param resource_criteria: The criteria to match resource cards to.
        :param tcg_type: Optional type of TCG to filter by. If None, all types are considered.
        """
        criteria = {'type': 'resource'} if 'type' not in resource_criteria else resource_criteria
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [c for c in cards if c.get('source_tcg') == tcg_type]
        return self._filter_by_criteria(cards, criteria)

    def gather_all_permanent_cards(self, permanent_criteria: dict,
                                   tcg_type: Optional[str] = None) -> List[dict]:
        """
        Gather permanent-styled cards to create a card batch. They match a battlefield static profile.
        :param permanent_criteria: The criteria to match permanent cards to.
        :param tcg_type: Optional type of TCG to filter by. If None, all types are considered.
        """
        criteria = {'type': 'permanent' if 'type' not in permanent_criteria else permanent_criteria}
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [c for c in cards if c.get('source_tcg') == tcg_type]
        return self._filter_by_criteria(cards, criteria)

    def gather_all_temporary_cards(self, temporary_criteria: dict,
                                   tcg_type: Optional[str]) -> List[dict]:
        """
        Gather temporary-styled cards to create a card batch. They match a battlefield effect profile.
        :param temporary_criteria: The criteria to match temporary cards to.
        :param tcg_type: Optional type of TCG to filter by. If None, all types are considered.
        """
        criteria = {'type': 'temporary'} if 'type' not in temporary_criteria else temporary_criteria
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [c for c in cards if c.get('source_tcg') == tcg_type]
        return self._filter_by_criteria(cards, criteria)

