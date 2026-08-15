import os
import json

import numpy as np
import rasterio
import matplotlib.pyplot as plt


# ============================================================
# AGRISHIELD AI - SATELLITE INDICES
#
# Reads:
#     sentinel_raw.tif
#
# Calculates:
#     NDVI
#     NDWI
#     NDMI
#
# Produces:
#     NDVI / NDWI / NDMI GeoTIFF
#     True-color map
#     NDVI overlay
#     NDWI overlay
#     NDMI overlay
#     analysis_summary.json
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
# 2. PATHS
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


RAW_FILE = os.path.join(

    OUTPUT_DIR,
    "sentinel_raw.tif"

)


METADATA_FILE = os.path.join(

    OUTPUT_DIR,
    "satellite_metadata.json"

)


# ============================================================
# 3. CHECK FILES
# ============================================================

if not os.path.exists(
    FARM_FILE
):

    raise FileNotFoundError(
        "farm.json not found. "
        "Run farm_geometry.py first."
    )


if not os.path.exists(
    RAW_FILE
):

    raise FileNotFoundError(
        "sentinel_raw.tif not found. "
        "Run sentinel2.py first."
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


coordinates = (

    farm_geometry[
        "coordinates"
    ][0]

)


# ============================================================
# 5. LOAD SATELLITE METADATA
# ============================================================

if os.path.exists(
    METADATA_FILE
):

    with open(

        METADATA_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        satellite_metadata = json.load(
            file
        )

else:

    satellite_metadata = {

        "analysis_period": {

            "from":
            None,

            "to":
            None

        }

    }


analysis_period = satellite_metadata.get(

    "analysis_period",

    {}

)


ANALYSIS_FROM = analysis_period.get(
    "from"
)

ANALYSIS_TO = analysis_period.get(
    "to"
)


# ============================================================
# 6. READ RAW TIFF
# ============================================================

with rasterio.open(

    RAW_FILE

) as src:

    raw = src.read()

    profile = src.profile

    transform = src.transform

    crs = src.crs

    width = src.width

    height = src.height


print()
print("=" * 70)
print("             AGRISHIELD AI - INDICES")
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

print()

print(
    "Raster shape:",
    raw.shape
)


# ============================================================
# 7. BAND CHECK
# ============================================================

if raw.shape[0] != 6:

    raise RuntimeError(

        f"Expected 6 bands but received "
        f"{raw.shape[0]}."

    )


# ============================================================
# 8. EXTRACT BANDS
# ============================================================

blue = raw[0].astype(
    np.float32
)

green = raw[1].astype(
    np.float32
)

red = raw[2].astype(
    np.float32
)

nir = raw[3].astype(
    np.float32
)

swir = raw[4].astype(
    np.float32
)

scl = np.rint(
    raw[5]
).astype(
    np.int16
)


# ============================================================
# 9. SCL CLASSES
# ============================================================

scl_classes = {

    0: "No Data",

    1: "Saturated / Defective",

    2: "Dark Area / Shadows",

    3: "Cloud Shadow",

    4: "Vegetation",

    5: "Bare Soil",

    6: "Water",

    7: "Low Probability Cloud / Unclassified",

    8: "Medium Probability Cloud",

    9: "High Probability Cloud",

    10: "Cirrus",

    11: "Snow / Ice"

}


unique_scl, counts = np.unique(

    scl,

    return_counts=True

)


print()

print(
    "========== SCL CLASSES =========="
)


for class_id, count in zip(

    unique_scl,

    counts

):

    name = scl_classes.get(

        int(class_id),

        "Unknown"

    )


    percentage = (

        100 *
        count /
        scl.size

    )


    print(

        f"SCL {int(class_id):>2} | "
        f"{name:<35} | "
        f"{count:>8} pixels | "
        f"{percentage:6.2f}%"

    )


# ============================================================
# 10. CLOUD MASK
# ============================================================

bad_classes = np.array(

    [

        0,   # No Data
        1,   # Saturated / defective
        3,   # Cloud shadow
        8,   # Medium cloud
        9,   # High cloud
        10,  # Cirrus
        11   # Snow / ice

    ],

    dtype=np.int16

)


bad_mask = np.isin(

    scl,

    bad_classes

)


valid_mask = ~bad_mask


valid_count = np.count_nonzero(
    valid_mask
)


invalid_count = np.count_nonzero(
    bad_mask
)


print()

print(
    "========== CLOUD MASK =========="
)

print(
    "Total pixels:",
    scl.size
)

print(
    "Valid pixels:",
    valid_count
)

print(
    "Removed pixels:",
    invalid_count
)

print(

    "Valid percentage:",

    f"{100 * valid_count / scl.size:.2f}%"

)


if valid_count == 0:

    raise RuntimeError(

        "No valid pixels remain after "
        "cloud masking. Try a different "
        "analysis period."

    )


# ============================================================
# 11. NDVI
#
# (NIR - RED) / (NIR + RED)
# ============================================================

ndvi = np.full(

    nir.shape,

    np.nan,

    dtype=np.float32

)


denominator = (

    nir + red

)


mask = (

    valid_mask

    &

    np.isfinite(
        denominator
    )

    &

    (
        denominator != 0
    )

)


ndvi[mask] = (

    (

        nir[mask]
        -
        red[mask]

    )

    /

    denominator[mask]

)


# ============================================================
# 12. NDWI
#
# (GREEN - NIR) / (GREEN + NIR)
# ============================================================

ndwi = np.full(

    nir.shape,

    np.nan,

    dtype=np.float32

)


denominator = (

    green + nir

)


mask = (

    valid_mask

    &

    np.isfinite(
        denominator
    )

    &

    (
        denominator != 0
    )

)


ndwi[mask] = (

    (

        green[mask]
        -
        nir[mask]

    )

    /

    denominator[mask]

)


# ============================================================
# 13. NDMI
#
# (NIR - SWIR) / (NIR + SWIR)
# ============================================================

ndmi = np.full(

    nir.shape,

    np.nan,

    dtype=np.float32

)


denominator = (

    nir + swir

)


mask = (

    valid_mask

    &

    np.isfinite(
        denominator
    )

    &

    (
        denominator != 0
    )

)


ndmi[mask] = (

    (

        nir[mask]
        -
        swir[mask]

    )

    /

    denominator[mask]

)


# ============================================================
# 14. STATISTICS
# ============================================================

def calculate_statistics(

    name,

    data

):

    values = data[
        np.isfinite(data)
    ]


    print()

    print(
        f"========== {name} =========="
    )


    print(
        "Total pixels:",
        data.size
    )


    print(
        "Valid pixels:",
        values.size
    )


    if values.size == 0:

        print(
            "❌ No valid values."
        )

        return None


    result = {

        "mean":
        float(
            np.mean(values)
        ),

        "median":
        float(
            np.median(values)
        ),

        "min":
        float(
            np.min(values)
        ),

        "max":
        float(
            np.max(values)
        ),

        "std":
        float(
            np.std(values)
        ),

        "valid_pixels":
        int(
            values.size
        )

    }


    print(
        f"Mean   : "
        f"{result['mean']:.4f}"
    )

    print(
        f"Median : "
        f"{result['median']:.4f}"
    )

    print(
        f"Min    : "
        f"{result['min']:.4f}"
    )

    print(
        f"Max    : "
        f"{result['max']:.4f}"
    )

    print(
        f"Std    : "
        f"{result['std']:.4f}"
    )


    return result


ndvi_stats = calculate_statistics(

    "NDVI",

    ndvi

)


ndwi_stats = calculate_statistics(

    "NDWI",

    ndwi

)


ndmi_stats = calculate_statistics(

    "NDMI",

    ndmi

)


# ============================================================
# 15. TRUE-COLOR RGB
# ============================================================

rgb = np.stack(

    [

        red,

        green,

        blue

    ],

    axis=-1

).astype(
    np.float32
)


# DN → approximate reflectance
rgb = (
    rgb / 10000.0
)


# Display stretch
rgb = np.clip(

    rgb * 2.5,

    0,

    1

)


# Hide bad pixels
rgb_display = rgb.copy()


rgb_display[
    bad_mask
] = np.nan


# ============================================================
# 16. FARM BOUNDARY
# ============================================================

polygon_x = [

    point[0]

    for point in coordinates

]


polygon_y = [

    point[1]

    for point in coordinates

]


# ============================================================
# 17. RASTER GEOGRAPHIC EXTENT
# ============================================================

left = transform.c

top = transform.f


right = (

    left

    +

    transform.a * width

)


bottom = (

    top

    +

    transform.e * height

)


extent = [

    left,

    right,

    bottom,

    top

]


# ============================================================
# 18. TRUE COLOR MAP
# ============================================================

true_color_file = os.path.join(

    OUTPUT_DIR,

    "farm_true_color.png"

)


plt.figure(

    figsize=(11, 9)

)


plt.imshow(

    rgb_display,

    extent=extent

)


plt.plot(

    polygon_x,

    polygon_y,

    linewidth=3

)


for i, point in enumerate(

    coordinates[:-1],

    start=1

):

    plt.annotate(

        f"P{i}",

        (

            point[0],

            point[1]

        ),

        xytext=(6, 6),

        textcoords="offset points",

        fontsize=10,

        fontweight="bold"

    )


plt.title(

    f"AgriShield AI - Farm True Color\n"
    f"{farm_id}\n"
    f"{ANALYSIS_FROM[:10] if ANALYSIS_FROM else ''}"
    f" → "
    f"{ANALYSIS_TO[:10] if ANALYSIS_TO else ''}"

)


plt.xlabel(
    "Longitude"
)

plt.ylabel(
    "Latitude"
)


plt.grid(
    alpha=0.2
)


plt.tight_layout()


plt.savefig(

    true_color_file,

    dpi=200,

    bbox_inches="tight"

)


plt.show()


# ============================================================
# 19. INDEX OVERLAY FUNCTION
# ============================================================

def create_overlay(

    data,

    name,

    colormap,

    filename

):

    output_file = os.path.join(

        OUTPUT_DIR,

        filename

    )


    plt.figure(

        figsize=(11, 9)

    )


    # --------------------------------------------------------
    # Satellite background
    # --------------------------------------------------------

    plt.imshow(

        rgb_display,

        extent=extent

    )


    # --------------------------------------------------------
    # Index overlay
    # --------------------------------------------------------

    image = plt.imshow(

        data,

        extent=extent,

        vmin=-1,

        vmax=1,

        cmap=colormap,

        alpha=0.68

    )


    # --------------------------------------------------------
    # Farm boundary
    # --------------------------------------------------------

    plt.plot(

        polygon_x,

        polygon_y,

        linewidth=3

    )


    # --------------------------------------------------------
    # Point labels
    # --------------------------------------------------------

    for i, point in enumerate(

        coordinates[:-1],

        start=1

    ):

        plt.annotate(

            f"P{i}",

            (

                point[0],

                point[1]

            ),

            xytext=(6, 6),

            textcoords="offset points",

            fontsize=10,

            fontweight="bold"

        )


    # --------------------------------------------------------
    # Color bar
    # --------------------------------------------------------

    colorbar = plt.colorbar(
        image
    )


    colorbar.set_label(
        name
    )


    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    plt.title(

        f"AgriShield AI - {name}\n"
        f"{farm_id}\n"
        f"{ANALYSIS_FROM[:10] if ANALYSIS_FROM else ''}"
        f" → "
        f"{ANALYSIS_TO[:10] if ANALYSIS_TO else ''}"

    )


    plt.xlabel(
        "Longitude"
    )

    plt.ylabel(
        "Latitude"
    )


    plt.grid(
        alpha=0.2
    )


    plt.tight_layout()


    plt.savefig(

        output_file,

        dpi=200,

        bbox_inches="tight"

    )


    plt.show()


    return output_file


# ============================================================
# 20. CREATE INDEX MAPS
# ============================================================

print()

print(
    "Creating farm maps..."
)


ndvi_map_file = create_overlay(

    ndvi,

    "NDVI",

    "RdYlGn",

    "ndvi_farm_overlay.png"

)


ndwi_map_file = create_overlay(

    ndwi,

    "NDWI",

    "BrBG",

    "ndwi_farm_overlay.png"

)


ndmi_map_file = create_overlay(

    ndmi,

    "NDMI",

    "YlGnBu",

    "ndmi_farm_overlay.png"

)


print(
    "✓ Farm maps created."
)


# ============================================================
# 21. SAVE GEOTIFF
# ============================================================

def save_geotiff(

    filename,

    data

):

    output_file = os.path.join(

        OUTPUT_DIR,

        filename

    )


    output_profile = profile.copy()


    output_profile.update(

        count=1,

        dtype="float32",

        compress="lzw"

    )


    with rasterio.open(

        output_file,

        "w",

        **output_profile

    ) as dst:

        dst.write(

            data.astype(
                np.float32
            ),

            1

        )


    return output_file


ndvi_tif = save_geotiff(

    "ndvi.tif",

    ndvi

)


ndwi_tif = save_geotiff(

    "ndwi.tif",

    ndwi

)


ndmi_tif = save_geotiff(

    "ndmi.tif",

    ndmi

)


print()

print(
    "✓ NDVI GeoTIFF:",
    ndvi_tif
)

print(
    "✓ NDWI GeoTIFF:",
    ndwi_tif
)

print(
    "✓ NDMI GeoTIFF:",
    ndmi_tif
)


# ============================================================
# 22. SUMMARY JSON
# ============================================================

summary = {

    "farm_id":
    farm_id,


    "analysis_period": {

        "from":
        ANALYSIS_FROM,

        "to":
        ANALYSIS_TO

    },


    "point_count":
    farm.get(
        "point_count"
    ),


    "area":
    farm.get(
        "area"
    ),


    "perimeter":
    farm.get(
        "perimeter"
    ),


    "centroid":
    farm.get(
        "centroid"
    ),


    "bounding_box":
    farm.get(
        "bounding_box"
    ),


    "indices": {

        "NDVI":
        ndvi_stats,

        "NDWI":
        ndwi_stats,

        "NDMI":
        ndmi_stats

    },


    "cloud_mask": {

        "total_pixels":
        int(
            scl.size
        ),

        "valid_pixels":
        int(
            valid_count
        ),

        "removed_pixels":
        int(
            invalid_count
        ),

        "valid_percentage":
        float(

            100 *
            valid_count /
            scl.size

        )

    },


    "scl_classes": {

        str(
            int(class_id)
        ):

        {

            "name":
            scl_classes.get(

                int(class_id),

                "Unknown"

            ),

            "pixels":
            int(
                count
            ),

            "percentage":
            float(

                100 *
                count /
                scl.size

            )

        }

        for class_id, count

        in zip(

            unique_scl,

            counts

        )

    },


    "files": {

        "raw":
        RAW_FILE,

        "true_color":
        true_color_file,

        "ndvi":
        ndvi_tif,

        "ndwi":
        ndwi_tif,

        "ndmi":
        ndmi_tif,

        "ndvi_overlay":
        ndvi_map_file,

        "ndwi_overlay":
        ndwi_map_file,

        "ndmi_overlay":
        ndmi_map_file

    }

}


summary_file = os.path.join(

    OUTPUT_DIR,

    "analysis_summary.json"

)


with open(

    summary_file,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        summary,

        file,

        indent=4

    )


# ============================================================
# 23. FINAL
# ============================================================

print()

print("=" * 70)

print(
    "              SATELLITE ANALYSIS COMPLETE"
)

print("=" * 70)

print()

print(
    "Farm ID:",
    farm_id
)

print(
    "Analysis:",
    f"{ANALYSIS_FROM} → {ANALYSIS_TO}"
)

print()

print(
    "Raw Sentinel-2:",
    RAW_FILE
)

print(
    "NDVI:",
    ndvi_tif
)

print(
    "NDWI:",
    ndwi_tif
)

print(
    "NDMI:",
    ndmi_tif
)

print()

print(
    "True color:",
    true_color_file
)

print(
    "NDVI overlay:",
    ndvi_map_file
)

print(
    "NDWI overlay:",
    ndwi_map_file
)

print(
    "NDMI overlay:",
    ndmi_map_file
)

print()

print(
    "Summary:",
    summary_file
)

print()

print(
    "✓ Satellite processing complete."
)