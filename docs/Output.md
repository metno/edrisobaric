# Output

## Landing page

```json
{
  "title": "EDR isobaric from Grib",
  "description": "An EDR API for isobaric data from Grib files",
  "links": [
    {
      "href": "http://localhost:5000/",
      "rel": "self",
      "type": "application/json",
      "title": "Landing Page"
    },
    {
      "href": "http://localhost:5000/api",
      "rel": "service-desc",
      "type": "application/json",
      "title": "OpenAPI document"
    },
    {
      "href": "http://localhost:5000/conformance",
      "rel": "conformance",
      "type": "application/json",
      "title": "Conformance document"
    },
    {
      "href": "http://localhost:5000/collections",
      "rel": "data",
      "type": "application/json",
      "title": "Collections metadata in JSON"
    }
  ],
  "provider": {
    "name": "Meteorologisk institutt / The Norwegian Meteorological Institute",
    "url": "https://api.met.no/"
  },
  "contact": {
    "email": "api-users-request@lists.met.no",
    "phone": "+47.22963000",
    "address": "Henrik Mohns plass 1",
    "postalCode": "0313",
    "city": "Oslo",
    "country": "Norway"
  }
}
```

## Collections

```json
{
  "links": [
    {
      "href": "http://localhost:5000/collections",
      "hreflang": "en",
      "rel": "self",
      "type": "aplication/json"
    }
  ],
  "collections": [
    {
      "id": "isobaric",
      "title": "IsobaricGRIB - GRIB files",
      "description": "These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions: southern_norway    Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME    It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)",
      "keywords": [
        "position",
        "data",
        "api",
        "temperature",
        "wind",
        "forecast",
        "isobaric"
      ],
      "links": [
        {
          "href": "http://localhost:5000/collections/isobaric/",
          "rel": "data"
        },
        {
          "href": "http://localhost:5000/collections/isobaric/instances",
          "rel": "alternate"
        }
      ],
      "extent": {
        "spatial": {
          "bbox": [
            [
              -1.4499999999999886,
              55.35,
              14.449999999999964,
              64.25000000000011
            ]
          ],
          "crs": "WGS84"
        },
        "temporal": {
          "interval": [
            [
              "2024-01-22T06:00:00Z",
              "2024-01-22T18:00:00Z"
            ]
          ],
          "values": [
            "2024-01-22T06:00:00+00:00"
          ],
          "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]"
        },
        "vertical": {
          "interval": [
            [
              "850.0"
            ],
            [
              "100.0"
            ]
          ],
          "values": [
            "850.0",
            "750.0",
            "700.0",
            "600.0",
            "500.0",
            "450.0",
            "400.0",
            "350.0",
            "300.0",
            "275.0",
            "250.0",
            "225.0",
            "200.0",
            "150.0",
            "100.0"
          ],
          "vrs": "Vertical Reference System: PressureLevel"
        }
      },
      "data_queries": {
        "position": {
          "link": {
            "href": "http://localhost:5000/collections/isobaric/position",
            "rel": "data",
            "variables": {
              "query_type": "position",
              "output_formats": [
                "CoverageJSON"
              ]
            }
          }
        },
        "instances": {
          "link": {
            "href": "http://localhost:5000/collections/isobaric/instances",
            "rel": "alternate",
            "variables": {
              "query_type": "instances",
              "output_formats": [
                "CoverageJSON"
              ]
            }
          }
        }
      },
      "parameter_names": {
        "wind_from_direction": {
          "type": "Parameter",
          "id": "wind_from_direction",
          "unit": {
            "symbol": {
              "value": "˚",
              "type": "https://codes.wmo.int/common/unit/_degree_(angle)"
            }
          },
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/wind_from_direction",
            "label": "Wind from direction"
          }
        },
        "wind_speed": {
          "type": "Parameter",
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/wind_speed",
            "label": "Wind speed"
          }
        },
        "Air temperature": {
          "type": "Parameter",
          "id": "Temperature",
          "unit": {
            "symbol": {
              "value": "˚C",
              "type": "https://codes.wmo.int/common/unit/_Cel"
            }
          },
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/air_temperature",
            "label": "Air temperature"
          }
        }
      }
    }
  ]
}
```

## Collections Isobaric

```json
{
  "id": "isobaric",
  "type": "Coverage",
  "domain": {
    "type": "Domain",
    "domainType": "VerticalProfile",
    "axes": {
      "x": {
        "values": [
          11.9384
        ]
      },
      "y": {
        "values": [
          60.1699
        ]
      },
      "z": {
        "values": [
          850,
          750,
          700,
          600,
          500,
          450,
          400,
          350,
          300,
          275,
          250,
          225,
          200,
          150,
          100
        ]
      },
      "t": {
        "values": [
          "2024-01-22T06:00:00Z"
        ]
      }
    },
    "referencing": [
      {
        "coordinates": [
          "x",
          "y"
        ],
        "system": {
          "type": "GeographicCRS",
          "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        }
      },
      {
        "coordinates": [
          "z"
        ],
        "system": {
          "type": "VerticalCRS",
          "cs": {
            "csAxes": [
              {
                "name": {
                  "en": "Pressure"
                },
                "direction": "down",
                "unit": {
                  "symbol": "Pa"
                }
              }
            ]
          }
        }
      },
      {
        "coordinates": [
          "t"
        ],
        "system": {
          "type": "TemporalRS",
          "calendar": "Gregorian"
        }
      }
    ]
  },
  "parameters": {
    "temperature": {
      "type": "Parameter",
      "id": "temperature",
      "label": {
        "en": "Air temperature"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/air_temperature",
        "label": {
          "en": "Air temperature"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_Cel",
        "label": {
          "en": "degree Celsius"
        },
        "symbol": "˚C"
      }
    },
    "wind_from_direction": {
      "type": "Parameter",
      "id": "wind_from_direction",
      "label": {
        "en": "Wind from direction"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/wind_from_direction",
        "label": {
          "en": "wind_from_direction"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_degree_(angle)",
        "label": {
          "en": "degree"
        },
        "symbol": "˚"
      }
    },
    "wind_speed": {
      "type": "Parameter",
      "id": "wind_speed",
      "label": {
        "en": "Wind speed"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/wind_speed",
        "label": {
          "en": "Wind speed"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_m_s-1",
        "label": {
          "en": "metres per second"
        },
        "symbol": "m/s"
      }
    }
  },
  "ranges": {
    "temperature": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        -0.8469604492187273,
        -6.090521240234352,
        -10.128485107421852,
        -19.968649291992165,
        -30.81133117675779,
        -34.8822082519531,
        -37.46372070312498,
        -43.608236694335915,
        -50.61138000488279,
        -53.1612609863281,
        -54.32878723144529,
        -54.856588745117165,
        -54.4368957519531,
        -56.80686035156248,
        -59.4251770019531
      ]
    },
    "wind_from_direction": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        251.89231324274408,
        268.025317042686,
        263.4171323732491,
        260.49710067525916,
        258.0192091798531,
        251.3188371490558,
        234.52648276392324,
        238.04217425111196,
        238.34091822223792,
        242.6413674798908,
        250.43217796317708,
        251.40792044357158,
        250.7129903177535,
        258.73423117112475,
        250.58257974351864
      ]
    },
    "wind_speed": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        24.397993461777496,
        26.897416387095273,
        25.714209710871682,
        23.937505099542538,
        21.697445570552986,
        17.251142823330213,
        15.077925132256935,
        14.047664700757982,
        15.371964814105377,
        17.383713986455557,
        18.75633763334451,
        20.04114420230292,
        23.694978927342127,
        22.832521447368254,
        27.751923365566597
      ]
    }
  }
}
```
