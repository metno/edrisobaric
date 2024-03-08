"""Collections page."""
from typing import List, Tuple, Annotated
import logging
from fastapi import APIRouter, status, Request, Query
from fastapi.responses import JSONResponse
import xarray as xr
from pydantic import AwareDatetime
from shapely import wkt, GEOSException, Point
import covjson_pydantic
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.ndarray import NdArray
from math import atan2, pi, sqrt

from initialize import (
    get_dataset,
    CELSIUS_SYMBOL,
    CELSIUS_ID,
    DEGREE_SYMBOL,
    DEGREE_ID,
)

from grib import (
    get_vertical_extent,
    get_temporal_extent,
    TEMPERATURE_LABEL,
    LAT_LABEL,
    LON_LABEL,
    UWIND_LABEL,
    VWIND_LABEL,
    ISOBARIC_LABEL,
)

POINT_REGEX = "^POINT\\(\\d+\\.?\\d* \\d+\\.?\\d*\\)$"
PRECISION = 2

router = APIRouter()
logger = logging.getLogger()


# Query for both position routes
coords_query = Query(
    min_length=9,
    pattern=POINT_REGEX,
    description="Coordinates, formated as a WKT point: POINT(11.9384 60.1699)",
    openapi_examples={
        "Oslo": {
            "summary": "Henrik Mohns Plass 1",
            "description": "Fetch data for a position in Oslo",
            "value": "POINT(11.9384 60.1699)",
        },
        "Asker": {
            "summary": "Asker",
            "description": "Fetch data for a position in Asker",
            "value": "POINT(10.45 59.83)",
        },
    },
)


def wind_speed_from_u_v(u, v):
    """Calculate wind speed from u and v wind components.

    Example copied from
    <https://spire.com/tutorial/how-to-process-grib2-weather-data-for-wind-turbine-applications-shapefile/>.
    """
    return sqrt(pow(u, 2) + pow(v, 2))


def wind_direction_from_u_v(u, v):
    """Calculate wind direction from u and v wind components.

    Example copied from
    <https://spire.com/tutorial/how-to-process-grib2-weather-data-for-wind-turbine-applications-shapefile/>.
    """
    if (u, v) == (0.0, 0.0):
        return 0.0
    return (180.0 / pi) * atan2(u, v) + 180.0


def create_point(coords: str) -> dict:
    """Return data for all isometric layers at a point."""
    # Parse coordinates given as WKT
    point = Point()
    try:
        point = wkt.loads(coords)
    except GEOSException:
        errmsg = (
            "Error, coords should be a Well Known Text, for example "
            + f"POINT(11.0 59.0). You gave <{coords}>"
        )
        logger.error(errmsg)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [
                    {
                        "type": "string",
                        "loc": ["query", "coords"],
                        "msg": errmsg,
                        "input": coords,
                    }
                ]
            },
        )

    logger.info("create_data for coord %s, %s", point.y, point.x)
    dataset = get_dataset()

    # Sanity check on coordinates
    coords_ok, errcoords = check_coords_within_bounds(dataset, point)
    if not coords_ok:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=errcoords
        )

    # Fetch temperature data for point
    temperatures = dataset[TEMPERATURE_LABEL].sel(
        longitude=point.x, latitude=point.y, method="nearest"
    )

    isobaric_values = get_vertical_extent(dataset)
    temperature_values: List[float] = []
    wind_dir: List[float] = []
    wind_speed: List[float] = []

    # For each temperature value found:
    for temperature in temperatures:
        # Convert temperature from Kelvin to Celsius
        temperature_values.append(round(float(temperature.data) - 273.15, PRECISION))

        # Fetch wind
        uwind = dataset[UWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )

        vwind = dataset[VWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )

        wind_dir.append(
            round(wind_direction_from_u_v(uwind.data, vwind.data), PRECISION)
        )
        wind_speed.append(round(wind_speed_from_u_v(uwind.data, vwind.data), PRECISION))

    cov = Coverage(
        id="isobaric",
        type="Coverage",
        domain=covjson_pydantic.domain.Domain(
            domainType=covjson_pydantic.domain.DomainType.vertical_profile,
            axes=covjson_pydantic.domain.Axes(
                x=covjson_pydantic.domain.ValuesAxis[float](values=[point.x]),
                y=covjson_pydantic.domain.ValuesAxis[float](values=[point.y]),
                z=covjson_pydantic.domain.ValuesAxis[float](values=isobaric_values),
                t=covjson_pydantic.domain.ValuesAxis[AwareDatetime](
                    values=[get_temporal_extent(dataset)]
                ),
            ),
            referencing=[
                covjson_pydantic.reference_system.ReferenceSystemConnectionObject(
                    coordinates=["x", "y"],
                    system=covjson_pydantic.reference_system.ReferenceSystem(
                        id="http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                        type="GeographicCRS",
                    ),
                ),
                covjson_pydantic.reference_system.ReferenceSystemConnectionObject(
                    coordinates=["z"],
                    system=covjson_pydantic.reference_system.ReferenceSystem(
                        type="VerticalCRS",
                        cs={
                            "csAxes": [
                                {
                                    "name": {"en": "Pressure"},
                                    "direction": "down",
                                    "unit": {"symbol": "hPa"},
                                }
                            ]
                        },
                    ),
                ),
                covjson_pydantic.reference_system.ReferenceSystemConnectionObject(
                    coordinates=["t"],
                    system=covjson_pydantic.reference_system.ReferenceSystem(
                        type="TemporalRS", calendar="Gregorian"
                    ),
                ),
            ],
        ),
        ranges={
            "temperature": NdArray(
                axisNames=["z"],
                shape=[len(isobaric_values)],
                values=temperature_values,
            ),
            "wind_from_direction": NdArray(
                axisNames=["z"],
                shape=[len(isobaric_values)],
                values=wind_dir,
            ),
            "wind_speed": NdArray(
                axisNames=["z"],
                shape=[len(isobaric_values)],
                values=wind_speed,
            ),
        },
        parameters={
            "temperature": covjson_pydantic.parameter.Parameter(
                id="temperature",
                label={"en": "Air temperature"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="http://vocab.met.no/CFSTDN/en/page/air_temperature",
                    label={"en": "Air temperature"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id=CELSIUS_ID,
                    label={"en": "degree Celsius"},
                    symbol=CELSIUS_SYMBOL,
                ),
            ),
            "wind_from_direction": covjson_pydantic.parameter.Parameter(
                id="wind_from_direction",
                label={"en": "Wind from direction"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="http://vocab.met.no/CFSTDN/en/page/wind_from_direction",
                    label={"en": "wind_from_direction"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id=DEGREE_ID,
                    label={"en": "degree"},
                    symbol=DEGREE_SYMBOL,
                ),
            ),
            "wind_speed": covjson_pydantic.parameter.Parameter(
                id="wind_speed",
                label={"en": "Wind speed"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="http://vocab.met.no/CFSTDN/en/page/wind_speed",
                    label={"en": "Wind speed"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id="https://codes.wmo.int/common/unit/_m_s-1",
                    label={"en": "metres per second "},
                    symbol="m/s",
                ),
            ),
        },
    )

    return cov.model_dump(exclude_none=True)


def check_coords_within_bounds(ds: xr.Dataset, point: Point) -> Tuple[bool, dict]:
    """Check coordinates are within bounds of dataset."""
    errmsg = {}
    if (
        point.y > ds[TEMPERATURE_LABEL][LAT_LABEL].values.max()
        or point.y < ds[TEMPERATURE_LABEL][LAT_LABEL].values.min()
    ):
        errmsg = {
            "detail": [
                {
                    "loc": ["string", 0],
                    "msg": f"Error, coord {point.y} out of bounds. Min/max is "
                    + f"{ds[TEMPERATURE_LABEL][LAT_LABEL].values.min()}/"
                    + f"{ds[TEMPERATURE_LABEL][LAT_LABEL].values.max()}",
                    "type": "string",
                    "input": point.y,
                }
            ]
        }
        logger.error(errmsg)
        return False, errmsg

    if (
        point.x > ds[TEMPERATURE_LABEL][LON_LABEL].values.max()
        or point.x < ds[TEMPERATURE_LABEL][LON_LABEL].values.min()
    ):
        errmsg = {
            "detail": [
                {
                    "loc": ["string", 0],
                    "msg": "Error, coord {point.x} out of bounds. Min/max is "
                    + f"{ds[TEMPERATURE_LABEL][LON_LABEL].values.min()}/"
                    + f"{ds[TEMPERATURE_LABEL][LON_LABEL].values.max()}",
                    "type": "string",
                    "input": point.x,
                }
            ]
        }
        logger.error(errmsg)
        return False, errmsg
    return True, errmsg


@router.get(
    "/collections/isobaric/position",
    tags=["Collection Data"],
    response_model=Coverage,
    response_model_exclude_unset=True,
)
async def get_isobaric_page(
    request: Request,
    coords: Annotated[str, coords_query],
) -> dict:
    """Return data closest to a position."""
    if len(coords) == 0:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "body": {
                    "detail": [
                        {
                            "loc": ["string", 0],
                            "msg": "Error: No coordinates provided. Example: "
                            + f'{str(request.base_url)[0:-1]}{request.scope["path"]}'
                            + "?coords=POINT(11.9384%2060.1699)",
                            "type": "string",
                        }
                    ]
                }
            },
        )

    return create_point(coords=coords)
