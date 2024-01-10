"""Landing page."""

from functools import lru_cache
from fastapi import APIRouter
from edr_pydantic.capabilities import LandingPageModel, Provider, Contact
from edr_pydantic.link import Link

from initialize import BASE_URL


@lru_cache
def create_landing_page(base_url) -> dict:
    """Creates the landing page model."""
    landing = LandingPageModel(
        title="EDR isobaric from Grib",
        description="An EDR API for isobaric data from Grib files",
        links=[
            Link(
                href=f"{base_url}",
                rel="self",
                type="application/json",
                title="Landing Page",
            ),
            Link(
                href=f"{base_url}openapi.json",
                rel="service-desc",
                type="application/json",
                title="OpenAPI document",
            ),
            Link(
                href=f"{base_url}conformance",
                rel="conformance",
                type="application/json",
                title="Conformance document",
            ),
            Link(
                href=f"{base_url}collections",
                rel="data",
                type="application/json",
                title="Collections metadata in JSON",
            ),
        ],
        provider=Provider(
            name="Meteorologisk institutt / The Norwegian Meteorological Institute",
            url="https://api.met.no/",
        ),
        contact=Contact(
            email="api-users-request@lists.met.no",
            phone="+47.22963000",
            postalCode="0313",
            city="Oslo",
            address="Henrik Mohns plass 1",
            country="Norway",
        ),
    )

    return landing.model_dump(exclude_none=True)


router = APIRouter()


@router.get("/", response_model=LandingPageModel, response_model_exclude_unset=True)
async def get_landing_page() -> dict:
    """Returns the landing page as JSON."""
    return create_landing_page(base_url=BASE_URL)
