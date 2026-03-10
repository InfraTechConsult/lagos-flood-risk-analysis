"""
PROJECT
-------
Lagos Flood Risk Impact on Road Infrastructure

DESCRIPTION
-----------
Analyzes road infrastructure exposure to potential flood zones
using OpenStreetMap road data and spatial buffering.

OUTPUT
------
flood_road_risk_map.png
"""

import logging
from pathlib import Path
import warnings

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import osmnx as ox
from xyzservices import providers

warnings.filterwarnings("ignore")

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_NAME = "Lagos Flood Risk Impact on Road Infrastructure"

BUFFER_DISTANCE_METERS = 200

DATA_FILE = "lagos_roads.geojson"

OUTPUT_MAP = "flood_road_risk_map.png"

PLACE_NAME = "Victoria Island, Lagos, Nigeria"

TARGET_CRS = "EPSG:3857"

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_PATH = PROJECT_DIR / DATA_FILE

OUTPUT_PATH = PROJECT_DIR / OUTPUT_MAP

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.getLogger(__name__)

# --------------------------------------------------
# DOWNLOAD ROAD DATA
# --------------------------------------------------

def download_road_data():

    log.info("Downloading road network from OpenStreetMap...")

    try:

        graph = ox.graph_from_place(
            PLACE_NAME,
            network_type="drive"
        )

        roads = ox.graph_to_gdfs(graph, nodes=False)

        roads.to_file(DATA_PATH, driver="GeoJSON")

        log.info("Road network saved to %s", DATA_PATH)

    except Exception as e:

        log.error("OSM download failed: %s", e)
        raise


# --------------------------------------------------
# LOAD ROADS
# --------------------------------------------------

def load_roads():

    if not DATA_PATH.exists():

        log.warning("Road dataset missing. Downloading...")

        download_road_data()

    roads = gpd.read_file(DATA_PATH)

    roads = roads[roads.geometry.notnull()]

    log.info("Loaded %d road segments", len(roads))

    return roads


# --------------------------------------------------
# GENERATE FLOOD BUFFERS
# --------------------------------------------------

def generate_flood_zones(roads):

    log.info("Generating flood risk buffers...")

    roads = roads.to_crs(TARGET_CRS)

    flood_buffers = roads.buffer(BUFFER_DISTANCE_METERS)

    flood_gdf = gpd.GeoDataFrame(
        geometry=flood_buffers,
        crs=TARGET_CRS
    )

    # dissolve overlapping buffers
    flood_gdf["dissolve"] = 1
    flood_gdf = flood_gdf.dissolve(by="dissolve")

    return roads, flood_gdf


# --------------------------------------------------
# MAP EXTENT PADDING
# --------------------------------------------------

def get_bounds(gdf):

    xmin, ymin, xmax, ymax = gdf.total_bounds

    padding_x = (xmax - xmin) * 0.05
    padding_y = (ymax - ymin) * 0.05

    return (
        xmin - padding_x,
        ymin - padding_y,
        xmax + padding_x,
        ymax + padding_y
    )


# --------------------------------------------------
# GENERATE MAP
# --------------------------------------------------

def generate_map(roads, flood_gdf):

    log.info("Rendering map...")

    fig, ax = plt.subplots(figsize=(12,12))

    flood_gdf.plot(
        ax=ax,
        color="red",
        alpha=0.25,
        edgecolor="none",
        label="Flood Risk Zone"
    )

    roads.plot(
        ax=ax,
        color="black",
        linewidth=0.7,
        label="Road Network"
    )

    xmin, ymin, xmax, ymax = get_bounds(roads)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # basemap
    try:

        ctx.add_basemap(
            ax,
            source=providers.OpenStreetMap.Mapnik,
            crs=TARGET_CRS,
            zoom="auto"
        )

    except Exception as e:

        log.warning("Basemap failed: %s", e)

    ax.set_title(PROJECT_NAME, fontsize=14)

    ax.legend()

    ax.set_axis_off()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    log.info("Map exported: %s", OUTPUT_PATH)


# --------------------------------------------------
# MAIN WORKFLOW
# --------------------------------------------------

def main():

    log.info("Starting Lagos flood risk analysis...")

    roads = load_roads()

    roads, flood_gdf = generate_flood_zones(roads)

    generate_map(roads, flood_gdf)

    log.info("Analysis completed successfully.")


# --------------------------------------------------

if __name__ == "__main__":

    main()