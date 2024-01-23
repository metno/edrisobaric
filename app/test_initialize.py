import unittest
import os
from initialize import download_gribfile, API_URL

datafile = ""
data_path = "test_data"


class TestInitialize(unittest.TestCase):
    def test_download_gribfile(self):
        global datafile
        datafile = download_gribfile(data_path=data_path, api_url=API_URL)
        self.assertTrue(os.path.isfile(datafile))
        os.remove(datafile)


if __name__ == "__main__":
    unittest.main()
