"""Initialize configuration data, open grib file."""

import os
import sys
import argparse
import logging
from datetime import datetime
import xarray as xr
import requests

from grib import ISOBARIC_LABEL, TEMPERATURE_LABEL

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
CELSIUS_ID = "https://codes.wmo.int/common/unit/_Cel"
AIRTEMP_ID = "http://vocab.met.no/CFSTDN/en/page/air_temperature"
WINDDIR_ID = "http://vocab.met.no/CFSTDN/en/page/wind_from_direction"
WINDSPEED_ID = "http://vocab.met.no/CFSTDN/en/page/wind_speed"
DEGREE_SYMBOL = "˚"
DEGREE_ID = "https://codes.wmo.int/common/unit/_degree_(angle)"
CONTACT_EMAIL = "weatherapi-adm@met.no"
CRS_SHORT = "CRS:84"
CRS_LONG = (
    'GEOGCS["Unknown", DATUM["Unknown", SPHEROID["WGS_1984", 6378137.0, '
    + '298.257223563]], PRIMEM["Greenwich",0], UNIT["degree", 0.017453], '
    + 'AXIS["Lon", EAST], AXIS["Lat", NORTH]]'
)
DATA_PATH = "./data"


def parse_args() -> argparse.Namespace:
    """Parse arguments for grib filename and URL."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
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
    parser.add_argument(
        "--file",
        help=("Local grib file to read data from. Default will fetch file from API.\n"),
        default="",
    )
    parser.add_argument(
        "--base_url",
        help="Base URL for API, with a trailing slash. Default is http://localhost:5000/",
        default="http://localhost:5000/",
        required=False,
    )
    parser.add_argument(
        "--bind_host",
        help="Which host to bind to. Default is 127.0.0.1. Use 0.0.0.0 when running in container.",
        default="127.0.0.1",
        required=False,
    )
    parser.add_argument(
        "--api_url",
        help=f"URL to download grib file from. Default is <{DEFAULT_API_URL}>.",
        default=DEFAULT_API_URL,
        required=False,
    )
    parser.add_argument(
        "--data_path",
        help=f"Where to store data files. Default is {DATA_PATH}",
        default=DATA_PATH,
        required=False,
    )
    return parser.parse_args()


def open_grib(datafile: str, dataset: xr.Dataset, timestamp: str = "") -> xr.Dataset:
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
    if os.access(os.path.dirname(datafile), os.W_OK):
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
        print("open_grib Error: ", err)
        return None
    if not validate_grib(dataset):
        return None
    return dataset


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
    global dataset

    if len(dataset) == 0:
        dataset = open_grib(DATAFILE, dataset, TIME)
        if dataset is None:
            print(
                f"get_dataset Error: Unable to open grib file. DATAFILE {DATAFILE}, TIME {TIME}"
            )
            sys.exit(1)
    return dataset


def download_gribfile(data_path: str, api_url: str) -> str:
    """Download latest file. Return filename."""
    fname = ""

    # Ensure data dir exists
    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass

    # Download file
    response = requests.get(api_url, timeout=30)
    if response.status_code != 200:
        error = (
            f"Error: Unable to download data file. Status code {response.status_code}."
        )
        if TIME:
            error += f" Check if time {TIME} exists in available data set at <{AVAILABLE_API}>."
        print(error)
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
    for f in os.listdir(data_path):
        if f.startswith(fname) and f.endswith(".idx"):
            logger.warning("Removing index file %s", f)
            os.remove(f)

    return fname


def validate_time_input(t: str) -> bool:
    """Validate time string."""
    if len(t) > 0:
        try:
            test_time = datetime.strptime(
                t, "%Y-%m-%dT%H:00:00Z"
            )  # 2024-01-24T18:00:00Z
            if test_time.hour % 3 != 0:
                print(
                    f"Time must be a whole 3 hour interval (00, 03, 06, 09, 12, 15, 18, 21). You gave {t}"
                )
                return False
        except ValueError:
            print(f"Time must be on format 2024-01-24T18:00:00Z. You gave {t}.")
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
