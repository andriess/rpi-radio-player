from mpd import MPDClient
from pigpio_encoder.rotary import Rotary

from rpi_radio_player.models import StationModel
from rpi_radio_player.views import StationListView

class RadioController():
    def __init__(self, model: StationModel, view: StationListView, button_input: Rotary, player: MPDClient) -> None:
        self._model = model
        self._view = view
        self._button_input = button_input
        self._player = player

        self._init_button_input()
        self._init_player()

    def _init_button_input(self) -> None:
        self._button_input.setup_rotary(
            up_callback=self._up_callback,
            down_callback=self._down_callback,
            )
        self._button_input.setup_switch(sw_short_callback=self._sw_short)
        print("Initialized the rotary input.")

    def _sw_short(self) -> None:
        current_station_pos = self._model.get_current_station_position()
        self._player.play(current_station_pos)

    def _up_callback(self, *_) -> None:
        next_station = self._model.next()
        self._view.show(next_station.processedImage)


    def _down_callback(self, *_) -> None:
        previous_station = self._model.previous()
        self._view.show(previous_station.processedImage)

    def _init_player(self) -> None:
        stations_urls = self._model.get_all_station_urls()
        for url in stations_urls:
            self._player.add(url)
        print("Initialized the mpd player.")
