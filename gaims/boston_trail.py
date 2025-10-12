from gaims.base_gaim import BaseGaim
from settings import themery as t
import random
import json

travel_distance = 241
party_members = []

class BostonTrail(BaseGaim):
    def __init__(self, txo, txi):
        super().__init__(txo, txi, "BostonTrail")
