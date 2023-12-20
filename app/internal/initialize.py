""" Initialize configuration data """

import sys
from functools import lru_cache
from datetime import datetime
import pytz
import xarray as xr

import app.internal.grib

APP_CONFIG = 'edriso.cnf'
TEMPERATURE_LABEL = "t"
LAT_LABEL = "latitude"
LON_LABEL = "longitude"
UWIND_LABEL = "u"
VWIND_LABEL = "v"

dataset = xr.Dataset()

# from pydantic_settings import BaseSettings  # pydantic v2
# class AppSettings(BaseSettings):
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#         env_prefix = "app_"

#     IS_GOOD_ENV: bool = True


# class InitApplicationConfig():
#     """
#     Initialize configuration for core functionalities in the FastAPI app
#     """
#     def __init__(self, config=APP_CONFIG):
#         self.config = config
#         self.mycnf = configparser.ConfigParser()
#         self.mycnf.read(config)

# def get_application_config(key):
#     """
#     Returns an element from the general application configuration.
#     """
#     config = None
#     try:
#         config = InitApplicationConfig().mycnf[key]
#     except KeyError as err:
#         logging.error("key %s not found in the configuration file %s", err, APP_CONFIG)

#     return config


@lru_cache()
def get_base_url() -> str:
    """
    Parse configuration file and return base_url
    """
    host="http://localhost:8000/"

    # get_application_config("host") or 
    return host


@lru_cache
def get_data_path() -> str:
    """
    Returns config parameter object
    """
    return "data"


@lru_cache
def get_filename() -> str:
    """
    Returns config parameter object
    """
    return "data/T_YTNE85_C_ENMI_20231213000000.bin"


@lru_cache
def get_temporal_extent() -> datetime:
    """Fetch time from grib data"""

    if len(dataset) == 0:
        open_grib()

    initial_time = str(
        dataset[TEMPERATURE_LABEL].time.data
    )  # 2023-12-13T00:00:00.000000000
    timestamp = datetime.strptime(initial_time, "%Y-%m-%dT%H:00:00.000000000")

    print("get_temporal_extent", timestamp.isoformat())
    return timestamp.replace(tzinfo=pytz.UTC)


def open_grib():
    """Open grib file"""
    global dataset

    print("Opening (or downloading) grib file")
    filename = app.internal.grib.build_gribfile_name(get_data_path(), time=datetime.now())
    if get_filename() is not None:
        filename = get_filename()
    else:
        if not app.internal.grib.validate_gribfile(data_path=get_data_path(), fname=get_filename()):
            app.internal.grib.download_gribfile(data_path=get_data_path(), api_url=get_base_url())

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
            f"Unable to open file {filename}. Check installation of python modules cfgrib, eccodes.\n",
            err,
        )
        sys.exit(1)


def get_dataset():
    """Get grib dataset"""
    if len(dataset) == 0:
        open_grib()
    return dataset
