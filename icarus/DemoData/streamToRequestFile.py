import sys, os, json, jsonpickle
from icarus.registry import RESULTS_READER

currDir = os.getcwd()
if currDir not in sys.path:
    sys.path.append(currDir)

def writefile(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close

def writeRequestFile(filename):
    results = RESULTS_READER['JSON'](filename)
    
    timeline = results[0][1]['EVENT_TIMELINE']['TIMELINE']
    f = open("requests.txt", 'w')

    for t in timeline:
        if t['event_type'] == 'request':
            f.write('(' + str(t['from_node']) + ',' + str(t['data_ID']) + ')\n')
    f.close

for i in sys.argv[1:]:
    writeRequestFile(i)
