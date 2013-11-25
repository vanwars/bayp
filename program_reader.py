import json

def read_programs(filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    
    return data