from datetime import datetime
from dataclasses import dataclass

from typing import List, Union, Optional

@dataclass
class Record:
    flow: int
    event: Union[str, int, datetime]
    raw_data: Optional[float] = None
    notes: Optional[str] = None

def records_factory(flows: List[int], 
                    events: Optional[Union[List[int], List[str], List[datetime]]] = None,
                    raw_data: Optional[List[float]] = None):    
    if events is None or len(events) == len(set(events)):
        return [Record(flow = flows[i], event = i if events is None else events[i], raw_data = None if raw_data is None else raw_data[i]) for i in range(len(flows))]
    else:
        raise KeyError(print([e for e in events if e in set(events)]))
        