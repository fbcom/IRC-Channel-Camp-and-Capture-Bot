# -*- coding: utf-8 -*-
import json


class Configuration:

    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        with open(self.filename) as config_file:
            config = json.load(config_file)
        self.config = config

    def save(self):
        with open(self.filename, 'w') as config_file:
            json.dump(self.config, config_file, sort_keys=True, indent=4)

    def get(self, parameter=None):
        if parameter:
            return self.config[parameter]
        return self.config

    def put(self, parameter, value):
        self.config[parameter] = value
