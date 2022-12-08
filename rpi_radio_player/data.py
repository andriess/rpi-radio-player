import abc
import json
from types import SimpleNamespace

class Dao( abc.ABC ):
    @abc.abstractclassmethod
    def load_data():
       pass

    @abc.abstractclassmethod
    def get_all_Items():
        pass

class JsonDao( Dao ):
    def __init__(self, file):
        self._file = file
        self._items = []

        # Init the data on creation.
        self.load_data()

    def load_data(self):
        # I could leave this file open all the time to support read/write and make this a proper dao.
        with open(self._file, "r") as db:
            data = json.load(db, object_hook=lambda d: SimpleNamespace(**d))
            self._items = data.stations

    def get_all_items(self):
        return self._items