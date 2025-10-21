from gaims.base_gaim import BaseGaim
from settings import themery as t
import random
import json

yakima_to_boston = 2955 #miles
POSSIBLE_STATUS = ["healthy", "hungry", "thirsty", "sick", "tired"]
HUNTABLE_ANIMALS = ["deer", "buffalo", "raccoon", "rabbit", "grizzly"]
GATHERABLE_ITEMS = {"herb": ['medicinal', 'tea', 'poisonous'],
                    "fruit": ['grape', 'apple', 'pear'],
                    "vegetable": ['carrot', 'onion', 'potato'],
                    "mushroom": ['energetic', 'poisonous', 'medicinal']}

OCCUPATIONS = ["doctor", "hunter", "explorer"]

first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen"
]
last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
    "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
    "Moore", "Martin", "Jackson", "Thompson", "White"
]

class HuntableAnimal:
    def __init__(self, name: str):
        self.name = name
        food_weight = random.randint(1, 5)
        pelt = "small"
        match name:
            case "deer":
                food_weight = random.randint(5, 10)
                pelt = "medium"
            case "buffalo":
                food_weight = random.randint(12, 18)
                pelt = "large"
            case "racoon":
                food_weight = random.randint(2, 4)
                pelt = "small"
            case "rabbit":
                food_weight = random.randint(1, 3)
                pelt = "small"
            case "grizzly":
                food_weight = random.randint(8, 11)
                pelt = "large"
        self.food_weight = food_weight
        self.pelt_size = pelt + " pelt"

class PartyMember:
    def __init__(self, name, age, occupation, status, hunger, thirst):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.status = status
        self.hunger_level = hunger
        self.thirst_level = thirst

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "status": self.status,
            "hunger_level": self.hunger_level,
            "thirst_level": self.thirst_level
        }

    def travel_action(self, traveling_dist: int):
        self.thirst_level += (self.age + random.randint(1, traveling_dist)) // 10
        self.hunger_level += (self.age + random.randint(1, traveling_dist)) // 10
        if self.thirst_level >= 60 >= self.hunger_level:
            self.status = "thirsty"
            if self.thirst_level >= 99:
                self.status = "sick"
        elif self.hunger_level >= 60 >= self.thirst_level:
            self.status = "hungry"
            if self.hunger_level >= 99:
                self.status = "sick"
        elif self.thirst_level >= 60 and self.hunger_level >= 60:
            self.status = "sick"
            if self.hunger_level >= 99 or self.thirst_level >= 99:
                self.status = "dead"
        else:
            self.status = "healthy"

    def rest_action(self):
        self.hunger_level -= random.randint(1, 3)
        self.thirst_level -= random.randint(1, 3)
        if self.hunger_level < 0:
            self.hunger_level = 0
        if self.thirst_level < 0:
            self.thirst_level = 0

class BostonTrail(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "BostonTrail")
        self.miles_traveled = 0
        self.hours_traveled = 0
        self.food_amount = 25
        self.water_amount = 25
        self.party_members = []
        self.party_inventory = []
        self.gaim_commands["travel"] = [self.travel_farther, "Travel farther, possibly encounter an event.",
                                        {'distance': 'How many miles to travel.'}, "BTRL", t.rgb_to_hex(t.CONTINENTAL_BLUE), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["hunt"] = [self.animal_hunt, "Hunt animals, possibly encounter an event.",
                                      {'animal': 'Animal for hunting.'}, "BTRL", t.rgb_to_hex(t.CONTINENTAL_BLUE), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["gather"] = [self.gather_stuff, "Gather things, possibly encounter an event.",
                                        {'item': 'Item to search and gather.'}, "BTRL", t.rgb_to_hex(t.CONTINENTAL_BLUE), t.rgb_to_hex(t.BLACK)]
        self.gaim_commands["rest"] = [self.party_rest, "Allow the party to rest/eat.",
                                      {'time': 'Length of time to rest.'}, "BTRL", t.rgb_to_hex(t.CONTINENTAL_BLUE), t.rgb_to_hex(t.BLACK)]

    def new_game(self):
        super().new_game()
        self.welcome_message([])
        self.party_members = []
        for i in range(4):
            self.party_members.append(PartyMember(random.choice(first_names) + " " + random.choice(last_names),
                                                  random.randint(18, 35),
                                                  random.choice(OCCUPATIONS),
                                                  "healthy", 0, 0))
        self.display_party_members()

    def welcome_message(self, welcoming_msgs):
        self.clear_texoty()
        self.display_party_members()
        self.display_inventory_distance()

    def display_help_message(self):
        self.clear_texoty()
        self.txo.priont_string("Type 'travel <distance>' to travel further, where <distance> is a number of miles.\n")
        self.txo.priont_string("Type 'hunt <animal>' to hunt an animal.")
        self.txo.priont_list(HUNTABLE_ANIMALS, parent_key='  Replace <animal> with one of the following:')
        self.txo.priont_string("\nType 'gather <category>' to gather an item.\n")
        self.txo.priont_list(['herb', 'fruit', 'vegetable', 'mushroom'], parent_key="  Replace <category> with one of the following:")

    def load_game(self):
        self.game_state = super().load_game()
        print(self.game_state)
        self.miles_traveled = self.game_state["distance_traveled"]
        self.hours_traveled = self.game_state["hours_traveled"]
        self.food_amount = self.game_state["food_amount"]
        self.party_members = []
        for member in list(self.game_state["party_members"].values()):
            self.party_members.append(PartyMember(
                member["name"], member["age"], member["occupation"],
                member["status"], member["hunger_level"], member["thirst_level"]
            ))
        self.party_inventory = self.game_state["party_inventory"]
        self.welcome_message([])

    def party_members_to_dicts(self) -> dict:
        dict_members = {}
        for member in self.party_members:
            dict_members[member.name] = member.to_dict()
        return dict_members

    def display_party_members(self):
        for member in self.party_members:
            self.txo.priont_string(f"{member.occupation.title()} {member.name} is {member.status}")
            self.txo.priont_string(f"          Thirst: {member.thirst_level} | Hunger: {member.hunger_level}")

    def save_game(self):
        self.game_state = {
            "player_name": self.txo.master.active_profile.username,
            'distance_traveled': self.miles_traveled,
            'hours_traveled': self.hours_traveled,
            'food_amount': self.food_amount,
            'party_members': self.party_members_to_dicts(),
            'party_inventory': self.party_inventory
        }
        super().save_game()

    def travel_farther(self, travel_dist):
        try:
            travel_dist = int(travel_dist)
        except ValueError:
            self.txo.priont_string("Please enter a number.")
            return
        self.miles_traveled += int(travel_dist)
        hours_spent = round(int(travel_dist) / 3, 1)  # HUMANS WALK ~3 MILES PER HOUR
        self.hours_traveled += hours_spent
        for member in self.party_members:
            member.travel_action(travel_dist)
        self.txo.priont_string(f"You have traveled another {travel_dist} miles in {hours_spent} hours.")
        self.txo.priont_string(f"       For a total of {self.miles_traveled} miles in {self.hours_traveled} hours.")
        if self.miles_traveled >= yakima_to_boston:
            self.txo.priont_string("You have reached Boston!")

    def animal_hunt(self, hunting: str):
        animal_found = HuntableAnimal(random.choice(HUNTABLE_ANIMALS))
        if hunting == animal_found.name:
            self.food_amount += animal_found.food_weight
            self.party_inventory.append(animal_found.pelt_size)
            self.txo.priont_string(f"FOUND the {hunting}! gained {animal_found.food_weight} pounds of food and a {animal_found.pelt_size} pelt.")
        else:
            self.txo.priont_string(f"NOPE! The {hunting} was not found.")

    def gather_stuff(self, gatherable: str):
        time_spent = round(random.randint(1, 3) + random.random(), 1)
        self.txo.priont_string(f"Attempting to gather a {gatherable}.")
        if gatherable in list(GATHERABLE_ITEMS.keys()):
            found_gath = random.choice(GATHERABLE_ITEMS[gatherable])
            if gatherable == "herb" or gatherable == "mushroom":
                found_gath += f" {gatherable}"
            self.txo.priont_string(f"Found {found_gath} in {time_spent} hours.")
            self.party_inventory.append(found_gath)
        else:
            self.txo.priont_string(f"No {gatherable} found, {time_spent} hours wasted.")
        self.hours_traveled += time_spent

    def positive_event(self, triggering_action: str):
        match triggering_action:
            case "travel":
                self.txo.priont_string(f"You have traveled further.")
            case "hunt":
                self.txo.priont_string(f"While hunting, you found some helpful items.")
            case "gather":
                self.txo.priont_string(f"You have gathered something.")

    def negative_event(self):
        pass

    def display_inventory_distance(self):
        self.txo.priont_list(self.party_inventory, parent_key="Inventory:")
        self.txo.priont_string(
            f"You have {self.food_amount} pounds of food and {self.water_amount} gallons of water."
        )
        self.txo.priont_string(f"You have traveled {self.miles_traveled} miles in {self.hours_traveled} hours.")

    def party_rest(self):
        for member in self.party_members:
            member.rest_action()