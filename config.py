import json

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
        print(config)

load_config()