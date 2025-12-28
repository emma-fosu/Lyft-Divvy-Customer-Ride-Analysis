import argparse
import asyncio
import pandas as pd
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
        csv_path = BASE_DIR / "test data" / "casual_week_and_hour_count.csv"
        data = pd.read_csv(csv_path)
    else:
        data = await get_model_data(__file__, options=OPTIONS)
    
    xTicks = np.array([[str(n) + " PM", str(n) + " AM"] for n in range(1, 12, 3)]).flatten()
    legendData = pd.DataFrame({
        "name": ["Weekends (Casual)", "Weekends (Member)", "Weekdays"],
        "color": ["red", "yellow", "green"],
        "x": [0, 15, 30]
    })

    base = alt.Chart(data).transform_calculate(
        day_type="datum['Day of Week'] == 'Sunday' || datum['Day of Week'] == 'Saturday' ? 'Weekdays' : 'Weekends'"
    )

    legendBase = alt.Chart(legendData).encode( x=alt.X("x:Q").axis(None))

    
    casualCountBase = base.transform_filter(
        alt.datum['Rider Type'] == 'Casual'
    ).encode(
       x=alt.X(
           "Hour of Day:N",
           axis=alt.Axis(values=xTicks)
        ).title(None).sort(data["Hour of Day Sort"], order="ascending")
    ).properties(width=400)

    casualCountLine = casualCountBase.mark_line().encode(
         y=alt.Y("Rides Count:Q").axis(title="Rides Count", format=".0s"),
         detail=alt.Detail("Day of Week:N"),
         color=alt.condition("datum['day_type'] == 'Weekdays'", alt.value("#4c78a8"), alt.value("gray")),
         opacity=alt.condition("datum['day_type'] == 'Weekdays'", alt.value(1), alt.value(0.2)),
    )
    
    memberCountBase = base.transform_filter(
        alt.datum['Rider Type'] == 'Member'
    ).encode(
       x=alt.X(
           "Hour of Day:N",
           axis=alt.Axis(values=xTicks)
        ).title(None).sort(data["Hour of Day Sort"], order="ascending")
    ).properties(width=400)

    memberCountLine = memberCountBase.mark_line().encode(
         y=alt.Y("Rides Count:Q").axis(title=None, format=".0s"),
         detail=alt.Detail("Day of Week:N"),
         color=alt.condition("datum['day_type'] == 'Weekdays'", alt.value("#854685"), alt.value("gray")),
         opacity=alt.condition("datum['day_type'] == 'Weekdays'", alt.value(1), alt.value(0.5)),
    )

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

    # durationLine = base.mark_line(
    #     color="#4c78a871",
    #     strokeWidth=2,
    #     strokeDash=[4, 4]
    # ).encode(
    #     y=alt.Y("Duration (min)").axis(title="Duration", labelExpr="datum.value + ' min'").scale(domain=[6, 15])
    # )

    # arrowImage = countLine.mark_image(
    #     width=50,
    #     height=50,
    #     yOffset=-220,
    #     xOffset=-20
    # ).transform_filter(
    #     alt.datum['Month'] == 'Saturday'
    # ).transform_calculate(
    #     url=f"'{arrow_image_data}'"
    # ).encode(
    #     url="url:N"
    # )

    # wednesdayText1 = base.mark_text(
    #     baseline='bottom',
    #     fontSize=15,
    #     fontWeight=400,
    #     align="left",
    #     lineHeight=20,
    #     color="#325172",
    #     dy=-180,
    #     dx=-220
    # ).transform_filter(
    #     alt.datum['Month'] == 'Saturday'
    # ).transform_calculate(
    #     text="['Weekend rides are 40%', 'longer despite fewer trips.']"
    # ).encode(
    #     text="text:N"
    # ) + arrowImage

    # weekend_band = base.mark_rect(
    #     opacity=0.2,
    #     color='lightgray'
    # ).transform_filter(
    #     (alt.datum['Month'] == 'Saturday') | (alt.datum['Month'] == 'Sunday')
    # ).transform_calculate(
    #     y='1'
    # ).encode(
    #     y=alt.Y("y:Q").axis(None)
    # )

    # note_data = pd.DataFrame({
    #     "text": [[
    #             "** Ride duration and count reflect typical usage patterns but do not capture trip distance or route.",
    #             "Y-axis minimum adjusted for clarity." 
    #     ]]
    # })

    # note = alt.Chart(note_data).mark_text(
    #     fontSize=10,
    #     font="Inter",
    #     color= "#808084",
    #     fontStyle="italic",
    #     lineHeight=16,
    #     align="left"
    # ).encode(
    #     text="text"
    # )

    # wednesdayText = alt.layer(wednesdayText1)
    casualCountChart = (casualCountLine)
    memberCountChart = (memberCountLine)


    countCharts = (casualCountChart | memberCountChart)
    legendChart = legendText + legendCircle
    chart = alt.vconcat(countCharts, legendChart, center=True, spacing=40)
    # chart =  alt.vconcat(
    # (alt.layer(
    #         countLine, 
    #         durationLine
    #     ).resolve_scale(
    #         y="independent"
    #     ) + weekend_band),
    # note
    # )

    chart = chart.properties(
        title=alt.Title(
            text="How ride goes during the day throughout the week",
            subtitle="Casual Riders Only"
        ),
    )
    
    chart.show()

asyncio.run(draw())