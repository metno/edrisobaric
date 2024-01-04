"""Collections page."""
from typing import List
import logging
from fastapi import APIRouter, status, Response, Request
from pydantic import AwareDatetime
from shapely import wkt, GEOSException, Point
import covjson_pydantic
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.ndarray import NdArray

from initialize import get_dataset

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

router = APIRouter()
logger = logging.getLogger()


def create_point(coords: str = "", instance: str = "") -> dict:
    """Return data for all isometric layers at a point."""
    # TODO: check instance
    point = Point()
    try:
        point = wkt.loads(coords)
    except GEOSException:
        errmsg = (
            "Error, coords should be a Well Known Text, for example "
            + f'"POINT(11.0 59.0)". You gave "{coords}"'
        )
        logger.error(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)

    logger.info("create_data for coord %s, %s", point.y, point.x)
    dataset = get_dataset()

    # Sanity checks on coordinates
    if (
        point.y > dataset[TEMPERATURE_LABEL][LAT_LABEL].values.max()
        or point.y < dataset[TEMPERATURE_LABEL][LAT_LABEL].values.min()
    ):
        errmsg = (
            f"Error, coord {point.y} out of bounds. Min/max is "
            + "{dataset[TEMPERATURE_LABEL][LAT_LABEL].values.min()}/"
            + "{dataset[TEMPERATURE_LABEL][LAT_LABEL].values.max()}"
        )
        logger.error(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)
    if (
        point.x > dataset[TEMPERATURE_LABEL][LON_LABEL].values.max()
        or point.x < dataset[TEMPERATURE_LABEL][LON_LABEL].values.min()
    ):
        errmsg = f"Error, coord {point.x} out of bounds. Min/max is \
            {dataset[TEMPERATURE_LABEL][LON_LABEL].values.min()}/\
            {dataset[TEMPERATURE_LABEL][LON_LABEL].values.max()}"
        logger.error(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)

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


@router.get("/collections/isobaric/position")
async def create_isobaric_page(coords: str, instance: str = "") -> dict:
    """Position.

    This is the main function of this API. Needs a string with the coordinates, and will return data for the nearest point.

    """
    return create_point(coords=coords)


@router.get("/collections/isobaric/instances/{instance}/position")
async def create_instance_isobaric_page(
    request: Request, coords: str = "", instance: str = ""
) -> dict:
    """Position.

    This is the main function of this API. Needs a string with the coordinates, and will return data for the nearest point.

    """
    if len(coords) == 0:
        return {
            "body": f'Error: No coordinates provided. Example: {str(request.base_url)[0:-1]}{request.scope["path"]}?coords=POINT(11 59)'
        }

    return create_point(coords=coords, instance=instance)
