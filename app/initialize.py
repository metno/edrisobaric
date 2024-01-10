"""Initialize configuration data, open grib file."""

from functools import lru_cache
import os
import sys
import argparse
from typing import Tuple
from datetime import datetime, timedelta
import logging
import xarray as xr
import requests
from fastapi import Path

from grib import ISOBARIC_LABEL, TEMPERATURE_LABEL, get_temporal_extent

dataset = xr.Dataset()
logger = logging.getLogger()
TIME_FORMAT = "%Y-%m-%dT%H:00:00Z"  #  RFC3339 date-time


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
        default="127.0.0.1",
        required=False,
    )
    parser.add_argument(
        "--api_url",
        help="URL to download grib file from",
        default="https://api.met.no/weatherapi/isobaricgrib/1.0/grib2?area=southern_norway",
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


def open_grib() -> None:
    """Open grib file."""
    global dataset

    filename = build_gribfile_name(get_data_path(), time=datetime.now())
    if len(DATAFILE) > 0:
        filename = DATAFILE
    else:
        if not check_gribfile_exists(data_path=get_data_path(), fname=DATAFILE):
            filename = download_gribfile(data_path=get_data_path(), api_url=API_URL)

    try:
        dataset = xr.open_dataset(filename, engine="cfgrib")
        logger.info("Opened data file %s", filename)
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


def get_dataset() -> xr.Dataset:
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


def download_gribfile(data_path: str, api_url: str) -> str:
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

    logger.warning("Downloading %s to path %s.", api_url, fname)
    with open(fname, "wb") as fd:
        for chunk in response.iter_content(chunk_size=524288):
            fd.write(chunk)
    logger.info("Download done.")
    return fname


def format_instance_id(timestamp: datetime) -> str:
    return timestamp.strftime(TIME_FORMAT)


def check_instance_exists(ds: xr.Dataset, instance_id: str) -> Tuple[bool, dict]:
    """Check instance id exists in dataset."""
    instance_dates = [get_temporal_extent(ds)]
    for d in instance_dates:
        if format_instance_id(d) == instance_id:
            logger.info("instance_id %s is valid", instance_id)
            return True, {}

    logger.error("instance_id %s does not exist in dataset", instance_id)
    valid_dates = [format_instance_id(x) for x in instance_dates]
    return (
        False,
        {
            "detail": [
                {
                    "type": "string",
                    "loc": ["query", "instance"],
                    "msg": f"instance_id {instance_id} does not exist in dataset. Valid dates are {valid_dates}.",
                    "input": instance_id,
                }
            ]
        },
    )


args = parse_args()
DATAFILE = args.file
BASE_URL = args.base_url
BIND_HOST = args.bind_host
API_URL = args.api_url


# There is only one instance available. Load and lock.
instance_id = get_temporal_extent(get_dataset()).strftime(TIME_FORMAT)
instance_path = Path(
    min_length=20,
    max_length=20,
    pattern="^" + instance_id + "$",
    title=f"Instance ID, consisting of date in format {TIME_FORMAT}",
    description=f"Only available instance is {instance_id}",
)
