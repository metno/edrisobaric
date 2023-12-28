"""Grib specific operations."""

import os
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen, urlretrieve
import cgi
import xarray as xr

# from initialize import get_data_path, get_filename, get_base_url


# Define labels in file
TEMPERATURE_LABEL = "t"
LAT_LABEL = "latitude"
LON_LABEL = "longitude"
UWIND_LABEL = "u"
VWIND_LABEL = "v"
ISOBARIC_LABEL = "isobaricInhPa"


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


def get_vertical_extent() -> list[str]:
    """Find and return a list of vertical levels, decending."""

    # ds[TEMPERATURE_LABEL][ISOBARIC_LABEL].data

    return ["850", "700", "500", "400", "300", "250", "200", "150", "100", "70"]


def get_spatial_extent() -> list[float]:
    """
    Find and return a list of the spatial extent.
    Order is [max lat, min lat, min long, max long](?).
    """
    return [64.25, -1.45, 55.35, 14.51]


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
        print(xr.show_versions())
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
