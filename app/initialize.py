""" Initialize configuration data """

from functools import lru_cache
from datetime import datetime, timedelta
import pytz

@lru_cache()
def get_base_url() -> str:
    """
    Parse configuration file and return base_url
    """
    return "http://localhost:5000/"


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

def get_temporal_extent() -> datetime:
    """ Fetch time from grib filename """
    basename = get_filename().split("/", maxsplit=1)[-1]
    file_timestamp = basename.replace("T_YTNE85_C_ENMI_", "").replace(".bin", "")
    file_time = datetime.strptime(file_timestamp, "%Y%m%d%H0000")

    print("get_temporal_extent", file_time.isoformat())
    return file_time.replace(tzinfo=pytz.UTC)
