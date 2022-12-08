# -*- coding: utf-8 -*-

from .context import rpi_radio_player
from pigpio_encoder.rotary import Rotary
from mpd import MPDClient

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_fails_when_input_is_not_Rotary_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controller.RadioController(None, None, MPDClient, MPDClient())


if __name__ == '__main__':
    unittest.main()