

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
    arrow_image_data = open_image(arrow_url, rotate=-40)

    if (OPTIONS.get("useTestData")):
        data = pd.DataFrame({
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
        data = await get_model_data(__file__, options=OPTIONS)

    base = alt.Chart(
        data
    ).encode(
       x=alt.X("Month:N").title(None).sort(data["Month Sort"], order="ascending")
    ).properties(width=700)

    countLine = base.mark_line().encode(
         y=alt.Y("Ride Count:Q").axis(title="Rides Count", format=".0s").scale(domain=[100000, 470000])
    )

    durationLine = base.mark_line(
        color="#4c78a871",
        strokeWidth=2,
        strokeDash=[4, 4]
    ).encode(
        y=alt.Y("Duration (min)").axis(title="Duration", labelExpr="datum.value + ' min'").scale(domain=[6, 10])
    )

    arrowImage = countLine.mark_image(
        width=50,
        height=50,
        yOffset=-220,
        xOffset=-20
    ).transform_filter(
        alt.datum['Month'] == 'Saturday'
    ).transform_calculate(
        url=f"'{arrow_image_data}'"
    ).encode(
        url="url:N"
    )

    wednesdayText1 = base.mark_text(
        baseline='bottom',
        fontSize=15,
        fontWeight=400,
        align="left",
        lineHeight=20,
        color="#325172",
        dy=-180,
        dx=-220
    ).transform_filter(
        alt.datum['Month'] == 'Saturday'
    ).transform_calculate(
        text="['Weekend rides are 40%', 'longer despite fewer trips.']"
    ).encode(
        text="text:N"
    ) + arrowImage

    weekend_band = base.mark_rect(
        opacity=0.2,
        color='lightgray'
    ).transform_filter(
        (alt.datum['Month'] == 'Saturday') | (alt.datum['Month'] == 'Sunday')
    ).transform_calculate(
        y='1'
    ).encode(
        y=alt.Y("y:Q").axis(None)
    )

    note_data = pd.DataFrame({
        "text": [[
                "** Ride duration and count reflect typical usage patterns but do not capture trip distance or route.",
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

    wednesdayText = alt.layer(wednesdayText1)
    countLine = (countLine)
    chart =  alt.vconcat(
    (alt.layer(
            countLine, 
            durationLine
        ).resolve_scale(
            y="independent"
        ) + weekend_band),
    note
    )

    chart = chart.properties(
        title=alt.Title(
            text="Seasonal Riding Patterns Show Strong Summer Peak and Winter Slowdown",
            subtitle="Member Riders Only"
        ),
    )
    
    chart.show()

asyncio.run(draw())