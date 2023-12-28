"""Initialize configuration data."""

import sys
from functools import lru_cache
from datetime import datetime
import argparse
import pytz
import xarray as xr

from grib import (
    TEMPERATURE_LABEL,
    build_gribfile_name,
    check_gribfile_exists,
    download_gribfile,
)


@lru_cache()
def get_base_url() -> str:
    """Return base url."""
    return BASE_URL


@lru_cache
def get_temporal_extent() -> datetime:
    """Fetch time from grib data."""
    if len(dataset) == 0:
        open_grib()

    initial_time = str(
        dataset[TEMPERATURE_LABEL].time.data
    )  # 2023-12-13T00:00:00.000000000
    timestamp = datetime.strptime(initial_time, "%Y-%m-%dT%H:00:00.000000000")

    print("get_temporal_extent", timestamp.isoformat())
    return timestamp.replace(tzinfo=pytz.UTC)


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
        sys.exit(1)


def get_dataset():
    """Get grib dataset."""
    if len(dataset) == 0:
        open_grib()
    return dataset


@lru_cache
def get_data_path() -> str:
    """Returns config parameter object."""
    return "data"


@lru_cache
def get_filename() -> str:
    """Returns config parameter object."""
    # return "data/T_YTNE85_C_ENMI_20231213000000.bin"
    return get_datafile()


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


dataset = xr.Dataset()
args = parse_args()
DATAFILE = args.file
BASE_URL = args.base_url
