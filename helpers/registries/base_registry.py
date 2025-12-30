from helpers.tex_helper import TexiotyHelper


class BaseRegistry(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.current_catalog = {}
