from utils.log import console_out

import json
import os

loaded_jsons = {}

def load_json_files(directory):
    global loaded_jsons

    for json_file_name in os.listdir(directory):
        if not json_file_name.split(".")[-1] == "json": continue
        json_file = os.path.join(directory, json_file_name)

        open_file = open(json_file, encoding="utf8")
        json_data = json.load(open_file)
        open_file.close()
        loaded_jsons[json_file_name] = json_data
        console_out.color_print("[JSON_LOADER] JSON_LOADED: " + json_file, "yellow")

    console_out.safe_print("")

# return content of all json files in specific directory
def get_jsons_inside_folder(directory):
    jsons = []
    for json_file_name in os.listdir(directory):
        json_file = os.path.join(directory, json_file_name)
        with open(json_file, "r") as json_content:
            jsons.append( json.load(json_content) )
    return jsons

# read json file from disk and save it to ram if it is not already saved to ram
def cache_json_read(json_file_path):
    global loaded_jsons

    if json_file_path in loaded_jsons:
        return loaded_jsons[json_file_path]

    open_file = open(json_file_path, encoding="utf8")
    json_data = json.load(open_file)
    open_file.close()
    loaded_jsons[json_file_path] = json_data
    #console_out.safe_print("[JSON_LOADER][TRACE] json file loaded: " + json_file_path)
    return json_data

def get_json_file_data(json_file_name):
    global loaded_jsons

    return loaded_jsons[json_file_name]
