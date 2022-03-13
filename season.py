from enum import Enum
from typing import List, Set

def register_seasons(seasons: List[str]) -> Enum:
    return Enum('SEASONS', seasons)

#TODO: #8 season object that holds information like how to animate the season. @JohnRushKucharski
