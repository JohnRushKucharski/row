from enum import Enum
from typing import Set

from location import Tag, Location
import random
import numpy as np

class System:
    def __init__(self,name: str, locations: Set[Location], seasons: Enum):
        self._name = name
        self._locations = locations
        self._seasons = seasons
    @property
    def seasons(self):
        return self._seasons
    @property
    def locations(self):
        return self._locations
    
    def animate(self, nrounds: int):
        n: int = 0
        while n < nrounds:
            print(f'====== round {n} ======')
            for season in self.seasons:
                for location in self.locations:
                    if location.tag == Tag.INFLOW:
                        location.season = season                    
                if season.name == 'dry':
                    print('______dry season______')
                    for location in self.locations:
                        if location.tag == Tag.OUTLET:
                            location.request_inflows()
                else: # season.name == 'wet'
                    print('=====================')
                    print('_____wet season______')
                    event = random.choice([True, False])
                    while event:
                        print('   * new flood *    ')
                        for location in self.locations:
                            if location.tag == Tag.OUTLET:
                                location.request_inflows()
                        event = random.choice([True, False])
            n += 1
                    
                    
                    