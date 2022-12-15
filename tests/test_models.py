import unittest
from types import SimpleNamespace
from unittest.mock import Mock, create_autospec

from rpi_radio_player.models import StationModel
from rpi_radio_player.components import ProcessImageComponent
from rpi_radio_player.data import JsonDao

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_when_no_stations_configured_get_current_position_returns_none(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = []
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        mock_image_processor.process_image.assert_not_called()
        self.assertIsNone(sut.get_current_station_position())


    def test_when_one_station_configured_get_all_items_returns_one(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = [SimpleNamespace(image="https://liveaudio.rte.ie/hls-radio/gold/chunk.m3u8")]
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        self.assertEqual(sut.get_current_station_position(), 0)

if __name__ == '__main__':
    unittest.main()
