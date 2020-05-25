import json


keys_dict = {
    'Kr': None,
    'Kc': None,
    'ITER_MAX': None
}


def save_keys(kr, kc, iter_max):
    keys_dict['Kr'] = kr
    keys_dict['Kc'] = kc
    keys_dict['ITER_MAX'] = iter_max

    with open('keys.json', 'w') as json_file:
        json.dump(keys_dict, json_file, indent=2)


def read_keys():
    with open('keys.json') as json_file:
        keys_dict = json.load(json_file)
    return keys_dict