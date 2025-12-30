import os
import requests
import random
from dotenv import load_dotenv
# from utils import dbHelper

load_dotenv()


class BaseAPIHelper:
    def __init__(self):
        self.base_url = 'https://api.api-ninjas.com'
        self.previous_endpoint = ''
        self.endpoint_names = {
            'Quote': ['/v2/quotes', '/v2/randomquotes', '/v2/quoteoftheday'],
            'Animal': ['/v1/animals'],
            'Fact': ['/v1/facts', '/v1/factoftheday'],
            'Joke': ['/v1/jokes', '/v1/jokeoftheday']
        }
        self.headers = {
            'X-Api-Key': os.getenv('API_NINJAS'),
        }

    def endpoint_builder(self, endpoint_name: str, url_ending: str):
        self.previous_endpoint = f'{self.base_url}{endpoint_name}{url_ending}'
        return self.previous_endpoint

if __name__ == "__main__":
    based_helper = BaseAPIHelper()
    rand_endpoint = random.choice(list(based_helper.endpoint_names.keys()))
    # rand_endpoint = 'Animal'
    print(rand_endpoint)
    if rand_endpoint == 'Animal':
        animal = input('Enter animal name: ')
        endpoint = based_helper.endpoint_builder(random.choice(based_helper.endpoint_names[rand_endpoint]), f'?name={animal}')
    else:
        endpoint = based_helper.endpoint_builder(random.choice(based_helper.endpoint_names[rand_endpoint]), '')
    print(endpoint)
    print(requests.get(endpoint, headers=based_helper.headers).json()[0][rand_endpoint.lower()])