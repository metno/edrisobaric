"""Grib contents operations."""

from datetime import datetime
import pytz
import xarray as xr


# Define labels in grib file
TEMPERATURE_LABEL = "t"
LAT_LABEL = "latitude"
LON_LABEL = "longitude"
UWIND_LABEL = "u"
VWIND_LABEL = "v"
ISOBARIC_LABEL = "isobaricInhPa"


def get_vertical_extent(dataset: xr.Dataset) -> list[str]:
    """Find and return a list of vertical levels, decending."""
    float_list = dataset[TEMPERATURE_LABEL][ISOBARIC_LABEL].data.tolist()
    str_list = [str(float_list[i]) for i in range(len(float_list))]
    return str_list


def get_spatial_extent(dataset: xr.Dataset) -> list[float]:
    """Find and return a list of the spatial extent.

    From the standard:

    bbox=minx,miny,maxx,maxy.

    The X and Y coordinates are values in the coordinate system defined by the
    crs query parameter. If crs is not defined, the values will be assumed to
    be WGS84 longitude/latitude coordinates and heights will be assumed to be
    in meters above mean sea level, or below for negative values.
    """
    return [
        dataset.coords[LON_LABEL].data.min(),
        dataset.coords[LAT_LABEL].data.min(),
        dataset.coords[LON_LABEL].data.max(),
        dataset.coords[LAT_LABEL].data.max(),
    ]


def get_temporal_extent(dataset: xr.Dataset) -> datetime:
    """Fetch time from grib data."""
    initial_time = str(
        dataset[TEMPERATURE_LABEL].valid_time.data
    )  # 2023-12-13T00:00:00.000000000
    timestamp = datetime.strptime(initial_time, "%Y-%m-%dT%H:00:00.000000000")
    return timestamp.replace(tzinfo=pytz.UTC)
