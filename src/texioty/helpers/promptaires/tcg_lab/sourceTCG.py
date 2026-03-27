from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Dict, Callable
from enum import Enum

from dotenv import load_dotenv
import requests
from src.texioty.helpers.apis.base_tcg_api import TCGAPI

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
        self.tcg_title_name = tcg_type.lower().replace(" ", "_") if tcg_type else "tcg"

        self.decoders: Dict[str, Callable] = {
            CardGameType.MAGIC_THE_GATHERING.value: self._decode_mtg,
            CardGameType.POKEMON.value: self._decode_pokemon,
            CardGameType.LORCANA.value: self._decode_lorcana,
            CardGameType.DIGIMON.value: self._decode_digimon,
            CardGameType.YUGIOH.value: self._decode_yugioh
        }

    def decode_card(self, raw_card_data: dict, tcg_type: str) -> dict:
        decoder = self.decoders.get(tcg_type)
        if not decoder:
            raise ValueError(f"No decoder found for TCG type: {tcg_type}")
        return decoder(raw_card_data)

    @staticmethod
    def card_to_dict(card: dict) -> dict:
        pass

    @staticmethod
    def _normalize_card(card_dict: dict) -> dict:
        normalized = {
            "source_tcg": card_dict.get("source_tcg", "Unknown"),
            "source_id": str(card_dict.get("source_id", card_dict.get("id", "Unknown"))),
            "name": card_dict.get("name", "Unknown"),
            "type": card_dict.get("type", "Unknown"),
            "rarity": card_dict.get("rarity", "Unknown"),
            "color": card_dict.get("color", "Unknown"),
            "artist": card_dict.get("artist", "Unknown"),
            "set_code": card_dict.get("set_code", card_dict.get("set",  "Unknown")),
            "image_url": card_dict.get("image_url", "Unknown"),
            "local_image_path": card_dict.get("local_image_path"),
            "raw_data": card_dict.get("raw_data", {}),
        }
        return normalized

    def _decode_mtg(self, card_data: dict) -> dict:
        return self._normalize_card({
            'source_tcg': CardGameType.MAGIC_THE_GATHERING.value,
            'source_id': f"{card_data.get('set_code')}_{card_data.get('number')}",
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('color'),
            'artist': card_data.get('artist'),
            'set_code': card_data.get('set_code'),
            'image_url': card_data.get("image_url"),
            'raw_data': str(card_data)
        })

    def _decode_pokemon(self, card_data: dict) -> dict:
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('energyType'),
            'artist': card_data.get('illustrator'),
            'set_code': card_data.get('set'),
            "source_id": card_data.get("source_id"),
            "image_url": card_data.get("image_url"),
            'source_tcg': CardGameType.POKEMON.value,
            'raw_data': card_data
        })

    def _decode_lorcana(self, card_data: dict) -> dict:
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('ink'),
            'artist': card_data.get('artist'),
            'set_code': card_data.get('set'),
            "source_id": card_data.get("id"),
            "image_url": card_data.get("image_url"),
            'source_tcg': CardGameType.LORCANA.value,
            'raw_data': card_data
        })

    def _decode_digimon(self, card_data: dict) -> dict:
        return self._normalize_card({
            'name': card_data.get('name'),
            'type': card_data.get('card_type'),
            'rarity': card_data.get('rarity'),
            'color': card_data.get('attribute'),
            'artist': card_data.get('creator'),
            'set_code': card_data.get('set_number'),
            "source_id": card_data.get("id"),
            "image_url": card_data.get("image_url"),
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
            'set_code': card_data.get('set'),
            "source_id": card_data.get("id"),
            "image_url": card_data.get("image_url"),
            'source_tcg': CardGameType.YUGIOH.value,
            'raw_data': card_data
        })

    def get_card_database(self, limit: Optional[int] = None, filters: Optional[dict] = None) -> List[dict]:
        rows = self.db_helper.fetch_all_cards(limit=limit)
        cards = [self._row_to_card_dict(row) for row in rows]
        if filters:
            cards = self._filter_by_criteria(cards, filters)
        return cards

    @staticmethod
    def _row_to_card_dict(row) -> dict:
        return dict(row)

    @staticmethod
    def _filter_by_criteria(cards: List[dict], criteria: dict) -> List[dict]:
        filtered = cards
        for key, value in criteria.items():
            if value is None:
                continue
            if isinstance(value, list):
                filtered = [card for card in filtered if card.get(key) in value]
            else:
                filtered = [card for card in filtered if card.get(key) == value]
        return filtered

    def card_exists(self, source_tcg: str, source_id: str) -> bool:
        return self.db_helper.card_exists(source_tcg, source_id)

    @staticmethod
    def download_card_image(card: dict, output_dir: str) -> str | None:
        image_url = card.get("image_url")
        if not image_url:
            return None

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        save_name = f"{card['source_id']}_{card['name'].replace(' ', '_')}.png"
        file_path = Path(output_dir) / save_name

        response = requests.get(image_url, timeout=15)
        response.raise_for_status()

        with open(sanitize_filename(str(file_path)), 'wb') as handler:
            handler.write(response.content)

        return str(file_path)

    def ingest_card(self, raw_card_data: dict, tcg_type: str, output_dir: str) -> dict:
        card = self.decode_card(raw_card_data, tcg_type)
        print(card, "DECODDDED")
        if self.card_exists(card['source_tcg'], card['source_id']):
            return card

        local_path = self.download_card_image(card, output_dir)
        card["local_image_path"] = local_path

        self.add_card_to_database(card)
        return card

    def add_card_local_database(self, card: dict) -> bool:
        return self.db_helper.insert_card(card)

    def gather_all_creature_cards(self, creature_criteria: dict,
                                  tcg_type: Optional[str] = None) -> List[dict]:
        criteria = {'type': 'creature'} if 'type' not in creature_criteria else creature_criteria
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [card for card in cards if card.get('source_tcg') == tcg_type]
        return self._filter_by_criteria(cards, criteria)

    def gather_all_resource_cards(self, resource_criteria: dict,
                                  tcg_type: Optional[str] = None) -> List[dict]:
        criteria = {'type': 'resource'} if 'type' not in resource_criteria else resource_criteria
        cards = self.get_card_database(limit=None)

        if tcg_type:
            cards = [card for card in cards if card.get('source_tcg') == tcg_type]
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
            cards = [card for card in cards if card.get('source_tcg') == tcg_type]
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


def sanitize_filename(filename: str) -> str:
    return ''.join(c for c in filename if c is not '/').rstrip()