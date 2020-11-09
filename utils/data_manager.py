import pickle

class DataManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, obj):
        with open(self.file_name, 'wb') as pickle_file:
            pickle.dump(obj, pickle_file)

    def load(self):
        with open(self.file_name, 'rb') as pickle_file:
            pickle.load(pickle_file)


