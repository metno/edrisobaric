"""Conformance page."""
from functools import lru_cache
from fastapi import APIRouter
from edr_pydantic.capabilities import ConformanceModel


router = APIRouter()


@lru_cache  # Cache reply, as it will never change.
def create_conformance_page() -> dict:
    """Creates the conformance page."""
    return ConformanceModel(
        conformsTo=[
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core",
        ],
    ).model_dump(exclude_none=True)


@router.get("/conformance")
async def get_conformance_page():
    """Returns the conformance page contents."""
    return create_conformance_page()
