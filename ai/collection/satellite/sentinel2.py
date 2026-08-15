import os
import json
import requests

import rasterio

from dotenv import load_dotenv


# ============================================================
# AGRISHIELD AI - SENTINEL-2 DATA COLLECTOR
#
# Reads:
#     ai/data/processed/farm/farm.json
#
# Downloads:
#     B02 = Blue
#     B03 = Green
#     B04 = Red
#     B08 = NIR
#     B11 = SWIR
#     SCL = Scene Classification
#
# Output:
#     ai/data/processed/satellite/output/sentinel_raw.tif
# ============================================================


# ============================================================
# 1. BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


# ============================================================
# 2. ENVIRONMENT
# ============================================================

ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    ENV_FILE
)


CLIENT_ID = os.getenv(
    "COPERNICUS_CLIENT_ID"
)

CLIENT_SECRET = os.getenv(
    "COPERNICUS_CLIENT_SECRET"
)


if not CLIENT_ID or not CLIENT_SECRET:

    raise RuntimeError(
        "COPERNICUS_CLIENT_ID or "
        "COPERNICUS_CLIENT_SECRET "
        "is missing from ai/.env"
    )


# ============================================================
# 3. PATHS
# ============================================================

FARM_FILE = os.path.join(

    BASE_DIR,
    "data",
    "processed",
    "farm",
    "farm.json"

)


OUTPUT_DIR = os.path.join(

    BASE_DIR,
    "data",
    "processed",
    "satellite",
    "output"

)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


if not os.path.exists(
    FARM_FILE
):

    raise FileNotFoundError(
        f"{FARM_FILE} not found.\n"
        "Run farm_geometry.py first."
    )


# ============================================================
# 4. LOAD FARM
# ============================================================

with open(
    FARM_FILE,
    "r",
    encoding="utf-8"
) as file:

    farm = json.load(
        file
    )


farm_id = farm[
    "farm_id"
]

farm_geometry = farm[
    "geometry"
]


# ============================================================
# 5. ANALYSIS PERIOD
# ============================================================
#
# Current testing period.
#
# Later this can be dynamically generated.
# ============================================================

ANALYSIS_FROM = (
    "2026-07-01T00:00:00Z"
)

ANALYSIS_TO = (
    "2026-08-15T23:59:59Z"
)


# ============================================================
# 6. COPERNICUS ENDPOINTS
# ============================================================

TOKEN_URL = (

    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"

)


PROCESS_URL = (

    "https://sh.dataspace.copernicus.eu/"
    "process/v1"

)


# ============================================================
# 7. HEADER
# ============================================================

print()
print("=" * 70)
print("            AGRISHIELD AI - SENTINEL-2")
print("=" * 70)

print()

print(
    "Farm ID:",
    farm_id
)

print(
    "Analysis period:",
    f"{ANALYSIS_FROM} → {ANALYSIS_TO}"
)


# ============================================================
# 8. AUTHENTICATION
# ============================================================

def get_access_token():

    response = requests.post(

        TOKEN_URL,

        data={

            "grant_type":
            "client_credentials",

            "client_id":
            CLIENT_ID,

            "client_secret":
            CLIENT_SECRET

        },

        timeout=30

    )


    if response.status_code != 200:

        print(
            "\n❌ Copernicus authentication failed."
        )

        print(
            response.text
        )


    response.raise_for_status()


    return response.json()[
        "access_token"
    ]


print()

print(
    "Authenticating with Copernicus..."
)


token = get_access_token()


print(
    "✓ Copernicus authentication successful"
)


# ============================================================
# 9. EVALSCRIPT
#
# ONE SENTINEL-2 INPUT
#
# Everything requested as DN.
#
# B02 = Blue
# B03 = Green
# B04 = Red
# B08 = NIR
# B11 = SWIR
# SCL = Scene Classification
# ============================================================

evalscript = """

//VERSION=3

function setup() {

    return {

        input: [

            {

                bands: [

                    "B02",
                    "B03",
                    "B04",
                    "B08",
                    "B11",
                    "SCL"

                ],

                units: "DN"

            }

        ],


        output: {

            bands: 6,

            sampleType:
                SampleType.FLOAT32

        }

    };

}


function evaluatePixel(sample) {

    return [

        sample.B02,
        sample.B03,
        sample.B04,
        sample.B08,
        sample.B11,
        sample.SCL

    ];

}

"""


# ============================================================
# 10. REQUEST BODY
# ============================================================

request_body = {

    "input": {

        "bounds": {

            "properties": {

                "crs":
                "http://www.opengis.net/def/"
                "crs/OGC/1.3/CRS84"

            },

            "geometry":
            farm_geometry

        },


        "data": [

            {

                "type":
                "sentinel-2-l2a",


                "dataFilter": {

                    "timeRange": {

                        "from":
                        ANALYSIS_FROM,

                        "to":
                        ANALYSIS_TO

                    },


                    "maxCloudCoverage":
                    80,


                    "mosaickingOrder":
                    "leastCC"

                },


                "processing": {

                    "harmonizeValues":
                    "true"

                }

            }

        ]

    },


    "output": {

        "width":
        700,

        "height":
        700,


        "responses": [

            {

                "identifier":
                "default",


                "format": {

                    "type":
                    "image/tiff"

                }

            }

        ]

    },


    "evalscript":
    evalscript

}


# ============================================================
# 11. REQUEST DATA
# ============================================================

print()

print(
    "Requesting Sentinel-2 data..."
)


response = requests.post(

    PROCESS_URL,

    headers={

        "Authorization":
        f"Bearer {token}",

        "Content-Type":
        "application/json",

        "Accept":
        "image/tiff"

    },

    json=request_body,

    timeout=180

)


# ============================================================
# 12. HANDLE ERROR
# ============================================================

if response.status_code != 200:

    print()

    print(
        "❌ Copernicus API request failed."
    )

    print(
        "HTTP status:",
        response.status_code
    )


    try:

        print(
            json.dumps(
                response.json(),
                indent=4
            )
        )

    except Exception:

        print(
            response.text
        )


    response.raise_for_status()


print(
    "✓ Sentinel-2 data received"
)


# ============================================================
# 13. SAVE RAW TIFF
# ============================================================

raw_file = os.path.join(

    OUTPUT_DIR,

    "sentinel_raw.tif"

)


with open(

    raw_file,

    "wb"

) as file:

    file.write(
        response.content
    )


print(
    "✓ Saved:",
    raw_file
)


# ============================================================
# 14. VALIDATE TIFF
# ============================================================

with rasterio.open(
    raw_file
) as src:

    band_count = src.count

    width = src.width

    height = src.height

    crs = src.crs


print()

print(
    "========== RASTER =========="
)

print(
    "Bands:",
    band_count
)

print(
    "Width:",
    width
)

print(
    "Height:",
    height
)

print(
    "CRS:",
    crs
)


if band_count != 6:

    raise RuntimeError(

        f"Expected 6 bands, "
        f"received {band_count}."

    )


# ============================================================
# 15. SAVE METADATA
# ============================================================

metadata = {

    "farm_id":
    farm_id,

    "analysis_period": {

        "from":
        ANALYSIS_FROM,

        "to":
        ANALYSIS_TO

    },

    "source":
    "Copernicus Sentinel-2 L2A",

    "bands": {

        "1": "B02 - Blue",

        "2": "B03 - Green",

        "3": "B04 - Red",

        "4": "B08 - NIR",

        "5": "B11 - SWIR",

        "6": "SCL - Scene Classification"

    },

    "output":
    raw_file

}


metadata_file = os.path.join(

    OUTPUT_DIR,

    "satellite_metadata.json"

)


with open(

    metadata_file,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        metadata,

        file,

        indent=4

    )


print(
    "✓ Metadata saved:",
    metadata_file
)


print()

print(
    "✓ Sentinel-2 collection complete."
)