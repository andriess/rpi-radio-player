from mpd import MPDClient
from pigpio_encoder.rotary import Rotary

from rpi_radio_player.models import StationModel, StationNotFoundException
from rpi_radio_player.views import StationListView

class RadioController():
    def __init__(self, model: StationModel, view: StationListView, button_input: Rotary, player: MPDClient) -> None:
        self._model = model
        self._view = view
        self._button_input = button_input
        self._player = player

        # Start listining to button events and assign controller callbacks.
        self._init_button_input()

        # Add the radiostations to the mpd player.
        self._init_player()

        # Display the image of the currently selected (0) station on boot.
        self._init_view()

    def _init_button_input(self) -> None:
        self._button_input.setup_rotary(
            up_callback=self._up_callback,
            down_callback=self._down_callback,
            )
        self._button_input.setup_switch(sw_short_callback=self._sw_short)
        print("Initialized the rotary input.")

    def _sw_short(self) -> None:
        self._model.select_station()
        self._player.play(self._model.get_currently_playing_station())

    def _up_callback(self, *_) -> None:
        self._model.next()

        self._view.show(self._model.get_currently_displayed_station().processedImage)

    def _down_callback(self, *_) -> None:
        self._model.previous()

        self._view.show(self._model.get_currently_displayed_station().processedImage)

    def _init_player(self) -> None:
        stations_urls = self._model.get_all_station_urls()
        for url in stations_urls:
            self._player.add(url)
        print("Initialized the mpd player.")

    def _init_view(self):
        try:
            current_station = self._model.get_currently_displayed_station()
            self._view.show(current_station.processedImage)
        except StationNotFoundException:
            # maybe display a qr, linking to github with some setup instructions.
            print("No stations configured.")
