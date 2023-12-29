"""Collections page."""
from functools import lru_cache
from typing import List
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, status, Response
import edr_pydantic
from edr_pydantic.collections import Collection
from pydantic import AwareDatetime
from shapely import wkt, GEOSException
import covjson_pydantic
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.ndarray import NdArray

from initialize import get_base_url, get_dataset

from grib import (
    get_vertical_extent,
    get_spatial_extent,
    get_temporal_extent,
    TEMPERATURE_LABEL,
    LAT_LABEL,
    LON_LABEL,
    UWIND_LABEL,
    VWIND_LABEL,
    ISOBARIC_LABEL,
)

base_url = get_base_url()
router = APIRouter()


@lru_cache
def create_collection(collection_id: str = "") -> dict:
    """Creates the collections page."""
    link_self = edr_pydantic.link.Link(
        href=base_url, hreflang="en", rel="self", type="aplication/json"
    )

    dataset = get_dataset()
    vertical_levels = get_vertical_extent()
    collection_url = f"{base_url}collections/isobaric"

    isobaric_col = Collection(
        id="isobaric",
        title="IsobaricGRIB - GRIB files",
        description="""
            These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions:

            southern_norway
                Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME

            It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)
        """,
        keywords=[
            "position",
            "area",
            "data",
            "api",
            "temperature",
            "wind",
            "forecast",
            "isobaric",
        ],
        extent=edr_pydantic.extent.Extent(
            spatial=edr_pydantic.extent.Spatial(
                bbox=[get_spatial_extent()], crs="WGS84"
            ),
            vertical=edr_pydantic.extent.Vertical(
                interval=[
                    [vertical_levels[0]],
                    [vertical_levels[len(vertical_levels) - 1]],
                ],
                values=vertical_levels,
                vrs="Vertical Reference System: PressureLevel",  # opendata.fmi.fi
            ),
            temporal=edr_pydantic.extent.Temporal(
                interval=[
                    [
                        get_temporal_extent(dataset),
                        get_temporal_extent(dataset) + timedelta(hours=12),
                    ]
                ],
                values=[get_temporal_extent(dataset).isoformat()],
                trs='TIMECRS["DateTime",TDATUM["Gregorian Calendar"],'
                + 'CS[TemporalDateTime,1],AXIS["Time (T)",future]',  # opendata.fmi.fi
            ),
        ),
        links=[
            edr_pydantic.link.Link(
                href=collection_url,
                rel="service-doc",
            )
        ],
        data_queries=edr_pydantic.data_queries.DataQueries(
            # List instances
            instances=edr_pydantic.data_queries.EDRQuery(
                link=edr_pydantic.data_queries.EDRQueryLink(
                    href=f"{collection_url}/instances",
                    rel="data",
                    variables=edr_pydantic.variables.Variables(
                        query_type="instance", output_formats=["CoverageJSON"]
                    ),
                )
            ),
            # Get posision in default instance
            position=edr_pydantic.data_queries.EDRQuery(
                link=edr_pydantic.data_queries.EDRQueryLink(
                    href=f"{collection_url}/position",
                    rel="data",
                    variables=edr_pydantic.variables.Variables(
                        query_type="position",
                        output_formats=["CoverageJSON"],
                        # coords="Well Known Text POINT value i.e. POINT(10.9 60.1)",
                    ),
                )
            ),
        ),
        parameter_names=edr_pydantic.parameter.Parameters(
            {
                "WindUMS": edr_pydantic.parameter.Parameter(
                    observedProperty=edr_pydantic.observed_property.ObservedProperty(
                        label="WindUMS"
                    )
                ),
                "WindVMS": edr_pydantic.parameter.Parameter(
                    observedProperty=edr_pydantic.observed_property.ObservedProperty(
                        label="WindVMS"
                    )
                ),
                "Air temperature": edr_pydantic.parameter.Parameter(
                    id="Temperature",
                    unit=edr_pydantic.unit.Unit(
                        symbol=edr_pydantic.unit.Symbol(
                            value="K", type="https://codes.wmo.int/common/unit/_K"
                        )
                    ),
                    observedProperty=edr_pydantic.observed_property.ObservedProperty(
                        id="https://codes.wmo.int/common/quantity-kind/_airTemperature",
                        label="Kelvin",
                    ),
                ),
            }
        ),
    )

    if len(collection_id) == 0:
        collections_page = edr_pydantic.collections.Collections(
            links=[link_self], collections=[isobaric_col]
        )
        return collections_page.model_dump(exclude_none=True)
    return isobaric_col.model_dump(exclude_none=True)


def create_point(coords: str = "") -> dict:
    """Fetch data based on coords."""
    point = None
    try:
        point = wkt.loads(coords)
    except GEOSException:
        errmsg = (
            "Error, coords should be a Well Known Text, for example "
            + f'"POINT(11.0 59.0)". You gave "{coords}"'
        )
        print(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)

    print("create_data for coord ", point.y, point.x)

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
        print(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)
    if (
        point.x > dataset[TEMPERATURE_LABEL][LON_LABEL].values.max()
        or point.x < dataset[TEMPERATURE_LABEL][LON_LABEL].values.min()
    ):
        errmsg = f"Error, coord {point.x} out of bounds. Min/max is \
            {dataset[TEMPERATURE_LABEL][LON_LABEL].values.min()}/\
            {dataset[TEMPERATURE_LABEL][LON_LABEL].values.max()}"
        print(errmsg)
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)

    # Fetch temperature
    temperatures = dataset[TEMPERATURE_LABEL].sel(
        longitude=point.x, latitude=point.y, method="nearest"
    )

    isobaric_values = temperatures.isobaricInhPa.data
    temperature_values: List[float | None] = []
    uwind_values: List[float | None] = []
    vwind_values: List[float | None] = []

    for temperature in temperatures:
        temperature_values.append(float(temperature.data))
        # print(ISOBARIC_LABEL, t[ISOBARIC_LABEL].data)
        # print("temp", t.data)

        # For same coord and isobaric, fetch wind vectors
        uwind = dataset[UWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )
        # print("uwind", uwind.data)
        uwind_values.append(float(uwind.data))

        vwind = dataset[VWIND_LABEL].sel(
            longitude=point.x,
            latitude=point.y,
            isobaricInhPa=temperature[ISOBARIC_LABEL].data,
            method="nearest",
        )
        # print("vwind", vwind.data)
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
            "t": covjson_pydantic.parameter.Parameter(
                id="t",
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
            "u": covjson_pydantic.parameter.Parameter(
                id="u",
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
            "v": covjson_pydantic.parameter.Parameter(
                id="v",
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


@router.get("/collections")
async def create_collections_page() -> dict:
    """List of collections."""
    return create_collection()


@router.get("/collections/isobaric/position")
async def create_isobaric_page(coords: str) -> dict:
    """Position."""
    return create_point(coords=coords)


@router.get("/collections/{collection_id}")
async def create_collection_page(collection_id: str) -> dict:
    """Show a specific collection."""
    return create_collection(collection_id)
