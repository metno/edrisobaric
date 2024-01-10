"""Collections page."""
from functools import lru_cache
from datetime import timedelta
import logging
from fastapi import APIRouter
import edr_pydantic
from edr_pydantic.collections import Instances, Instance

from initialize import get_dataset, BASE_URL, format_instance_id, TIME_FORMAT

from grib import (
    get_vertical_extent,
    get_spatial_extent,
    get_temporal_extent,
)

router = APIRouter()
logger = logging.getLogger()


@lru_cache
def create_instances() -> dict:
    """List all instances (dates) available in data file."""
    dataset = get_dataset()
    vertical_levels = get_vertical_extent(dataset)
    collection_url = f"{BASE_URL}collections/isobaric/"
    instance_dates = [get_temporal_extent(dataset)]

    instance_list = []
    for d in instance_dates:
        formatted_date = format_instance_id(d)
        instance_list.append(
            Instance(
                id=formatted_date,
                title=formatted_date,
                description=f"Data from date {formatted_date}, formatted as {TIME_FORMAT}.",
                links=[
                    edr_pydantic.link.Link(
                        href=f"{collection_url}instances/{formatted_date}/",
                        hreflang="en",
                        rel="self",
                        type="aplication/json",
                    ),
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
                data_queries=edr_pydantic.data_queries.DataQueries(
                    # Get posision in instance
                    position=edr_pydantic.data_queries.EDRQuery(
                        link=edr_pydantic.data_queries.EDRQueryLink(
                            href=f"{collection_url}instances/{formatted_date}/position",
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
                                    value="K",
                                    type="https://codes.wmo.int/common/unit/_K",
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
        )

    isobaric_inst = Instances(
        links=[
            edr_pydantic.link.Link(
                href=f"{collection_url}instances/",
                hreflang="en",
                rel="self",
                type="aplication/json",
            )
        ],
        instances=instance_list,
    )

    return isobaric_inst.model_dump(exclude_none=True)


@router.get(
    "/collections/isobaric/instances",
    response_model=Instances,
    response_model_exclude_unset=True,
)
async def get_isobaric_instances_page() -> dict:
    """Return list of available instances as JSON."""
    return create_instances()
