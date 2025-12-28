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
            "Total Rides": [2052513, 3634336],
            "Proportion (%)": [0.3609, 0.6391]
        })
    else:
        data = await get_model_data(__file__, options=OPTIONS)

    base = alt.Chart(
        data
    ).encode(
       x=alt.X("Rider Type:N"),
       y=alt.Y("Total Rides:Q", axis=alt.Axis(format=".1s")),
       color=alt.Color("Rider Type:N").legend(None).scale(domain=data["Rider Type"], range=theme.themeColor),
    ).properties(width=300)

    bar = base.mark_bar()

    text = base.mark_text(
        baseline='bottom',
        dy=-5,
        fontSize=20,
        fontWeight=500,
    ).encode(
        text=alt.Text("Total Rides:Q", format='.2s')
    )

    kpi_data = pd.DataFrame({
        'main_text': [data.loc[data['Rider Type'] == 'Member', 'Proportion (%)']],
        'sub_text': [
            ['of rides is Member account.', 
             ' ',
             'Higher frequency indicates not a one-time or ',
             'occasional customer, but strong engagement ',
             'and repeat usage.']
            ]
    })

    emphasisBase = alt.Chart(kpi_data, width=300).properties(width=300)

    boldText = emphasisBase.mark_text(
        fontSize=130,
        fontWeight='bold',
        color='#f58518',
        align='left',
        baseline='top'
    ).encode(
        x=alt.value(0),
        y=alt.value(0),
        text=alt.Text("main_text").format(".0%")
    )
    sub_label = alt.Chart(kpi_data).mark_text(
        fontSize=13,
        font="Inter",
        color="#5A5A5A",
        align='left',
        baseline='top',
        lineHeight=20
    ).encode(
        x=alt.value(10),
        y=alt.value(115),
        text='sub_text'
    )

    note_data = pd.DataFrame({
        "text": [[
                "** Frequency refers strictly to trip counts, not trip length or time.",
                "Further investigation is necessary to explore scenarios where casual riders may outnumber member" 
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

    kpi_text = boldText + sub_label
    barchart = bar + text
    chart =  alt.vconcat(barchart | kpi_text, note)

    chart = chart.properties(
        title=alt.Title(
            text="Who Rides the Most?",
        ),
    )
    
    chart.show()

asyncio.run(draw())