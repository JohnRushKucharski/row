from enum import Enum
from typing import List

import numpy as np
from season import register_seasons

from data import records_factory
from system import System
from location import InflowLocation, OutflowLocation, OutletLocation, StorageLocation
from flows import BootstrapInflow, ParametricInflow

seed = 6476434686
rng = np.random.default_rng(seed=seed)

SEASON: Enum = register_seasons(['wet', 'dry'])
inflow_hth = InflowLocation('hetch hetch inflow', 
                   {SEASON.dry: BootstrapInflow(records_factory(rng.integers(0, 4, 11)), seed=seed),
                    SEASON.wet: ParametricInflow(sample_range=(0, 3), seed=seed)})
hetch_hetchy = StorageLocation('hetch hetchy', {inflow_hth}, 1, 5)
outflow_sjp = OutflowLocation('san joaquin pipeline', {hetch_hetchy})
inflow_dnp = InflowLocation('don pedro inflow', 
                   {SEASON.dry: BootstrapInflow(records_factory(rng.integers(1, 17, 11)), seed=seed),
                    SEASON.wet: ParametricInflow(sample_range=(1, 21), seed=seed)})
don_pedro = StorageLocation('Don Pedro', {inflow_dnp, outflow_sjp}, 21, 35)
outlet = OutletLocation('modesto', {don_pedro})

sys = System('tuolumne', {inflow_hth, hetch_hetchy, outflow_sjp, inflow_dnp, don_pedro, outlet}, SEASON)
sys.animate(2)
                   
    
# #Inflow locations (where flows start in our game)
# yrs = [2000 + i for i in range(0, 11)] # [2000, 2010]
# toyHHdata = rng.integers(0, 3, 10, endpoint=True) # ten uniform integers [0, 3]
# toyDPdata = rng.integers(1, 8, 10, endpoint=True) # ten uniform integers [1, 8]

# inflows = [BootstrapInflow('Hetch Hetchy Dry Season Inflow', records_factory(flows=list(toyHHdata), events=yrs), seed=seed),
#            ParametricInflow('Hetch Hetch Wet Season Inflow', sample_range=(0, 3), seed=seed),
#            BootstrapInflow('Don Pedro Dry Season Inflow', records_factory(flows=list(toyDPdata), events=yrs), seed = seed),
#            ParametricInflow('Don Pedro Wet Season Inflow', sample_range = (0, 21), seed=seed)]

# #Reservoirs
# # Introduce concept of "Location" whcih would be the actual Senders and Recievers. Reservoirs would be locations, a list of flows would be locations too.
# reservoirs: List[Reservoir] = []


# # from storage import StorageLocation

# # DonPedro = StorageLocation(storage=30, capacity=35, name='DonPedro')
# # HetchHetchy = StorageLocation(storage=4, capacity=5, name='HetchHetchy')

