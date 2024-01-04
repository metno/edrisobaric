"""Collections page."""
from functools import lru_cache
from datetime import timedelta
import logging
from fastapi import APIRouter
import edr_pydantic
from edr_pydantic.collections import Collection

from initialize import get_dataset, BASE_URL

from grib import (
    get_vertical_extent,
    get_spatial_extent,
    get_temporal_extent,
)

router = APIRouter()
logger = logging.getLogger()


@lru_cache
def create_collection(collection_id: str = "", instance: str = "") -> dict:
    """Creates the collections page."""

    # TODO: Check for instance

    link_self = edr_pydantic.link.Link(
        href=BASE_URL, hreflang="en", rel="self", type="aplication/json"
    )

    dataset = get_dataset()
    vertical_levels = get_vertical_extent(dataset)
    collection_url = f"{BASE_URL}collections/isobaric"

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
                        query_type="instances", output_formats=["CoverageJSON"]
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


@router.get("/collections")
async def create_collections_page() -> dict:
    """List all collections available.

    Returns
    -------
        dict: A dictionary with the collection information.

    """
    return create_collection()


@router.get("/collections/{collection_id}")
async def create_collection_page(collection_id: str) -> dict:
    """Show a specific collection. Isobaric is the only one available. No data is returned, only info about the collection."""
    return create_collection(collection_id)


@router.get("/collections/{collection_id}/instances/{instance}/")
async def create_instance_collection_page(collection_id: str, instance: str) -> dict:
    """Show a specific instance of a collection. Isobaric is the only one available, and the date in current file is the only instance available. No data is returned, only info about the collection."""
    return create_collection(collection_id, instance)
