from typing import TypeVar
from .data import Dao

class StationModel(object):

    D = TypeVar('D', bound=Dao)
    def __init__(self, dao: Dao, processImageComponent):
        self._dao = dao
        self._processImageComponent = processImageComponent
        self._currentStation = 0
        self._stations = self._initialize_stations()

    def _initialize_stations(self):
        self._stations = self._dao.get_all_items()

        for station in self._stations:
            station.processedImage = self._processImageComponent(station.image)

    def next(self):
        if self._currentStation + 1 > len(self._stations) - 1 :
            self._currentStation = 0
        else:
            self._currentStation = (self._currentStation + 1)

        return self._stations[self._currentStation]

    def previous(self):
        if(self._currentStation - 1 < 0):
            self._currentStation = len(self._stations) - 1
        else:
            self._currentStation = (self._currentStation - 1)

        return self._stations[self._currentStation]

    def get_current_station_position(self):
        return self._currentStation

    def get_all_station_urls(self):
        return [s.url for s in self._stations]