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
          "2024-01-02T00:00:00Z"
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
        265.2215576171875,
        259.9833679199219,
        257.7770080566406,
        251.81332397460938,
        241.3728790283203,
        235.02456665039062,
        228.87094116210938,
        223.64459228515625,
        219.7703857421875,
        217.16880798339844,
        215.72781372070312,
        216.06739807128906,
        216.294677734375,
        216.29222106933594,
        213.58628845214844
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
        -9.472707748413086,
        -5.6416473388671875,
        -8.608570098876953,
        -2.9874706268310547,
        -2.010671615600586,
        -1.089141845703125,
        3.077432632446289,
        7.741827011108398,
        15.359514236450195,
        14.823564529418945,
        15.586624145507812,
        16.409372329711914,
        16.006080627441406,
        14.155519485473633,
        14.394664764404297
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
        7.1608076095581055,
        3.1872730255126953,
        3.172501802444458,
        4.89569091796875,
        6.060311794281006,
        6.570158004760742,
        4.772284507751465,
        0.407745361328125,
        -4.047607421875,
        -4.984434127807617,
        -5.65689754486084,
        -6.880097389221191,
        -7.920446395874023,
        -11.362939834594727,
        -18.519521713256836
      ]
    }
  }
}
```
