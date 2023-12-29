"""Grib contents operations."""

from datetime import datetime
import pytz
import xarray as xr

# from initialize import get_data_path, get_filename, get_base_url


# Define labels in file
TEMPERATURE_LABEL = "t"
LAT_LABEL = "latitude"
LON_LABEL = "longitude"
UWIND_LABEL = "u"
VWIND_LABEL = "v"
ISOBARIC_LABEL = "isobaricInhPa"


def get_vertical_extent() -> list[str]:
    """Find and return a list of vertical levels, decending."""
    # ds[TEMPERATURE_LABEL][ISOBARIC_LABEL].data
    return ["850", "700", "500", "400", "300", "250", "200", "150", "100", "70"]


def get_spatial_extent() -> list[float]:
    """Find and return a list of the spatial extent.

    Order: [max lat, min lat, min long, max long](?).
    """
    return [64.25, -1.45, 55.35, 14.51]


def get_temporal_extent(dataset: xr.Dataset) -> datetime:
    """Fetch time from grib data."""
    initial_time = str(
        dataset[TEMPERATURE_LABEL].time.data
    )  # 2023-12-13T00:00:00.000000000
    timestamp = datetime.strptime(initial_time, "%Y-%m-%dT%H:00:00.000000000")

    return timestamp.replace(tzinfo=pytz.UTC)
