import os
import json
import random
from typing import Dict, Optional, List

from src.texioty.helpers.gaims.base_gaim import BaseGaim
from src.texioty.helpers.registries.command_definitions import bind_commands, BATTLESHIP_COMMANDS

from dataclasses import dataclass
from typing import Optional

BOARD_FILE = "filesOutput/boards.json"
BOARD_LETTERS = "ABCDEFGHIJ"

def make_blank_board() -> Dict[str, list]:
    return {letter: [' '] * 10 for letter in 'ABCDEFGHIJ'}

def clone_board(board: Dict[str, list]) -> Dict[str, list]:
    return {letter: row[:] for letter, row in board.items()}

def is_valid_coord(callout: str) -> bool:
    if not isinstance(callout, str):
        return False
    callout = callout.strip().upper()
    if len(callout) != 2:
        return False
    if callout[0] not in BOARD_LETTERS:
        return False
    if callout[1] not in '0123456789':
        return False
    return True

def board_has_ships(board: Dict[str, list]) -> bool:
    for letter in BOARD_LETTERS:
        if "#" in board[letter]:
            return True
    return False

def check_player_call(callout: str) -> bool:
    if len(callout) != 2:
        return False
    if callout[0].upper() not in 'ABCDEFGHIJ':
        return False
    if callout[1] not in '0123456789':
        return False
    return True


def fire_at(board_loc: str, board: Dict[str, list]) -> str:
    row = board_loc[0].upper()
    col = int(board_loc[1])
    if board[row][col] == "#":
        board[row][col] = "+"
        return "hit"
    if board[row][col] == " ":
        board[row][col] = "-"
        return "miss"
    return 'repeat'

def can_place_ship(board: Dict[str, list], start: str, direction: str, length: int) -> bool:
    if not is_valid_coord(start):
        return False
    if direction not in ['h', 'v', 'north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
        return False
    if length < 1 or length > 5:
        return False
    row_letter = start[0].upper()
    col_index = int(start[1])
    row_index = BOARD_LETTERS.index(row_letter)
    match direction:
        case 'n':
            dir_tuple = (0, -1)
        case 's':
            dir_tuple = (0, 1)
        case 'e':
            dir_tuple = (1, 0)
        case 'w':
            dir_tuple = (-1, 0)
        case _:
            return False
    for offset in range(length):
        current_row = row_index + offset * dir_tuple[0]
        current_col = col_index + offset * dir_tuple[1]

        if current_row >= 10 or current_col >= 10:
            return False

        board_row_letter = BOARD_LETTERS[current_row]
        if board[board_row_letter][current_col] != ' ':
            return False

    return True

def place_ship(board: Dict[str, list], start: str, direction: str, length: int) -> bool:

    if not can_place_ship(board, start, direction, length):
        return False

    row_letter = start[0].upper()
    col_index = int(start[1])
    row_index = BOARD_LETTERS.index(row_letter)
    print(direction, "PLACING")
    match direction:
        case 'n':
            dir_tuple = (-1, 0)
        case 's':
            dir_tuple = (1, 0)
        case 'e':
            dir_tuple = (0, 1)
        case 'w':
            dir_tuple = (0, -1)
        case _:
            return False
    for offset in range(length):
        current_row, current_col = dir_tuple[0] * offset + row_index, dir_tuple[1] * offset + col_index
        # current_row = row_index + offset if direction == 'V' else row_index
        # current_col = col_index + offset if direction == 'H' else col_index
        board_row_letter = BOARD_LETTERS[current_row]
        board[board_row_letter][current_col] = '#'
    return True

def serialize_board(board: Dict[str, list]) -> List[str]:
    return [''.join(board[letter]) for letter in BOARD_LETTERS]

class BattleshipRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "Battleship")
        self.game_playing = False
        self.player_board = make_blank_board()
        self.enemy_board = make_blank_board()
        self.enemy_mask = make_blank_board()
        self.player_called_shots = []
        self.enemy_called_shots = []
        self.available_boards = {}
        self.selected_player_board_name: Optional[str] = None
        self.selected_enemy_board_name: Optional[str] = None
        self.builder_board = make_blank_board()
        self.builder_board_name: Optional[str] = None
        self.last_status_message = "Use 'fire [COORD]', for example 'fire C2'."

        self.helper_commands = bind_commands(BATTLESHIP_COMMANDS, {
            "show": self.show_game,
            "fire": self.fire_shot,
            "boards": self.list_boards,
            "use": self.use_boards,
            "build": self.start_board_builder,
            "place": self.place_builder_ship,
            "showbuild": self.show_builder_board,
            "clearbuild": self.clear_builder_board,
            "saveboard": self.save_builder_board
        }) | self.gaim_commands

    def get_header_right_status(self) -> str:
        enemy_ships_left = sum(row.count("#") for row in self.enemy_board.values())
        player_ships_left = sum(row.count("#") for row in self.player_board.values())
        return f"Enemy:{enemy_ships_left} | Player:{player_ships_left} "

    def get_header_bottom_status(self) -> str:
        if self.game_playing:
            return self.last_status_message
        if self.builder_board_name:
            return f"Builder: {self.builder_board_name}"
        return self.last_status_message

    def new_game(self):
        super().new_game()
        self.available_boards = self.load_available_boards()

        if not self.available_boards:
            self.txo.priont_string(f"No boards found in {BOARD_FILE}.")
            self.txo.priont_string("Please create a boards.json file with your boards.")
            self.game_playing = False
            self.last_status_message = "No boards available."
            self.refresh_header_status()
            return

        if self.selected_player_board_name is None:
            self.selected_player_board_name = sorted(self.available_boards.keys())[0]

        if self.selected_enemy_board_name is None:
            self.selected_enemy_board_name = random.choice(list(self.available_boards.keys()))

        self.player_board = self.board_from_name(self.selected_player_board_name)
        self.enemy_board = self.board_from_name(self.selected_enemy_board_name)
        self.enemy_mask = make_blank_board()
        self.player_called_shots = []
        self.enemy_called_shots = []
        self.game_playing = True
        self.last_status_message = f"Use 'fire [COORD]' | Board: {self.selected_player_board_name}"
        self.welcome_message([])
        self.show_game()

    def welcome_message(self, welcoming_msgs=None):
        self.txo.clear_add_header("Battleship")
        self.txo.priont_string("Welcome to Battleship!\n")
        self.txo.priont_string("Use 'fire A5' to attack and 'show' to see the current board.\n")

    def save_game(self):
        self.game_state = {
            "player_name": self.txo.master.active_profile.username,
            "game_playing": self.game_playing,
            "player_board": self.player_board,
            "enemy_board": self.enemy_board,
            "enemy_mask": self.enemy_mask,
            "player_called_shots": self.player_called_shots,
            "enemy_called_shots": self.enemy_called_shots,
            "selected_player_board_name": self.selected_player_board_name,
            "selected_enemy_board_name": self.selected_enemy_board_name
        }
        super().save_game()

    def load_game(self):
        loaded_state = super().load_game()
        if loaded_state is None:
            return
        self.game_state = loaded_state
        self.game_playing = self.game_state["game_playing"]
        self.player_board = clone_board(self.game_state["player_board"])
        self.enemy_board = clone_board(self.game_state["enemy_board"])
        self.enemy_mask = clone_board(self.game_state["enemy_mask"])
        self.player_called_shots = self.game_state["player_called_shots"][:]
        self.enemy_called_shots = self.game_state["enemy_called_shots"][:]
        self.selected_player_board_name = self.game_state["selected_player_board_name"]
        self.selected_enemy_board_name = self.game_state["selected_enemy_board_name"]
        self.available_boards = self.load_available_boards()

        self.welcome_message([])
        self.show_game(None)

    def stop_game(self):
        self.game_playing = False
        super().stop_game()

    def show_game(self, args=None):
        self.render_with_header()
        self.txo.priont_string("Enemy Waters:")
        for line in self.board_to_lines(self.enemy_mask):
            self.txo.priont_string(line)

        self.txo.priont_string("")
        self.txo.priont_string("Player Waters:")
        for line in self.board_to_lines(self.player_board):
            self.txo.priont_string(line)

    @staticmethod
    def render_board_lines(board: Dict[str, list]) -> list[str]:
        lines = [" 0123456789"]
        for letter in BOARD_LETTERS:
            lines.append(f"{letter}{''.join(board[letter])}")
        return lines

    def list_boards(self, args=None):
        self.available_boards = self.load_available_boards()
        if not self.available_boards:
            self.txo.priont_string(f"No boards found in {BOARD_FILE}.")
            return
        self.txo.priont_string("Available Boards:")
        for board_name in sorted(self.available_boards.keys()):
            self.txo.priont_string(f" - {board_name}")

    def use_boards(self, args: str):
        self.available_boards = self.load_available_boards()
        if not self.available_boards:
            self.txo.priont_string(f"No boards found in {BOARD_FILE}.")
            return
        if not args:
            self.txo.priont_string("Please specify a board to use.")
            return
        parts = args.split()
        if len(parts) not in [1, 2]:
            self.txo.priont_string("Please specify a board to use.")
            return

        player_name = parts[0]
        enemy_name = parts[1] if len(parts) == 2 else random.choice(list(self.available_boards.keys()))

        if player_name not in self.available_boards:
            self.txo.priont_string(f"Board '{player_name}' not found.")
            return

        if enemy_name not in self.available_boards:
            self.txo.priont_string(f"Board '{enemy_name}' not found.")
            return

        self.selected_player_board_name = player_name
        self.selected_enemy_board_name = enemy_name
        self.last_status_message = f"Using boards: you={player_name} enemy={enemy_name}"
        self.refresh_header_status()

    def start_board_builder(self, args:str=None):
        self.builder_board = make_blank_board()
        self.builder_board_name = args.strip() if args else None
        if self.builder_board_name:
            self.last_status_message = f"Building board: {self.builder_board_name}"
            self.txo.priont_string(f"Starting board builder for '{self.builder_board_name}'")
        else:
            self.last_status_message = "Building new unnamed board"
            self.txo.priont_string("Starting board builder with new board")
        self.show_builder_board()

    def show_builder_board(self):
        self.render_with_header()
        title = self.builder_board_name or "unnamed"
        self.txo.priont_string(f"Builder Board: {title}")
        for line in self.board_to_lines(self.builder_board):
            self.txo.priont_string(line)

    def clear_builder_board(self):
        self.builder_board = make_blank_board()
        self.last_status_message = "Builder board cleared."
        self.txo.priont_string("Builder board cleared.")
        self.show_builder_board()

    def place_builder_ship(self, start: str, direction: str, length: int):
        direction = direction.lower()

        try:
            length = int(length)
        except ValueError:
            self.txo.priont_string("Invalid length. Use 'place A0 north 5'")
            return

        if direction not in ['n', 's', 'e', 'w', 'north', 'south', 'east', 'west', 'h', 'v']:
            self.txo.priont_string("Invalid direction. Use 'place A0 north 5'")
            return
        start = start.upper()
        if not place_ship(self.builder_board, start, direction, length):
            self.txo.priont_string("Invalid ship placement. Use 'place A0 north 5'")
            return

        self.last_status_message = f"Ship placed at {start} {direction} {length}"
        self.txo.priont_string(f"Ship placed at {start} {direction} {length}")
        self.show_builder_board()

    def save_builder_board(self, args: str = None):
        board_name = args.strip() if args else self.builder_board_name
        if not board_name:
            self.txo.priont_string("Please specify a board name.")
            return
        os.makedirs(os.path.dirname(BOARD_FILE), exist_ok=True)
        if os.path.exists(BOARD_FILE):
            with open(BOARD_FILE, 'r', encoding='utf-8') as board_json:
                try:
                    boards = json.load(board_json)
                except json.JSONDecodeError:
                    boards = {}
        else:
            boards = {}
        boards[board_name] = serialize_board(self.builder_board)

        with open(BOARD_FILE, 'w', encoding='utf-8') as board_json:
            json.dump(boards, board_json, indent=2)

        self.builder_board_name = board_name
        self.available_boards = self.load_available_boards()
        self.txo.priont_string(f"Board saved as '{board_name}'")

    def player_win(self):
        self.txo.priont_string("Congratulations! You beat the enemy!")
        self.game_playing = False

    def enemy_win(self):
        self.txo.priont_string("Sorry, the enemy beat you!")
        self.game_playing = False

    @staticmethod
    def board_to_lines(board: Dict[str, list], hide_ships: bool = False) -> list[str]:
        lines = [" 0123456789"]
        for letter in "ABCDEFGHIJ":
            row = ''.join(board[letter])
            if hide_ships:
                row = row.replace("#", " ")
            lines.append(f"{letter}{row}")
        return lines

    def get_enemy_call(self) -> str:
        callout = random.choice("ABCDEFGHIJ") + str(random.randint(0, 9))
        while callout in self.enemy_called_shots:
            callout = random.choice("ABCDEFGHIJ") + str(random.randint(0, 9))
        self.enemy_called_shots.append(callout)
        return callout

    def fire_shot(self, target: str):
        if not self.game_playing:
            self.txo.priont_string("Start a new game with 'new'")
            return

        if not target:
            self.txo.priont_string("Use 'fire [COORD], for example 'fire C2'.")
            return

        target = target.strip().upper()
        if not is_valid_coord(target):
            self.txo.priont_string("Invalid target.  Use 'fire [COORD], for example 'fire C2'.")
            return

        if target in self.player_called_shots:
            self.txo.priont_string("You already fired at that location.")
            return

        self.player_called_shots.append(target)
        player_result = fire_at(target, self.enemy_board)

        target_row = target[0]
        target_col = int(target[1])
        if player_result == 'hit':
            self.enemy_mask[target_row][target_col] = '+'
            self.last_status_message = f"You hit {target}!"
            self.txo.priont_string(f"You hit {target}!")
        elif player_result == 'miss':
            self.enemy_mask[target_row][target_col] = '-'
            self.last_status_message = f"You missed {target}."
            self.txo.priont_string(f"You missed {target}.")
        else:
            self.txo.priont_string(f"You already targeted {target}.")
            return

        if not board_has_ships(self.enemy_board):
            self.player_win()
            self.show_game(None)
            return

        enemy_call = self.get_enemy_call()
        enemy_result = fire_at(enemy_call, self.player_board)
        if enemy_result == 'hit':
            self.last_status_message = f"You fired at {target}; enemy hit {enemy_call}"
            self.txo.priont_string(f"The enemy hit your ship at {enemy_call}")
        else:
            self.last_status_message = f"You fired at {target}; enemy missed {enemy_call}"
            self.txo.priont_string(f"The enemy missed at {enemy_call}")

        if not board_has_ships(self.player_board):
            self.enemy_win()

        self.show_game()

    def load_available_boards(self) -> dict:
        if not os.path.exists(BOARD_FILE):
            return {}
        with open(BOARD_FILE, 'r', encoding='utf-8') as board_json:
            boards = json.load(board_json)

        valid_boards = {}
        for board_name, board_data in boards.items():
            try:
                valid_boards[board_name] = self.normalize_board(board_data)
            except (KeyError, IndexError, ValueError):
                continue
        return valid_boards

    def board_from_name(self, board_name: str) -> Dict[str, list]:
        if board_name not in self.available_boards:
            raise ValueError(f"Board '{board_name}' not found.")
        return clone_board(self.available_boards[board_name])

    @staticmethod
    def normalize_board(board_data: dict) -> Dict[str, list]:
        if isinstance(board_data, dict):
            normalized = {}
            for letter in BOARD_LETTERS:
                row = board_data[letter]
                if len(row) != 10:
                    raise ValueError(f"Invalid board data for letter {letter}. Expected 10 characters, got {len(row)}")
                normalized[letter] = list(row)
            return normalized
        if isinstance(board_data, list):
            if len(board_data) != 10:
                raise ValueError(
                    f"Invalid board data format. Expected a dictionary with 10 keys, got {len(board_data)} keys."
                )
            normalized = {}
            for index, letter in enumerate(BOARD_LETTERS):
                row = board_data[index]
                if len(row) != 10:
                    raise ValueError(f"Invalid board data for letter {letter}. Expected 10 characters, got {len(row)}")
                normalized[letter] = list(row)
            return normalized
        raise ValueError("Invalid board data format. Expected a dictionary.")
