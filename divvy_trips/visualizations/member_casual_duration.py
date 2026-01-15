import argparse
import asyncio
import pandas as pd
import altair as alt
from utils import get_model_data
from .charts import theme


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
    if (OPTIONS.get("useTestData")):
        data = pd.DataFrame({
            "Rider Type": ["Casual", "Member"],
            "Duration (min)": [12, 8],
            "Distance (km)": [1.64, 1.6]
        })
    else:
        data = await get_model_data(__file__, options=OPTIONS)

    base1 = alt.Chart(
        data
    ).encode(
       x=alt.X("Rider Type:N"),
       y=alt.Y("Duration (min):Q", axis=alt.Axis(title="Duration", labels=False)),
       color=alt.Color("Rider Type:N").legend(None).scale(domain=data['Rider Type'], range=theme.themeColor),
    ).transform_calculate(
        duration_label="datum['Duration (min)'] + ' min'"
    )

    chart1 = base1.mark_bar().properties(
        width=300
    )

    text1 = base1.mark_text(
        baseline='bottom',
        dy=-5,
        fontSize=20,
        fontWeight=500,
    ).encode(
        text=alt.Text("duration_label:N")
    )

    base2 = alt.Chart(
        data
    ).encode(
       x=alt.X("Rider Type:N"),
       y=alt.Y("Distance (km):Q", axis=alt.Axis(title="Distance", labels=False)),
       color=alt.Color("Rider Type:N").legend(None).scale(domain=data["Rider Type"], range=theme.themeColor),
    ).transform_calculate(
        distance_label="format(datum['Distance (km)'], '.2f') + ' km'"
    )

    chart2 = base2.mark_bar().properties(width=300)

    text2 = base2.mark_text(
        baseline='bottom',
        dy=-5,
        fontSize=20,
        fontWeight=500,
    ).encode(
        text=alt.Text("distance_label:N")
    )

    note_data = pd.DataFrame({
        "text": [[
                "** Equal distances do not imply similar riding speeds.",
                "A longer duration for casual riders suggests behavioral differences and may require further investigation." 
        ]]
    })

    note = alt.Chart(note_data).mark_text(
        fontSize=10,
        font="Inter",
        color= "#808084",
        fontStyle="italic",
        lineHeight=16,
        align="left"
    ).encode(
        text="text"
    )

    barchart1 = chart1 + text1
    barchart2 = chart2 + text2
    chart =  alt.vconcat(alt.hconcat(barchart1, barchart2, spacing=30), note)

    chart = chart.properties(
        title=["Same Distance Covered", "But Casuals Ride 4 min Longer."]
    ).configure_axisY(
        titleColor="#818181",
        titleFontWeight=400,
        titleFontStyle="italic",
        titleAnchor="start",
    )
    
    # chart.show() # Show the chart with the default browser
    chart.save("visualizations/jsons/member_casual_duration.json") # Create the json spec to be embeded in html.

asyncio.run(draw())