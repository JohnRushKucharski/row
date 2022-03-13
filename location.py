from enum import Enum
from typing import List, Set, Dict, Protocol

from abc import abstractmethod, update_abstractmethods

from data import Record
from flows import Inflow

class Tag(Enum):
    '''Describes the type of location.'''
    INFLOW = 1
    '''Upstream most locations, creates new inflows.'''
    STORAGE = 2
    '''Accept upstream inflow, sends flow downstream, can store water.'''
    TRANSFER = 3
    '''Accept upstream inflow, sends flow downsteam, used for aggregation or rescaling flows.'''
    OUTFLOW = 4
    '''Accept upstream inflow that can be diverted out of the system.'''
    OUTLET = 5
    '''Downstream most location in the watershed.'''

#region Protocols    
class Location(Protocol):
    '''Interface description of all locations'''
    @property
    @abstractmethod
    def name(self) -> str:
        '''A name for the location'''
    @property
    @abstractmethod
    def tag(self) -> Tag:
        '''Describes the type of location: [inflow, transfer, outflow]'''
    @property
    @abstractmethod
    def simulation(self) -> List[Record]:
        '''Simulation results'''      


class Upstream(Protocol):
    '''Interface description of location that sends flow to downstream locations.'''
    @abstractmethod
    def send(self) -> int:
        '''Sends flow downsteam.'''     


class Downstream(Protocol):
    '''Interface description of location that accepts upstream inflow.'''
    @property
    @abstractmethod
    def upstream(self) -> Set[Upstream]:
        '''Locations that send flow to the reciever.'''
    @abstractmethod
    def add_upstream(self, flow: Upstream) -> None:
        '''Adds location that sends flow to reciever.'''
    @abstractmethod
    def remove_upstream(self, flow: Upstream) -> None:
        '''Removes location that sends flow to reciever.'''
    @abstractmethod
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
#endregion


#region Locations
class InflowLocation(Upstream, Location):
    '''Location that creates new inflow'''
    def __init__(self, name: str, seasons: Dict[Enum, Inflow]):
        self._name = name
        self._tag = Tag.INFLOW
        self._seasons = seasons
        self._active_season = None
        self._simulation: List[Record] = []
    @property
    def seasons(self) -> Dict[Enum, Inflow]:
        '''Key: dynamically generated season enum, value: object implementing Inflow interface.'''
        return self._seasons
    @property
    def season(self) -> Enum:
        '''Enum value for active season during simulation.'''
        return self._active_season
    @season.setter
    def season(self, season) -> None:
        '''Sets active season.'''
        self._active_season = season #SEASONS
    #region Location
    @property
    def tag(self) -> Tag:
        return self._tag
    @property
    def name(self) -> str:
        return self._name
    @property
    def simulation(self) -> List[Record]:
        self._simulation
    #endregion
    #region Inflow
    def create_input(self) -> Record:
        '''Samples new flow record for active season.'''
        return self.seasons[self.season].create_flow()
    #endregion
    #region Upstream
    def send(self) -> int:
        '''Sends flow downstream.'''
        record = self.create_input()
        self._simulation.append(record)
        print(f'{self.name} flow: {record.flow}')
        return record.flow
    #endregion
    
    
class TransferLocation(Upstream, Downstream, Location):
    '''Location that accepts upsteam inflow and sends it downstream, used to aggregate and/or rescale flows.'''
    #TODO: #7 Add flow adjustment factor, for very different size rivers, storage objects, etc... @JohnRushKucharski
    def __init__(self, name: str, upstream: Set[Upstream]):
        self._name = name
        self._simulation = []
        self._tag = Tag.TRANSFER
        self._upstream = upstream  
    #region Location
    @property
    def name(self) -> str:
        return self._name
    @property
    def tag(self) -> Tag:
        self._tag 
    @property
    def simulation(self) -> List[Record]:
        return self._simulation
    #endregion
    #region Downstream
    @property
    def upstream(self) -> Set[Upstream]:
        '''Locations that send flow to the reciever.'''
        return self._upstream
    def add_upstream(self, flow: Upstream) -> None:
        '''Adds location that sends flow to reciever.'''
        self._upstream.add(flow)
    def remove_upstream(self, flow: Upstream) -> None:
        '''Removes location that sends flow to reciever.'''
        self._upstream.remove(flow)
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
        inflows: int = 0
        for flow in self.upstream:
            inflows += flow.send()
        self._simulation.append(Record(inflows, 'simulated'))
        print(f'{self.name} flow: {inflows}')
        return inflows  
    #endregion
    #region Upstream
    def send(self) -> int:
        return self.request_inflows()  
    #endregion
    
       
class StorageLocation(Downstream, Upstream, Location):
    def __init__(self, name: str, upstream: Set[Upstream], initialstorage: int, capacity: int):
        self._name = name
        self._tag = Tag.STORAGE
        self._simulation = []
        self._upstream = upstream
        self._capacity = capacity
        self._storage = initialstorage
        self._floods: int = 0
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
    def statusreport(self, inflow: int, outflow: int) -> str:
        report = f'--- {self.name} status report ---'
        report +=f'\n\t previous storage: {self.storage}'
        report +=f'\n\t current inflow: {inflow}'
        report +=f'\n\t spilled release: {outflow}'
        report +=f'\n\t new storage: {self.storage + inflow - outflow}'
        report +=f'\n----------------------------------'
        return report
    def user_input(self, inflow: int, outflow: int):
        release = None
        maxrelease = int(self.storage + inflow - outflow)
        while release is None:
            print(self.statusreport(inflow, outflow))
            print(f'Enter an integer amount of flow to release from {self.name} on the range: [0, {maxrelease}]...')
            uinput: str = input()
            if uinput.isdigit() and (0 <= int(uinput) <= maxrelease):
                release = int(uinput)
            else:
                print(f'The input value: {uinput} is invalid. It is not a number on the range: [0, {maxrelease}]. Press Enter to continue...')
        return release
    def operate(self) -> int:
        inflow = self.request_inflows()
        isflood = False if (inflow + self.storage) <= self.capacity else True
        self._floods += 1 if isflood else 0
        outflow = self.storage + inflow - self.capacity if isflood else 0
        outflow += self.user_input(inflow, outflow)
        self._storage += inflow - outflow
        self._simulation.append(Record(outflow, 'user input', notes=f'storage: {self.storage}'))
        print(f'{self.name} inflow: {inflow}, storage: {self.storage}, outflow: {outflow}')
        return outflow
    #region Location
    @property
    def name(self) -> str:
        return self._name
    @property
    def tag(self) -> Tag:
        return self._tag
    @property
    def simulation(self) -> List[Record]:
        return self._simulation
    #endregion
    #region Downstream
    @property
    def upstream(self) -> Set[Upstream]:
        '''Locations that send flow to the reciever.'''
        return self._upstream
    def add_upstream(self, flow: Upstream) -> None:
        '''Adds location that sends flow to reciever.'''
        self._upstream.add(flow)
    def remove_upstream(self, flow: Upstream) -> None:
        '''Removes location that sends flow to reciever.'''
        self._upstream.remove(flow)
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
        inflow: int = 0
        for flow in self.upstream:
            inflow += flow.send()
        return inflow
    #endregion
    #region Upstream
    def send(self) -> int:
        return self.operate()
    #endregion   

class OutflowLocation(Upstream, Downstream):
    def __init__(self, name: str, upstream: Set[Upstream]):
        self._name = name
        self._tag = Tag.OUTFLOW
        self._simulation = []
        self._upstream = upstream
    def user_input(self, inflow: int) -> int:
        divert = None
        while divert is None:
            print(f'The flow at {self.name} is: {inflow}. Enter an integer value of the range: [0, {inflow}] to divert out of the river.')
            uinput = input()
            if uinput.isdigit() and (0 <= int(uinput) <= inflow):
                divert = int(uinput)
            else:
                print(f'The flow value: {uinput} is invalud because it is not a positive integer on the range: [0, {inflow}].')
        return divert
    def operate(self) -> int:
        inflow = self.request_inflows()
        divert = self.user_input(inflow)
        self._simulation.append(Record((inflow - divert), 'user input', notes= f'diversion: {divert}')) 
        print(f'{self.name} inflow: {inflow}, diversion: {divert}, outflow: {inflow - divert}')
        return inflow - divert       
    #region Location
    @property
    def name(self) -> str:
        return self._name
    @property
    def tag(self) -> Tag:
        return self._tag
    @property
    def simulation(self) -> List[Record]:
        return self._simulation
    #endregion
    #region Downstream
    @property
    def upstream(self) -> Set[Upstream]:
        '''Locations that send flow to the reciever.'''
        return self._upstream
    def add_upstream(self, flow: Upstream) -> None:
        '''Adds location that sends flow to reciever.'''
        self._upstream.add(flow)
    def remove_upstream(self, flow: Upstream) -> None:
        '''Removes location that sends flow to reciever.'''
        self._upstream.remove(flow)
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
        inflow: int = 0
        for flow in self.upstream:
            inflow += flow.send()
        return inflow
    #endregion   
    #region Upstream
    def send(self) -> int:
        return self.operate()
    #endregion     
         
class OutletLocation(Downstream, Location):
    def __init__(self, name: str, upstream: Set[Upstream]):
        self._name = name
        self._tag = Tag.OUTLET
        self._simulation = []
        self._upstream = upstream
    #region Location
    @property
    def name(self) -> str:
        return self._name
    @property
    def tag(self) -> Tag:
        return self._tag
    @property
    def simulation(self) -> List[Record]:
        return self._simulation
    #endregion
    #region Downstream
    @property
    def upstream(self) -> Set[Upstream]:
        return self._upstream
    def add_upstream(self, flow: Upstream) -> None:
        return self._upstream.add(flow)
    def remove_upstream(self, flow: Upstream) -> None:
        return self._upstream.remove(flow)
    def request_inflows(self) -> int:
        inflows: int = 0
        for flow in self.upstream:
            inflows += flow.send()
        self._simulation.append(Record(inflows, 'simulated'))
        print(f'{self.name} outflow: {inflows}')
        return inflows
    #endregion