import json


def readfile(filename):
    f = open(filename)
    input_file = f.read()
    f.close()
    return input_file

def writefile(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close


#json_string = readfile('../icarus/examples/JSON_results_test/results_topology_0.json')
json_string = readfile('../fixtures/GeantTopology.json')
#json_string = readfile('../fixtures/6NodeTopology.json')
parsed_json = json.loads(json_string)

nodes = []
i = 0
for key in parsed_json['nodes']:
    node_type = parsed_json['nodes'][key]['py/tuple'][0]
    #only add a cache_size attribute for routers
    if parsed_json['nodes'][key]['py/tuple'][0] == 'router':
        #check if router dictionary is empty - cache size is null
        if bool(parsed_json['nodes'][key]['py/tuple'][1]):
            #print parsed_json['nodes'][key]['py/tuple'][1]
            cache_size = parsed_json['nodes'][key]['py/tuple'][1]['cache_size']
        else:
            cache_size = 0
        nodes.append({"name": key, "group":i, "type": node_type, "cache_size" : cache_size})
    else:
        nodes.append({"name": key, "group":i, "type": node_type, "cache_size" : "N/A - not a router"})
    i += 1

print len(nodes)

node_dict = {}
for node in nodes:
    node_dict[node['name']] = node['group']   


edges = []
for j in range(len(parsed_json['edges'])):
    edges.append({"source": node_dict[str(parsed_json['edges'][j][u'py/tuple'][0])], 
                    "target": node_dict[str(parsed_json['edges'][j][u'py/tuple'][1])],
                    "value": 1 })    

print len(edges)

output_format = {}
output_format['nodes'] = nodes
output_format['edges'] = edges

writefile('input data/formatted_topology.json', json.dumps(output_format,sort_keys=True, indent=2))
