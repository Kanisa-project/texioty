from osrsbox import monsters_api
from src.texioty.helpers.apis.api_helper import BaseAPIHelper


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


for monster in monsters_api.load():
    print(monster.name, monster.magic_level)