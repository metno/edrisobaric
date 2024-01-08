"""Collections page."""
from functools import lru_cache
from datetime import timedelta
import logging
from typing import Annotated, Optional, List
from fastapi import APIRouter, status, Response, Path
import edr_pydantic
from edr_pydantic.collections import Collection
from edr_pydantic.data_queries import DataQueries
from edr_pydantic.link import Link
from edr_pydantic.extent import Extent
from edr_pydantic.parameter import Parameters
from edr_pydantic.base_model import EdrBaseModel
from pydantic import ConfigDict

from initialize import get_dataset, BASE_URL, check_instance_exists, CollectionID

from grib import (
    get_vertical_extent,
    get_spatial_extent,
    get_temporal_extent,
)

class CollectionWithExamples(EdrBaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    links: List[Link]
    extent: Extent
    data_queries: Optional[DataQueries] = None
    crs: Optional[List[str]] = None
    output_formats: Optional[List[str]] = None
    parameter_names: Parameters
    distanceunits: Optional[List[str]] = None
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="allow",
        str_min_length=1,
        validate_default=True,
        validate_assignment=True,
        strict=True,
    )

class CollectionsWithExamples(EdrBaseModel):
    links: List[Link]
    collections: List[CollectionWithExamples]

router = APIRouter()
logger = logging.getLogger()


@lru_cache
def create_collection(collection_id: str = "", instance_id: str = "") -> dict:
    """Creates the collections page."""
    instance_url = f"{BASE_URL}collections/isobaric/instances/{instance_id}/"

    link_self = edr_pydantic.link.Link(
        href=f"{BASE_URL}collections/",
        hreflang="en",
        rel="self",
        type="aplication/json",
    )

    dataset = get_dataset()
    vertical_levels = get_vertical_extent(dataset)
    collection_url = f"{BASE_URL}collections/isobaric/"
    if len(instance_id) > 0:
        # Sanity check on instance id
        instance_ok, errmsg = check_instance_exists(dataset, instance_id)
        if not instance_ok:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content=errmsg)

        collection_url = instance_url

    isobaric_col = CollectionWithExamples(
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
            "data",
            "api",
            "temperature",
            "wind",
            "forecast",
            "isobaric",
        ],
        extent=edr_pydantic.extent.Extent(
            spatial=edr_pydantic.extent.Spatial(
                bbox=[get_spatial_extent(dataset)], crs="WGS84"
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
                rel="collection",
            )
        ],
        data_queries=edr_pydantic.data_queries.DataQueries(
            # List instances
            instances=edr_pydantic.data_queries.EDRQuery(
                link=edr_pydantic.data_queries.EDRQueryLink(
                    href=f"{collection_url}instances/",
                    rel="data",
                    variables=edr_pydantic.variables.Variables(
                        query_type="instances", output_formats=["CoverageJSON"]
                    ),
                )
            ),
            # Get posision in default instance
            position=edr_pydantic.data_queries.EDRQuery(
                link=edr_pydantic.data_queries.EDRQueryLink(
                    href=f"{collection_url}position",
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
        model_config = ConfigDict(
            from_attributes=True,
            json_schema_extra={
                "example": {
                    "id": "1234",
                    "name": "Foo",
                }
            },
        )
    )

    print(isobaric_col.model_config)

    if len(collection_id) == 0:
        print(isobaric_col.model_dump_json(indent=4))
        collections_page = CollectionsWithExamples(
            links=[link_self], collections=[isobaric_col]
        )
        return collections_page.model_dump(exclude_none=True)
    return isobaric_col.model_dump(exclude_none=True)


@router.get("/collections/", response_model=CollectionsWithExamples)
async def get_collections_page() -> dict:
    """List collections as JSON. Isobaric is the only one available. No data is returned, only info about the collection."""
    return create_collection()


@router.get("/collections/{collection_id}/", response_model=CollectionsWithExamples)
async def get_collection_page(collection_id: CollectionID) -> dict:
    """List a specific collection as JSON. Isobaric is the only one available. No data is returned, only info about the collection.."""
    return create_collection(collection_id)


@router.get("/collections/{collection_id}/instances/{instance_id}/", response_model=CollectionsWithExamples)
async def get_instance_collection_page(
    collection_id: CollectionID,
    instance_id: Annotated[
        str,
        Path(
            min_length=14,
            max_length=14,
            pattern="^\\d{10}0{4}$",
            title="Instance ID, consisting of date in format %Y%m%d%H0000",
        ),
    ],
) -> dict:
    """Return a specific instance of a collection. Isobaric is the only collection available. The date in current grib file is only instance available, format %Y%m%d%H0000, so string has to be 14 characters, where first 8 are a number and last 6 are all zeros, example 20240104000000. No data is returned, only info about the instance."""
    return create_collection(collection_id, instance_id)
