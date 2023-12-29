# Output

## Landing page:

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
      "href": "http://localhost:5000/",
      "hreflang": "en",
      "rel": "self",
      "type": "aplication/json"
    }
  ],
  "collections": [
    {
      "id": "isobaric",
      "title": "IsobaricGRIB - GRIB files",
      "description": "These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions:\n\n            southern_norway\n                Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME\n\n            It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)",
      "keywords": [
        "position",
        "area",
        "data",
        "api",
        "temperature",
        "wind",
        "forecast",
        "isobaric"
      ],
      "links": [
        {
          "href": "http://localhost:5000/collections/isobaric",
          "rel": "service-doc"
        }
      ],
      "extent": {
        "spatial": {
          "bbox": [
            [
              64.25,
              -1.45,
              55.35,
              14.51
            ]
          ],
          "crs": "WGS84"
        },
        "temporal": {
          "interval": [
            [
              "2023-12-13T00:00:00Z",
              "2023-12-13T12:00:00Z"
            ]
          ],
          "values": [
            "2023-12-13T00:00:00+00:00"
          ],
          "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]"
        },
        "vertical": {
          "interval": [
            [
              "850"
            ],
            [
              "70"
            ]
          ],
          "values": [
            "850",
            "700",
            "500",
            "400",
            "300",
            "250",
            "200",
            "150",
            "100",
            "70"
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
            "rel": "data",
            "variables": {
              "query_type": "instance",
              "output_formats": [
                "CoverageJSON"
              ]
            }
          }
        }
      },
      "parameter_names": {
        "WindUMS": {
          "type": "Parameter",
          "observedProperty": {
            "label": "WindUMS"
          }
        },
        "WindVMS": {
          "type": "Parameter",
          "observedProperty": {
            "label": "WindVMS"
          }
        },
        "Air temperature": {
          "type": "Parameter",
          "id": "Temperature",
          "unit": {
            "symbol": {
              "value": "K",
              "type": "https://codes.wmo.int/common/unit/_K"
            }
          },
          "observedProperty": {
            "id": "https://codes.wmo.int/common/quantity-kind/_airTemperature",
            "label": "Kelvin"
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
  "title": "IsobaricGRIB - GRIB files",
  "description": "These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions:\n\n            southern_norway\n                Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME\n\n            It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)",
  "keywords": [
    "position",
    "area",
    "data",
    "api",
    "temperature",
    "wind",
    "forecast",
    "isobaric"
  ],
  "links": [
    {
      "href": "http://localhost:5000/collections/isobaric",
      "rel": "service-doc"
    }
  ],
  "extent": {
    "spatial": {
      "bbox": [
        [
          64.25,
          -1.45,
          55.35,
          14.51
        ]
      ],
      "crs": "WGS84"
    },
    "temporal": {
      "interval": [
        [
          "2023-12-13T00:00:00Z",
          "2023-12-13T12:00:00Z"
        ]
      ],
      "values": [
        "2023-12-13T00:00:00+00:00"
      ],
      "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]"
    },
    "vertical": {
      "interval": [
        [
          "850"
        ],
        [
          "70"
        ]
      ],
      "values": [
        "850",
        "700",
        "500",
        "400",
        "300",
        "250",
        "200",
        "150",
        "100",
        "70"
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
        "rel": "data",
        "variables": {
          "query_type": "instance",
          "output_formats": [
            "CoverageJSON"
          ]
        }
      }
    }
  },
  "parameter_names": {
    "WindUMS": {
      "type": "Parameter",
      "observedProperty": {
        "label": "WindUMS"
      }
    },
    "WindVMS": {
      "type": "Parameter",
      "observedProperty": {
        "label": "WindVMS"
      }
    },
    "Air temperature": {
      "type": "Parameter",
      "id": "Temperature",
      "unit": {
        "symbol": {
          "value": "K",
          "type": "https://codes.wmo.int/common/unit/_K"
        }
      },
      "observedProperty": {
        "id": "https://codes.wmo.int/common/quantity-kind/_airTemperature",
        "label": "Kelvin"
      }
    }
  }
}
```

## Position

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
          11
        ]
      },
      "y": {
        "values": [
          59
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
          "2023-12-29T06:00:00Z"
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
    "t": {
      "type": "Parameter",
      "id": "t",
      "label": {
        "en": "Air temperature"
      },
      "observedProperty": {
        "id": "https://codes.wmo.int/common/quantity-kind/_airTemperature",
        "label": {
          "en": "Air temperature"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_K",
        "label": {
          "en": "Kelvin"
        },
        "symbol": "K"
      }
    },
    "u": {
      "type": "Parameter",
      "id": "u",
      "label": {
        "en": "U component of wind"
      },
      "observedProperty": {
        "id": "https://codes.wmo.int/bufr4/b/11/_095",
        "label": {
          "en": "u-component of wind"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_m_s-1",
        "label": {
          "en": "m/s"
        },
        "symbol": "m/s"
      }
    },
    "v": {
      "type": "Parameter",
      "id": "v",
      "label": {
        "en": "V component of wind"
      },
      "observedProperty": {
        "id": "https://codes.wmo.int/bufr4/b/11/_096",
        "label": {
          "en": "v-component of wind"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_m_s-1",
        "label": {
          "en": "m/s"
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
        269.9638671875,
        263.765869140625,
        261.3076171875,
        253.26571655273438,
        242.0166778564453,
        235.99783325195312,
        229.5700225830078,
        223.16067504882812,
        214.585205078125,
        210.64242553710938,
        212.03057861328125,
        214.134033203125,
        213.90895080566406,
        211.02976989746094,
        207.67926025390625
      ]
    },
    "uwind": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        6.8963623046875,
        8.512636184692383,
        9.602980613708496,
        8.94186019897461,
        9.743428230285645,
        11.693525314331055,
        14.32834243774414,
        15.352088928222656,
        17.455934524536133,
        17.20410919189453,
        17.171850204467773,
        14.954035758972168,
        15.326517105102539,
        19.514265060424805,
        20.895008087158203
      ]
    },
    "vwind": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        -4.2901611328125,
        -1.595428466796875,
        -2.675847053527832,
        -0.5176115036010742,
        -1.15081787109375,
        -1.5518064498901367,
        -2.8052377700805664,
        -3.5451431274414062,
        -4.186882019042969,
        -3.8458547592163086,
        -2.029743194580078,
        -2.1753368377685547,
        -1.0900764465332031,
        -2.35732364654541,
        -3.6956052780151367
      ]
    }
  }
}
```
