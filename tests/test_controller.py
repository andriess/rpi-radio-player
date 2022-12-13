# -*- coding: utf-8 -*-

from rpi_radio_player.models import StationModel
from .context import rpi_radio_player
from pigpio_encoder.rotary import Rotary
from mpd import MPDClient

import unittest
from unittest import mock

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_passes_when_controller_created_with_correct_types(self):
        rpi_radio_player.controllers.RadioController()

    def test_fails_when_input_is_not_Rotary_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controllers.RadioController(None, None, MPDClient, MPDClient)

    def test_fails_when_player_is_not_MPDClient_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controllers.RadioController(None, None, Rotary(1,2,3), MPDClient)


if __name__ == '__main__':
    unittest.main()