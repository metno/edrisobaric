"""Initialize configuration data, open grib file."""

import argparse
import contextlib
import logging
import os
import sys
from datetime import datetime

import requests
import xarray as xr

from edriso.grib import ISOBARIC_LABEL, TEMPERATURE_LABEL

dataset = xr.Dataset()
logger = logging.getLogger()

# Constants used throughout

DEFAULT_API_URL = (
    "https://api.met.no/weatherapi/isobaricgrib/1.0/grib2?area=southern_norway"
)
AVAILABLE_API = (
    "https://api.met.no/weatherapi/isobaricgrib/1.0/available.json?type=grib2"
)
TIME_FORMAT = "%Y-%m-%dT%H:00:00Z"  #  RFC3339 date-time
CELSIUS_SYMBOL = "˚C"
CELSIUS_ID = "https://qudt.org/vocab/unit/DEG_C"
AIRTEMP_ID = "https://vocab.nerc.ac.uk/standard_name/air_temperature/"
WINDDIR_ID = "https://vocab.nerc.ac.uk/standard_name/wind_from_direction/"
WINDSPEED_ID = "https://vocab.nerc.ac.uk/standard_name/wind_speed/"
SPEED_ID = "https://qudt.org/vocab/unit/M-PER-SEC"
DEGREE_SYMBOL = "˚"
DEGREE_ID = "https://qudt.org/vocab/unit/DEG"
CONTACT_EMAIL = "weatherapi-adm@met.no"
CRS_SHORT = "OGC:CRS84"

DATA_PATH = "./data"
COLLECTION_NAME = "weather_forecast"


def parse_args() -> argparse.Namespace:
    """Parse arguments for grib filename and URL."""
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "--time",
        help=(
            "Timestamp to fetch data for. Must be in format 2024-01-24T18:00:00Z, "
            + "where time matches an available production.\n"
            + f"See <{AVAILABLE_API}> "
            + "for available files. They are produced every 3rd hour. \nExample: "
            + '--datetime="2024-01-24T18:00:00Z"'
        ),
        default="",
    )
    _ = parser.add_argument(
        "--file",
        help=("Local grib file to read data from. Default will fetch file from API.\n"),
        default="",
    )
    _ = parser.add_argument(
        "--base_url",
        help="Base URL for API, with a trailing slash. Default is http://localhost:5000/",
        default="http://localhost:5000/",
        required=False,
    )
    _ = parser.add_argument(
        "--bind_host",
        help="Which host to bind to. Default is 127.0.0.1. Use 0.0.0.0 when running in container.",
        default="127.0.0.1",
        type=str,
        required=False,
    )
    _ = parser.add_argument(
        "--api_url",
        help=f"URL to download grib file from. Default is <{DEFAULT_API_URL}>.",
        default=DEFAULT_API_URL,
        required=False,
    )
    _ = parser.add_argument(
        "--data_path",
        help=f"Where to store data files. Default is {DATA_PATH}",
        default=DATA_PATH,
        required=False,
    )
    return parser.parse_args()


def open_grib(
    datafile: str, dataset: xr.Dataset, timestamp: str = ""
) -> xr.Dataset | None:
    """Open grib file, return dataset."""
    filename = ""

    # If nothing given, download default given by API
    if len(datafile) == 0 and timestamp == "":
        filename = download_gribfile(data_path=DATA_PATH, api_url=API_URL)
    else:
        # If timestamp is given, download file for that time
        if timestamp:
            filename = download_gribfile(
                data_path=DATA_PATH, api_url=f"{API_URL}&time={timestamp}"
            )

        # If datafile is a filename, open that file
        else:
            filename = datafile

    # Check if dir is writable
    indexpath = ""
    if os.access(os.path.dirname(filename), os.W_OK):
        indexpath = filename + ".idx"

    try:
        logger.info("Opening data file %s", filename)
        dataset = xr.open_dataset(
            filename, engine="cfgrib", decode_cf=True, indexpath=indexpath
        )
    except ValueError as err:
        logger.error(
            "Unable to open file %s. Check installation of modules cfgrib, eccodes.\n%s",
            filename,
            err,
        )
        logger.info("xarray versions: %s", xr.show_versions())
        return None
    except FileNotFoundError as err:
        logger.error("open_grib Error: %s", err)
        return None
    if not validate_grib(dataset):
        return None
    return dataset


def validate_grib(ds: xr.Dataset) -> bool:
    """Check that variables are as expected."""
    if len(ds[ISOBARIC_LABEL]) < 10:
        logger.error("Error: Count of ISOBARIC_LABEL in file is unexpected")
        return False
    if TEMPERATURE_LABEL not in ds:
        logger.error("Error: TEMPERATURE_LABEL not found in file")
        return False

    return True


def get_dataset() -> xr.Dataset:
    """Get grib dataset."""
    global dataset

    if len(dataset) == 0:
        result = open_grib(DATAFILE, dataset, TIME)
        if result is None:
            logger.error(
                "get_dataset Error: Unable to open grib file. DATAFILE %s, TIME %s",
                DATAFILE,
                TIME,
            )
            sys.exit(1)
        dataset = result
    return dataset


def download_gribfile(data_path: str, api_url: str) -> str:
    """Download latest file. Return filename."""
    # Ensure data dir exists
    with contextlib.suppress(FileExistsError):
        os.mkdir(data_path)

    # Download file
    response = requests.get(api_url, timeout=30)
    if response.status_code != 200:
        error = (
            f"Error: Unable to download data file. Status code {response.status_code}."
        )
        if TIME:
            error += f" Check if time {TIME} exists in available data set at <{AVAILABLE_API}>."
        logger.error(error)
        sys.exit(1)

    fname = (
        data_path
        + os.path.sep
        + str(response.headers.get("Content-Disposition"))
        .split("filename=")[1]
        .replace('"', "")
    )

    # The filenames are not to be trusted, so we download and overwrite every time.
    logger.warning("Downloading %s to path %s.", api_url, fname)
    with open(fname, "wb") as fd:
        for chunk in response.iter_content(chunk_size=524288):
            fd.write(chunk)
    logger.info("Download done.")

    # Remove index file if exists
    index_path = os.path.join(data_path, fname + ".idx")
    if os.path.exists(index_path):
        logger.warning("Removing index file %s", index_path)
        os.remove(index_path)

    return fname


def validate_time_input(t: str) -> bool:
    """Validate time string."""
    if len(t) > 0:
        try:
            test_time = datetime.strptime(
                t, "%Y-%m-%dT%H:00:00Z"
            )  # 2024-01-24T18:00:00Z
            if test_time.hour % 3 != 0:
                logger.error(
                    "Time must be a whole 3 hour interval (00, 03, 06, 09, 12, 15, 18, 21). You gave %s",
                    t,
                )
                return False
        except ValueError:
            logger.error("Time must be on format 2024-01-24T18:00:00Z. You gave %s.", t)
            return False
    return True


args = parse_args()
DATAFILE = args.file
TIME = args.time
BASE_URL = args.base_url
BIND_HOST = args.bind_host
API_URL = args.api_url
DATA_PATH = args.data_path

# Validate time
if not validate_time_input(args.time):
    sys.exit(1)

if len(DATAFILE) > 0 and TIME:
    sys.exit("Cannot specify both --file and --time")
