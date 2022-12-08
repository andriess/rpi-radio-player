# -*- coding: utf-8 -*-

from .context import rpi_radio_player
from pigpio_encoder.rotary import Rotary
from mpd import MPDClient

import unittest
from unittest import mock

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    @mock.patch('__main__.StationModel')
    @mock.patch('__main__.StationListView')
    @mock.patch('__main__.MPDClient')
    @mock.patch('__main__.Rotary')
    def test_passes_when_controller_created_with_correct_types(self, mock_model, mock_view, mock_input, mock_player):
        rpi_radio_player.controller.RadioController(mock_model, mock_view, mock_input, mock_player)

    def test_fails_when_input_is_not_Rotary_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controller.RadioController(None, None, MPDClient, MPDClient)

    def test_fails_when_player_is_not_MPDClient_type(self):
        with self.assertRaises(TypeError):
            rpi_radio_player.controller.RadioController(None, None, Rotary(0,0,0), MPDClient)


if __name__ == '__main__':
    unittest.main()