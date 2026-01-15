import argparse
import asyncio
import pandas as pd
import altair as alt
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
    
    if (OPTIONS.get("useTestData")):
        data = pd.DataFrame({
        "Month": [
            "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
            "Sep","Oct","Nov","Dec"
        ],
        "Month Sort": [1,2,3,4,5,6,7,8,9,10,11,12],
        "Ride Count": [
            23453,45551,79421,125864,219378,285465,304612,303141,
            330811,207728,89938,37151
        ]
    })
        data2 = pd.DataFrame({
            "Month": [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ],
            "Month Sort": [1,2,3,4,5,6,7,8,9,10,11,12],
            "Ride Count": [
                116079,172342,214033,276286,369259,401307,
                421087,429440,464902,394054,238352,137195
            ],
            "Duration (min)": [7,8,8,8,9,9,9,9,8,8,7,7]
        })
    else:
        print(__file__)
        data = await get_model_data(__file__, options=OPTIONS)
        data2 = await get_model_data("member_count_by_month.py", options=OPTIONS)

    base = alt.Chart(
        data
    ).encode().properties(width=700)

    countLine = base.mark_line().encode(
        y=alt.Y("Ride Count:Q").axis(title=None, format=".0s").scale(domain=[22000, 305000]),
        color=alt.value(theme.themeColor[0])
    )

    countLine2 = alt.Chart(data=data2).mark_line().encode(
        y=alt.Y("Ride Count:Q").axis(title=None, format=".0s").scale(domain=[100000, 500000]),
        color=alt.value(theme.themeColor[1])
    )

    legendData = pd.DataFrame({
        "name": ["Casual", "Member"],
        "color": theme.themeColor,
        "x": [0, 10]
    })

    legendBase = alt.Chart(legendData).encode( x=alt.X("x:Q").axis(None)).properties(width=100)

    legendText = legendBase.mark_text(
        align="left",
        dx=10,
        dy=1
    ).encode(
        text=alt.Text("name:N")
    )

    legendCircle = legendBase.mark_circle().encode(
        size=alt.value(120),
        color=alt.Color("name:N", scale=alt.Scale(domain=legendData['name'], range=legendData['color'])).legend(None)
    )

    legend = legendText + legendCircle

    note_data = pd.DataFrame({
        "text": [[
                "** Ride count reflects typical usage patterns but do not capture trip distance.",
                "Y-axis minimum adjusted for clarity." 
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

    mainChart = (countLine +
     countLine2
    ).encode(
        x=alt.X("Month:N").title(None).sort(data["Month Sort"], order="ascending")
    ).resolve_scale(
        y="independent"
    ).resolve_axis(
        y="independent"
    )

    countLine = (countLine)
    chart =  alt.vconcat(
        alt.vconcat(mainChart, legend, center=True, spacing=40), 
        note
    )

    chart = chart.properties(
        title=alt.Title(
            text=["Seasonal Changes Affect Equally or", "Doesn't Affect Riders' Behavior Significantly."],
        ),
    )
    
    # chart.show()
    chart.save("visualizations/jsons/member_casual_by_month.json") # Create the json spec to be embeded in html.

asyncio.run(draw())