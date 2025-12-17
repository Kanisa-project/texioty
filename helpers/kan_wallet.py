import os

import requests

from helpers.api_helper import BaseAPIHelper


class KanWallet(BaseAPIHelper):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.sandbox.immutable.com'
        self.headers = {'Accept': 'application/json',
                        'X-API-Key': os.getenv('IMX_API_KEY')}
        self.imx_endpoint_names = {
            'list_erc20_tokens': ['/v1/chains/', '/tokens']
        }

    def build_endpoint(self, path_list: list):
        pass


if __name__ == '__main__':
    k_wallet = KanWallet()
    endpoint = k_wallet.endpoint_builder('', '')
    print(requests.get(endpoint, headers=k_wallet.headers).json()[0])
