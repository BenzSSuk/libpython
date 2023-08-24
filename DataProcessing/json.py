import json

def read_json(pathFile, mode='r'):
    f = open(pathFile, mode)
    dict_json = json.load(f)
    f.close()

    return dict_json

