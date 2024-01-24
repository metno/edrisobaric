"""Initialize configuration data, open grib file."""

from functools import lru_cache
import os
import sys
import argparse
import logging
import xarray as xr
import requests

from grib import ISOBARIC_LABEL, TEMPERATURE_LABEL

dataset = xr.Dataset()
logger = logging.getLogger()

# Constants used throughout

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


def parse_args() -> argparse.Namespace:
    """Parse arguments for grib filename and URL."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help=(
            "Grib file or URL to read data from. Default will fetch latest file.\n"
            + "See <https://api.met.no/weatherapi/isobaricgrib/1.0/available.json?type=grib2> "
            + "for available files.\nExample: "
            + '--file="https://api.met.no/weatherapi/isobaricgrib/1.0/grib2?area=southern_norway&time=2024-01-24T18:00:00Z"'
        ),
        default="",
    )
    parser.add_argument(
        "--base_url",
        help="Base URL for API, with a trailing slash.",
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


def open_grib(datafile: str, dataset: xr.Dataset) -> xr.Dataset:
    """Open grib file, return dataset."""
    filename = ""

    # If nothing given, download nearest date
    if len(datafile) == 0:
        filename = download_gribfile(data_path=get_data_path(), api_url=API_URL)
    else:
        # If datafile is a URL, download that file
        if datafile.startswith("http"):
            filename = download_gribfile(data_path=get_data_path(), api_url=datafile)

        # If datafile is a filename, open that file
        else:
            filename = datafile

    try:
        logger.info("Opening data file %s", filename)
        dataset = xr.open_dataset(filename, engine="cfgrib")
    except ValueError as err:
        logger.error(
            "Unable to open file %s. Check installation of modules cfgrib, eccodes.\n%s",
            filename,
            err,
        )
        logger.info("xarray versions: %s", xr.show_versions())
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
        dataset = open_grib(DATAFILE, dataset)
        if dataset is None:
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

    response = requests.get(api_url, timeout=30)
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


args = parse_args()
DATAFILE = args.file
BASE_URL = args.base_url
BIND_HOST = args.bind_host
API_URL = args.api_url
