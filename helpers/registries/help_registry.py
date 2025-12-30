from helpers.registries.base_registry import BaseRegistry


class HelpRegistry(BaseRegistry):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)