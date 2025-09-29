from gaims.base_gaim import BaseGaim
import theme as t
import random
import json
import os

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
        'casino': [],
        'arcade': []}
CANDIES = {
    "skittle": {'price_range': (1, 3), "inventory_range": (6, 9)},
    "dumdum": {'price_range': (2, 4), "inventory_range": (4, 7)},
    "gumdrop": {'price_range': (3, 6), "inventory_range": (3, 6)},
    "butterscotch": {'price_range': (6, 8), "inventory_range": (2, 3)}
    }

title_msg = "A game where you can buy and sell candy all around town."


def gather_candy_amount(buyorsell) -> int:
    return int(input(f"How many to {buyorsell}? "))

class CandySlingerRunner(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "Candy Slinger")
        self.gaim_commands["move"] = [self.move_location, "Move to a new location in the city.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["buy"] = [self.buy_candy, "Buy some candy from your location.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["sell"] = [self.sell_candy, "Sell some candy where you are.",
                                       {}, "CNDY", t.rgb_to_hex(t.LIGHT_SEA_GREEN), t.rgb_to_hex(t.BLACK)]

    def new_game(self, args):
        super().new_game(args)
        self.texioty_commands = self.gaim_commands
        self.txo.master.add_command_dict(self.texioty_commands)

    def move_location(self, args):
        pass

    def buy_candy(self, args):
        pass

    def sell_candy(self, args):
        pass


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
            "location": self.location}

    def buy_candy(self, candy: str, purchase_amt: int, candy_price_ea: int):
        if self.money >= purchase_amt * candy_price_ea:
            self.inventory[candy]['inventory'] += purchase_amt
            self.inventory[candy]['last_price'] = candy_price_ea
            self.money -= purchase_amt * candy_price_ea

    def sell_candy(self, candy: str, sale_amt: int, candy_price_ea: int):
        if self.inventory[candy]['inventory'] >= sale_amt:
            self.inventory[candy]['inventory'] -= sale_amt
            self.money += sale_amt * candy_price_ea


def new_gaim(player_name) -> Player:
    new_player = Player(player_name)
    return new_player


def load_gaim(player_name) -> Player:
    loaded_player = Player(player_name)
    return loaded_player


class World:
    def __init__(self, player):
        self.player = player
        self.selling_prices = {}
        self.buying_prices = {}
        self.player_location = random.choice(list(LOCATIONS.keys()))
        # self.new_buying_prices()
        # self.new_selling_prices()

    def display_player_invo(self):
        invo_cash_line = f" Inventory: ────────────────────── ${self.player.money} "
        print(f"╔{invo_cash_line}╗")
        print(f"║{' '*len(invo_cash_line)}║")
        price_mod = LOCATIONS[self.player.location]['price_mod']
        for candy in list(self.player.inventory.keys()):
            selling_price = self.selling_prices[candy][0]
            sell_avail = f"{self.player.inventory[candy]['inventory']}x"
            sell_price = f"${selling_price}"
            candy_line = f"{sell_avail} {candy.title()} {'┄'*(len(invo_cash_line)-len(candy)-len(sell_price)-len(sell_avail)-3)} {sell_price}"
            print(f"║{candy_line}{' '*(len(invo_cash_line)-len(candy_line))}║")
        print(f"╚{'═'*(len(invo_cash_line))}╝\n")
        return len(invo_cash_line)

    def display_loca(self, invo_width: int):
        location_line = f"{'─'*(invo_width-len(self.player_location)-11)} Location: {self.player_location.title()}"
        print(f"╭{location_line}╮")
        print(f"│{' '*len(location_line)}╽")
        for candy in list(CANDIES.keys()):
            buy_price = f'${self.buying_prices[candy][0]}'
            buy_avail = f'{self.buying_prices[candy][1]}x'
            candy_buy_line = f"{buy_avail} {candy.title()} {'┄'*(invo_width-len(candy)-len(buy_price)-len(buy_avail)-3)} {buy_price}"
            print(f"│{candy_buy_line}{' '*(len(location_line)-len(candy_buy_line))}║")
        print(f"╘{'═'*(len(location_line))}╝\n")

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

    def gather_buying_choice(self):
        candy_bought = input(" -Wutar ya buyin? ")
        while candy_bought not in list(self.buying_prices.keys()):
            if candy_bought == 'nvm':
                return ""
            candy_bought = input("'nvm' to exit or type a candy to buy: ")
        if candy_bought in list(CANDIES.keys()):
            return candy_bought

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



def game_running_loop(player, world):
    running = True
    while running:
        os.system('clear')
        #print(os.get_terminal_size().columns)
        inv_width = world.display_player_invo()
        world.display_loca(inv_width)
        option_line = ' | '.join(PLAYER_CHOICES)
        player_choice = input(f" {option_line} --> ")
        if 'move' in player_choice:
            player.location = world.player_move_location()
            world.update_new_location(player.location)
        elif 'buy' in player_choice:
            print('')
            candy = world.gather_buying_choice()
            if candy == '':
                continue
            purch_amnt = player.gather_candy_amount('buy')
            if purch_amnt <= world.buying_prices[candy][1]:
                player.buy_candy(candy, purch_amnt, world.buying_prices[candy][0])
                world.buying_prices[candy][1] -= purch_amnt
        elif 'sell' in player_choice:
            print('')
            candy = world.gather_selling_choice()
            if candy == '':
                continue
            sale_amnt = player.gather_candy_amount('sell')
            if sale_amnt <= player.inventory[candy]['inventory']:
                player.sell_candy(candy, sale_amnt, world.selling_prices[candy][0])
        elif 'save' in player_choice:
            player_data = {
                "player_name": player.player_name,
                "money": player.money,
                "inventory": player.inventory,
                "location": player.location}
            world.save_progress(player_data)
            running = input("Saved!\n'y' to continue '' to exit: ")
        elif player_choice in '':
            running = False


def print_save_files():
    pass


def load_json_save(player_name):
    pass


def main_menu():
    script_running = True
    while script_running:
        os.system('clear')
        print("Welcome to.....")
        # s.print_block_font('   candy')
        # s.print_block_font('  slinger!')
        print("\n" + title_msg + '\n\n')
        for choice in USER_CHOICES:
            print(f"  {choice.title()}")
        user_input = input("What would you like to do? ")

        if "new" in user_input.lower():
            player_name = input(" -What is your candy dealin' name, partn'r? ")
            player = Player(player_name)
            world = World(player)
            game_running_loop(player, world)
        elif "load" in user_input.lower():
            print_save_files()
            player_name = input("What name are you trying to load, mate? ")
            player = Player(player_name)
            world = World(player)
            player_datadict = load_json_save(player_name)
            if isinstance(player_datadict, dict):
                world.load_player(player_datadict)
            else:
                player_name = input(" -What is your candy dealin' name, partn'r? ")
                player = Player(player_name)
                world = World(player)
                game_running_loop(player, world)

            game_running_loop(player, world)
        elif "exit" in user_input.lower():
            script_running = False

if __name__ == "__main__":
    main_menu()
