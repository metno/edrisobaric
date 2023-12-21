"""Grib specific operations."""

import os
from datetime import datetime, timedelta
from urllib.request import urlopen, urlretrieve
import cgi


def build_gribfile_name(data_path: str, time: datetime) -> str:
    """Generate correct name for grib files."""
    filename_prefix = "T_YTNC85_C_ENMI_"
    filename_postfix = ".bin"

    if time is None:
        time = datetime.now()

    while time.hour not in [0, 6, 12, 18, 21]:
        time = time - timedelta(hours=1)

    filename_date = datetime.strftime(time, "%Y%m%d%H0000")  # "20231212060000"
    return data_path + os.path.sep + filename_prefix + filename_date + filename_postfix


def validate_gribfile(data_path: str, fname: str) -> bool:
    """Fetch latest grib-file."""
    if not os.path.isfile(data_path + os.pathsep + fname):
        print("Datafile with name %s not found", fname)
        return False
    return True


def download_gribfile(data_path: str, api_url: str):
    """Ensure data dir exists, download latest file."""
    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass

    remotefile = urlopen(api_url)
    contentdisposition = remotefile.info()["Content-Disposition"]
    _, params = cgi.parse_header(contentdisposition)
    fname = data_path + os.path.sep + params["filename"]

    if os.path.exists(fname):
        print(
            "Latest file is %s, already have that. Skipping download.",
            params["filename"],
        )
        return

    print("Downloading %s to path %s", api_url, fname)
    urlretrieve(api_url, fname)
