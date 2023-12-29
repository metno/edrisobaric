"""Initialize configuration data, open grib file."""

from functools import lru_cache
import os
import sys
import argparse
from datetime import datetime, timedelta
from urllib.request import urlopen, urlretrieve
import xarray as xr
import cgi

dataset = xr.Dataset()


@lru_cache()
def get_base_url() -> str:
    """Return base url."""
    return BASE_URL


def parse_args() -> argparse.Namespace:
    """Parse incoming json argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Grib file to read data from", required=True)
    parser.add_argument(
        "--base_url",
        help="Base URL for API",
        default="http://localhost:5000/",
        required=False,
    )

    return parser.parse_args()


def get_datafile() -> str:
    """Expose path to datafile."""
    return DATAFILE


@lru_cache
def get_data_path() -> str:
    """Returns config parameter object."""
    return "data"


@lru_cache
def get_filename() -> str:
    """Returns config parameter object."""
    # return "data/T_YTNE85_C_ENMI_20231213000000.bin"
    return get_datafile()


def open_grib():
    """Open grib file."""
    global dataset

    print("Opening (or downloading) grib file")
    filename = build_gribfile_name(get_data_path(), time=datetime.now())
    if get_filename() is not None:
        filename = get_filename()
    else:
        if not check_gribfile_exists(data_path=get_data_path(), fname=get_filename()):
            download_gribfile(data_path=get_data_path(), api_url=get_base_url())

    try:
        dataset = xr.open_dataset(filename, engine="cfgrib")
        # print("Variables in file:")
        # for v in dataset:
        #     print(
        #         "Name <%s>   Long name <%s>   Unit <%s>"
        #         % (v, dataset[v].attrs["long_name"], dataset[v].attrs["units"])
        #     )
        # print(dataset.coords)
    except ValueError as err:
        print(
            f"Unable to open file {filename}. Check installation of modules cfgrib, eccodes.\n",
            err,
        )
        print("xarray versions:", xr.show_versions())
        sys.exit(1)


def get_dataset():
    """Get grib dataset."""
    if len(dataset) == 0:
        open_grib()
    return dataset


def build_gribfile_name(data_path: str, time: datetime) -> str:
    """Generate correct name for grib files."""
    filename_prefix = "T_YTNE85_C_ENMI_"
    filename_postfix = ".bin"

    if time is None:
        time = datetime.now()

    while time.hour not in [0, 6, 12, 18, 21]:
        time = time - timedelta(hours=1)

    filename_date = datetime.strftime(time, "%Y%m%d%H0000")  # "20231212060000"
    return data_path + os.path.sep + filename_prefix + filename_date + filename_postfix


def check_gribfile_exists(data_path: str, fname: str) -> bool:
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

    fname = ""
    with urlopen(api_url) as remotefile:
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


args = parse_args()
DATAFILE = args.file
BASE_URL = args.base_url
