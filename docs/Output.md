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
          59
        ]
      },
      "y": {
        "values": [
          11
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
          "2023-12-29T11:30:02.704158Z"
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
        263.1169738769531,
        262.35382080078125,
        258.91680908203125,
        253.2777099609375,
        243.75233459472656,
        237.86471557617188,
        231.14321899414062,
        224.18624877929688,
        215.8541717529297,
        212.9508819580078,
        211.1704864501953,
        211.0353546142578,
        212.0680389404297,
        210.50584411621094,
        206.67608642578125
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
        -4.319040298461914,
        -5.2903733253479,
        -2.768329620361328,
        -0.853179931640625,
        4.596181869506836,
        6.923764705657959,
        12.939920425415039,
        16.423559188842773,
        17.806337356567383,
        14.97916030883789,
        13.260116577148438,
        10.80927562713623,
        7.9914140701293945,
        9.47538948059082,
        11.780913352966309
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
        -4.4760026931762695,
        -0.1428232192993164,
        -0.306304931640625,
        -3.4065065383911133,
        -5.428422927856445,
        -6.210893630981445,
        -6.557270050048828,
        -8.134696960449219,
        -8.590213775634766,
        -6.409160614013672,
        -5.806972503662109,
        -7.910373687744141,
        -9.70693588256836,
        -10.129161834716797,
        -12.838037490844727
      ]
    }
  }
}
```
