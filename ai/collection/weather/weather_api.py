from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# AGRISHIELD AI - OPENWEATHER WEATHER COLLECTOR
#
# Input:
#   ai/data/processed/farm/farm.json
#
# Source:
#   OpenWeather
#
# Collects:
#   1. Current weather
#   2. 5-day / 3-hour forecast
#
# Output:
#   ai/data/processed/weather/
#       current_weather.json
#       forecast_weather.json
#       weather_summary.json
# ============================================================


# ============================================================
# 1. BASE DIRECTORY
# ============================================================

# This file:
#
# ai/
# └── collection/
#     └── weather/
#         └── weather_api.py
#
# ..       -> collection
# ..       -> ai
#
# Therefore BASE_DIR = ai/

BASE_DIR = Path(
    __file__
).resolve().parents[2]


# ============================================================
# 2. ENVIRONMENT
# ============================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    ENV_FILE
)


OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)


if not OPENWEATHER_API_KEY:

    raise RuntimeError(
        "OPENWEATHER_API_KEY is missing "
        f"from {ENV_FILE}"
    )


# ============================================================
# 3. PATHS
# ============================================================

FARM_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "farm"
    / "farm.json"
)


WEATHER_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "weather"
)


CURRENT_FILE = (
    WEATHER_DIR
    / "current_weather.json"
)


FORECAST_FILE = (
    WEATHER_DIR
    / "forecast_weather.json"
)


SUMMARY_FILE = (
    WEATHER_DIR
    / "weather_summary.json"
)


WEATHER_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 4. CHECK FARM FILE
# ============================================================

if not FARM_FILE.exists():

    raise FileNotFoundError(
        "\nFarm file not found.\n"
        f"Expected:\n{FARM_FILE}\n\n"
        "Run:\n"
        "python ai/collection/geometry/"
        "farm_geometry.py"
    )


# ============================================================
# 5. LOAD FARM
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
        "farm.json does not contain centroid data."
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
# 6. OPENWEATHER ENDPOINTS
# ============================================================

CURRENT_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)


# ============================================================
# 7. COMMON PARAMETERS
# ============================================================

common_params = {

    "lat":
    latitude,

    "lon":
    longitude,

    "appid":
    OPENWEATHER_API_KEY,

    "units":
    "metric"

}


# ============================================================
# 8. HEADER
# ============================================================

print()
print("=" * 75)
print("             AGRISHIELD AI - OPENWEATHER")
print("=" * 75)

print()

print(
    f"Farm ID       : {farm_id}"
)

print(
    f"Latitude      : {latitude}"
)

print(
    f"Longitude     : {longitude}"
)

print()

print(
    "Weather source: OpenWeather"
)


# ============================================================
# 9. GET CURRENT WEATHER
# ============================================================

print()
print(
    "Requesting current weather..."
)


try:

    current_response = requests.get(

        CURRENT_URL,

        params=common_params,

        timeout=60

    )

except requests.RequestException as error:

    raise RuntimeError(
        f"OpenWeather current-weather request failed: "
        f"{error}"
    ) from error


if current_response.status_code != 200:

    print()
    print(
        "❌ OpenWeather current-weather API error"
    )

    print(
        "HTTP status:",
        current_response.status_code
    )

    print(
        current_response.text
    )

    current_response.raise_for_status()


current_data = current_response.json()


print(
    "✓ Current weather received"
)


# ============================================================
# 10. GET FORECAST
# ============================================================

print()
print(
    "Requesting 5-day forecast..."
)


try:

    forecast_response = requests.get(

        FORECAST_URL,

        params=common_params,

        timeout=60

    )

except requests.RequestException as error:

    raise RuntimeError(
        f"OpenWeather forecast request failed: "
        f"{error}"
    ) from error


if forecast_response.status_code != 200:

    print()
    print(
        "❌ OpenWeather forecast API error"
    )

    print(
        "HTTP status:",
        forecast_response.status_code
    )

    print(
        forecast_response.text
    )

    forecast_response.raise_for_status()


forecast_data = forecast_response.json()


print(
    "✓ Forecast received"
)


# ============================================================
# 11. RETRIEVAL TIME
# ============================================================

retrieved_at = datetime.now(
    timezone.utc
).isoformat()


# ============================================================
# 12. SAVE CURRENT WEATHER
# ============================================================

current_output = {

    "farm_id":
    farm_id,

    "source":
    "OpenWeather",

    "retrieved_at":
    retrieved_at,

    "location":
    {

        "latitude":
        latitude,

        "longitude":
        longitude

    },

    "data":
    current_data

}


with open(

    CURRENT_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(
        current_output,
        file,
        indent=4
    )


print(
    "✓ Saved:",
    CURRENT_FILE
)


# ============================================================
# 13. SAVE FORECAST
# ============================================================

forecast_output = {

    "farm_id":
    farm_id,

    "source":
    "OpenWeather",

    "retrieved_at":
    retrieved_at,

    "location":
    {

        "latitude":
        latitude,

        "longitude":
        longitude

    },

    "data":
    forecast_data

}


with open(

    FORECAST_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(
        forecast_output,
        file,
        indent=4
    )


print(
    "✓ Saved:",
    FORECAST_FILE
)


# ============================================================
# 14. EXTRACT CURRENT VALUES
# ============================================================

main = current_data.get(
    "main",
    {}
)


wind = current_data.get(
    "wind",
    {}
)


clouds = current_data.get(
    "clouds",
    {}
)


weather_list = current_data.get(
    "weather",
    []
)


weather_condition = (
    weather_list[0]
    if weather_list
    else {}
)


rain = current_data.get(
    "rain",
    {}
)


visibility = current_data.get(
    "visibility"
)


# ============================================================
# 15. CURRENT WEATHER SUMMARY
# ============================================================

current_summary = {

    "temperature_c":
    main.get(
        "temp"
    ),

    "feels_like_c":
    main.get(
        "feels_like"
    ),

    "temperature_min_c":
    main.get(
        "temp_min"
    ),

    "temperature_max_c":
    main.get(
        "temp_max"
    ),

    "pressure_hpa":
    main.get(
        "pressure"
    ),

    "humidity_percent":
    main.get(
        "humidity"
    ),

    "visibility_m":
    visibility,

    "wind_speed_mps":
    wind.get(
        "speed"
    ),

    "wind_direction_deg":
    wind.get(
        "deg"
    ),

    "wind_gust_mps":
    wind.get(
        "gust"
    ),

    "cloud_cover_percent":
    clouds.get(
        "all"
    ),

    "rain_1h_mm":
    rain.get(
        "1h"
    ),

    "rain_3h_mm":
    rain.get(
        "3h"
    ),

    "weather_id":
    weather_condition.get(
        "id"
    ),

    "weather_main":
    weather_condition.get(
        "main"
    ),

    "weather_description":
    weather_condition.get(
        "description"
    )

}


# ============================================================
# 16. EXTRACT FORECAST VALUES
# ============================================================

forecast_list = forecast_data.get(
    "list",
    []
)


forecast_records = []


for item in forecast_list:

    item_main = item.get(
        "main",
        {}
    )

    item_wind = item.get(
        "wind",
        {}
    )

    item_clouds = item.get(
        "clouds",
        {}
    )

    item_weather = item.get(
        "weather",
        []
    )

    item_weather_condition = (
        item_weather[0]
        if item_weather
        else {}
    )

    item_rain = item.get(
        "rain",
        {}
    )

    forecast_records.append({

        "datetime":
        item.get(
            "dt_txt"
        ),

        "timestamp":
        item.get(
            "dt"
        ),

        "temperature_c":
        item_main.get(
            "temp"
        ),

        "feels_like_c":
        item_main.get(
            "feels_like"
        ),

        "temperature_min_c":
        item_main.get(
            "temp_min"
        ),

        "temperature_max_c":
        item_main.get(
            "temp_max"
        ),

        "pressure_hpa":
        item_main.get(
            "pressure"
        ),

        "humidity_percent":
        item_main.get(
            "humidity"
        ),

        "wind_speed_mps":
        item_wind.get(
            "speed"
        ),

        "wind_direction_deg":
        item_wind.get(
            "deg"
        ),

        "wind_gust_mps":
        item_wind.get(
            "gust"
        ),

        "cloud_cover_percent":
        item_clouds.get(
            "all"
        ),

        "rain_3h_mm":
        item_rain.get(
            "3h"
        ),

        "weather_id":
        item_weather_condition.get(
            "id"
        ),

        "weather_main":
        item_weather_condition.get(
            "main"
        ),

        "weather_description":
        item_weather_condition.get(
            "description"
        )

    })


# ============================================================
# 17. AGGREGATE FORECAST FEATURES
# ============================================================

forecast_temperatures = [

    record["temperature_c"]

    for record in forecast_records

    if record["temperature_c"] is not None

]


forecast_humidity = [

    record["humidity_percent"]

    for record in forecast_records

    if record["humidity_percent"] is not None

]


forecast_rain = [

    record["rain_3h_mm"] or 0.0

    for record in forecast_records

]


forecast_wind = [

    record["wind_speed_mps"]

    for record in forecast_records

    if record["wind_speed_mps"] is not None

]


forecast_rain_total = sum(
    forecast_rain
)


forecast_summary = {

    "forecast_points":
    len(
        forecast_records
    ),

    "temperature_mean_c":
    (
        sum(forecast_temperatures)
        / len(forecast_temperatures)
        if forecast_temperatures
        else None
    ),

    "temperature_max_c":
    (
        max(forecast_temperatures)
        if forecast_temperatures
        else None
    ),

    "temperature_min_c":
    (
        min(forecast_temperatures)
        if forecast_temperatures
        else None
    ),

    "humidity_mean_percent":
    (
        sum(forecast_humidity)
        / len(forecast_humidity)
        if forecast_humidity
        else None
    ),

    "rainfall_total_mm":
    forecast_rain_total,

    "wind_speed_mean_mps":
    (
        sum(forecast_wind)
        / len(forecast_wind)
        if forecast_wind
        else None
    )

}


# ============================================================
# 18. FINAL SUMMARY JSON
# ============================================================

summary = {

    "farm_id":
    farm_id,

    "source":
    "OpenWeather",

    "retrieved_at":
    retrieved_at,

    "location":
    {

        "latitude":
        latitude,

        "longitude":
        longitude

    },

    "current":
    current_summary,

    "forecast_summary":
    forecast_summary,

    "forecast":
    forecast_records,

    "files":
    {

        "current":
        str(CURRENT_FILE),

        "forecast":
        str(FORECAST_FILE),

        "summary":
        str(SUMMARY_FILE)

    }

}


with open(

    SUMMARY_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(
        summary,
        file,
        indent=4
    )


print(
    "✓ Saved:",
    SUMMARY_FILE
)


# ============================================================
# 19. PRINT RESULTS
# ============================================================

print()
print("=" * 75)
print("              CURRENT WEATHER")
print("=" * 75)

print()

print(
    f"Temperature     : "
    f"{current_summary['temperature_c']} °C"
)

print(
    f"Feels like      : "
    f"{current_summary['feels_like_c']} °C"
)

print(
    f"Humidity        : "
    f"{current_summary['humidity_percent']} %"
)

print(
    f"Pressure        : "
    f"{current_summary['pressure_hpa']} hPa"
)

print(
    f"Wind            : "
    f"{current_summary['wind_speed_mps']} m/s"
)

print(
    f"Cloud cover     : "
    f"{current_summary['cloud_cover_percent']} %"
)

print(
    f"Rain (1h)       : "
    f"{current_summary['rain_1h_mm'] or 0} mm"
)

print(
    f"Condition       : "
    f"{current_summary['weather_description']}"
)


print()
print("=" * 75)
print("              FORECAST SUMMARY")
print("=" * 75)

print()

print(
    f"Forecast points       : "
    f"{forecast_summary['forecast_points']}"
)

print(
    f"Forecast mean temp    : "
    f"{forecast_summary['temperature_mean_c']}"
)

print(
    f"Forecast max temp     : "
    f"{forecast_summary['temperature_max_c']}"
)

print(
    f"Forecast min temp     : "
    f"{forecast_summary['temperature_min_c']}"
)

print(
    f"Forecast mean humid.  : "
    f"{forecast_summary['humidity_mean_percent']}"
)

print(
    f"Forecast rainfall     : "
    f"{forecast_summary['rainfall_total_mm']:.2f} mm"
)

print(
    f"Forecast mean wind    : "
    f"{forecast_summary['wind_speed_mean_mps']}"
)


print()
print("=" * 75)
print("            WEATHER COLLECTION COMPLETE")
print("=" * 75)

print()

print(
    "Current JSON:",
    CURRENT_FILE
)

print(
    "Forecast JSON:",
    FORECAST_FILE
)

print(
    "Summary JSON:",
    SUMMARY_FILE
)