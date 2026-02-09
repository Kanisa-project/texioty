from osrsbox import monsters_api, items_api
from helpers.apis.api_helper import BaseAPIHelper


class OSRSAPIHelper(BaseAPIHelper):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.osrsbox.com'
        self.endpoint_names = {
            'items': ['/items'],
            'equipment': ['/equipment'],
            'weapons': ['/weapons'],
            'monsters': ['/monsters'],
            'prayers': ['/prayers']
        }


for item in monsters_api.load():
    print(item.name, item.magic_level)