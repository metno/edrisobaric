"""Conformance page."""
from functools import lru_cache
from fastapi import APIRouter
from edr_pydantic.capabilities import ConformanceModel


@lru_cache  # Cache reply, as it will never change.
def create_conformance_page() -> dict:
    """Creates the conformance page."""
    return ConformanceModel(
        conformsTo=[
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/covjson",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/queries",
            # "https://github.com/metno/edr-profile/blob/main/profile_weather_forecast_timeseries.md#Conformance",
        ],
    ).model_dump(exclude_none=True)


router = APIRouter()


@router.get(
    "/conformance",
    tags=["Capabilities"],
    response_model=ConformanceModel,
    response_model_exclude_unset=True,
)
async def describe_standards_this_API_conforms_to() -> dict:
    """Provides a list of all requirements classes this service conforms to."""
    return create_conformance_page()
