import argparse
import asyncio
import pandas as pd
import geopandas as geopd 
import altair as alt
import numpy as np
from utils import get_model_data
from pathlib import Path
from .charts import theme
from .charts import open_image


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--compile", action='store_true')
parser.add_argument("--useTestData", action="store_true")

args = parser.parse_args()

OPTIONS = {
    "shouldCompile": args.compile,
    "useTestData": args.useTestData
}

alt.renderers.enable("browser")

arrow_url = Path("visualizations/assets/arrow_left_down.png").resolve()

async def draw():
    # arrow_image_data = open_image(arrow_url, rotate=-40)
    
    if (OPTIONS.get("useTestData")):
        BASE_DIR = Path(__file__).resolve().parent
        csv_path = BASE_DIR / "test data" / "top_10_start_location_casual_member.csv"
        startStationData = pd.read_csv(csv_path)

        csv_path = BASE_DIR / "test data" / "top_10_end_location_casual_member.csv"
        endStationData  = pd.read_csv(csv_path)
    else:
        startStationData = await get_model_data("top_10_start_location_casual_member", options=OPTIONS)
        endStationData = await get_model_data("top_10_end_location_casual_member", options=OPTIONS)

    chicago =  geopd.read_file(filename="https://data.cityofchicago.org/resource/unjd-c2ca.geojson")
    centroids = chicago.geometry.union_all().centroid
    center = [centroids.x, centroids.y]

    selection = alt.selection_point(fields=['Rider Type'], bind='legend')

    california_map = alt.Chart(chicago).mark_geoshape(
        fill="#f2f2f2",
        stroke="#cacaca",
        strokeWidth=0.5,
        clip=True
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[600/2, 600/2]
    ).properties(
        width=600,
        height=600
    )

    points = alt.Chart(startStationData).mark_circle(

    ).encode(
        longitude='lng:Q',
        latitude='lat:Q',
        size=alt.Size('Ride Count:Q', scale=alt.Scale(domain=startStationData['Ride Count'], range=np.array(startStationData['Ride Count']) / 50)).legend(None),
        color=alt.Color("Rider Type:N"),
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
        tooltip=alt.Tooltip('Station Name:N')
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[600/2, 600/2]
        ).add_params(selection)

    points2 = alt.Chart(endStationData).mark_circle(
        
    ).encode(
        longitude='lng:Q',
        latitude='lat:Q',
        size=alt.Size('Ride Count:Q', scale=alt.Scale(domain=startStationData['Ride Count'], range=np.array(startStationData['Ride Count']) / 50)).legend(None),
        color=alt.Color("Rider Type:N"),
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
        tooltip=alt.Tooltip('Station Name:N')
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[600/2, 600/2]
        )

    geoChart1 = (california_map + points)
    geoChart2 = (california_map + points2)
    alt.hconcat(geoChart1, geoChart2, center=True).configure_legend(
        orient="bottom",
        title=None,
        symbolSize=120,
        direction="horizontal",
        labelFontSize=14,
    ).resolve_legend(color="shared").show()



asyncio.run(draw())