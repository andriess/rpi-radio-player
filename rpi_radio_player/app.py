import time

import board
import digitalio
import mpd

from pigpio_encoder.rotary import Rotary
from adafruit_rgb_display import st7789

from rpi_radio_player.models import StationModel
from rpi_radio_player.views import StationListView
from rpi_radio_player.data import JsonDao
from rpi_radio_player.controllers import RadioController
from rpi_radio_player.components import ProcessImageComponent

def run():
    client = mpd.MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect("/run/mpd/socket")
    print(client.mpd_version)
    client.clear()

    cs_pin = digitalio.DigitalInOut(board.D7)
    dc_pin = digitalio.DigitalInOut(board.D9)

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    display = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, y_offset=80, baudrate=10000000)
    my_rotary = Rotary(clk_gpio=17, dt_gpio=18, sw_gpio=27)

    station_dao = JsonDao("resources/radiostations.json")
    image_processing_component = ProcessImageComponent(240, 240, "resources")
    station_list_view = StationListView(display)
    station_model = StationModel(station_dao, image_processing_component)

    # passing the rotary and mpd client seems wrong.
    radio_controller = RadioController(station_model, station_list_view, my_rotary, client)

    while True:
        # just wait and wait.
        time.sleep(2)

        # I guess pinging the client will keep the socket connection open. Otherwise maybe
        # implement some kind of re-connect try/catch logic.
        client.ping()

