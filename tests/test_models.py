import unittest
from types import SimpleNamespace
from unittest.mock import create_autospec

from rpi_radio_player.models import StationModel, StationNotFoundException
from rpi_radio_player.components import ProcessImageComponent
from rpi_radio_player.data import JsonDao

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    # I still feel like there must be a way to group these tests under a class and run a setup for
    # them. So there is no mock instantiation duplication.
    def test_when_no_stations_configured_get_current_position_returns_none(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = []
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        mock_image_processor.process_image.assert_not_called()
        self.assertIsNone(sut.get_current_station_position())

    def test_when_no_stations_configured_get_current_station_raises_exception(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = []
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        with self.assertRaises(StationNotFoundException):
            sut.get_current_station()

    def test_when_no_stations_configured_get_all_station_urls_raises_exception(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = []
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        with self.assertRaises(StationNotFoundException):
            sut.get_all_station_urls()

    def test_when_one_station_configured_get_all_items_returns_one(self):
        mock_dao = create_autospec(JsonDao)
        mock_dao.get_all_items.return_value = self._create_station_list(1)
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        self.assertEqual(sut.get_current_station_position(), 0)

    def test_when_one_station_configured_get_current_station_returns_station(self):
        mock_dao = create_autospec(JsonDao)
        station_return_value = self._create_station_list(1)
        mock_dao.get_all_items.return_value = station_return_value
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        self.assertEqual(sut.get_current_station(), station_return_value[0])

    def test_when_one_station_configured_get_all_station_urls_returns_urls(self):
        mock_dao = create_autospec(JsonDao)
        station_return_value = self._create_station_list(1)
        mock_dao.get_all_items.return_value = station_return_value
        mock_image_processor = create_autospec(ProcessImageComponent)

        sut = StationModel(mock_dao, mock_image_processor)

        self.assertEqual(sut.get_all_station_urls(), [station_return_value[0].url])


    def _create_station_list(self, amount) -> list:
        station_list = []
        for i in range(amount):
            station_list.append(
                SimpleNamespace(image=f"image{i}", name=f"radio {i}", url=f"https://radio-{i}.com"))

        return station_list

if __name__ == '__main__':
    unittest.main()
