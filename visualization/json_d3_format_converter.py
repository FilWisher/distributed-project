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


json_string = readfile('../icarus/examples/JSON_results_test/results_topology_0.json')
parsed_json = json.loads(json_string)

nodes = []
i = 0
for key in parsed_json['nodes']:
    #print parsed_json['nodes'][key]
    #print parsed_json['nodes'][key]['py/tuple']
    #print parsed_json['nodes'][key]['py/tuple'][0]
    nodes.append({"name": key, "group":i, "type": parsed_json['nodes'][key]['py/tuple'][0]})
    i += 1

node_dict = {}
for node in nodes:
    node_dict[node['name']] = node['group']

edges = []

for j in range(len(parsed_json['edges'])):
    edges.append({"source": node_dict[str(parsed_json['edges'][j][u'py/tuple'][0])], 
                    "target": node_dict[str(parsed_json['edges'][j][u'py/tuple'][1])],
                    "value": 1 })    

output_format = {}
output_format['nodes'] = nodes
output_format['edges'] = edges

writefile('input data/formatted_topology.json', json.dumps(output_format,sort_keys=True, indent=2))
