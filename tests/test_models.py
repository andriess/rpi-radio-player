import unittest
from types import SimpleNamespace
from unittest.mock import create_autospec
from unittest import mock

from rpi_radio_player.models import StationModel, StationNotFoundException
from rpi_radio_player.components import ProcessImageComponent
from rpi_radio_player.data import JsonDao

class StationModelTests_Without_Stations_Configured(unittest.TestCase):
    """StationModel tests where the class is instantiated with no stations."""

    def setUp(self) -> None:
        self.mock_dao = create_autospec(JsonDao)
        self.mock_dao.get_all_items.return_value = []
        self.mock_image_processor = create_autospec(ProcessImageComponent)

        self.sut = StationModel(self.mock_dao, self.mock_image_processor)

    def test_when_get_current_position_returns_none(self):
        self.mock_image_processor.process_image.assert_not_called()
        self.assertIsNone(self.sut.get_current_station_position())

    def test_when_get_current_station_raises_exception(self):
        with self.assertRaises(StationNotFoundException):
            self.sut.get_currently_displayed_station()

    def test_when_get_all_station_urls_raises_exception(self):
        with self.assertRaises(StationNotFoundException):
            self.sut.get_all_station_urls()

    def test_when_next_returns_none(self):
        self.assertEqual(self.sut.next(), None)

    def test_when_previous_returns_none(self):
        self.assertEqual(self.sut.previous(), None)

class StationModelTests_With_Stations_Configured(unittest.TestCase):
    """StationModel tests where the class is instantiated with three stations."""

    def setUp(self) -> None:
        self.mock_dao = create_autospec(JsonDao)
        self.station_list = create_station_list(3)

        # creating on purpose an unordered list. All tests should still pass, as the init should
        # order this.
        self.mock_dao.get_all_items.return_value = [
            self.station_list[2], self.station_list[1], self.station_list[0]
        ]

        self.mock_image_processor = create_autospec(ProcessImageComponent)

        self.sut = StationModel(self.mock_dao, self.mock_image_processor)

    def test_init_stations_stations_should_be_ordered_ascending_by_position(self):
        self.assertEqual(self.sut._stations, self.station_list )

    def test_when_get_current_station_position_returns_zero(self):
        self.assertEqual(self.sut.get_current_station_position(), 0)

    def test_when_get_current_station_returns_station_at_zero(self):
        self.assertEqual(self.sut.get_currently_displayed_station(), self.station_list[0])

    def test_when_get_all_station_urls_returns_urls(self):
        self.assertEqual(self.sut.get_all_station_urls(), [s.url for s in self.station_list])

    @mock.patch('time.time', return_value=12345)
    def test_when_next_is_called_should_update_position_and_display_updated_time(self, mock_time):
        self.sut.next()

        self.assertEqual(self.sut._currently_displayed_station, 1)
        self.assertEqual(self.sut._last_update, 12345)

    @mock.patch('time.time', side_effect=[10, 20, 30])
    def test_when_next_is_called_at_last_element_should_be_set_to_first_element_position(self, mock_time):
        self.sut.next() # returns position 1

        self.assertEqual(self.sut._last_update, 10)
        self.assertEqual(self.sut._currently_displayed_station, 1)

        self.sut.next() # returns postion 2 and last element in the station list.

        self.assertEqual(self.sut._last_update, 20)
        self.assertEqual(self.sut._currently_displayed_station, 2)

        # on the third call we expect the method to return the first elemement in the list.
        self.sut.next()
        self.assertEqual(self.sut._currently_displayed_station, 0)
        self.assertEqual(self.sut._last_update, 30)

    @mock.patch('time.time', return_value=12345)
    def test_previous_when_at_first_element_should_be_set_to_last_element_postion(self, mock_time):
        self.sut.previous()

        self.assertEqual(self.sut._currently_displayed_station, 2)
        self.assertEqual(self.sut._last_update, 12345)
        mock_time.assert_called_once()

    def test_select_station_when_pos_is_0_currently_playing_should_be_0(self):
        self.sut.select_station()

        self.assertEqual(self.sut._currently_playing, 0)
        self.assertEqual(self.sut._last_update, None)

    def test_get_currently_playing_station_returns_selected_station(self):
        self.sut.select_station()
        self.assertEqual(self.sut.get_currently_playing_station(), self.station_list[0])

    @mock.patch('time.time', return_value=20)
    def test_should_refresh_when_last_update_is_none_should_return_false(self, mock_time):
        self.sut._currently_playing = 0
        self.assertFalse(self.sut.should_refresh())

    @mock.patch('time.time', return_value=20)
    def test_should_refresh_when_last_update_is_10_seconds_ago_should_return_true(self, mock_time):
        self.sut._currently_playing = 0
        self.sut._last_update = 10
        self.assertTrue(self.sut.should_refresh())

    @mock.patch('time.time', return_value=20)
    def test_should_refresh_when_last_update_is_less_then_10_seconds_ago_should_return_false(self, mock_time):
        self.sut._currently_playing = 0
        self.sut._last_update = 11
        self.assertFalse(self.sut.should_refresh())

    @mock.patch('time.time', return_value=20)
    def test_should_refresh_when_last_update_is_10_seconds_ago_and_nothing_plays_should_return_false(self, mock_time):
        self.sut._last_update = 11
        self.assertFalse(self.sut.should_refresh())

    def test_switch_blacklight_when_true_should_set_backlight_on_to_false(self):
        self.sut.switch_blacklight()

        self.assertFalse(self.sut._backlight_on)
        self.assertIsNone(self.sut._currently_playing)

    def test_switch_blacklight_when_false_should_set_backlight_on_to_true(self):
        self.sut._backlight_on = False

        self.sut.switch_blacklight()

        self.assertTrue(self.sut._backlight_on)
        self.assertIsNone(self.sut._currently_playing)

def create_station_list(amount) -> list:
    station_list = []
    for i in range(amount):
        station_list.append(
            SimpleNamespace(pos=i, image=f"image{i}", name=f"radio {i}", url=f"https://radio-{i}.com"))

    return station_list

if __name__ == '__main__':
    unittest.main()
