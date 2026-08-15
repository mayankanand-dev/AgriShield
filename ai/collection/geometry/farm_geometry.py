import os
import json
import re

import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from pyproj import Geod


# ============================================================
# AGRISHIELD AI - FARM GEOMETRY
#
# Input:
#   P1, P2, P3, ... Pn
#
# Output:
#   - Valid farm polygon
#   - Area
#   - Perimeter
#   - Centroid
#   - Bounding box
#   - farm.json
#   - farm_boundary.png
# ============================================================


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

FARM_OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "farm"
)

FARM_JSON = os.path.join(
    FARM_OUTPUT_DIR,
    "farm.json"
)

FARM_MAP = os.path.join(
    FARM_OUTPUT_DIR,
    "farm_boundary.png"
)


# ============================================================
# GEODESIC CALCULATOR
# ============================================================

GEOD = Geod(
    ellps="WGS84"
)


# ============================================================
# COORDINATE PARSER
# ============================================================

def parse_coordinate(value):
    """
    Supports:

    Decimal:
        23.0748056

    DMS:
        23°04'29.3"

    DMS with spaces:
        23 04 29.3

    Direction:
        23°04'29.3"N
        76°51'47.0"E
    """

    value = value.strip()

    if not value:
        raise ValueError(
            "Coordinate cannot be empty."
        )

    # --------------------------------------------------------
    # Decimal
    # --------------------------------------------------------

    try:
        return float(value)

    except ValueError:
        pass


    # --------------------------------------------------------
    # Normalize symbols
    # --------------------------------------------------------

    normalized = (
        value
        .replace("°", " ")
        .replace("'", " ")
        .replace('"', " ")
        .replace("d", " ")
        .replace("m", " ")
        .replace("s", " ")
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    ).strip()


    # --------------------------------------------------------
    # DMS
    # --------------------------------------------------------

    pattern = re.compile(
        r"""
        ^\s*
        (-?\d+(?:\.\d+)?)
        \s+
        (\d+(?:\.\d+)?)
        \s+
        (\d+(?:\.\d+)?)
        \s*
        ([NSEW])?
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE
    )


    match = pattern.match(
        normalized
    )


    if not match:

        raise ValueError(
            "Invalid coordinate format."
        )


    degrees = float(
        match.group(1)
    )

    minutes = float(
        match.group(2)
    )

    seconds = float(
        match.group(3)
    )

    direction = match.group(4)


    if minutes >= 60:

        raise ValueError(
            "Minutes must be less than 60."
        )


    if seconds >= 60:

        raise ValueError(
            "Seconds must be less than 60."
        )


    decimal = (
        abs(degrees)
        + minutes / 60
        + seconds / 3600
    )


    if direction:

        direction = direction.upper()

        if direction in ["S", "W"]:

            decimal = -decimal

    elif degrees < 0:

        decimal = -decimal


    return decimal


# ============================================================
# CREATE POLYGON
# ============================================================

def create_polygon(points):

    # Shapely expects:
    # (longitude, latitude)

    coordinates = [

        (
            longitude,
            latitude
        )

        for latitude, longitude
        in points

    ]


    # Close polygon
    if coordinates[0] != coordinates[-1]:

        coordinates.append(
            coordinates[0]
        )


    return Polygon(
        coordinates
    )


# ============================================================
# AREA / PERIMETER
# ============================================================

def calculate_geodesic_metrics(points):

    longitudes = [

        longitude

        for latitude, longitude
        in points

    ]


    latitudes = [

        latitude

        for latitude, longitude
        in points

    ]


    area_m2, perimeter_m = (
        GEOD.polygon_area_perimeter(
            longitudes,
            latitudes
        )
    )


    area_m2 = abs(
        area_m2
    )


    area_hectares = (
        area_m2 / 10000
    )


    area_acres = (
        area_m2 / 4046.8564224
    )


    return (
        area_m2,
        area_hectares,
        area_acres,
        perimeter_m
    )


# ============================================================
# DRAW FARM
# ============================================================

def draw_farm(
    points,
    polygon
):

    longitudes = [

        longitude

        for latitude, longitude
        in points

    ]


    latitudes = [

        latitude

        for latitude, longitude
        in points

    ]


    plot_longitudes = (
        longitudes
        + [longitudes[0]]
    )


    plot_latitudes = (
        latitudes
        + [latitudes[0]]
    )


    plt.figure(
        figsize=(10, 8)
    )


    plt.plot(
        plot_longitudes,
        plot_latitudes,
        marker="o"
    )


    plt.fill(
        plot_longitudes,
        plot_latitudes,
        alpha=0.25
    )


    # --------------------------------------------------------
    # Point labels
    # --------------------------------------------------------

    for index, (
        latitude,
        longitude
    ) in enumerate(
        points,
        start=1
    ):

        plt.annotate(

            f"P{index}",

            (
                longitude,
                latitude
            ),

            xytext=(6, 6),

            textcoords="offset points",

            fontsize=10
        )


    # --------------------------------------------------------
    # Centroid
    # --------------------------------------------------------

    centroid = polygon.centroid


    plt.scatter(
        centroid.x,
        centroid.y,
        marker="x",
        s=100
    )


    plt.annotate(
        "Centroid",
        (
            centroid.x,
            centroid.y
        ),
        xytext=(8, -15),
        textcoords="offset points"
    )


    plt.title(
        "AgriShield AI - Registered Farm Boundary"
    )


    plt.xlabel(
        "Longitude"
    )

    plt.ylabel(
        "Latitude"
    )


    plt.grid(
        True,
        alpha=0.3
    )


    plt.axis(
        "equal"
    )


    plt.tight_layout()


    os.makedirs(
        FARM_OUTPUT_DIR,
        exist_ok=True
    )


    plt.savefig(
        FARM_MAP,
        dpi=200,
        bbox_inches="tight"
    )


    plt.show()


# ============================================================
# SAVE FARM JSON
# ============================================================

def save_farm(

    farm_id,
    points,
    area_m2,
    area_hectares,
    area_acres,
    perimeter_m,
    centroid_lat,
    centroid_lon

):

    longitudes = [

        longitude

        for latitude, longitude
        in points

    ]


    latitudes = [

        latitude

        for latitude, longitude
        in points

    ]


    geometry_coordinates = [

        [
            longitude,
            latitude
        ]

        for latitude, longitude
        in points

    ]


    # Close GeoJSON polygon

    geometry_coordinates.append(
        geometry_coordinates[0]
    )


    bounding_box = {

        "min_longitude":
        min(longitudes),

        "min_latitude":
        min(latitudes),

        "max_longitude":
        max(longitudes),

        "max_latitude":
        max(latitudes)

    }


    farm_data = {

        "farm_id":
        farm_id,

        "point_count":
        len(points),

        "points": [

            {

                "id":
                f"P{index}",

                "latitude":
                latitude,

                "longitude":
                longitude

            }

            for index, (
                latitude,
                longitude
            )

            in enumerate(
                points,
                start=1
            )

        ],


        "geometry": {

            "type":
            "Polygon",

            "coordinates": [
                geometry_coordinates
            ]

        },


        "area": {

            "square_meters":
            area_m2,

            "hectares":
            area_hectares,

            "acres":
            area_acres

        },


        "perimeter": {

            "meters":
            perimeter_m,

            "kilometers":
            perimeter_m / 1000

        },


        "centroid": {

            "latitude":
            centroid_lat,

            "longitude":
            centroid_lon

        },


        "bounding_box":
        bounding_box

    }


    os.makedirs(
        FARM_OUTPUT_DIR,
        exist_ok=True
    )


    with open(

        FARM_JSON,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            farm_data,

            file,

            indent=4

        )


    return farm_data


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 65)
    print("           AGRISHIELD AI - FARM GEOMETRY")
    print("=" * 65)

    print()

    print(
        "Enter farm boundary points in order:"
    )

    print(
        "P1 → P2 → P3 → ... → Pn"
    )

    print()

    print(
        "Enter 'done' as latitude when finished."
    )


    points = []

    point_number = 1


    while True:

        print()
        print(
            "-" * 50
        )

        print(
            f"Boundary Point P{point_number}"
        )


        latitude_input = input(
            "Latitude: "
        ).strip()


        if latitude_input.lower() == "done":

            break


        longitude_input = input(
            "Longitude: "
        ).strip()


        try:

            latitude = parse_coordinate(
                latitude_input
            )

            longitude = parse_coordinate(
                longitude_input
            )


            if not -90 <= latitude <= 90:

                raise ValueError(
                    "Latitude must be between -90 and 90."
                )


            if not -180 <= longitude <= 180:

                raise ValueError(
                    "Longitude must be between -180 and 180."
                )


            points.append(
                (
                    latitude,
                    longitude
                )
            )


            print(
                f"✓ P{point_number} added"
            )

            print(
                f"  Latitude : {latitude:.10f}"
            )

            print(
                f"  Longitude: {longitude:.10f}"
            )


            point_number += 1


        except ValueError as error:

            print(
                f"❌ {error}"
            )

            continue


    # --------------------------------------------------------
    # Minimum points
    # --------------------------------------------------------

    if len(points) < 3:

        raise ValueError(
            "A farm requires at least 3 points."
        )


    # --------------------------------------------------------
    # Polygon
    # --------------------------------------------------------

    polygon = create_polygon(
        points
    )


    if not polygon.is_valid:

        raise ValueError(
            "Invalid farm polygon. "
            "The boundary may self-intersect."
        )


    if polygon.area == 0:

        raise ValueError(
            "Farm area is zero."
        )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    (
        area_m2,
        area_hectares,
        area_acres,
        perimeter_m

    ) = calculate_geodesic_metrics(
        points
    )


    centroid = polygon.centroid


    centroid_lat = centroid.y
    centroid_lon = centroid.x


    # --------------------------------------------------------
    # Farm ID
    # --------------------------------------------------------

    farm_id = input(
        "\nFarm ID "
        "(default FARM_001): "
    ).strip()


    if not farm_id:

        farm_id = "FARM_001"


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_farm(

        farm_id,

        points,

        area_m2,

        area_hectares,

        area_acres,

        perimeter_m,

        centroid_lat,

        centroid_lon

    )


    # --------------------------------------------------------
    # Draw
    # --------------------------------------------------------

    draw_farm(
        points,
        polygon
    )


    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("                 FARM REGISTERED")
    print("=" * 65)

    print()

    print(
        f"Farm ID      : {farm_id}"
    )

    print(
        f"Points       : {len(points)}"
    )

    print(
        f"Area         : {area_m2:,.2f} m²"
    )

    print(
        f"Area         : {area_hectares:.4f} ha"
    )

    print(
        f"Area         : {area_acres:.4f} acres"
    )

    print(
        f"Perimeter    : {perimeter_m:.2f} m"
    )

    print(
        f"Centroid     : "
        f"{centroid_lat:.8f}, "
        f"{centroid_lon:.8f}"
    )

    print()

    print(
        "Farm JSON    :",
        FARM_JSON
    )

    print(
        "Farm map     :",
        FARM_MAP
    )

    print()

    print(
        "✓ Farm geometry complete."
    )


if __name__ == "__main__":
    main()