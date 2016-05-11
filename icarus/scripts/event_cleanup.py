'''
Cleans up event data from Icarus Simulator

Input format: JSON formats provided by the 'EVENT_TIMELINE' data collector

Output format: JSON object in the form:
{
  topology: {
    nodes: [...],
    edges: [...]
  },
  events: [
    {"event_type":"...", ...}, ...
  ]
}
'''
import sys, os, json, jsonpickle
from icarus.registry import RESULTS_READER

currDir = os.getcwd()
if currDir not in sys.path:
    sys.path.append(currDir)

def writefile(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close

def reFormat(filename):
    results = RESULTS_READER['JSON'](filename)
    
    for curr_res in results:
        timeline = curr_res[1]['EVENT_TIMELINE']['TIMELINE']
        name = curr_res[0]['cache_policy']['name']
        f = open(name+"_clean_events.json", 'w')
        if curr_res[1]['TOPOLOGY']:
            nodes = results[0][1]['TOPOLOGY']['TOPOLOGY'].nodes(True)
            structured_nodes = {}
            for n in nodes:
                if 'contents' in n[1]['stack'][1]:
                    n[1]['stack'][1]['contents'] = list(n[1]['stack'][1]['contents'])
                    structured_nodes[n[0]] = n[1]
                    
            topology = {'NODES':structured_nodes,'EDGES':
                        curr_res[1]['TOPOLOGY']['TOPOLOGY'].edges(data = True)}
            output = {'TOPOLOGY':topology, 'EVENTS':timeline}
            json.dump(output, f)
        else:
            json.dump(timeline, f)

for i in sys.argv[1:]:
    reFormat(i)


