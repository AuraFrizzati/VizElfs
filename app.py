import streamlit as st
import geopandas as gpd
import pydeck as pdk
import json

st.title("Wales LSOA Map - PyDeck Version")

# ---- LOAD SHAPEFILE ----
shapefile_path = "data/shapefile/small_areas_british_grid.shp"
lsoa_gdf = gpd.read_file(shapefile_path)

# ---- FILTER TO WALES ----
lsoa_gdfWal = lsoa_gdf[lsoa_gdf['small_area'].str.startswith('W')]

# ---- REPROJECT ----
lsoa_gdfWal = lsoa_gdfWal.to_crs(epsg=4326)

# ---- CONVERT TO GEOJSON ----
geojson_data = json.loads(lsoa_gdfWal.to_json())

# ---- DEFINE LAYER ----
polygon_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,
    stroked=True,
    filled=False,
    get_line_color=[0, 0, 255],
    get_line_width=20,
)

# ---- VIEW SETTINGS ----
view_state = pdk.ViewState(
    latitude=52.3,
    longitude=-3.8,
    zoom=6.5,
    min_zoom=6,
    max_zoom=12,
    bearing=0,
    pitch=0,
)

# ---- BUILD DECK ----
deck = pdk.Deck(
    layers=[polygon_layer],
    initial_view_state=view_state,
    map_style="light",
)

# ---- DISPLAY ----
st.pydeck_chart(deck)