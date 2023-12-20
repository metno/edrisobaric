""" Conformance page """
from functools import lru_cache
from edr_pydantic.capabilities import ConformanceModel

from initialize import get_base_url

BASE_URL = get_base_url()


@lru_cache
def create_conformance_page() -> dict:
    """Creates the conformance page"""

    return ConformanceModel(
        conformsTo=[
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core",
        ],
    ).model_dump(exclude_none=True)
