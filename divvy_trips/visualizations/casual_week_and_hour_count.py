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
curly_url = Path("visualizations/assets/open-bracket.png").resolve()

async def draw():
    width = 130
    height = 50
    arrow_left_down_image = open_image(arrow_url, rotate=-40, opaque=150)
    arrow_right_down_image = open_image(arrow_url, rotate=-50, flip="left", opaque=150)
    curly_down_image = open_image(curly_url, rotate=-90, width=width, height=height)
    
    if (OPTIONS.get("useTestData")):
        BASE_DIR = Path(__file__).resolve().parent
        csv_path = BASE_DIR / "test data" / "casual_week_and_hour_count.csv"
        data = pd.read_csv(csv_path)
    else:
        data = await get_model_data(__file__, options=OPTIONS)
    
    xTicks = np.array([[str(n) + " PM", str(n) + " AM"] for n in range(1, 12, 3)]).flatten()
    legendData = pd.DataFrame({
        "name": ["Weekends (Casual)", "Weekends (Member)", "Weekdays"],
        "color": [theme.themeColor[0], theme.themeColor[1], "gray"],
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
    ).properties(width=500)

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
    ).properties(width=500)

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

    # isCasual = data['Rider Type'] == 'Casual'
    # isCasualWeekEnd = (isCasual) & ((data['Day of Week'] == 'Sunday') | (data['Day of Week'] == 'Saturday'))
    # isMember = ~isCasual
    # isMemberWeekEnd = (isMember) & ((data['Day of Week'] == 'Sunday') | (data['Day of Week'] == 'Saturday'))

    # casualTotal = np.sum(base.data.loc[isCasual, 'Rides Count'])
    # casualWeekendTotal = np.sum(base.data.loc[isCasualWeekEnd, 'Rides Count'])
    # memberTotal = np.sum(base.data.loc[isMember, 'Rides Count'])
    # memberWeekendTotal = np.sum(base.data.loc[isMemberWeekEnd, 'Rides Count'])

    # print(np.round(np.divide(casualWeekendTotal, casualTotal) * 100))
    # print(np.round(np.divide(memberWeekendTotal, memberTotal) * 100))

    curlyBracketImage = alt.Chart().mark_image(
        width=width,
        height=height,
        xOffset=-200
    ).transform_calculate(
        url=f"'{curly_down_image}'"
    ).encode(
        url="url:N"
    )

    arrowImage = alt.Chart().mark_image(
        width=40,
        height=40,
        yOffset=90,
        xOffset=-350
    ).transform_calculate(
        url=f"'{arrow_left_down_image}'"
    ).encode(
        url="url:N",
    )

    arrowImage2 = alt.Chart().mark_image(
        width=40,
        height=40,
        yOffset=10,
        xOffset=-130
    ).transform_calculate(
        url=f"'{arrow_right_down_image}'"
    ).encode(
        url="url:N",
    )

    text1 = alt.Chart().mark_text(
        dy=-70,
        dx=-170
    ).encode(
        text=alt.value(["Morning Commute", "(7-9 AM)"])
    )

    text2 = alt.Chart().mark_text(
        dy=-170,
        dx=170
    ).encode(
        text=alt.value(["Evening Commute", "(4-6 PM)"])
    )

    text3 = alt.Chart().mark_text(
        dy=-190,
        dx=50
    ).encode(
        text=alt.value(["Leisure, tourism, recreation time", "(10 AM - 5 PM)"])
    )

    casualCountChart = (casualCountLine + text3 + curlyBracketImage)
    memberCountChart = (memberCountLine + arrowImage + arrowImage2 + text1 + text2)


    countCharts = (casualCountChart | memberCountChart)
    legendChart = legendText + legendCircle
    chart = alt.vconcat(countCharts, legendChart, center=True, spacing=40)

    chart = chart.properties(
        title=alt.Title(
            text=["Weekdays Are for Work; Weekends Are for Leisure—", "Casual Takes it Far."],
        ),
    )
    
    chart.show()

asyncio.run(draw())