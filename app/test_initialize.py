import unittest
import os
from datetime import datetime
from initialize import build_gribfile_name, download_gribfile, API_URL, TIME_FORMAT

datafile = ""
data_path = "test_data"


class TestInitialize(unittest.TestCase):
    def test_build_gribfile_name(self):
        time = datetime(2023, 1, 1, 6)
        expected = os.path.join(data_path, "T_YTNE85_C_ENMI_20230101060000.bin")
        actual = build_gribfile_name(data_path, time)
        self.assertEqual(expected, actual)

    def test_build_gribfile_name2(self):
        expected = os.path.join(data_path, "T_YTNE85_C_ENMI_20230101120000.bin")
        actual = build_gribfile_name(data_path, datetime(2023, 1, 1, 13))
        self.assertEqual(expected, actual)

    def test_download_gribfile(self):
        global datafile
        datafile = download_gribfile(data_path=data_path, api_url=API_URL)
        print(datafile)
        self.assertTrue(os.path.isfile(datafile))
        os.remove(datafile)


if __name__ == "__main__":
    unittest.main()
