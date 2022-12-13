import json

from abc import ABCMeta, abstractmethod
from types import SimpleNamespace
from typing import List

class Dao(metaclass=ABCMeta):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def get_all_items(self) -> List[any]:
        pass

class JsonDao(Dao):
    def __init__(self, file) -> None:
        self._file = file
        self._items = []

        # Init the data on creation.
        self.load_data()

    def load_data(self) -> None:
        # I could leave this file open all the time to support read/write and make this a proper dao
        with open(self._file, "r", encoding="utf-8") as database:
            data = json.load(database, object_hook=lambda d: SimpleNamespace(**d))
            self._items = data.stations

    def get_all_items(self) -> List[any]:
        return self._items
