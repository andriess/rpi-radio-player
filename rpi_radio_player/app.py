import mpd
import board
import digitalio

from rpi_radio_player.models import StationModel
from rpi_radio_player.views import StationListView
from rpi_radio_player.data import JsonDao
from rpi_radio_player.controllers import RadioController
from rpi_radio_player.components import ProcessImageComponent

from pigpio_encoder.rotary import Rotary
from adafruit_rgb_display import st7789

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

    stationDao = JsonDao("resources/radiostations.json")
    imageProcessingComponent = ProcessImageComponent(240, 240, "resources/")
    stationListView = StationListView(display)
    stationModel = StationModel(stationDao, imageProcessingComponent)

    # passing the rotary and mpd client seems wrong.
    radioController = RadioController(stationModel, stationListView, my_rotary, client)