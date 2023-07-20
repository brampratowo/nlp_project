import os
import json
from json import JSONEncoder


class HelperFunction(object):
    def loadJsonFile(filename):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, filename)
        with open(file_path) as data_file:
            data = json.load(data_file)
        return data

    def loadTextFile(filename):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, filename)
        with open(file_path, encoding="utf-8") as data_file:
            data = data_file.read()
        return data


class SetEncoder(JSONEncoder):
    def default(self, obj):
        return list(obj)
