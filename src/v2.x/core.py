import os
import json

VERSION_TAG = 'v2.1.0'


def read_config_file(attributes_dict: dict) -> dict:
    """
    Read configurations in file 'settings.json', if file do not exist then return default settings.

    Parameters:
      attributes_dict    - attributes need to read out, with default value

    Returns:
      Attributes value ordered in dict, or default value when not exist
    """
    value_dict = {}
    file = os.path.exists('./settings.json')
    if file:
        with open('./settings.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for attribute in attributes_dict.keys():
            if attribute in json_data:
                value_dict[attribute] = json_data[attribute]
            else:
                value_dict[attribute] = attributes_dict[attribute]
        return value_dict
    return attributes_dict


def save_config_file(config):
    with open('./settings.json', 'w') as f:
        json_str = json.dumps(config, indent=4, ensure_ascii=False)
        f.write(json_str)
