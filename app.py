# coding=utf-8 

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from mylib import *
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import datetime as dt
import dash_table

# Input
regione ="Emilia-Romagna"
provincia = "Bologna"
# number of seconds between re-calculating the data                                                                                                                           
UPDADE_INTERVAL = 5 # 1 day
# Aggiorniamo alle 19:00
desired_update_time = 16 #hour (heroku server 2 ore indietro)
server_start_time = dt.datetime.now()
delta = desired_update_time-server_start_time.hour
if delta>0:
    period = delta*60*60
elif delta==0:
    period = 60
else:
    period = (24 + delta)*60*60
print("Nuovo Aggiornameto tra: " +  str(period/60.0)  + " minuti")

def get_data():
    global df_nazionale, df_regioni, df_province

    df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
    df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date

    df_regioni = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
    df_regioni["data"] = pd.to_datetime(df_regioni["data"]).dt.date

    df_province = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
    df_province["data"] = pd.to_datetime(df_province["data"]).dt.date  

def get_data_every(period=UPDADE_INTERVAL):
    #Updates the global variables with new data every day
    #delta = dt.datetime.now()-server_start_time

    while True:
        get_data()
        #print("data updated")
        time.sleep(period)

# get initial data                                                                                                                                                            
get_data()

lista_date = (df_province["data"].unique())
ultima_data = lista_date[-1].strftime("%A %d %b  %Y")
dict_date={}
for c in range(0,len(lista_date),3):
    # https://www.guru99.com/date-time-and-datetime-classes-in-python.html
    dict_date[c] = {"label": lista_date[c].strftime("%b %d")} 
fig_reg = plot_regioni(df_regioni, regione)
fig_naz = plot_nazionale(df_nazionale)
fig_var_naz = plot_variazione_nazionale(df_nazionale)
totale_positivi,dimessi_guariti,deceduti,nuovi_positivi,totale_casi = get_info_data(df_nazionale)
nomi_regioni_province = ["Tutte"] +  get_nomi_regioni(df_province) + get_nomi_province(df_province)
fig_line=fig_pie=fig_map=None 
fig_line,fig_pie = plot_totale_casi_provincia(df_province, regione)
fig_map = plot_map(df_province)

valore = list(df_nazionale.iloc[-1:,2:13].values[0])
incremento = list(df_nazionale.iloc[-1:,2:13].values[0] - df_nazionale.iloc[-2:,2:13].values[0])
for i in range(0,len(incremento)):
    if incremento[i]>=0:  incremento[i] = "+"+str(incremento[i])
    else: incremento[i] = str(incremento[i]) 

table_dict = {
    "tipo" :   [i.replace("_"," ") for i in list(df_nazionale.keys()[2:13])],
    "numero" : [f'{valore[i]:,}' + " (" + incremento[i] +")" for i in range(0,len(valore))],
}
table_pd = pd.DataFrame(table_dict)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
                html.Div(
                    [html.P("Covid19 Dashboard Italia"), #html.P("Autore: Manuel Rucci"), 
                    html.P(html.A("Github Project Link", href="https://github.com/visiont3lab/covid19-dash-plotly")),  
                    html.P(html.A("Dati forniti dalla Protezione Civile", href="https://github.com/pcm-dpc/COVID-19")),
                    html.P("Ultimo aggiornamento: " + ultima_data)],
                    id="info",
                    className="four columns info_container "
                ),
                html.Div([
                    html.Div([   
                        dash_table.DataTable(
                            id='table_one',
                            columns=[{"name": "", "id": "tipo"},{"name": "", "id": "numero"}], #[{"name": i.replace("_"," "), "id": i} for i in list(df_nazionale.keys()[2:7])],
                            data=table_pd.loc[0:4].to_dict("records"),
                            style_as_list_view=False,
                            style_header={"display" : "none"},
                            style_cell={
                                'textAlign': 'center',
                                'backgroundColor': 'rgb(44, 44, 44)',
                                'color': 'white',
                            },  
                            style_data_conditional=[{
                                "if": {"row_index": 0},
                                "backgroundColor": "#3E1D2A",
                            },{ "if": {"row_index": 1},
                                "backgroundColor": "#3E1D2A",
                            }]
                        ),
                        ], id='table-one-layout', className="four columns info_container "), #,style={ 'padding' : '0px 15px'}),
                    html.Div([   
                        dash_table.DataTable(
                            id='table-two',
                            columns=[{"name": "", "id": "tipo"},{"name": "", "id": "numero"}], #[{"name": i.replace("_"," "), "id": i} for i in list(df_nazionale.keys()[2:7])],
                            data=table_pd.loc[6:].to_dict("records"),
                            style_as_list_view=False,
                            style_header={"display" : "none"},
                            style_cell={
                                'textAlign': 'center',
                                'backgroundColor': 'rgb(44, 44, 44)',
                                'color': 'white',
                            },  
                            style_data_conditional=[{
                                "if": {"row_index": 2 },
                                "backgroundColor": "#3E1D2A",
                            }]
                        ),
                        ], id='table-two-layout', className="four columns info_container "),
                    ],
                ),
               
                # html.Div([
                #     html.Div(
                #         [html.H6(id="totale-positivi"), html.H6("Totale Positivi"), html.H6(totale_positivi, style={"text-align": "center"})],
                #         className="mini_container"
                #     ),
                #     html.Div(
                #         [html.H6(id="dimessi-guariti"), html.H6("Dimessi Guariti"), html.H6(dimessi_guariti, style={"text-align": "center"})],
                #         className="mini_container"
                #     ),
                #     html.Div(
                #         [html.H6(id="deceduti"), html.H6("Deceduti"),html.H6(deceduti, style={"text-align": "center"})],
                #         className="mini_container"
                #     ),
                #     html.Div(
                #         [html.H6(id="nuovi-positivi"), html.H6("Nuovi Positivi"),html.H6(nuovi_positivi , style={"text-align": "center"})],
                #         className="mini_container"
                #     ),
                #     html.Div(
                #         [html.H6(id="totale-casi"), html.H6("Totale Casi"),html.H6(totale_casi, style={"text-align": "center"})],
                #         className="mini_container"
                #     )
                # ], id="info-container", className="eight columns flex-display"),
          
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
                        options=[{'label':nome, 'value':nome} for nome in get_nomi_regioni(df_province)],
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
    fig_line, fig_pie = plot_totale_casi_provincia(df_province, lista_province,radio_buttom_value)
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
    fig_map = plot_map(df_province, lista_date[slider_value])
    return fig_map

@app.callback(dash.dependencies.Output('fig-reg', 'figure'),
    [dash.dependencies.Input('checklist', 'value'),
    dash.dependencies.Input('radio-buttom-plot-style', 'value'),
    dash.dependencies.Input('dropdown-regioni', 'value')])
def update_fig_reg(checklist_value, plot_style_value, dropdown_regioni_value):
    #print(checklist_value)
    fig_reg = plot_regioni(df_regioni, dropdown_regioni_value, checklist_value,plot_style_value)
    return fig_reg

def daily_update():
    # Daily update https://community.plotly.com/t/solved-updating-server-side-app-data-on-a-schedule/6612/2
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(get_data_every)

if __name__ == '__main__':
    daily_update()
    app.run_server(host="0.0.0.0") #,debug=True) #, host="0.0.0.0", port=8800)