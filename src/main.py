from model import one_simulation, many_simulation
import json

with open('config.json', 'r') as f:
    config = json.load(f)

for item in config:
    one_simulation(item['loops'], item['sampling'], item['output_prefix'], item['server_A'], item['server_B'])
    many_simulation(item['loops'], item['sampling'], item['output_prefix'], item['server_A'], item['server_B'])

