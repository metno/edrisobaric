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
      "description": "These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions:\n\n            southern_norway\n                Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME\n\n            It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)",
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
              "2024-01-16T00:00:00Z",
              "2024-01-16T12:00:00Z"
            ]
          ],
          "values": [
            "2024-01-16T00:00:00+00:00"
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
          "2024-01-16T00:00:00Z",
          "2024-01-16T12:00:00Z"
        ]
      ],
      "values": [
        "2024-01-16T00:00:00+00:00"
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
          "2024-01-16T00:00:00Z"
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
    "uwind": {
      "type": "Parameter",
      "id": "uwind",
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
    "vwind": {
      "type": "Parameter",
      "id": "vwind",
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
        259.9708557128906,
        255.4127655029297,
        251.11085510253906,
        241.6421661376953,
        232.36569213867188,
        227.9706573486328,
        221.93441772460938,
        215.32928466796875,
        211.61489868164062,
        211.59326171875,
        211.47825622558594,
        211.1735076904297,
        211.833251953125,
        208.94456481933594,
        204.8937530517578
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
        10.003143310546875,
        6.364622116088867,
        6.2812418937683105,
        8.020271301269531,
        9.430185317993164,
        9.842438697814941,
        10.665620803833008,
        13.8545560836792,
        20.12831687927246,
        23.134765625,
        23.885570526123047,
        21.438627243041992,
        22.899555206298828,
        25.33365249633789,
        27.79376983642578
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
        5.889827728271484,
        0.17238855361938477,
        -0.34173011779785156,
        -2.2754268646240234,
        -1.5704689025878906,
        0.13471412658691406,
        0.9284391403198242,
        -0.3315868377685547,
        -9.34195327758789,
        -11.123899459838867,
        -10.690530776977539,
        -11.88523006439209,
        -12.98432445526123,
        -12.6998291015625,
        -13.967351913452148
      ]
    }
  }
}
```
