import time
from typing import TypeVar, List
from .data import Dao
from .components import ProcessImageComponent

class StationModel(object):

    D = TypeVar('D', bound=Dao)
    def __init__(self, dao: Dao, process_image_component: ProcessImageComponent):
        self._dao = dao
        self._process_image_component = process_image_component
        self._currently_displayed_station = None
        self._currently_playing = None
        self._station_selected_at = None
        self._stations = []

        self._initialize_stations()

    def _initialize_stations(self) -> None:
        self._stations = self._dao.get_all_items()
        self._stations.sort(key=lambda x: x.pos)

        for station in (self._stations):
            station.processedImage = self._process_image_component.process_image(station.image)

        if len(self._stations) > 0:
            self._currently_displayed_station = 0

        print("Initialized the station model.")

    def next(self) -> None:
        if self._currently_displayed_station is None:
            return None

        if self._currently_displayed_station + 1 > len(self._stations) - 1 :
            self._currently_displayed_station = 0
        else:
            self._currently_displayed_station = (self._currently_displayed_station + 1)

    def previous(self) -> None:
        if self._currently_displayed_station is None:
            return None

        if self._currently_displayed_station - 1 < 0:
            self._currently_displayed_station = len(self._stations) - 1
        else:
            self._currently_displayed_station = (self._currently_displayed_station - 1)

    def get_current_station_position(self) -> int:
        return self._currently_displayed_station

    def get_all_station_urls(self) -> List[str]:
        if self._currently_displayed_station is None:
            raise StationNotFoundException

        return [s.url for s in self._stations]

    def get_currently_displayed_station(self) -> any:
        if self._currently_displayed_station is None:
            raise StationNotFoundException

        return self._stations[self._currently_displayed_station]

    def get_currently_playing_station(self) -> any:
        return self._stations[self._currently_playing]

    def select_station(self) -> None:
        self._currently_playing = self._currently_displayed_station

class StationNotFoundException(Exception):
    "Raised when a station cannot be found."
