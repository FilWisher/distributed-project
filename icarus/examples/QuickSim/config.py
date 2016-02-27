"""This module contains all configuration information used to run simulations
"""
from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

# GENERAL SETTINGS
LOG_LEVEL = 'INFO'
PARALLEL_EXECUTION = True
N_PROCESSES = cpu_count()
CACHING_GRANULARITY = 'OBJECT'
RESULTS_FORMAT = 'PICKLE'
N_REPLICATIONS = 1

# List of metrics to be measured in the experiments
# The implementation of data collectors are located in ./icaurs/execution/collectors.py
DATA_COLLECTORS = ['CACHE_HIT_RATIO', 'LATENCY', 'LINK_LOAD', 'PATH_STRETCH', 'BULK_DATA']
ALPHA = [0.6]
# Total size of network cache as a fraction of content population
NETWORK_CACHE = [0.004]
# Number of content objects
N_CONTENTS = 3*10**5
# Number of requests per second (over the whole network)
NETWORK_REQUEST_RATE = 12.0
# Number of content requests generated to prepopulate the caches
# These requests are not logged
N_WARMUP_REQUESTS = 3*10**5
# Number of content requests generated after the warmup and logged
# to generate results. 
N_MEASURED_REQUESTS = 6*10**5
# List of all implemented topologies
# Topology implementations are located in ./icarus/scenarios/topology.py
TOPOLOGIES =  [
        'GEANT',
              ]
# List of caching and routing strategies
# The code is located in ./icarus/models/strategy.py
STRATEGIES = [
     'LCE',             # Leave Copy Everywhere
             # No caching, shorest-path routing
             ]
CACHE_POLICY = 'LRU'

# Queue of experiments
EXPERIMENT_QUEUE = deque()
default = Tree()
default['workload'] = {'name':       'STATIONARY',
                       'n_contents': N_CONTENTS,
                       'n_warmup':   N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS,
                       'rate':       NETWORK_REQUEST_RATE
                       }
default['cache_placement']['name'] = 'UNIFORM'
default['content_placement']['name'] = 'UNIFORM'
default['cache_policy']['name'] = CACHE_POLICY

# Create experiments multiplexing all desired parameters
for alpha in ALPHA:
    for strategy in STRATEGIES:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment['workload']['alpha'] = alpha
                experiment['strategy']['name'] = strategy
                experiment['topology']['name'] = topology
                experiment['cache_placement']['network_cache'] = network_cache
                experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, network cache: %s" \
                                     % (str(alpha), strategy, topology, str(network_cache))
                EXPERIMENT_QUEUE.append(experiment)
