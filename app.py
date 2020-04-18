# https://stackoverflow.com/questions/53622518/launch-a-dash-app-in-a-google-colab-notebook
### Save file with Dash app on the Google Colab machine

# Deployment https://dash.plotly.com/deployment

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from mylib import *
import time



# dati regioni: df_regioni = pd.read_csv(https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv)

# https://plotly.com/~yusuf.sultan/119/pie-charts-5-labels-text-hoverinf/#/
# lista contenente nomi di tutte le regioni e province

regione ="Emilia-Romagna"
provincia = "Bologna"

# Dati per provincia
df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
fig_naz = plot_nazionale(df_nazionale)
fig_var_naz = plot_variazione_nazionale(df_nazionale)
totale_positivi,dimessi_guariti,deceduti,nuovi_positivi,totale_casi = get_info_data(df_nazionale)


# Dati per provincia
df_regioni = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
df_regioni["data"] = pd.to_datetime(df_regioni["data"]).dt.date
fig_reg = plot_regioni(df_regioni, regione)

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
df["data"] = pd.to_datetime(df["data"]).dt.date
lista_date = (df["data"].unique())
ultima_data = lista_date[-1].strftime("%A %d %b  %Y")
dict_date={}
for c in range(0,len(lista_date),3):
    # https://www.guru99.com/date-time-and-datetime-classes-in-python.html
    dict_date[c] = {"label": lista_date[c].strftime("%b %d")} 

nomi_regioni_province = ["Tutte"] +  get_nomi_regioni(df) + get_nomi_province(df)


#fig1 = es1(df,provincia,regione)
fig_line=fig_pie=fig_map=None 
fig_line,fig_pie = plot_totale_casi_provincia(df, regione)
fig_map = plot_map(df)
#fig2 = es2(df,regione)
#fig3 = es3(df,regione)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
                html.Div(
                    [html.H6(id="info_text"), 
                    html.P("Covid19 Dashboard Italia"), #html.P("Autore: Manuel Rucci"), 
                    html.P(html.A("Github Project Link", href="https://github.com/visiont3lab/covid19-dash-plotly")),  
                    html.P(html.A("Dati forniti dalla Protezione Civile", href="https://github.com/pcm-dpc/COVID-19")),
                    html.P("Ultimo aggiornamento: " + ultima_data)],
                    id="info",
                    className="four columns info_container "
                ),
                html.Div([
                    html.Div(
                        [html.H6(id="totale-positivi"), html.H6("Totale Positivi"), html.H6(totale_positivi, style={"text-align": "center"})],
                        className="mini_container"
                    ),
                    html.Div(
                        [html.H6(id="dimessi-guariti"), html.H6("Dimessi Guariti"), html.H6(dimessi_guariti, style={"text-align": "center"})],
                        className="mini_container"
                    ),
                    html.Div(
                        [html.H6(id="deceduti"), html.H6("Deceduti"),html.H6(deceduti, style={"text-align": "center"})],
                        className="mini_container"
                    ),
                    html.Div(
                        [html.H6(id="nuovi-positivi"), html.H6("Nuovi Positivi"),html.H6(nuovi_positivi , style={"text-align": "center"})],
                        className="mini_container"
                    ),
                    html.Div(
                        [html.H6(id="totale-casi"), html.H6("Totale Casi"),html.H6(totale_casi, style={"text-align": "center"})],
                        className="mini_container"
                    )
                ], id="info-container", className="eight columns flex-display"),
            ], className="row"),
        html.Div([
                html.Div([
                    html.H3("Analisi Nazionale"),
                    # Config figure options https://plotly.com/python/configuration-options/
                    dcc.Graph(id='fig-naz', figure=fig_naz) #, config=dict(scrollZoom=False))
                ], className="six columns pretty_container"),
                html.Div([
                    html.H3("Variazione Nazionale Totale Positivi"),
                    dcc.Graph(id='fig-var-naz', figure=fig_var_naz)
                ], className="six columns pretty_container"),
            ], className="row"),
        html.Div([
                html.Div([
                    html.H3("Analisi Regionale"),
                    dcc.Dropdown(
                        id="dropdown-regioni",
                        options=[{'label':nome, 'value':nome} for nome in get_nomi_regioni(df)],
                        value=regione,
                        searchable=True,
                        multi=True
                    ), 
                    dcc.RadioItems(
                        id = "radio-buttom-plot-style",
                        options=[
                            {'label': 'line plot', 'value': 'line_plot'},
                            {'label': 'area plot', 'value': 'area_plot'},
                        ],
                        value='area_plot',
                        labelStyle={'display': 'inline-block'}
                    ),   
                    dcc.Graph(id='fig-reg', figure=fig_reg),
                    dcc.Checklist(
                        id="checklist",
                        options=[{'label':  nome.replace("_"," "), 'value': nome} for nome in list(df_regioni.keys()[6:-2])],
                        value=['deceduti', 'variazione_totale_positivi','terapia_intensiva'],
                        labelStyle={'display': 'inline-block'}
                    ),  
                ],className="six columns pretty_container"),
                html.Div([
                    html.H3("Totale Casi per provincia"),
                    dcc.Graph(id='fig-map', figure=fig_map),
                    #dcc.Interval(id='auto-stepper',
                    #    interval=1*1000, # in milliseconds
                    #    n_intervals=0
                    #),
                    dcc.Slider(
                        id='slider-map',
                        min=1,
                        max=len(lista_date)-1,
                        step=1,
                        value=len(lista_date)-1,
                        #updatemode='drag', #'mpuseup' #https://dash.plotly.com/dash-core-components/slider
                        marks = dict_date,
                        vertical=False
                        ),
                    ], className="six columns pretty_container"),
            ], className="row"), 
        html.Div([
                html.Div([
                    html.H3("Analisi provinciale"),
                    dcc.Dropdown(
                        id="dropdown-province",
                        options=[{'label':nome, 'value':nome} for nome in nomi_regioni_province],
                        value=regione,
                        searchable=True,
                        multi=True
                    ), 
                    dcc.RadioItems(
                        id = "radio-buttom-province",
                        options=[
                            {'label': 'Mostra Tutti', 'value': 'Mostra Tutti'},
                            {'label': 'Mostra Solo Primi 10', 'value': 'Mostra Solo Primi 10'},
                        ],
                        value='Mostra Solo Primi 10',
                        labelStyle={'display': 'inline-block'}
                    ),      
                    dcc.Graph(id='fig-line', figure=fig_line)
                ],className="six columns pretty_container"),
                html.Div([
                    dcc.Graph(id='fig-pie', figure=fig_pie)
                ], className="six columns pretty_container"),
            ],className="row")
        ])
    ],id="main")

@app.callback(
    [dash.dependencies.Output('fig-line', 'figure'),dash.dependencies.Output('fig-pie', 'figure')],
    [dash.dependencies.Input('dropdown-province', 'value'),dash.dependencies.Input('radio-buttom-province', 'value')])
def update_figs(lista_province, radio_buttom_value):
    fig_line, fig_pie = plot_totale_casi_provincia(df, lista_province,radio_buttom_value)
    return fig_line, fig_pie

'''
@app.callback(
    [dash.dependencies.Output('fig-map', 'figure'),dash.dependencies.Output('slider-map', 'value')],
    [dash.dependencies.Input('auto-stepper', 'n_intervals')])
def update_map(n_intervals):
    step_num = len(lista_date)-2
    num=1
    if n_intervals is not None:
        num = (n_intervals+1)%step_num
        fig_map = plot_map(df, lista_date[num])
    return fig_map,num
'''


@app.callback(dash.dependencies.Output('fig-map', 'figure'),
    [dash.dependencies.Input('slider-map', 'value')])
def update_map(slider_value):
    fig_map = plot_map(df, lista_date[slider_value])
    return fig_map


@app.callback(dash.dependencies.Output('fig-reg', 'figure'),
    [dash.dependencies.Input('checklist', 'value'),
    dash.dependencies.Input('radio-buttom-plot-style', 'value'),
    dash.dependencies.Input('dropdown-regioni', 'value')])
def update_fig_reg(checklist_value, plot_style_value, dropdown_regioni_value):
    #print(checklist_value)
    fig_reg = plot_regioni(df_regioni, dropdown_regioni_value, checklist_value,plot_style_value)
    return fig_reg


if __name__ == '__main__':
    app.run_server(host="0.0.0.0") #debug=True, host="0.0.0.0", port=8800)