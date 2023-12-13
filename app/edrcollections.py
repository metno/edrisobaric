""" Collections page """
from functools import lru_cache
from edr_pydantic.collections import Collection, Collections
from edr_pydantic.data_queries import EDRQuery, EDRQueryLink, DataQueries
from edr_pydantic.extent import Extent, Spatial
from edr_pydantic.link import Link
from edr_pydantic.observed_property import ObservedProperty
from edr_pydantic.parameter import Parameters, Parameter
from edr_pydantic.unit import Unit
from edr_pydantic.variables import Variables

from initialize import get_base_url

collections = []

# Collection(EdrBaseModel):
#     id: str
#     title: Optional[str] = None
#     description: Optional[str] = None
#     keywords: Optional[List[str]] = None
#     links: List[Link]
#     extent: Extent
#     data_queries: Optional[DataQueries] = None
#     # TODO According to req A.13 it shall be CRS object, according to C.1 it is a string array
#     crs: Optional[List[str]] = None
#     output_formats: Optional[List[str]] = None
#     parameter_names: Parameters
#     # TODO According to req A.13 may have distanceunits. If radius is in link, it shall have distanceunits
#     distanceunits: Optional[List[str]] = None

coords = None
collections.append(Collection(
    id="isobaric",
    title="IsobaricGRIB - GRIB files",
    description="""
        These files are used by Avinor ATM systems but possibly also of interest to others.
        They contain temperature and wind forecasts for a set of isobaric layers
        (i.e. altitudes having the same pressure).

        The files are (normally) produced every 6 hours. You can check the time when generated
        using the Last-Modified header or the `updated` key in `available`.

        These files are in GRIB2 format (filetype BIN) for the following regions:

        southern_norway
            Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME

        It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)
    """,

    extent=Extent(
        spatial=Spatial(
            bbox=[
                [64.25, -1.45, 55.35, 14.51]
            ],
            crs="WGS84"
        )
    ),
    links=[
        Link(
            href="https://api.met.no/weatherapi/isobaricgrib/1.0/documentation",
            rel="service-doc"
        )
    ],
    data_queries=DataQueries(
        position=EDRQuery(
            link=EDRQueryLink(
                href=f"{get_base_url()}/collections/isobaric/position?coords={coords}",
                rel="data",
                variables=Variables(
                    query_type="position",
                    output_formats=[
                        "CoverageJSON"
                    ]
                )
            )
        )
    ),
    parameter_names=Parameters({
        "Wind Direction": Parameter(
            unit=Unit(
                label="degree true"
            ),
            observedProperty=ObservedProperty(
                id="https://codes.wmo.int/common/quantity-kind/_windDirection",
                label="Wind Direction"
            )
        )
    })
))


@lru_cache
def create_collections_page() -> dict:
    """ Creates the collections page """

    link_self = Link(
        href=get_base_url() + "collections",
        hreflang="en",
        rel="self",
        type="aplication/json"
    )

    collections_page = Collections(
        links=[
            link_self
        ],
        collections=collections
    )

    return collections_page
