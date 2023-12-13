""" Landing page """
from functools import lru_cache
from edr_pydantic.capabilities import LandingPageModel, Provider, Contact
from edr_pydantic.link import Link

from initialize import get_base_url

BASE_URL = get_base_url()


@lru_cache
def create_landing_page() -> dict:
    """ Creates the landing page """

    landing = LandingPageModel(
        title = "EDR isobaric from Grib",
        description = "An EDR API for isobaric data from Grib files",
        links = [
            Link(href=f"{BASE_URL}", rel="self", type="application/json",
                title = "Landing Page")
        ],
        keywords = [
            "position",
            "area",
            "weather",
            "data",
            "api"
        ],
        provider = Provider(
            name = "met.no",
            url = "https://met.no/"
        ),
        contact = Contact(
            email = "example@example.com",
        )
    )

    return landing
