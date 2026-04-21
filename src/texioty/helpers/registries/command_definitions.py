from typing import Dict, Any, Callable
from src.texioty.settings import themery as t, utils as u

TEXIOTY_COMMANDS: Dict[str, Dict[str, Any]] = {
    "welcome": {
        'name': 'welcome',
        'usage': '"welcome"',
        'call_func': None,
        'lite_desc': 'Displays a welcoming message.',
        'full_desc': ['Displays a welcoming message with a few commands to get started.',
                      'Available at any point using the system.'],
        'possible_args': {},
        'args_desc': {},
        'examples': ['welcome'],
        'group_tag': 'HLPR',
        'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
        'back_color': u.rgb_to_hex(t.BLACK)
        },
        "commands": {
            'name': 'commands',
            'usage': '"commands"',
            'call_func': None,
            'lite_desc': 'Displays available commands.',
            'full_desc': ['Displays all commands available to use in the active Texioty mode.',
                          'Available at any point using the system.'],
            'possible_args': {},
            'args_desc': {},
            'examples': ['commands'],
            'group_tag': 'HLPR',
            'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
            'back_color': u.rgb_to_hex(t.BLACK)
        },
        "help": {
            'name': 'help',
            'usage': '"help (GROUP_TAG/COMMAND_NAME)"',
            'call_func': None,
            'lite_desc': 'Displays a helpful message.',
            'full_desc': ['Displays some helpful tips and info based on the active Texioty mode.',
                          'Available at any point using the system.'],
            'possible_args': {'(GROUP_TAG)': None,
                              '(COMMAND_NAME)': None},
            'args_desc': {'(GROUP_TAG)': ['Group tag for getting help with.', str],
                          '(COMMAND_NAME)': ['Name of the command to get help with.', str]},
            'examples': ['help help', 'help', 'help HLPR', 'help commands'],
            'group_tag': 'HLPR',
            'font_color': u.rgb_to_hex(t.GREEN_YELLOW),
            'back_color': u.rgb_to_hex(t.BLACK)
        }
    }

DIRY_COMMANDS: Dict[str, Dict[str, Any]] = {
    "dear_sys,":{
        "name": "dear_sys,",
        "usage": '"dear_sys,"',
        "call_func": None,
        "lite_desc": "Starts a diary entry.",
        "full_desc": ["Starts a diary entry.",
                      "Can only be used in Texioty mode."],
        "possible_args": {},
        "args_desc": {},
        'examples': ['dear_sys,'],
        "group_tag": "DIRY",
        "font_color": u.rgb_to_hex(t.VIOLET_RED),
        "back_color": u.rgb_to_hex(t.BLACK)
    },
    "/until_next_time": {
        "name": "/until_next_time",
        "usage": '"/until_next_time"',
        "call_func": None,
        "lite_desc": "Ends a diary entry.",
        "full_desc": ["Ends a diary entry.",
                      "Can only be used inside of Digiary mode."],
        "possible_args": {},
        "args_desc": {},
        'examples': ['/until_next_time'],
        "group_tag": "DIRY",
        "font_color": u.rgb_to_hex(t.VIOLET_RED),
        "back_color": u.rgb_to_hex(t.BLACK)
    },
    "redear": {
        "name": "redear",
        "usage": '"redear"',
        "call_func": None,
        "lite_desc": "Select a date to read through.",
        "full_desc": ["Select a date to read through.",
                      "Can only be used in Texioty mode."],
        "possible_args": {},
        "args_desc": {},
        'examples': ['redear'],
        "group_tag": "DIRY",
        "font_color": u.rgb_to_hex(t.VIOLET_RED),
        "back_color": u.rgb_to_hex(t.BLACK)
    }
}

PROMPT_COMMANDS: Dict[str, Dict[str, Any]] = {
    "tcg_lab": {
        "name": "tcg_lab",
        "usage": '"tcg_lab"',
        "call_func": None,
        "lite_desc": "Enter the TCG lab.",
        "full_desc": ["Entering the TCG lab allows a person to make card game stuff.",
                      "Randomized decks, abstract art and word games from cards."],
        "possible_args": {},
        "args_desc": {},
        "examples": ['tcg_lab'],
        "group_tag": "PRUN",
        "font_color": u.rgb_to_hex(t.KHAKI),
        "back_color": u.rgb_to_hex(t.BLACK)
    },
    "foto_worx": {
        "name": "foto_worx",
        "usage": '"foto_worx"',
        "call_func": None,
        "lite_desc": "Work in the foto hop.",
        "full_desc": ["Designed after restaurant equipment, it manipulates fotoes.",],
        "possible_args": {},
        "args_desc": {},
        "examples": ['foto_worx'],
        "group_tag": "PRUN",
        "font_color": u.rgb_to_hex(t.KHAKI),
        "back_color": u.rgb_to_hex(t.BLACK)
    },
    "profile_make": {
        "name": "profile_make",
        "usage": '"profile_make"',
        "call_func": None,
        "lite_desc": "Make some type of profile.",
        "full_desc": ["Make some type of profile.",],
        "possible_args": {},
        "args_desc": {},
        "examples": ['profile_make'],
        "group_tag": "PRUN",
        "font_color": u.rgb_to_hex(t.KHAKI),
        "back_color": u.rgb_to_hex(t.BLACK)
    }
}

PIJUN_COMMANDS: Dict[str, Dict[str, Any]] = {
    'send': {
        'name': 'send',
        'usage': '"send (MESSAGE) (HOST) (PORT)"',
        'call_func': None,
        'lite_desc': 'Sends a message to a host.',
        'full_desc': ['Sends a message to a host.',
                      'Available at any point using the system.'],
        'possible_args': {},
        'args_desc': {'(MESSAGE)': ['The message to send.', str],
                      '(HOST)': ['The host to send the message to.', str],
                      '(PORT)': ['The port to send the message to.', int]},
        'examples': ['send "Hello, world!" 7.41.241.42 8080',
                     'send "Hello, dovecot!" 192.168.1.10 9000'],
        'group_tag': 'PIJN',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    },
    'deliver': {
        'name': 'deliver',
        'usage': '"deliver [GAME_DATA] [HOST] [PORT]"',
        'call_func': None,
        'lite_desc': 'Deliver game data to a host.',
        'full_desc': ['Deliver game data to a host.'],
        'possible_args': {},
        'args_desc': {'[GAME_DATA]': 'The game data to deliver.',
                      '(HOST)': 'The host to deliver the game to.',
                      '(PORT)': 'The port to deliver the game to.'},
        'examples': ['deliver \'{"player": "Bluebeard", "score": 420}\' 7.41.241.42 8080'],
        'group_tag': 'PIJN',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    },
    'enter': {
        'name': 'enter',
        'usage': '"enter (HOST) (PORT)"',
        'call_func': None,
        'lite_desc': 'Enter a coop server.',
        'full_desc': ['Enter a coop server. This will allow you to play with other pijuns in the same server.',
                      'Available at any point using the system.'],
        'possible_args': {},
        'args_desc': {'(HOST)': ['The host IP to enter.', str],
                      '(PORT)': ['The port to enter.', int]},
        'examples': ['enter 7.41.241.42 8080',
                     'enter 192.168.1.10 9000'],
        'group_tag': 'PIJN',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    },
    'leave': {
        'name': 'leave',
        'usage': '"leave [HOST] [PORT]"',
        'call_func': None,
        'lite_desc': 'Leave a coop server.',
        'full_desc': ['Leave the server coop.'],
        'possible_args': {},
        'args_desc': {'(HOST)': 'The host to deliver the game to.',
                      '(PORT)': 'The port to deliver the game to.'},
        'examples': ['leave 7.41.241.42 8080'],
        'group_tag': 'PIJN',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    }
}

DOVECOT_COMMANDS= {
    'coop': {
        'name': 'coop',
        'usage': '"coop [dovecot_num] (game_engine)"',
        'call_func': None,
        'lite_desc': 'Host a coop with a dovecote id',
        'full_desc': ['Host a coop with a dovecote id. If no game engine is specified, it will default to messaging board.'],
        'possible_args': {},
        'args_desc': {'[dovecot_num]': ['The dovecot number to host 0-255.', int],
                      '(game_engine)': ['The game engine to use.', str]},
        'examples': ['coop 124', 'coop 124 slinger'],
        'group_tag': 'DOVE',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    },
    'decoop': {
        'name': 'decoop',
        'usage': '"decoop [dovecot_num]"',
        'call_func': None,
        'lite_desc': 'Take down a hosted coop',
        'full_desc': ['Take down the hosted coop number.'],
        'possible_args': {},
        'args_desc': {'[dovecot_num]': ['The dovecot number to take down 0-255.', int],
                      '(game_engine)': ['The game engine to use.', str]},
        'examples': ['decoop 124', 'decoop 124 slinger'],
        'group_tag': 'DOVE',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)
    },
    'message': {
        'name': 'message',
        'usage': '"message [TEXT]"',
        'call_func': None,
        'lite_desc': 'Send a message to all pijuns.',
        'full_desc': ['Send a message to all pijuns.'],
        'possible_args': {},
        'args_desc': {'[TEXT]': 'The text to send to all pijuns.'},
        'examples': ['message "Hello, world!"'],
        'group_tag': 'DOVE',
        'font_color': u.rgb_to_hex(t.PIGEON_GREY),
        'back_color': u.rgb_to_hex(t.BLACK)

    }
}


HANGMAN_COMMANDS: Dict[str, Dict[str, Any]] = {
    "guess": {
        "name": "guess",
        "usage": "guess [LETTER]",
        "call_func": None,
        "lite_desc": "Guess a single letter.",
        "full_desc": ["Guess a single letter."],
        "possible_args": {},
        "args_desc": {
            '[LETTER]': 'A letter of the alphabet.'
        },
        "group_tag": "HMAN",
        "examples": ["guess a", 'guess e', 'guess h', 'guess y'],
        "font_color": t.rgb_to_hex(t.MUSTARD_YELLOW),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "solve": {
        "name": "solve",
        "usage": "solve [PHRASE]",
        "call_func": None,
        "lite_desc": "Guess the entire phrase.",
        "full_desc": ["Guess the entire phrase."],
        "possible_args": {'unknown': 'too many possibilities'},
        "args_desc": {
            '[PHRASE]': 'The exact phrase of what you think it says.'
        },
        "group_tag": "HMAN",
        "examples": ['solve this is the puzzle'],
        "font_color": t.rgb_to_hex(t.MUSTARD_YELLOW),
        "back_color": t.rgb_to_hex(t.BLACK)
    }
}

BATTLESHIP_COMMANDS: Dict[str, Dict[str, Any]] = {
    "show" : {
        "name": "show",
        "usage": "'show'",
        "call_func": None,
        "lite_desc": "Show the current game.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["show"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "fire" : {
        "name": "fire",
        "usage": "'fire [COORD]'",
        "call_func": None,
        "lite_desc": "Fire a shot at a location.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["fire A2"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "boards" : {
        "name": "boards",
        "usage": "'boards'",
        "call_func": None,
        "lite_desc": "List available saved boards.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["boards"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "use" : {
        "name": "use",
        "usage": "'use [PLAYER_BOARD] (ENEMY_BOARD)'",
        "call_func": None,
        "lite_desc": "Fire a shot at a location.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["use alpha", "use echo romeo"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "build": {
        "name": "build",
        "usage": "'build [BOARD_NAME]'",
        "call_func": None,
        "lite_desc": "Build a board for battleship.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {
            "[BOARD_NAME]": ["Name of the board to create", str]
        },
        "examples": ["build alpha"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "place": {
        "name": "place",
        "usage": "'place [COORDS] [DIRECTION] [LENGTH]'",
        "call_func": None,
        "lite_desc": "Place a ship while building a board.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {
            "[COORDS]": ["Starting place of ship.", str],
            "[DIRECTION]": ["Direction of ship 'n', 's', 'e', 'w'.", str],
            "[LENGTH]": ["Length of ship to place.", int]
        },
        "examples": ["place D3 h 3", "place C4 v 4"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "showbuild": {
        "name": "showbuild",
        "usage": "'showbuild'",
        "call_func": None,
        "lite_desc": "Show the current placed ships being built.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["showbuild"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "clearbuild": {
        "name": "clearbuild",
        "usage": "'clearbuild'",
        "call_func": None,
        "lite_desc": "Clear the current board being built.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["clearbuild"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    },
    "saveboard": {
        "name": "saveboard",
        "usage": "'saveboard'",
        "call_func": None,
        "lite_desc": "Save the current board being built.",
        "full_desc": [],
        "possible_args": {},
        "args_desc": {},
        "examples": ["saveboard alpha"],
        "group_tag": "BTSH",
        "font_color": t.rgb_to_hex(t.LIGHT_SEA_GREEN),
        "back_color": t.rgb_to_hex(t.BLACK)
    }

}

def bind_commands(command_dict: Dict[str, Dict[str, Any]],
                  binding_map: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    for command_name, command_info in command_dict.items():
        if command_name in binding_map:
            if isinstance(binding_map[command_name], dict):
                for key, value in binding_map[command_name].items():
                    command_info[key] = value
            else:
                command_info['call_func'] = binding_map[command_name]
    return command_dict

def merge_command_groups(*command_dicts: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    merged_dict = {}
    for command_dict in command_dicts:
        merged_dict.update(command_dict)
    return merged_dict

