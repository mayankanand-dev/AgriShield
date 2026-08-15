from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv


# ============================================================
# AGRISHIELD AI - SOIL DATA COLLECTOR
#
# Source:
#   OpenEPI / SoilHive
#
# Input:
#   ai/data/processed/farm/farm.json
#
# Output:
#   ai/data/processed/soil/
#       soil_raw.json
#       soil_summary.json
#
# Uses:
#   OpenEPI Python client
# ============================================================


# ============================================================
# 1. BASE DIRECTORY
# ============================================================

# File:
#
# ai/collection/soil/soil_api.py
#
# parents[0] -> soil
# parents[1] -> collection
# parents[2] -> ai

BASE_DIR = Path(
    __file__
).resolve().parents[2]


# ============================================================
# 2. ENVIRONMENT
# ============================================================

ENV_FILE = (
    BASE_DIR / ".env"
)

load_dotenv(
    ENV_FILE
)


SOILHIVE_CLIENT_ID = os.getenv(
    "SOILHIVE_CLIENT_ID"
)

SOILHIVE_CLIENT_SECRET = os.getenv(
    "SOILHIVE_CLIENT_SECRET"
)

SOILHIVE_API_TOKEN = os.getenv(
    "SOILHIVE_API_TOKEN"
)


# ------------------------------------------------------------
# We require the token for the actual request.
#
# Client ID and secret are retained in .env because they
# belong to your SoilHive application credentials.
# The SoilHive/OpenEPI portal instructs users to create an
# application and generate a token for API usage.
# ------------------------------------------------------------

if not SOILHIVE_API_TOKEN:

    raise RuntimeError(
        "SOILHIVE_API_TOKEN is missing from:\n"
        f"{ENV_FILE}\n\n"
        "Add your SoilHive token to ai/.env."
    )


# ============================================================
# 3. IMPORT OPENEPI CLIENT
# ============================================================

try:

    from openepi_client import (
        GeoLocation,
        BoundingBox
    )

    from openepi_client.soil import (
        SoilClient
    )

except ImportError as error:

    raise RuntimeError(

        "openepi-client is not installed.\n\n"

        "Run:\n"

        "pip install openepi-client"

    ) from error


# ============================================================
# 4. PATHS
# ============================================================

FARM_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "farm"
    / "farm.json"
)


SOIL_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "soil"
)


RAW_FILE = (
    SOIL_DIR
    / "soil_raw.json"
)


SUMMARY_FILE = (
    SOIL_DIR
    / "soil_summary.json"
)


SOIL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 5. FARM FILE
# ============================================================

if not FARM_FILE.exists():

    raise FileNotFoundError(

        "Farm file not found:\n"
        f"{FARM_FILE}\n\n"

        "Run:\n"
        "python ai/collection/geometry/"
        "farm_geometry.py"

    )


# ============================================================
# 6. LOAD FARM
# ============================================================

with open(

    FARM_FILE,

    "r",

    encoding="utf-8"

) as file:

    farm = json.load(
        file
    )


farm_id = farm.get(
    "farm_id",
    "UNKNOWN"
)


centroid = farm.get(
    "centroid"
)


if not centroid:

    raise ValueError(
        "farm.json does not contain centroid."
    )


latitude = centroid.get(
    "latitude"
)


longitude = centroid.get(
    "longitude"
)


if latitude is None or longitude is None:

    raise ValueError(

        "Farm centroid must contain "
        "latitude and longitude."

    )


# ============================================================
# 7. BOUNDING BOX
# ============================================================

bounding_box = farm.get(
    "bounding_box"
)


if not bounding_box:

    raise ValueError(

        "farm.json does not contain "
        "bounding_box."

    )


min_lat = bounding_box.get(
    "min_latitude"
)

max_lat = bounding_box.get(
    "max_latitude"
)

min_lon = bounding_box.get(
    "min_longitude"
)

max_lon = bounding_box.get(
    "max_longitude"
)


if any(
    value is None
    for value in (
        min_lat,
        max_lat,
        min_lon,
        max_lon
    )
):

    raise ValueError(
        "Invalid bounding_box in farm.json."
    )


# ============================================================
# 8. GEOLOCATION OBJECT
# ============================================================

location = GeoLocation(

    lat=float(
        latitude
    ),

    lon=float(
        longitude
    )

)


bbox = BoundingBox(

    min_lat=float(
        min_lat
    ),

    max_lat=float(
        max_lat
    ),

    min_lon=float(
        min_lon
    ),

    max_lon=float(
        max_lon
    )

)


# ============================================================
# 9. REQUEST SOIL DATA
# ============================================================

print()
print("=" * 75)
print("             AGRISHIELD AI - SOIL DATA")
print("=" * 75)

print()

print(
    "Farm ID:",
    farm_id
)

print(
    "Latitude:",
    latitude
)

print(
    "Longitude:",
    longitude
)

print()

print(
    "Source:",
    "OpenEPI / SoilHive"
)


# ============================================================
# 10. SOIL PROPERTIES
# ============================================================
#
# Start with properties explicitly useful for the ML layer.
#
# SoilHive/OpenEPI's Python client documents querying soil
# properties by location, depth and statistic/value.
# ============================================================

properties = [

    "clay",
    "silt",
    "sand"
]


depths = [

    "0-5cm",
    "5-15cm",
    "15-30cm"
]


values = [

    "mean",
    "Q0.05"
]


# ============================================================
# 11. QUERY SOIL PROPERTY AT CENTROID
# ============================================================

print()
print(
    "Requesting soil properties..."
)


try:

    soil_property_response = (
        SoilClient.get_soil_property(

            geolocation=location,

            depths=depths,

            properties=properties,

            values=values

        )
    )

except Exception as error:

    raise RuntimeError(

        "SoilHive/OpenEPI soil-property request failed:\n"
        f"{error}"

    ) from error


print(
    "✓ Soil property response received"
)


# ============================================================
# 12. QUERY SOIL TYPE
# ============================================================

print()
print(
    "Requesting soil type..."
)


try:

    soil_type_response = (
        SoilClient.get_soil_type(

            geolocation=location,

            top_k=4

        )
    )

except Exception as error:

    print(
        "⚠ Soil type request failed:"
    )

    print(
        error
    )

    soil_type_response = None


# ============================================================
# 13. QUERY BOUNDING-BOX SOIL TYPE SUMMARY
# ============================================================

print()
print(
    "Requesting soil type summary for farm area..."
)


try:

    soil_type_summary = (
        SoilClient.get_soil_type_summary(

            bounding_box=bbox

        )
    )

except Exception as error:

    print(
        "⚠ Bounding-box soil summary failed:"
    )

    print(
        error
    )

    soil_type_summary = None


# ============================================================
# 14. SERIALIZE RESPONSES
# ============================================================

def serialize(
    value
):

    # Pydantic / dataclass-style response
    if hasattr(
        value,
        "model_dump"
    ):

        return value.model_dump()

    
    if hasattr(
        value,
        "dict"
    ):

        return value.dict()

    
    if isinstance(
        value,
        dict
    ):

        return value

    
    if isinstance(
        value,
        list
    ):

        return [
            serialize(item)
            for item in value
        ]

    
    if hasattr(
        value,
        "__dict__"
    ):

        return {
            key: serialize(val)
            for key, val
            in value.__dict__.items()
            if not key.startswith("_")
        }

    
    return value


soil_property_json = serialize(
    soil_property_response
)


soil_type_json = serialize(
    soil_type_response
)


soil_type_summary_json = serialize(
    soil_type_summary
)


# ============================================================
# 15. RAW OUTPUT
# ============================================================

retrieved_at = datetime.now(
    timezone.utc
).isoformat()


raw_output = {

    "farm_id":
    farm_id,

    "source":
    "OpenEPI / SoilHive",

    "retrieved_at":
    retrieved_at,

    "location":
    {

        "latitude":
        float(latitude),

        "longitude":
        float(longitude)

    },

    "bounding_box":
    {

        "min_latitude":
        float(min_lat),

        "max_latitude":
        float(max_lat),

        "min_longitude":
        float(min_lon),

        "max_longitude":
        float(max_lon)

    },

    "soil_property_request":
    {

        "properties":
        properties,

        "depths":
        depths,

        "values":
        values

    },

    "soil_properties":
    soil_property_json,

    "soil_type":
    soil_type_json,

    "soil_type_summary":
    soil_type_summary_json

}


with open(

    RAW_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        raw_output,

        file,

        indent=4,

        default=str

    )


print()

print(
    "✓ Raw soil data saved:"
)

print(
    RAW_FILE
)


# ============================================================
# 16. FEATURE-READY SUMMARY
# ============================================================
#
# We intentionally preserve the API response rather than
# guessing field names for N/P/K/pH.
#
# Once we inspect the actual response from your account,
# feature_engineering/soil_features.py can normalize the
# exact properties into:
#
# pH
# nitrogen
# phosphorus
# potassium
# organic carbon
# clay
# sand
# silt
# etc.
# ============================================================

summary = {

    "farm_id":
    farm_id,

    "source":
    "OpenEPI / SoilHive",

    "retrieved_at":
    retrieved_at,

    "location":
    {

        "latitude":
        float(latitude),

        "longitude":
        float(longitude)

    },

    "soil_properties":
    soil_property_json,

    "soil_type":
    soil_type_json,

    "soil_type_summary":
    soil_type_summary_json,

    "requested_properties":
    properties,

    "requested_depths":
    depths,

    "requested_values":
    values

}


with open(

    SUMMARY_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        summary,

        file,

        indent=4,

        default=str

    )


print(
    "✓ Soil summary saved:"
)

print(
    SUMMARY_FILE
)


# ============================================================
# 17. PRINT
# ============================================================

print()
print("=" * 75)
print(
    "             SOIL COLLECTION COMPLETE"
)
print("=" * 75)

print()

print(
    "Farm ID:",
    farm_id
)

print(
    "Centroid:",
    latitude,
    longitude
)

print()

print(
    "Raw soil data:"
)

print(
    RAW_FILE
)

print()

print(
    "Soil summary:"
)

print(
    SUMMARY_FILE
)

print()

print(
    "✓ OpenEPI / SoilHive soil collection complete."
)