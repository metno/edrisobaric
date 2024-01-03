"""Initialize configuration data, open grib file."""

from functools import lru_cache
import os
import sys
import argparse
from datetime import datetime, timedelta
import logging
import xarray as xr
import requests

from grib import ISOBARIC_LABEL, TEMPERATURE_LABEL


API_URL = "https://api.met.no/weatherapi/isobaricgrib/1.0/grib2?area=southern_norway"
dataset = xr.Dataset()
logger = logging.getLogger()


def parse_args() -> argparse.Namespace:
    """Parse arguments for grib filename and URL."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Grib file to read data from", default="")
    parser.add_argument(
        "--base_url",
        help="Base URL for API",
        default="http://localhost:5000/",
        required=False,
    )
    parser.add_argument(
        "--bind_host",
        help="Which host to bind to.",
        default="0.0.0.0",
        required=False,
    )
    return parser.parse_args()


@lru_cache
def get_data_path() -> str:
    """Returns directory to grib file."""
    return "data"


@lru_cache
def get_filename() -> str:
    """Returns config parameter object."""
    return DATAFILE


def open_grib():
    """Open grib file."""
    global dataset

    filename = build_gribfile_name(get_data_path(), time=datetime.now())
    if len(DATAFILE) > 0:
        filename = DATAFILE
    else:
        if not check_gribfile_exists(data_path=get_data_path(), fname=DATAFILE):
            filename = download_gribfile(data_path=get_data_path())

    try:
        dataset = xr.open_dataset(filename, engine="cfgrib")
    except ValueError as err:
        logger.error(
            "Unable to open file %s. Check installation of modules cfgrib, eccodes.\n%s",
            filename,
            err,
        )
        logger.info("xarray versions: %s", xr.show_versions())
        sys.exit(1)
    if not validate_grib(dataset):
        sys.exit(1)


def validate_grib(ds: xr.Dataset) -> bool:
    """Check that variables are as expected."""
    # print(dataset.coords)
    # print("Variables in file:")
    # for v in ds:
    #     print(
    #         "Name <%s>   Long name <%s>   Unit <%s>"
    #         % (v, ds[v].attrs["long_name"], dataset[v].attrs["units"])
    #     )

    if len(ds[ISOBARIC_LABEL]) < 10:
        logger.error("Error: Count of ISOBARIC_LABEL in file is unexpected")
        return False
    if ds[TEMPERATURE_LABEL] is None:
        logger.error("Error: Count of TEMPERATURE_LABEL in file is unexpected")
        return False

    return True


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
    """Check if grib file exists."""
    if len(fname) == 0:
        # print("check_gribfile_exists: No filename given.")
        return False
    if not os.path.isfile(data_path + os.pathsep + fname):
        logger.info("check_gribfile_exists: Datafile with name %s not found", fname)
        return False
    return True


def download_gribfile(data_path: str, api_url: str = API_URL) -> str:
    """Ensure data dir exists, download latest file. Returns filename."""
    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass

    fname = ""
    response = requests.get(api_url, timeout=30)
    fname = (
        data_path
        + os.path.sep
        + str(response.headers.get("Content-Disposition"))
        .split("filename=")[1]
        .replace('"', "")
    )

    if os.path.exists(fname):
        logger.info("Latest file is %s, already have that. Skipping download.", fname)
        return fname

    logger.info("Downloading %s to path %s.", api_url, fname)
    with open(fname, "wb") as fd:
        for chunk in response.iter_content(chunk_size=524288):
            fd.write(chunk)
    logger.info("Download done.")
    return fname


args = parse_args()
DATAFILE = args.file
BASE_URL = args.base_url
BIND_HOST = args.bind_host
