from src.texioty.helpers.apis.api_helper import BaseAPIHelper
from src.texioty.helpers.promptaires.prompt_helper import BasePrompt
from src.texioty.settings import themery as t, utils as u


class LyricalAPI(BasePrompt, BaseAPIHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.endpoint_names = {'search': ['/api/search'],
                               'get_id': ['/api/get/']}

        self.base_url = 'https://lrclib.net'
        self.headers = {'Content-Type': 'application/json',
                        'User-Agent': 'texioty https://github.com/Kanisa-project/texioty'}

        self.helper_commands['lyrics'] = {
            "name": "lyrics",
            "usage": '"lyrics"',
            "lite_desc": "Search for lyrics by artist or song name.",
            "full_desc": ["Search for lyrics by artist or song name."],
            "args_desc": {},
            "examples": ['lyrics'],
            "group_tag": "PRUN",
            "font_color": u.rgb_to_hex(t.GREEN_YELLOW),
            "back_color": u.rgb_to_hex(t.BLACK)
        }

    def endpoint_builder(self, endpoint_name: str, url_ending: str):
        self.previous_endpoint = f'{self.base_url}{endpoint_name}{url_ending}'
        return self.previous_endpoint


    def