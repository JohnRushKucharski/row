from typing import Set
from observer import Flow, Reciever

class Reservoir(Reciever, Flow):
    def __init__(self, inflows: Set[Flow], initialstorage: int, capacity: int, name: str):
        self._name = name
        self._capacity = capacity
        self._storage = initialstorage
        self._inflows = inflows
        self._floods: int = 0
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
    @property
    def storage(self) -> int:
        return self._storage
    @storage.setter
    def storage(self, change: int) -> None:
        self._storage += change # assumes outflows are negative
    @property
    def capacity(self) -> int:
        return self._capacity
    @property
    def floods(self) -> int:
        return self._floods
    #region Reciever
    @property
    def inflows(self) -> Set[Flow]:
        '''Locations that send flow to the reciever.'''
    def add_flow(self, flow: Flow) -> None:
        '''Adds location that sends flow to reciever.'''
        self._inflows.add(flow)
    def remove_flow(self, flow: Flow) -> None:
        '''Removes location that sends flow to reciever.'''
        self._inflows.remove(flow)
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
        inflow: int = 0
        for flow in self.inflows:
            inflow += flow.send()
        return inflow
    #endregion
    def isflood(self, inflow: int):
        return False if (inflow + self.storage) <= self.capacity else True
    def statusreport(self, inflow: int, outflow: int) -> str:
        report = f'--- {self.name} status report ---'
        report +=f'\n\t previous storage: {self.storage}'
        report +=f'\n\t   current inflow: {inflow}'
        report +=f'\n\t  spilled release: {outflow}'
        report +=f'\n\t new storage: {self.storage + inflow - outflow}'
        report +=f'----------------------------------'
        return report
    def operate(self) -> int:
        inflow = self.request_inflows()
        isflood = self.isflood(inflow)
        self._floods += 1 if isflood else 0
        outflow = self.capacity - (self.storage + inflow) if isflood else 0
        # Get User Input
        while True:
            maxrelease = int(self.storage + inflow - outflow)
            print(self.statusreport)
            print(f'Enter an integer release value on the range: [0, {maxrelease}]...')
            release: str = input()
            if release.isdigit() and (0 <= int(release) <= maxrelease):
                outflow += int(release)
                break
            else:
                print(f'The input release: {release} is invalid because it is not an integer on the range: [0, {maxrelease}].')
        self._storage += inflow - outflow
        return outflow
    #region Flow (sender)
    def send(self) -> int:
        return self.operate()
    #endregion

    
        
    