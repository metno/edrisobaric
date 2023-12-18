""" Collections page """
from functools import lru_cache
from datetime import datetime, timedelta, timezone
from edr_pydantic.collections import Collection, Collections
from edr_pydantic.data_queries import EDRQuery, EDRQueryLink, DataQueries
from edr_pydantic.extent import Extent, Spatial, Vertical, Temporal
from edr_pydantic.link import Link
from edr_pydantic.observed_property import ObservedProperty
from edr_pydantic.parameter import Parameters, Parameter
from edr_pydantic.unit import Unit, Symbol
from edr_pydantic.variables import Variables
from pydantic import AwareDatetime
from shapely import wkt
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.domain import Domain, Axes, ValuesAxis, DomainType
from covjson_pydantic.ndarray import NdArray
from covjson_pydantic.reference_system import ReferenceSystem, ReferenceSystemConnectionObject

from initialize import get_base_url, get_temporal_extent, get_dataset, \
    TEMPERATURE_LABEL, LAT_LABEL, LON_LABEL, UWIND_LABEL, VWIND_LABEL


@lru_cache
def create_collections_page(url: str, instance_id: str = "") -> dict:
    """ Creates the collections page """
    link_self = Link(
        href=url,
        hreflang="en",
        rel="self",
        type="aplication/json"
    )

    collections = [Collection(
        id="isobaric",
        title="IsobaricGRIB - GRIB files",
        description="""
            These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions:

            southern_norway
                Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME

            It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)
        """,
        keywords = [
            "position",
            "area",
            "data",
            "api",
            "temperature",
            "wind",
            "forecast",
            "isobaric"
        ],
        extent=Extent(
            spatial=Spatial(
                bbox=[
                    [64.25, -1.45, 55.35, 14.51]
                ],
                crs="WGS84"
            ),
            vertical=Vertical(
                interval = [["850"], ["70"]],
                values = [
                    "850",
                    "700",
                    "500",
                    "400",
                    "300",
                    "250",
                    "200",
                    "150",
                    "100",
                    "70",
                ],
                vrs = "Vertical Reference System: PressureLevel",
            ),
            temporal=Temporal(
                interval = [
                    [get_temporal_extent(), get_temporal_extent()+timedelta(hours=12)]
                ],
                values = [get_temporal_extent().isoformat()],
                trs = 'TIMECRS["DateTime",TDATUM["Gregorian Calendar"],CS[TemporalDateTime,1],AXIS["Time (T)",future]'
            ),
        ),
        links=[
            Link(
                href="https://api.met.no/weatherapi/isobaricgrib/1.0/documentation",
                rel="service-doc"
            )
        ],
        data_queries=DataQueries(
            # List instances
            instances=EDRQuery(
                link=EDRQueryLink(
                    href=f"{get_base_url()}collections/instances",
                    rel="data",
                    variables=Variables(
                        query_type="instance",
                        output_formats=[
                            "CoverageJSON"
                        ]
                    )
                )
            ),
            # Get posision in default instance
            position=EDRQuery(
                link=EDRQueryLink(
                    href=f"{get_base_url()}collections/position",
                    rel="data",
                    variables=Variables(
                        query_type="position",
                        output_formats=[
                            "CoverageJSON"
                        ],
                        coords="Well Known Text POINT value i.e. POINT(10.9 60.1)",
                    )
                )
            ),
        ),
        parameter_names=Parameters({
            "WindUMS": Parameter(
                observedProperty=ObservedProperty(
                    label="WindUMS"
                )
            ),
            "WindVMS": Parameter(
                observedProperty=ObservedProperty(
                    label="WindVMS"
                )
            ),
            "Air temperature": Parameter(
                id="Temperature",
                unit=Unit(
                    symbol=Symbol(
                        value="K",
                        type="https://codes.wmo.int/common/unit/_K"
                    )
                ),
                observedProperty=ObservedProperty(
                    id="https://codes.wmo.int/common/quantity-kind/_airTemperature",
                    label="Kelvin"
                )
            ),
        }),
    )]

    collections_page = Collections(
        links=[
            link_self
        ],
        collections=collections
    )

    return collections_page


def create_data(coords: str = "") -> dict:
    """ Fetch data based on coords """
    point = wkt.loads(coords)
    print("create_data for coord ", point.y, point.x)

    ds = get_dataset()

    # Sanity checks on coordinates
    # print("ds[TIMELABEL][LAT_LABEL].values.max", ds[TEMPERATURE_LABEL][LAT_LABEL].values.max())
    # print("ds[TIMELABEL][LAT_LABEL].values.min", ds[TEMPERATURE_LABEL][LAT_LABEL].values.min())
    if point.y > ds[TEMPERATURE_LABEL][LAT_LABEL].values.max() \
        or point.y < ds[TEMPERATURE_LABEL][LAT_LABEL].values.min():
        print(f"Error, point.y ({point.y}) is outside data min/max \
            {ds[TEMPERATURE_LABEL][LAT_LABEL].values.min()}/{ds[TEMPERATURE_LABEL][LAT_LABEL].values.max()}")
        return {}
    if point.x > ds[TEMPERATURE_LABEL][LON_LABEL].values.max() \
        or point.x < ds[TEMPERATURE_LABEL][LON_LABEL].values.min():
        print(f"Error, point.y ({point.x}) is outside data min/max \
            {ds[TEMPERATURE_LABEL][LON_LABEL].values.min()}/{ds[TEMPERATURE_LABEL][LON_LABEL].values.max()}")
        return {}

    # data = {}

    # Fetch temperature
    temperatures = ds[TEMPERATURE_LABEL].sel(longitude=point.x, latitude=point.y, method='nearest')

    isobaric_values=temperatures.isobaricInhPa.data
    temperature_values=[]
    uwind_values=[]
    vwind_values=[]

    for t in temperatures:
        temperature_values.append(float(t.data))
        # print("isobaricInhPa", t["isobaricInhPa"].data)
        # print("temp", t.data)

        # For same coord and isobaric, fetch wind vectors
        uwind = ds[UWIND_LABEL].sel(longitude=point.x, latitude=point.y, isobaricInhPa=t["isobaricInhPa"].data, method='nearest')
        # print("uwind", uwind.data)
        uwind_values.append(float(uwind.data))

        vwind = ds[VWIND_LABEL].sel(longitude=point.x, latitude=point.y, isobaricInhPa=t["isobaricInhPa"].data, method='nearest')
        # print("vwind", vwind.data)
        vwind_values.append(float(vwind.data))

    c = Coverage(
        domain=Domain(
            domainType=DomainType.vertical_profile,
            axes=Axes(
                x=ValuesAxis[float](values=[point.y]),
                y=ValuesAxis[float](values=[point.x]),
                z=ValuesAxis[float](values=isobaric_values),
                t=ValuesAxis[AwareDatetime](values=[datetime.now(tz=timezone.utc)])
            ),
            referencing=[
                ReferenceSystemConnectionObject(
                    coordinates=["x", "y", "z"],
                    system=ReferenceSystem(
                        type="VerticalCRS",
                    )
                ),
                ReferenceSystemConnectionObject(
                    coordinates=["t"],
                    system=ReferenceSystem(
                        type="TemporalRS",
                        calendar="Gregorian"
                    )
                )
            ]
        ),
        ranges={
            "temperature": NdArray(axisNames=["x", "y", "z"], shape=[1, 1, len(isobaric_values)], values=temperature_values),
            "uwind": NdArray(axisNames=["x", "y", "z"], shape=[1, 1, len(isobaric_values)], values=uwind_values),
            "vwind": NdArray(axisNames=["x", "y", "z"], shape=[1, 1, len(isobaric_values)], values=vwind_values),
        },
        # parameters={
        #     "temperature": Parameter(
        #         type="Parameter",
        #         # id="Temperature",
        #         # label="temperature",
        #         # description="The air temperature measured in Kelvin.",
        #         observedProperty=ObservedProperty(
        #             # id="https://codes.wmo.int/common/quantity-kind/_airTemperature",
        #             # label={"en": "Air temperature"},
        #             label="Air temperature",
        #         ),
        #         # unit=Unit(
        #         #     id="https://codes.wmo.int/common/unit/_K",
        #         #     symbol="K"
        #         # )
        #     ),
        # },
            # Parameter(
            #     type="Parameter",
            #     id="WindUMS",
            #     label=[
            #         {
            #             "en": "U component of wind"
            #         },
            #     ],
            #     description= [
            #         {
            #             "en": "U component of wind"
            #         },
            #     ],
            #     observedProperty=ObservedProperty(
            #         id="http://codes.wmo.int/grib2/codeflag/4.2/_0-2-2",
            #         label=[
            #             {"en": "u-component of wind"},
            #         ],
            #     ),
            #     unit=Unit(
            #         id="https://codes.wmo.int/common/unit/_m_s-1",
            #         symbol="m/s"
            #     )
            # ),
            # Parameter(
            #     type="Parameter",
            #     id="WindVMS",
            #     label=[
            #         {
            #             "en": "V component of wind"
            #         },
            #     ],
            #     description= [
            #         {
            #             "en": "V component of wind"
            #         },
            #     ],
            #     observedProperty=ObservedProperty(
            #         id="https://codes.wmo.int/grib2/codeflag/4.2/_0-2-3",
            #         label=[
            #             {"en": "v-component of wind "},
            #         ],
            #     ),
            #     unit=Unit(
            #         id="https://codes.wmo.int/common/unit/_m_s-1",
            #         symbol="m/s"
            #     )
            # )
    )

    return c
