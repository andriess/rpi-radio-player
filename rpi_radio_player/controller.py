from mpd import MPDClient
from pigpio_encoder.rotary import Rotary

class RadioController():
    def __init__(self, model, view, input: Rotary, player: MPDClient):
        if not isinstance(input, Rotary):
            raise TypeError("Input should be of type: Rotary")
        if not isinstance(player, MPDClient):
            raise TypeError("player should be of type: MPDClient")

        self._model = model
        self._view = view
        self._input = input
        self._player = player

        # Why am I doing the init here. Makes more sense to do this as an app start action.
        #self._initPlayer()

        input.setup_rotary(
            up_callback=self._up_callback,
            down_callback=self._down_callback,
            )
        input.setup_switch(sw_short_callback=self._sw_short)
        input.watch()

    def _sw_short(self):
        currentStationPos = self._model.get_current_station_position
        self._player.play(currentStationPos)

    def _up_callback(self, counter):
        nextStation = self._model.next()
        self._view.show(nextStation.image)

    def _down_callback(self, counter):
        previousStation = self._model.previous()
        self._view.show(previousStation.image)

    def _initPlayer(self):
        stations = self._model.get_all_station_urls()
        for station in stations:
            self._player.add(station.url)