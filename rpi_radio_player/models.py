from typing import TypeVar, List
from .data import Dao
from .components import ProcessImageComponent

class StationModel(object):

    D = TypeVar('D', bound=Dao)
    def __init__(self, dao: Dao, process_image_component: ProcessImageComponent):
        self._dao = dao
        self._process_image_component = process_image_component
        self._current_station = 0

        self._initialize_stations()

    def _initialize_stations(self) -> None:
        self._stations = self._dao.get_all_items()

        for station in self._stations:
            station.processedImage = self._process_image_component.process_image(station.image)

        print("Initialized the station model.")

    def next(self) -> any:
        if self._current_station + 1 > len(self._stations) - 1 :
            self._current_station = 0
        else:
            self._current_station = (self._current_station + 1)

        return self._stations[self._current_station]

    def previous(self) -> any:
        if self._current_station - 1 < 0:
            self._current_station = len(self._stations) - 1
        else:
            self._current_station = (self._current_station - 1)

        return self._stations[self._current_station]

    def get_current_station_position(self) -> int:
        return self._current_station

    def get_all_station_urls(self) -> List[str]:
        return [s.url for s in self._stations]
