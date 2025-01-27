import json


def dump_charity_data_to_json(output_file, data):
    with open(output_file, "w") as charity_data:
        json.dump(data, charity_data, indent=4, sort_keys=True)
