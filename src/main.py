from model import main
import json

with open('config.json', 'r') as f:
    config = json.load(f)
main(config['loops'], config['sampling'], config['output_prefix'])