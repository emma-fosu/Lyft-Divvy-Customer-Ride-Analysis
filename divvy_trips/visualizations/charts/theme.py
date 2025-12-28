import altair as alt

@alt.theme.register("divvy_trip_theme", enable=True)
def divvy_trip_theme() -> alt.theme.ThemeConfig:
    return {
        "config": {
            "background": "#f9f9f9",
            "padding": 30,
            "font": "Roboto",
            "customFormatTypes": True,
            "title": {
               "font": "Roboto",
               "fontWeight": 600,
               "fontSize": 25,
               "color": "#031b42",
               "subtitleColor": "#747474",
               "subtitleFontSize": 14,
               "anchor": "start",
               "offset": 60
            },
            "axisX": {
                "ticks": False,
                "title": None,
                "labelFontSize": 12,
                "domain": False,
                "labelAngle": 0,
                "offset": 5,
                "labelFont": "Gotham",
                "labelColor": "#6D6D6D",
                "labelFontWeight": 500
            },
            "axisY": {
                "title": None,
                "ticks": True,
                "domain": False,
                "labelPadding": 5,
                "labelFont": "Libre Franklin",
                "labelBaseline": "middle",
                "labelColor": "#c4c4c4",
                "tickSize": 0,
                "offset": 10,
                "tickCount": 4,
                "gridColor": "#ffffff6c"
            },
            "axis": {
                "titleColor": "#8d8d8d",
                "titleFontWeight": 500
            },
            "view": {
                "stroke": None,
                "clip": False
            },
            "bar": {
                "cornerRadiusTopLeft": 5,
                "cornerRadiusTopRight": 5
            },
            "text": {
                "font": "Roboto",
                "align": "center"
            },
            "line": {
                "interpolate": "monotone",
                "strokeCap": "round",
                "strokeWidth": 4
            }
        }
    }

themeColor = ["#4c78a8", "#720074"]