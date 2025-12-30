import random
import sqlite3
import sqlite3 as sq3
# from helpers import dummyHelper
from mtgsdk import Card


def create_table_statement_maker(table_name: str, column_names: list) -> (str, dict):
    """
    Makes a sqlite3 statement from the parameters.
    :param table_name: Name of the new table being created.
    :param column_names: Name of columns being used.
    :return: Statement string and dictionary of info for the table.
    """
    if not column_names:
        raise ValueError("No columns provided for table creation.")

    add_new_table_info = {column_names[0]: []}
    statement_maked = f'CREATE TABLE IF NOT EXISTS {table_name} ('
    statement_maked += f'{column_names[0]} TEXT PRIMARY KEY,'
    for column in column_names[1:]:
        statement_maked += f' {column} TEXT NOT NULL,'
        add_new_table_info[column] = []
    return statement_maked[:-1] + ');', add_new_table_info


def update_table_statement_maker(table_name: str, column_names: list, updated_column=None) -> (str, dict):
    """
    Makes a sqlite3 statement from the parameters.
    :param updated_column:
    :param table_name: Name of the table being updated.
    :param column_names: Name of columns being used.
    :return: Statement string and dictionary of info for the table.
    """
    if len(column_names) < 2:
        raise ValueError("Insufficient columns provided for table update.")

    set_clause = ', '.join(f"{column} = ?" for column in column_names[1:])
    update_statement = f"UPDATE {table_name} SET {set_clause}"
    if updated_column:
        update_statement += f" WHERE {updated_column} = ?"
    update_statement += ";"

    return update_statement, column_names


def insert_table_statement_maker(table_name: str, column_names: list) -> (str, dict):
    """
    Makes a sqlite3 statement from the parameters.
    :param table_name: Name of the new table being edited.
    :param column_names: Name of columns being used.
    :return: Statement string and dictionary of info for the table.
    """
    if not column_names:
        raise ValueError("No columns provided for inserting into table.")

    columns_formatted = ', '.join([f"'{column}'" for column in column_names])
    values_placeholder = ', '.join(['?' for _ in column_names])
    statement_made = f'INSERT INTO {table_name} ({columns_formatted}) VALUES ({values_placeholder});'

    return statement_made, {}


class DatabaseHelper:
    """ Something to help keep track and centralize control of the database """

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = None
        self.connect()
        self.cursor = None
        # self.create_tcg_tables()

    def create_tables_from_templates(self, table_templates: dict):
        for table_name, template in table_templates.items():
            create_sql = create_table_statement_maker(table_name, list(template.keys()))[0]
            self.execute_query(create_sql)

    # def create_tcg_tables(self):
    #     """
    #     Create each of the TCG tables.
    #     :return:
    #     """
    #     tcg_templates = {
    #         'all_cards': dummyHelper.all_card_template,
    #         'pokemon_cards': dummyHelper.pokemon_card_template,
    #         'magic_cards': dummyHelper.mtg_card_template,
    #         'digimon_cards': dummyHelper.digimon_card_template,
    #         'lorcana_cards': dummyHelper.lorcana_card_template,
    #         'yugioh_cards': dummyHelper.yugioh_card_template
    #     }
    #     self.create_tables_from_templates(tcg_templates)

    # def create_gaim_tables(self):
    #     """Create necessary starting tables and populate the columns."""
    #     gaim_templates = {
    #         'all_gaims': dummyHelper.all_gaim_template,
    #         'candy_gaim': dummyHelper.candy_slinger_template,
    #         'kpaint_gaim': dummyHelper.k_paint_template,
    #         'pylane_gaim': dummyHelper.pylanes_template,
    #         'othaido_gaim': dummyHelper.othaido_template
    #     }
    #     self.create_tables_from_templates(gaim_templates)

    def init_databases(self):
        """Create necessary starting tables and populate the columns."""
        create_all_gaims_table_sql = create_table_statement_maker('all_gaims',
                                                                    list(dummyHelper.all_gaim_template.keys()))[0]
        self.execute_query(create_all_gaims_table_sql)


    def connect(self):
        """Creates a connection to the db_file."""
        try:
            self.connection = sq3.connect(self.db_file)
            print(f"Connected to '{self.db_file}' successfully!")
        except sq3.Error as e:
            print(f"Unable to connect successfully: {e}")

    def disconnect(self):
        """Closes the connection to the db_file."""
        if self.connection:
            self.connection.close()
            print(f"Disconnected for '{self.db_file}'")

    def execute_query(self, query, params=None) -> sqlite3.Cursor or None:
        """
        Takes in a query with/without params and returns the cursor.
        :param query: sqlite3 command statement
        :param params: list of column names, if required
        :return: sqlite3.Cursor or None (for error)
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            # print(query.split()[0] + f" {query.split()[5]}" + "\n     ╚►  executed successfully.")
            return cursor
        except sq3.Error as e:
            # print(f"Query execution failed for this reason: {e}")
            return None

    def fetch_data(self, query: str, params=None):
        """Fetches data from the db_file connection."""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print(query + "\n     ╚►  executed successfully.")
            return cursor.fetchall()
        except sq3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def get_table_data(self, table_name: str, column_index: int = None) -> list:
        """Fetches all data from a table."""
        select_query = f"SELECT * FROM {table_name};"
        data = self.fetch_data(select_query)

        if column_index is not None and data:
            return [row[column_index] for row in data]
        return data


if __name__ == "__main__":
    dbhelp = DatabaseHelper('mtg_spells.db')
    card_list = Card.where(set="ONE").where(layout='normal').all()
    for i in range(16):
        next_card = random.choice(card_list)
        while "Land" in next_card.type:
            next_card = random.choice(card_list)
        insert_norm_spells_table_sql = insert_table_statement_maker('norm_spells',
                                                                    list(dummyHelper.mtg_card_template.keys()))[0]
        print(dbhelp.execute_query(insert_norm_spells_table_sql,
                                   [next_card.name, next_card.set, str(next_card.cmc),
                                    next_card.layout, next_card.type.replace('\u2014', '-'),
                                    str(next_card.colors), next_card.mana_cost]))
    for card in dbhelp.get_available_spells():
        if card[3] == "normal":
            print(card)
