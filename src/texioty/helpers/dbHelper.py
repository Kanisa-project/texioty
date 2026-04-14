from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

def insert_table_statement_maker(table_name: str, columns: list[str]) -> tuple[str, int]:
    placeholders = ', '.join(["?"] * len(columns))
    column_names = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    return query, len(columns)


class DatabaseHelper:
    """ Something to help keep track and centralize control of the database """

    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize_connection()

    def _initialize_connection(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        if getattr(self, 'conn', None) is not None:
            self.conn.close()

    def execute_query(self, query, params: Optional[Iterable[Any]] = None) -> None:
        if params is None:
            params = []
        self.cursor.execute(query, tuple(params))
        self.conn.commit()

    def execute_many(self, query: str, params_list: list[Iterable[Any]]) -> None:
        self.cursor.executemany(query, [tuple(params) for params in params_list])
        self.conn.commit()

    def fetch_one(self, query: str, params: Optional[Iterable[Any]] = None):
        if params is None:
            params = []
        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: Optional[Iterable[Any]] = None):
        if params is None:
            params = []
        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def create_tables_from_templates(self, templates: dict) -> None:
        for table_name, columns in templates.items():
            column_defs = []
            for column_name in columns.keys():
                column_type = self._infer_sqlite_type(column_name)
                column_defs.append(f"{column_name} {column_type}")

            if "id" not in columns and "source_id" not in columns:
                create_stmt = (
                    f"CREATE TABLE IF NOT EXISTS {table_name} ("
                    f"source_id TEXT PRIMARY KEY NOT NULL, "
                    f"{', '.join(column_defs)})"
                )
            else:
                create_stmt = (
                    f"CREATE TABLE IF NOT EXISTS {table_name} ("
                    f"{', '.join(column_defs)}"
                    f")"
                )
            print(create_stmt)
            self.execute_query(create_stmt)

    @staticmethod
    def _infer_sqlite_type(column_name: str) -> str:
        numeric_int_fields = {
            "id", "number", "lvl", "level", "play_cost", "atk", "def", "dp",
            "deck_size", "batch_size", "amount"
        }
        numeric_real_fields = {
            "ratio", "chance", "weight", "price", "cost"
        }

        if column_name.lower() in numeric_int_fields:
            return "INTEGER"
        if column_name.lower() in numeric_real_fields:
            return "REAL"
        if column_name in {"raw_data", "card_criteria"}:
            return "TEXT"
        return "TEXT"

    def insert_card(self, card: dict) -> bool:
        raw_data = card.get("raw_data", {})
        if not isinstance(raw_data, str):
            raw_data = json.dumps(raw_data)

        query = """
        INSERT OR REPLACE INTO all_cards (
            source_tcg,
            source_id,
            name,
            type,
            rarity,
            color,
            artist,
            set_code,
            image_url,
            local_image_path,
            raw_data,
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.execute_query(
            query,
            [
                card.get("source_tcg", "Unknown"),
                str(card.get("source_id", "Unknown")),
                card.get("name", "Unknown"),
                card.get("type", "Unknown"),
                card.get("rarity", "Unknown"),
                card.get("color", "Unknown"),
                card.get("artist", "Unknown"),
                card.get("set_code", "Unknown"),
                card.get("image_url"),
                card.get("local_image_path"),
                raw_data,
            ]
        )
        return True

    def update_card_image_path(self, source_tcg: str, source_id: str, local_image_path: str) -> None:
        query = """
        UPDATE all_cards
        SET local_path_image = ?
        WHERE source_tcg = ? AND source_id = ?
        """
        self.execute_query(query, [local_image_path, source_tcg, str(source_id)])

    def card_exists(self, source_tcg: str, source_id: str) -> bool:
        query = """
        SELECT 1
        FROM all_cards
        WHERE source_tcg = ? AND source_id = ?
        LIMIT 1
        """
        row = self.fetch_one(query, [source_tcg, str(source_id)])
        return row is not None

    def fetch_all_cards(self, limit: Optional[int] = None):
        query = """
        SELECT
            source_tcg,
            source_id,
            name,
            type,
            rarity,
            color,
            artist,
            set_code,
            image_url,
            local_image_path,
            raw_data
        FROM all_cards
        ORDER BY name COLLATE NOCASE
        """
        params: list[Any] = []
        if limit is not None:
            query += " LIMIT ?"
            params.append(int(limit))
        return self.fetch_all(query, params)

    def fetch_cards_by_filters(self, filters: dict, limit: Optional[int] = None):
        query = """
        SELECT
            source_tcg,
            source_id,
            name,
            type,
            rarity,
            color,
            artist,
            set_code,
            image_url,
            local_image_path,
            raw_data
        FROM all_cards
        WHERE 1=1
        """
        params: list[Any] = []

        for key, value in filters.items():
            if value is None:
                continue
            if isinstance(value, list):
                placeholders = ', '.join(['?'] * len(value))
                query += f" AND {key} IN ({placeholders})"
                params.extend(value)
            else:
                query += f" AND {key} = ?"
                params.append(value)

        query += " ORDER BY name COLLATE NOCASE"

        if limit is not None:
            query += " LIMIT ?"
            params.append(int(limit))

        return self.fetch_all(query, params)

