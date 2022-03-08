'''
Provides protocols for the subscribers and publishers using the observer pattern.

- patterned from: https://refactoring.guru/design-patterns/observer/python/example
'''
from abc import abstractmethod
from typing import Set, Protocol

class Flow(Protocol):
    '''A location that sends flow to a reciever downstream.'''
    @abstractmethod
    def send(self) -> int:
        '''Send flow tor reciever.'''
class Reciever(Protocol):
    @property
    @abstractmethod
    def inflows(self) -> Set[Flow]:
        '''Locations that send flow to the reciever.'''
    @abstractmethod
    def add_flow(self, flow: Flow) -> None:
        '''Adds location that sends flow to reciever.'''
    @abstractmethod
    def remove_flow(self, flow: Flow) -> None:
        '''Removes location that sends flow to reciever.'''
    @abstractmethod
    def request_inflows(self) -> int:
        '''Calls all senders and requests inflows.'''
    
   

# class Subscriber(Protocol):
#     '''Subscribers will be storage in flow locations they will recieve notifications from upstream flows.'''
#     @property
#     @abstractmethod
#     def publishers(self) -> Set[Publisher]
    
#     @abstractmethod
#     def update(self, inflow: int) -> int:
#         '''Updates the subscriber flow or storage values based on publisher notification.'''

# class Publisher(Protocol):    
#     @property
#     @abstractmethod
#     def subscriber(self) -> Subscriber:
#         '''A list of downstream storage and flow locations that recieve flow from the publisher.'''
#     @abstractmethod
#     def add_subscriber(self, subscriber: Subscriber) -> None:
#         '''Appends a new subscriber to the list of subscribers.'''   
#     @abstractmethod
#     def notify(self, flow: int) -> None:
#         '''Notifies downstream locations that accept the flow as an inflow.'''