from abc import abstractmethod
from typing import List, Set, Tuple, Optional, Protocol
from enum import Enum

import numpy as np

from data import Record

class Tag(Enum):
    INFLOW = 0
    TRANSFER = 1
    OUTFLOW = 2

class Inflow(Protocol):
    #TODO: #4 Add risk adjustment to records and parametric inflows @jolszew2
    @abstractmethod
    def create_flow(self) -> Record:
        '''Generates inflow for the location'''
    @property
    @abstractmethod
    def records(self) -> Optional[List[Record]]:
        '''An optional list of observational data to link to the simulated values.'''

class BootstrapInflow(Inflow):  
    def __init__(self, records: List[Record], seed: int):
        self._tag = Tag.INFLOW
        self._records = records
        self._rng = np.random.default_rng(seed)
    @property
    def tag(self) -> Tag:
        return Tag.INFLOW
    @property
    def records(self) -> List[Record]:
        return self._records
    def create_flow(self) -> Record:
        '''Returns a bootstrapped record'''
        return self.records[self._rng.integers(0, len(self.records))]
   
    # #region SENDER
    # def send(self) -> int:
    #     '''Returns new bootstrapped flow value.'''
    #     return self.create_flow().flow
    # #endregion
    
class ParametricInflow(Inflow):
    # TODO: #5 Add records and event matching @JohnRushKucharski
    def __init__(self, sample_range: Tuple[int, int], seed: int):
        self._tag = Tag.INFLOW
        self._sample_range = sample_range
        self._rng = np.random.default_rng(seed)
    @property
    def tag(self) -> Tag:
        return self._tag
    @property
    def records(self) -> List[Record]:
        raise NotImplementedError()
    @property
    def sample_range(self) -> Tuple[int, int]:
        return self._sample_range
    def create_flow(self) -> Record:
        return Record(flow=self._rng.integers(self.sample_range[0], self.sample_range[1]), event='synthetic')
 
# class Confluence(Reciever, Sender):
#     # TODO: #6 Add multiplication/division of flows @JohnRushKucharski
#     def __init__(self, name: str, inflows: Set[Sender]):
#         self._name = name
#         self._inflows = inflows
#     @property
#     def inflows(self) -> Set[Sender]:
#         return self._inflows
#     def add_flow(self, flow: Sender) -> None:
#         self._inflows.add(flow)
#     def remove_flow(self, flow: Sender) -> None:
#         self._inflows.remove(flow)
#     def request_inflows(self) -> int:
#         inflow: int = 0
#         for flow in self.inflows:
#             inflow += flow.send()
#         return inflow
#     def send(self) -> int:
#         return self.request_inflows()
    



# # class FlowLocation(Publisher):
# #     def __init__(self, subscriber: Subscriber = set()):
# #         self._simulation: List[Record] = []
# #         self._subscriber: Subscriber = subscriber    
# #     #region Publisher
# #     @property
# #     def subscribers(self) -> Set[Subscriber]:
# #         '''Downstream storage and flow locations that accept flows from this object as inflows.'''
# #         return self._subscribers
# #     def new_subscriber(self, subscriber: Subscriber) -> None:
# #         self._subscribers.add(subscriber)
# #     def remove_subscriber(self, subscriber: Subscriber) -> None:
# #         self._subscribers.remove(subscriber)
# #     def notify(self, flow: int) -> None:
# #         for subscription in self.subscribers:
# #             subscription.update(flow)
# #     #endregion
# #     @property
# #     def simulation(self) -> List[Record]:
# #         return self._simulation
# #     def simulated_flows(self) -> List[int]:
# #         return [t.flow for t in self.simulation]
# #     def simulated_events(self) -> List[Union[str, int, datetime]]:
# #         return [t.event for t in self.simulation]
    
# #     def sample(self, input: int) -> None:
# #         #logic to sample from dry or wet, turn input into flow
# #         #self.notify(flow)
# #         pass
    
# # class SeasonLocation(Protocol):
# #     '''Interface for dry or wet season records for a inflow location.'''
# #     @abstractmethod
# #     def pick_record(self, i: int) -> Record:
# #         '''Samples an event from the records.'''
# # @dataclass
# # class Dry:
# #     '''Holds dry season records for a location.'''
# #     records: List[Record]
# #     name: str = 'dry season' 
# #     '''Data used to bootstrap inflows'''
# #     def pick_record(self, item: int) -> Record:
# #         return self.records[item]    
# # @dataclass
# # class WetSeason:
# #     records: Optional[List[Record]]
# #     name: str = 'wet season'
# #     def pick_record(self, flow: int) -> Record:
# #         if self.records is None:
# #             return Record(flow=flow, event='synthetic')
# #         else:
# #             epsilon = min([abs(flow - record.flow) for record in self.records])
# #             for record in set(self.records):
# #                 if flow - record.flow == epsilon:
# #                     return record
# #             raise RuntimeError('An unexpected error occured when a flow matching the epsilon value was not found in the Wet season pick_record method.')
            

   
    
# # class Inflows:
# #     def __init__(self, inflowlocations: Set[InflowLocation], seed: int, sampletogether: bool = True):
# #         self._random = np.random.default_rng(seed) 
# #         self._sample_together = sampletogether
# #         #TODO: Need check to make sure inflow locations have record of same events in same order. @JohnRushKucharski
# #         self._inflowlocations = inflowlocations
# #         self._nrecords = min([len(inflow.inputs) for inflow in list(inflowlocations)])
    
# #     @property
# #     def inflowlocations(self):
# #         self._inflowlocations
# #     @property
# #     def sample_together(self) -> bool:
# #         return self._sample_together
# #     @property 
# #     def random(self) -> np.random.Generator:
# #         return self._random

# #     def simulate_round(self):
# #         if self.sample_together:
# #             pass
        
    