# https://stackoverflow.com/questions/53622518/launch-a-dash-app-in-a-google-colab-notebook
### Save file with Dash app on the Google Colab machine

# Deployment https://dash.plotly.com/deployment

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from my_lib import es1,es2,es3

# Dati per provincia
df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
regione ="Emilia-Romagna"
provincia = "Bologna"

fig1 = es1(df,provincia,regione)
fig2 = es2(df,regione)
fig3 = es3(df,regione)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(id='g1', figure=fig1)
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='g3', figure=fig3)
        ], className="six columns"),
    ], className="row"),
    html.Div([
        dcc.Graph(id='g2', figure=fig2)
    ])
],style={'backgroundColor': "rgb(0,0,0)",  "margin": "0", "padding": "0"})

if __name__ == '__main__':
    app.run_server() #debug=True, host="0.0.0.0", port=8900)