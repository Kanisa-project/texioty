from gaims.base_gaim import BaseGaim
from settings import themery as t
import random
import json

INSTRUCTIONS = {'objective': 'Main point of this game is to buy candy cheap and sell it expensive.',
                     'controls': 'You\'ll have an inventory to manage, along with money.',
                     'scoring': 'Different locations have different candies available at different prices.'}
BUY_WIDTH = 25
PLAYER_CHOICES = ["move", "buy", "sell", "save"]
USER_CHOICES = ["new game", "load game", "settings", "exit"]
LOCATIONS = {
        'laundromat': {
            'price_mod': 3,
            'amount_mod': 8},
        'library': {
            'price_mod': 7,
            'amount_mod': 5},
        'park': {
            'price_mod': 2,
            'amount_mod': 9},
        'theater': {
            'price_mod': 6,
            'amount_mod': 4},
        'casino': {
            'price_mod': 8,
            'amount_mod': 7},
        'arcade': {
            'price_mod': 4,
            'amount_mod': 3}}
CANDIES = {
    "skittle": {'price_range': (1, 3), "inventory_range": (6, 9)},
    "dumdum": {'price_range': (2, 4), "inventory_range": (4, 7)},
    "gumdrop": {'price_range': (3, 6), "inventory_range": (3, 6)},
    "butterscotch": {'price_range': (6, 8), "inventory_range": (2, 3)}
    }

title_msg = "A game where you can buy and sell candy all around town."

class CandySlingerRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "CandySlinger")
        self.gaim_commands["move"] = [self.move_location, "Move to a new location in the city.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["buy"] = [self.buy_candy, "Buy some candy from your location.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["sell"] = [self.sell_candy, "Sell some candy where you are.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]
        self.player = Player(self.txo.master.active_profile.username)
        self.world = World(self.player)

    def new_game(self):
        super().new_game()
        self.welcome_message([])
        self.display_player_invo()


    def load_game(self):
        self.game_state = super().load_game()
        self.player = Player(self.game_state['player_name'])
        self.player.money = self.game_state['money']
        self.player.inventory = self.game_state['inventory']
        self.player.location = self.game_state['location']
        self.world = World(self.player)
        self.welcome_message([])
        self.display_player_invo()

    def save_game(self):
        self.game_state = {
            'player_name': self.txo.master.active_profile.username,
            'money': self.player.money,
            'inventory': self.player.inventory,
            'location': self.player.location
        }
        super().save_game()

    def move_location(self, *args):
        self.world.update_new_location(args[0])
        self.welcome_message([])
        self.display_player_invo()

    def buy_candy(self, *args):
        if self.world.buying_prices[args[1]][1] < int(args[0]):
            self.txo.priont_string(f"Sorry, but there's not enough {args[1]} to buy.")
            return
        if self.player.buy_candy(candy=args[1],
                              purchase_amt=int(args[0]),
                              candy_price_ea=self.world.buying_prices[args[1]][0]):
            self.world.buying_prices[args[1]][1] -= int(args[0])
        self.welcome_message([])
        self.display_player_invo()

    def sell_candy(self, *args):
        if self.world.selling_prices[args[1]][1] < int(args[0]):
            self.txo.priont_string(f"Sorry, but you don't have enough {args[1]} to sell.")
            return
        if self.player.sell_candy(candy=args[1],
                               sale_amt=int(args[0]),
                               candy_price_ea=self.world.selling_prices[args[1]][0]):
            self.world.buying_prices[args[1]][1] += int(args[0])
        self.welcome_message([])
        self.display_player_invo()

    def display_player_invo(self):
        invo_cash_line = f" Inventory: ────────────────────── ${self.player.money} "
        self.txo.priont_string(f"╔{invo_cash_line}╗")
        self.txo.priont_string(f"║{' '*len(invo_cash_line)}║")
        for candy in list(self.player.inventory.keys()):
            selling_price = self.world.selling_prices[candy][0]
            sell_avail = f"{self.player.inventory[candy]['inventory']}x"
            sell_price = f"${selling_price}"
            candy_line = f"{sell_avail} {candy.title()} {'┄'*(len(invo_cash_line)-len(candy)-len(sell_price)-len(sell_avail)-3)} {sell_price}"
            self.txo.priont_string(f"║{candy_line}{' '*(len(invo_cash_line)-len(candy_line))}║")
        self.txo.priont_string(f"╚{'═'*(len(invo_cash_line))}╝\n\n")
        self.display_loca(len(invo_cash_line))

    def display_loca(self, invo_width: int):
        location_line = f"{'─'*(invo_width-len(self.player.location)-11)} Location: {self.player.location.title()}"
        self.txo.priont_string(f"╭{location_line}╮")
        self.txo.priont_string(f"│{' '*len(location_line)}╽")
        for candy in list(CANDIES.keys()):
            buy_price = f'${self.world.buying_prices[candy][0]}'
            buy_avail = f'{self.world.buying_prices[candy][1]}x'
            candy_buy_line = f"{buy_avail} {candy.title()} {'┄'*(invo_width-len(candy)-len(buy_price)-len(buy_avail)-3)} {buy_price}"
            self.txo.priont_string(f"│{candy_buy_line}{' '*(len(location_line)-len(candy_buy_line))}║")
        self.txo.priont_string(f"╘{'═'*(len(location_line))}╝\n")

    def welcome_message(self, welcoming_msgs):
        super().welcome_message([])
        self.txo.priont_string("")
        self.txo.priont_string("Candy Slinger is as simple as the market should be.")
        self.txo.priont_string("Buy what you can low, sell what you have high.")
        self.txo.priont_string("Move around town to get the best prices.")
        self.txo.priont_string("")

class Player:
    def __init__(self, player_name):
        """
        Player class for storing player data and performing transactions.
        """
        self.money = 500
        self.inventory = {}
        self.player_name = player_name
        for candy in list(CANDIES.keys()):
            self.inventory[candy] = {}
            self.inventory[candy]['inventory'] = random.randint(0, 2) * random.randint(CANDIES[candy]['inventory_range'][0], CANDIES[candy]['inventory_range'][1])
            self.inventory[candy]['last_price'] = 1
        self.location = random.choice(list(LOCATIONS.keys()))
        self.data = {
            "player_name": self.player_name,
            "money": self.money,
            "inventory": self.inventory,
            "location": self.location
        }

    def buy_candy(self, candy: str, purchase_amt: int, candy_price_ea: int) -> bool:
        if self.money >= purchase_amt * candy_price_ea:
            self.inventory[candy]['inventory'] += purchase_amt
            self.inventory[candy]['last_price'] = candy_price_ea
            self.money -= purchase_amt * candy_price_ea
            return True
        return False

    def sell_candy(self, candy: str, sale_amt: int, candy_price_ea: int) -> bool:
        if self.inventory[candy]['inventory'] >= sale_amt:
            self.inventory[candy]['inventory'] -= sale_amt
            self.money += sale_amt * candy_price_ea
            return True
        return False


class World:
    def __init__(self, player):
        self.player = player
        self.selling_prices = {}
        self.buying_prices = {}
        self.player_location = player.location
        self.new_buying_prices()
        self.new_selling_prices()

    def new_selling_prices(self):
        self.selling_prices = {}
        price_mod = LOCATIONS[self.player_location]['price_mod']
        for candy in list(CANDIES.keys()):
            cndy_price_range = CANDIES[candy]['price_range']
            cndy_price = random.randint(cndy_price_range[0] * price_mod, cndy_price_range[1] * price_mod)
            avail_amnt = self.player.inventory[candy]['inventory']
            self.selling_prices[candy] = [cndy_price, avail_amnt]

    def new_buying_prices(self):
        self.buying_prices = {}
        price_mod = LOCATIONS[self.player_location]['price_mod']
        avail_mod = LOCATIONS[self.player_location]['amount_mod']
        for candy in list(CANDIES.keys()):
            cndy_price_range = CANDIES[candy]['price_range']
            cndy_avail_range = CANDIES[candy]['inventory_range']
            cndy_price = random.randint(cndy_price_range[0] * price_mod, cndy_price_range[1] * price_mod)
            avail_amnt = random.randint(cndy_avail_range[0] * avail_mod, cndy_avail_range[1] * avail_mod)
            self.buying_prices[candy] = [cndy_price, avail_amnt]

    def gather_selling_choice(self):
        candy_sold = input(" -Whater ye sellin? ")
        while candy_sold not in list(self.selling_prices.keys()):
            if candy_sold == 'nvm':
                return ''
            candy_sold = input("'nvm' to exit or type a candy to sell: ")
        if candy_sold in list(CANDIES.keys()):
            return candy_sold
        return None

    def gather_buying_choice(self):
        candy_bought = input(" -Wutar ya buyin? ")
        while candy_bought not in list(self.buying_prices.keys()):
            if candy_bought == 'nvm':
                return ""
            candy_bought = input("'nvm' to exit or type a candy to buy: ")
        if candy_bought in list(CANDIES.keys()):
            return candy_bought
        return None

    def player_move_location(self):
        for i, location in enumerate(LOCATIONS):
            if location == self.player_location:
                print(f" -{location}")
            else:
                print(f"{location}")
        new_location = input("Where ya movin to? ")
        while new_location not in LOCATIONS:
            new_location = input("Type where you're going: ")
        if new_location in LOCATIONS:
            self.player_location = new_location
            return new_location
        else:
            self.player_location = "park"
            return "park"

    def update_new_location(self, new_location):
        self.player_location = new_location
        self.player.location = new_location
        self.new_buying_prices()
        self.new_selling_prices()

    def save_progress(self, player_data):
        json_object = json.dumps(player_data, indent=4)
        with open(f"{self.player.player_name}.json", "w") as saved_json:
            saved_json.write(json_object)

    def load_player(self, player_data):
        yesorno_load = input(f"Load {player_data['player_name']} with ${player_data['money']}, at {player_data['location']} (y/n)? ")
        if yesorno_load.startswith("y"):
            self.player.player_name = player_data['player_name']
            self.player.money = player_data['money']
            self.player.inventory = player_data['inventory']
            self.player.location = player_data['location']
        else:
            return
