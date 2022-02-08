import json
import os
from copy import deepcopy


class SaveFile:

    def __init__(self, file_path, default_data):
        self.file_path = file_path + '.json'
        self.default_data = default_data

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as new_save:
                json.dump(self.default_data, new_save, indent=4)

        with open(self.file_path, 'r') as save:
            self.data = json.load(save)

    def save(self):
        with open(self.file_path, 'w') as save:
            json.dump(self.data, save, indent=4)

    def reset(self):
        with open(self.file_path, 'w') as save:
            json.dump(self.default_data, save, indent=4)
        self.data = deepcopy(self.default_data)
