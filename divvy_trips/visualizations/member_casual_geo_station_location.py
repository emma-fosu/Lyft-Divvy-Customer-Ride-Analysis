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

async def draw():

    BASE_DIR = Path(__file__).resolve().parent
    if (OPTIONS.get("useTestData")):
        csv_path = BASE_DIR / "test data" / "top_10_start_location_casual_member.csv"
        startStationData = pd.read_csv(csv_path)

        csv_path = BASE_DIR / "test data" / "top_10_end_location_casual_member.csv"
        endStationData  = pd.read_csv(csv_path)
    else:
        startStationData = await get_model_data("top_10_start_location_casual_member", options=OPTIONS)
        endStationData = await get_model_data("top_10_end_location_casual_member", options=OPTIONS)

    csv_path = BASE_DIR / "test data" / "casual_station_image.csv"
    startStationMap = pd.read_csv(csv_path)
    startStationData = pd.merge(startStationData, startStationMap, on="Station Name", how="left")

    chicago =  geopd.read_file(filename="https://data.cityofchicago.org/resource/unjd-c2ca.geojson")
    centroids = chicago.geometry.union_all().centroid
    center = [centroids.x, centroids.y]
    width = 300
    height = 500

    selection = alt.selection_point(
        fields=["Rider Type"]
    )

    california_map = alt.Chart(chicago).mark_geoshape(
        fill="#f2f2f2",
        stroke="#cacaca",
        strokeWidth=0.5,
        clip=True
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[width/2, height/2]
    ).properties(
        width=width,
        height=height
    )

    points = alt.Chart(startStationData).mark_circle(

    ).encode(
        longitude='lng:Q',
        latitude='lat:Q',
        size=alt.Size('Ride Count:Q', scale=alt.Scale(domain=startStationData['Ride Count'], range=np.array(startStationData['Ride Count']) / 50)).legend(None),
        color=alt.Color("Rider Type:N").legend(None).scale(domain=startStationData['Rider Type'], range=theme.themeColor),
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
        tooltip=alt.Tooltip(['Station Name'])
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[width/2, height/2]
        )

    points2 = alt.Chart(endStationData).mark_circle(
        
    ).encode(
        longitude='lng:Q',
        latitude='lat:Q',
        size=alt.Size('Ride Count:Q', scale=alt.Scale(domain=startStationData['Ride Count'], range=np.array(startStationData['Ride Count']) / 50)).legend(None),
        color=alt.Color("Rider Type:N").legend(None).scale(domain=startStationData['Rider Type'], range=theme.themeColor),
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
        tooltip=alt.Tooltip('Station Name:N')
    ).project(
        type="mercator",
        center=center,
        scale=85000,
        translate=[width/2, height/2]
        )
    
    legendData = pd.DataFrame({
        "Rider Type": ["Casual", "Member"],
        "color": [theme.themeColor[0], theme.themeColor[1]],
        "x": [0, 15]
    })

    legendBase = alt.Chart(legendData).encode( x=alt.X("x:Q").axis(None))

    legendText = legendBase.mark_text(
        align="left",
        dx=10,
        dy=1
    ).encode(
        text=alt.Text("Rider Type:N"),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    )

    legendCircle = legendBase.mark_circle().encode(
        size=alt.value(120),
        color=alt.Color("Rider Type:N", scale=alt.Scale(domain=legendData['Rider Type'], range=legendData['color'])).legend(None),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    )

    legendChart = (legendText + legendCircle).add_params(selection).properties(width=100)
    geoChart1 = (california_map + points)
    geoChart2 = (california_map + points2)
    chart = alt.vconcat(
        alt.hconcat(geoChart1, geoChart2, center=True, spacing=150),
        legendChart,
        spacing=30,
        center=True
    )

    chart = chart.properties(
        title=alt.Title(
            text=[f"Casual Engages More in Weekends than in Weekdays", f"with min Longer Rides"]
        ),
    )

    chart.show()



asyncio.run(draw())