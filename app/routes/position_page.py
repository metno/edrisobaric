"""Collections page."""
from typing import List, Tuple, Annotated, Union
import logging
from fastapi import APIRouter, status, Response, Request, Query
from fastapi.responses import JSONResponse
import xarray as xr
from pydantic import AwareDatetime
from shapely import wkt, GEOSException, Point
import covjson_pydantic
import covjson_pydantic.coverage
from covjson_pydantic.ndarray import NdArray
from covjson_pydantic.domain import ValuesAxis, DomainType

from initialize import get_dataset, check_instance_exists, instance_path

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

router = APIRouter()
logger = logging.getLogger()


"""
    Workaround for nulls.

    The following classes overrides Axes from having optional values. In 
    pydantic v2 optinal values causes "anyOf null" in the openapi schema.
    This breaks validation.

    My workaround is unsustainable, as there are about 117 more nulls in my
    current schema.

    Ref.
    - https://github.com/KNMI/covjson-pydantic/issues/8
    - https://github.com/tiangolo/fastapi/pull/9873
"""


class Axes(covjson_pydantic.domain.Axes):
    x: ValuesAxis[float]
    y: ValuesAxis[float]
    z: ValuesAxis[float]
    t: ValuesAxis[AwareDatetime]
    composite: bool = False


class Domain(covjson_pydantic.domain.Domain):
    domainType: DomainType
    axes: Axes


class Coverage(covjson_pydantic.coverage.Coverage):
    domain: Domain


def create_point(coords: str, instance_id: str = "") -> dict:
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

    # Sanity check on instance id
    if len(instance_id) > 0:
        instance_ok, errinstance = check_instance_exists(dataset, instance_id)
        if not instance_ok:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST, content=errinstance
            )

    # Fetch temperature
    temperatures = dataset[TEMPERATURE_LABEL].sel(
        longitude=point.x, latitude=point.y, method="nearest"
    )

    isobaric_values = get_vertical_extent(dataset)
    temperature_values: List[float | None] = []
    uwind_values: List[float | None] = []
    vwind_values: List[float | None] = []

    for temperature in temperatures:
        temperature_values.append(float(temperature.data))

        uwind = dataset[UWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )
        uwind_values.append(float(uwind.data))

        vwind = dataset[VWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )
        vwind_values.append(float(vwind.data))

    cov = Coverage(
        id="isobaric",
        type="Coverage",
        domain=Domain(
            domainType=DomainType.vertical_profile,
            axes=Axes(
                x=ValuesAxis[float](
                    values=[point.x], dataType="float", coordinates=["x"]
                ),
                y=ValuesAxis[float](values=[point.y]),
                z=ValuesAxis[float](values=isobaric_values),
                t=ValuesAxis[AwareDatetime](values=[get_temporal_extent(dataset)]),
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
                                    "unit": {"symbol": "Pa"},
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
            "uwind": NdArray(
                axisNames=["z"],
                shape=[len(isobaric_values)],
                values=uwind_values,
            ),
            "vwind": NdArray(
                axisNames=["z"],
                shape=[len(isobaric_values)],
                values=vwind_values,
            ),
        },
        parameters={
            "temperature": covjson_pydantic.parameter.Parameter(
                id="temperature",
                label={"en": "Air temperature"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="https://codes.wmo.int/common/quantity-kind/_airTemperature",
                    label={"en": "Air temperature"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id="https://codes.wmo.int/common/unit/_K",
                    label={"en": "Kelvin"},
                    symbol="K",
                ),
            ),
            "uwind": covjson_pydantic.parameter.Parameter(
                id="uwind",
                label={"en": "U component of wind"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="https://codes.wmo.int/bufr4/b/11/_095",
                    label={"en": "u-component of wind"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id="https://codes.wmo.int/common/unit/_m_s-1",
                    label={"en": "m/s"},
                    symbol="m/s",
                ),
            ),
            "vwind": covjson_pydantic.parameter.Parameter(
                id="vwind",
                label={"en": "V component of wind"},
                observedProperty=covjson_pydantic.observed_property.ObservedProperty(
                    id="https://codes.wmo.int/bufr4/b/11/_096",
                    label={"en": "v-component of wind"},
                ),
                unit=covjson_pydantic.unit.Unit(
                    id="https://codes.wmo.int/common/unit/_m_s-1",
                    label={"en": "m/s"},
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
                    "msg": f"Error, coord {point.y} out of bounds. Min/max is {ds[TEMPERATURE_LABEL][LAT_LABEL].values.min()}/{ds[TEMPERATURE_LABEL][LAT_LABEL].values.max()}",
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
                    "msg": f"Error, coord {point.x} out of bounds. Min/max is {ds[TEMPERATURE_LABEL][LON_LABEL].values.min()}/{ds[TEMPERATURE_LABEL][LON_LABEL].values.max()}",
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
    response_model=Coverage,
    response_model_exclude_unset=True,
)
async def get_isobaric_page(
    request: Request,
    coords: Annotated[
        str,
        Query(
            min_length=9,
            max_length=50,
            pattern=POINT_REGEX,
            title="Coordinates, formated as a WKT point: POINT(11.9384 60.1699)",
        ),
    ],
) -> dict:
    """Return data closest to a position.

    This is the main function of this API. Needs a string with the coordinates, formated as a WKT. Example: POINT(11.9384 60.1699) or POINT(11 60).
    """
    if len(coords) == 0:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "body": {
                    "detail": [
                        {
                            "loc": ["string", 0],
                            "msg": f'Error: No coordinates provided. Example: {str(request.base_url)[0:-1]}{request.scope["path"]}?coords=POINT(11.9384%2060.1699)',
                            "type": "string",
                        }
                    ]
                }
            },
        )

    return create_point(coords=coords)


@router.get(
    "/collections/isobaric/instances/{instance_id}/position",
    response_model=Coverage,
    response_model_exclude_unset=True,
)
async def get_instance_isobaric_page(
    request: Request,
    instance_id: Annotated[
        str,
        instance_path,
    ],
    coords: Annotated[
        str,
        Query(
            min_length=9,
            max_length=50,
            pattern=POINT_REGEX,
            title="Coordinates, formated as a WKT point. Default is POINT(11.9384 60.1699)",
        ),
    ],
) -> dict:
    """Return data closest to a position.

    Same as "Get Isobaric Page", but with selectable instance ID. See "Get Isobaric Instances Page" for a list of valid instance IDs.
    """
    if len(coords) == 0:
        return {
            "body": f'Error: No coordinates provided. Example: {str(request.base_url)[0:-1]}{request.scope["path"]}?coords=POINT(11.9384%2060.1699)'
        }

    return create_point(coords=coords, instance_id=instance_id)
