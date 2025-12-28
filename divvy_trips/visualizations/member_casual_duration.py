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
       y=alt.Y("Duration (min):Q", axis=alt.Axis(labelExpr="datum.value + 'min'", title="Duration")),
       color=alt.Color("Rider Type:N").legend(None),
    ).transform_calculate(
        duration_label="datum['Duration (min)'] + ' min'"
    )

    chart1 = base1.mark_bar().properties(
        width=200
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
       y=alt.Y("Distance (km):Q", axis=alt.Axis(labelExpr="datum.value + 'km'", title="Distance")),
       color=alt.Color("Rider Type:N").legend(None),
    ).transform_calculate(
        distance_label="datum['Distance (km)'] + ' km'"
    )

    chart2 = base2.mark_bar().properties(width=200)

    text2 = base2.mark_text(
        baseline='bottom',
        dy=-5,
        fontSize=20,
        fontWeight=500,
    ).encode(
        text=alt.Text("distance_label:N")
    )

    duration = (data.loc[data['Rider Type'] == 'Casual', 'Duration (min)']).iloc[0] - (data.loc[data['Rider Type'] == 'Member', 'Duration (min)']).iloc[0]
    kpi_data = pd.DataFrame({
        'text1': [['Both fairly rides the same distance but,', 'Casual goes']],
        'text2': ['more than Member.'],
        'duration': [
            str(duration) +
            ' min'
        ]
    })

    emphasisBase = alt.Chart(kpi_data).properties(width=300)

    stext1 = alt.Chart(kpi_data).mark_text(
        fontSize=13,
        font="Inter",
        color="#5A5A5A",
        align='left',
        baseline='top',
        lineHeight=25
    ).encode(
        x=alt.value(0),
        y=alt.value(0),
        text='text1'
    )
    stext2 = alt.Chart(kpi_data).mark_text(
        fontSize=13,
        font="Inter",
        color="#5A5A5A",
        align='left',
        baseline='top',
        lineHeight=20
    ).encode(
        x=alt.value(0),
        y=alt.value(135),
        text='text2'
    )
    durationText = emphasisBase.mark_text(
        fontSize=110,
        fontWeight='bold',
        color='#4c78a8',
        align='left',
        baseline='top'
    ).encode(
        x=alt.value(0),
        y=alt.value(40),
        text=alt.Text("duration")
    )

    note_data = pd.DataFrame({
        "text": [[
                "** Equal distances do not imply similar riding speeds.",
                "Longer duration for casual riders suggests behavioral differences and may require further investigation." 
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

    kpi_text = stext1 + stext2 + durationText

    barchart1 = chart1 + text1
    barchart2 = chart2 + text2
    chart =  alt.vconcat(
                alt.hconcat(
                    alt.hconcat(barchart1, barchart2, spacing=20), 
                    kpi_text, spacing=50),
                note)

    chart = chart.properties(
        title=alt.Title(
            text="Frequent Riders, Shorter Duration, Longer Distance?",
            subtitle="Does the notion longer ride time always means longer distance?"
        ),
    ).configure_axisY(
        titleColor="#818181",
        titleFontWeight=400,
        titleFontStyle="italic",
        titleAnchor="start",
    )
    
    chart.show()

asyncio.run(draw())