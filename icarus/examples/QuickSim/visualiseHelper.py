import sys, os
import pickle
import jsonpickle

#set the environment variables to let icarus get imported

#ONLY WORKS IF THIS IS IN ONE OF THE EXAMPLE FOLDERS OTHERWISE EDIT PATH
currDir = os.getcwd()

if currDir + "/../.." not in sys.path:
    print sys.path
    sys.path.append(currDir + "/../..")

import icarus


def unPickle(path):
    '''
    returns the structured results object from results.pickle file - 
    tuple in the form (metadata, results), both dictionaries
    '''
    resFile = open(path)
    return pickle.load(resFile)


#ans = unPickle("results.pickle")


def jsonDumper(path):

    resFile = open(path)
    unpickle = pickle.load(resFile)

    unpickle = jsonpickle.encode(unpickle[0])

    f = open("jsonDump.json", "w+")
    f.write(unpickle)
    return

def jsonDumperForLarge(path):

    resFile = open(path)
    unpickle = pickle.load(resFile)

    unpickle = jsonpickle.encode(unpickle[0])

    f = open("jsonDump.json", "w+")
    f.write(unpickle)
    return



def pullTopology():
    '''
    returns structured fnss topology object as it integrates with icarus
    allows for reading of edge/node information
    '''

    #icntopology object initilisation - inherits from fnss topology & networkX graph object
    #the attribute .graph['icr_candidates'] holds all router nodes with >2 edges
    #if a node has 1 edge it is a receiver
    #otherwise it's a router
    #source nodes are created for each node with 2 edges - they are missing metadata such as
    #longitude, labels, etc, that come from the file 
    topObj = icarus.registry.TOPOLOGY_FACTORY['GEANT']()

    #call the add cache fuctions from icarus
    #the cache budget is normally calculated by the contents * network_cache constant, estimating a value here

    icarus.registry.CACHE_PLACEMENT['UNIFORM'](topObj, 100)

    print "NODES"
    print topObj.stacks()
    print "CACHES"
    print topObj.cache_nodes()
    print "EDGES"
    print topObj.edges()

    f = open("topology.json", "w+")
    f.write(jsonpickle.encode(topObj))

    return topObj

