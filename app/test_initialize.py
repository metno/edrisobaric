import unittest
import os
from initialize import download_gribfile, API_URL, open_grib
from grib import get_temporal_extent
from datetime import datetime
import pytz

datafile = ""
data_path = "test_data"


class TestInitialize(unittest.TestCase):
    def test_download_gribfile(self):
        """Test downloading a grib file."""
        datafile = download_gribfile(data_path=data_path, api_url=API_URL)
        self.assertTrue(os.path.isfile(datafile))
        os.remove(datafile)

    def test_open_gribfile(self):
        """Test opening a known grib file."""
        datafile = "../test_data/T_YTNE85_C_ENMI_20240122060000.bin"
        dataset = None
        dataset = open_grib(datafile, dataset)
        self.assertIsNotNone(dataset)

        # Test reading time from a known file
        self.assertEqual(
            get_temporal_extent(dataset),
            datetime(2024, 1, 22, 18, 0, 0, tzinfo=pytz.UTC),
        )


if __name__ == "__main__":
    unittest.main()
