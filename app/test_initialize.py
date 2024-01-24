import unittest
import os
from initialize import download_gribfile, API_URL, open_grib, validate_time_input
from grib import get_temporal_extent
from datetime import datetime
import pytz

datafile = ""
data_path = "test_data"


class TestInitialize(unittest.TestCase):
    def test_download_gribfile(self):
        """Test downloading a grib file."""
        datafile = download_gribfile(data_path="/tmp", api_url=API_URL)
        self.assertTrue(os.path.isfile(datafile))
        os.remove(datafile)

    def test_open_gribfile(self):
        """Test opening a known grib file."""
        dataset = None
        datafile = "test_data/T_YTNE85_C_ENMI_20240122060000.bin"
        if not os.path.exists(data_path):
            datafile = "../" + datafile
        print(f"Current dir {os.getcwd()}. Datafile {datafile}.")

        dataset = open_grib(datafile, dataset)
        self.assertIsNotNone(dataset)

        # Test reading time from a known file
        self.assertEqual(
            get_temporal_extent(dataset),
            datetime(2024, 1, 22, 18, 0, 0, tzinfo=pytz.UTC),
        )

    def test_validate_time_input(self):
        """Test that a valid time input is parsed correctly."""
        self.assertTrue(validate_time_input("2024-01-22T18:00:00Z"))
        self.assertFalse(validate_time_input("2024-01-2218:00:00Z"))
        self.assertFalse(validate_time_input("2024-01-22T19:00:00Z"))


if __name__ == "__main__":
    unittest.main()
