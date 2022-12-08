# -*- coding: utf-8 -*-

from .context import rpi_radio_player
from pigpio_encoder.rotary import Rotary
from mpd import MPDClient

import unittest
from unittest import mock

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    @mock.patch('rpi_radio_player.models.StationModel')
    @mock.patch('rpi_radio_player.views.StationListView')
    def test_passes_when_controller_created_with_correct_types(self, mock_model, mock_view, mock_input, mock_player):
        rpi_radio_player.controller.RadioController(mock_model, mock_view)

    def test_fails_when_input_is_not_Rotary_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controller.RadioController(None, None, MPDClient, MPDClient)

    def test_fails_when_player_is_not_MPDClient_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controller.RadioController(None, None, Rotary(1,2,3), MPDClient)


if __name__ == '__main__':
    unittest.main()