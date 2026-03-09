import os
import json
import random
from typing import Dict

player_called_shots = []
enemy_called_shots = []
MENU_OPTIONS = ["Create new board", "Play new game", "Load old game"]
PLAYER_BOARD = {
        "A": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "B": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "C": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "D": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "E": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "F": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "G": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "H": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "I": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "J": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        }
ENEMY_BOARD = {
        "A": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "B": [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' '],
        "C": [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' '],
        "D": [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' '],
        "E": [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '],
        "F": ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "G": ['#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', ' '],
        "H": ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "I": ['#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
        "J": ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        }

SHIP_DIR_DICT = {
        "north": (0, -1),
        "south": (0, 1),
        "east": (1, 0),
        "west": (-1, 0)
        }

          
            
BLANK_BOARD = [
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]



def reset_enemy_mask():
    return {
            "A": BLANK_BOARD[0],
            "B": BLANK_BOARD[1],
            "C": BLANK_BOARD[2],
            "D": BLANK_BOARD[3],
            "E": BLANK_BOARD[4],
            "F": BLANK_BOARD[5],
            "G": BLANK_BOARD[6],
            "H": BLANK_BOARD[7],
            "I": BLANK_BOARD[8],
            "J": BLANK_BOARD[9],
            }


def board_builder() -> dict:
    ship_lengths = [3, 4, 4, 5, 6]
    for ship_len in ship_lengths:
        start_loc, ship_dir = get_ship_start_position(ship_len)
        place_ship(start_loc, ship_len, SHIP_DIR_DICT[ship_dir])
    try:
        with open('boards.json', 'r') as json_file:
            boards = json.load(json_file)
            boards[input("Name the board: ")] = BLANK_BOARD

        with open('boards.json', 'w') as json_file:
            json.dump(boards, json_file, indent=4)
    except IOError as e:
        print("Something fucked up:", e)

def get_ship_start_position(ship_len: int) -> [str, str]:
        start_loc = input(f"Where would you like to place a {ship_len} length ship?  ").upper()
        while len(start_loc) != 2:
            start_loc = input("Start location in the form of: 'a2', 'd7', or 'e4'").upper()
        ship_dir = input("Which direction to face the ship?  ")
        while ship_dir.lower() not in list(SHIP_DIR_DICT.keys()):
            ship_dir = input("Face the ship, north, south, east or west?  ")
        return start_loc, ship_dir

def display_board(board: Dict[str, list]):
    print(' 0123456789')
    for letter in board:
        print(letter + ''.join(board[letter]))

def can_place(place_loc: [int, int]) -> bool:
    if 0 <= place_loc[0] < 10 and 0 <= place_loc[1] < 10:
        if BLANK_BOARD[place_loc[0]][place_loc[1]] == ' ':
            return True
    return False

def place_ship(start_loc: str, ship_length: int, ship_direction: [int, int]):
    """Place a ship at start_loc for the ship_length facing the ship_direction"""
    start_loc = ["ABCDEFGHIJ".index(start_loc[0]), int(start_loc[1])]
    loc = [0, 0]
    for i in range(ship_length):
        loc[0] = start_loc[0] + (ship_direction[1] * i)
        loc[1] = start_loc[1] + (ship_direction[0] * i)
        if can_place(loc):
            BLANK_BOARD[loc[0]][loc[1]] = "#"
        else:
            BLANK_BOARD[loc[0]][loc[1]] = '-'
    for line in BLANK_BOARD:
        print("".join(line))
    input("Press enter...")

def get_enemy_call():
    callout = random.choice("ABCDEFGHIJ") + str(random.randint(0, 9))
    while callout in enemy_called_shots:
        callout = random.choice("ABCDEFGHIJ") + str(random.randint(0, 9))
    enemy_called_shots.append(callout)
    return callout

def get_player_call():
    callout = input("What's your target?  ")
    good_call = check_player_call(callout)
    if good_call:
        return callout.upper()
    while not good_call:
        callout = input("What's the real target?  ")
        good_call = check_player_call(callout)
    return callout.upper()


def check_player_call(callout: str):
    if len(callout) == 2:
        if callout[0].upper() in 'ABCDEFGHIJ':
            if callout[1] in '0123456789':
                return True
    return False

def send_torpedo(board_loc: str, board: Dict[str, list], player_target: str = "enemy"):
    if len(board_loc) == 2:
        if board[board_loc[0]][int(board_loc[1])] == "#":
           board[board_loc[0]][int(board_loc[1])] = "+"
        else:
           board[board_loc[0]][int(board_loc[1])] = "-"

def load_board():
    with open('boards.json', 'r') as board_json:
        boards = json.load(board_json)
        board_choices = list(boards.keys())
        for board_name in board_choices:
            print("- ", board_name)
        board_choice = input("Which board to use?  ")
        chosen_board = boards[board_choice]
        BOARD = {
                "A": chosen_board[0],
                "B": chosen_board[1],
                "C": chosen_board[2],
                "D": chosen_board[3],
                "E": chosen_board[4],
                "F": chosen_board[5],
                "G": chosen_board[6],
                "H": chosen_board[7],
                "I": chosen_board[8],
                "J": chosen_board[9]
                }
    return BOARD

def endgame_check(board: dict):
    for key in board:
        if "#" in board[key]:
            return True
    return False



def welcome_menu():
    print("Welcome to battleship!\nWhat would you like to do:")
    for i, option in enumerate(MENU_OPTIONS):
        print(f"  {i}- {option}")
    menu_choice = input("Type the number of your choice: ")
    while menu_choice not in '012':
        menu_choice = input("Just the number of your choice:  ")
    return MENU_OPTIONS[int(menu_choice)]

class BoardBuilder:
    def __init__(self):
        self.BLANK_ROW = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.current_board = {
                "A": self.BLANK_ROW,
                "B": self.BLANK_ROW,
                "C": self.BLANK_ROW,
                "D": self.BLANK_ROW,
                "E": self.BLANK_ROW,
                "F": self.BLANK_ROW,
                "G": self.BLANK_ROW,
                "H": self.BLANK_ROW,
                "I": self.BLANK_ROW,
                "J": self.BLANK_ROW,
                }
    def display_current_board(self):
        print(" 0123456789")
        for l in 'ABCDEFGHIJ':
            print(f"{l}{''.join(self.current_board[l])}")

    def get_ship_start_pos(self):
        pass

    def can_place(self):
        pass

    def place_ship(self):
        pass

class Battleship:
    def __init__(self):
        self.game_playing = False
        self.BLANK_ROW = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.player_board = {}
        self.enemy_board = {}
        self.enemy_mask = {}

    def new_game(self):
        pass

    def save_game(self):
        pass

    def load_game(self):
        pass

    def player_win(self):
        ready_continue = input("Congratulations! You beat the enemy!")

    def enemy_win(self):
        ready_continue = input("Sorry, the enemy beat the player!")

    def display_enemy_mask(self):
        print(" 0123456789")
        for l in 'ABCDEFGHIJ':
            print(f'{l}{"".join(self.enemy_board[l]).replace("#", " ")}')

    def reset_enemy_mask(self):
        self.enemy_mask = {}
        for l in 'ABCDEFGHIJ':
            self.enemy_mask[l] = self.BLANK_ROW




game_running = True

bs = Battleship()
bb = BoardBuilder()
while game_running:
    os.system('clear')
    match welcome_menu():
        case "Create new board":
            bb.display_current_board()
        case "Play new game":
            bs.player_board = load_board()
            bs.enemy_board = load_board()
            bs.reset_enemy_mask()
            bs.game_playing = True
            while bs.game_playing:
                os.system('clear')
                bs.display_enemy_mask()
                print("\n/\/\/\/\/\/\/\/\n")
                display_board(bs.player_board)
                player_call = get_player_call()
                send_torpedo(player_call, bs.enemy_board)
                enemy_call = get_enemy_call()
                send_torpedo(enemy_call, bs.player_board, "player")
                if not endgame_check(bs.player_board):
                    bs.enemy_win()
                if not endgame_check(bs.enemy_board):
                    bs.player_win()
                bs.game_playing = endgame_check(bs.player_board) and endgame_check(bs.enemy_board)
