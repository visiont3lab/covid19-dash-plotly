# coding=utf-8 

'''
Interactive User Interface -Data Visualization 
GUIs with Dash and Python p.3
https://pythonprogramming.net/data-visualization-application-dash-python-tutorial-introduction/

Pandas based

'''

'''
Dictionary
data
data.keys()
data.values
data.values()[0] row 0 as array
data.iloc[0]
data.iloc[0]["Date"]
list(data.values()[0]) row 0 as list
np.asarray(list(data.values[0]))
for key in data.keys():
    display(data[key]) 
list(data.keys())
Vogliamo creare un nuovo dataframe con solo i dati italiani
Multiple conditions
data[data['CountryCode'] == 'IT']
Missing data
data.iloc[0].isnull()
for i in range(len(data.index)) :
    print("Nan in row ", i , " : " ,  data.iloc[i].isnull().sum())
Selezioniamo L'italia
itdata = data[data["CountryCode]=='IT'] # selezionare l'italia
itdata = itdata.reset_index()  # resettare gli indici
Selezioniamo italia e spagna
# or | and &
dataitsp = data[
    (data["CountryName"]=='Spain') |
    (data["CountryName"]=='Italy')
]
display(dataitsp)

# Selezioniamo Italia
# Ordiniamo i dati in base alla latitudine
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
datait = data[data["CountryCode"]=='IT']
datait = datait.reset_index()
datait = datait.sort_values(by='Latitude', ascending=False)
Per ogni data il numero di morti

Noi vogliamo sapere:
Numero di morti per regione nel tempo
datait[datait["RegionCode"]=='BZ']["Deaths"].sum()
dammi tutti i region name se compaino piu volte dammi uno solo e tolgi il Nan

arr_region_names = d["RegionName"].dropna().unique()
df = pd.DataFrame(columns=['RegionName', 'TotalDeaths'])
i=0
for name in arr_region_names:
    temp_val = datait[datait["RegionName"]==name]["Deaths"].sum()
    df.loc[i] = [name, temp_val]
    i+=1
df = df.sort_values(by="TotalDeaths", ascending=False)

Aggiungiamo confermati popolazione etch
arr_region_names = d["RegionName"].dropna().unique()
df = pd.DataFrame(columns=['RegionName', 'TotalDeaths', "TotalConfirmed", "Population"])
i=0
for name in arr_region_names:
    temp_deaths = datait[datait["RegionName"]==name]["Deaths"].sum()
    temp_confirmed = datait[datait["RegionName"]==name]["Confirmed"].sum()
    temp_polulation = datait[datait["RegionName"]==name]["Population"].unique()[0]
    df.loc[i] = [name, temp_deaths, temp_confirmed,temp_polulation]
    i+=1
df = df.sort_values(by="TotalDeaths", ascending=False)
display(df)

# Aggiungiamo percentuale confermati e morti
datait = data[data["CountryCode"]=="IT"] # seleziona italia
update_date = datait["Date"].max()
arr_region_names = datait["RegionName"].dropna().unique()
df = pd.DataFrame(columns=['Date','RegionName', 'TotalDeaths', "TotalConfirmed", "Population", "%Deaths", "%Confirmed"])
i=0
for name in arr_region_names:
    temp_deaths = datait[datait["RegionName"]==name]["Deaths"].iloc[-1]
    temp_confirmed = datait[datait["RegionName"]==name]["Confirmed"].iloc[-1]
    temp_polulation = datait[datait["RegionName"]==name]["Population"].unique()[0]
    temp_perc_deaths = np.round((temp_deaths/temp_polulation)*100,2)
    temp_perc_confirmed = np.round((temp_confirmed/temp_polulation)*100,2)
    df.loc[i] = [update_date, name, temp_deaths, temp_confirmed,temp_polulation,temp_perc_deaths,temp_perc_confirmed]
    i+=1
df = df.sort_values(by="TotalDeaths", ascending=False)
#df = df.reset_index()
display(df)

# Aggiornamneto ad oggi 
td = df["TotalDeaths"].sum()
tc = df["TotalConfirmed"].sum()
perc =  np.round((df["TotalConfirmed"].sum()/df["Population"].sum())*100,2)
tp = df["Population"].sum()
df_resume_it = pd.DataFrame(data=[[update_date, tc, td, tp, perc]], columns=['Italia Date', 'Morti ', 'Contagiati' , 'Popolazione', '% Polazione Infetta'])
display(df_resume_it)

Per ogni region (emilia romagna) vedere l'andamento nel tempo morti e confermati

# Pandas tips
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
df.at[4,"RegionName"]
df.at[4,"RegionName"] = 10
df.loc[4].at["RegionName"]
df.shape
df.loc[0:5, ['RegionName', 'TotalDeaths']]
df.iloc[8:10, 5:8]

https://colab.research.google.com/github/open-covid-19/data/blob/master/examples/logistic_modeling.ipynb#scrollTo=bfkyXFuH2I-Z
https://colab.research.google.com/github/open-covid-19/data/blob/master/examples/exponential_modeling.ipynb
https://colab.research.google.com/github/open-covid-19/data/blob/master/examples/data_loading.ipynb
https://colab.research.google.com/github/open-covid-19/data/blob/master/examples/category_estimation.ipynb

# Andamento in italia
for date in dates:
    table = datait[datait["Date"]==date]
    display(table)

# Table andamento italia
sum_conf = 0
data_andamento_italia = pd.DataFrame(columns=['Data', 'Morti ', 'Contagiati'])
c = 0
for date in dates:
    table = datait[datait["Date"]==date]
    sum_conf = table["Confirmed"].sum() # sum all regions
    sum_deaths = table["Deaths"].sum() # sum all regions
    data_andamento_italia.loc[c] = [date, sum_deaths, sum_conf]
    c+=1
display(data_andamento_italia)

'''
# https://github.com/pcm-dpc/COVID-19
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_auth
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def dati_andamento_italia():
    '''
    Data	Morti	Contagiati
    0	2020-01-01	0.0	0.0
    1	2020-01-02	0.0	0.0
    2	2020-01-03	0.0	0.0
    3	2020-01-04	0.0	0.0
    4	2020-01-05	0.0	0.0
    ...	...	...	...
    85	2020-03-26	15668.0	154925.0
    86	2020-03-27	17299.0	167037.0
    87	2020-03-28	19157.0	178970.0
    88	2020-03-29	20802.0	190161.0
    89	2020-03-30	10779.0	97689.0
    '''

    # Get data overall world
    data_total = pd.read_csv('https://open-covid-19.github.io/data/data.csv')
    
    # Extract data italy
    data_italy = data_total[data_total["CountryCode"]=="IT"] # seleziona italia

    # Get dates
    dates = data_italy["Date"].unique()
    sum_conf = 0
    data_andamento_italy = pd.DataFrame(columns=['Data', 'Morti', 'Contagiati'])
    c = 0
    for date in dates:
        table = data_italy[data_italy["Date"]==date]
        sum_conf = table["Confirmed"].sum() # sum all regions
        sum_deaths = table["Deaths"].sum() # sum all regions
        if (sum_conf!=0 or sum_deaths!=0):
            data_andamento_italy.loc[c] = [date, sum_deaths, sum_conf]
            c+=1
    return data_andamento_italy

def dati_morti_contagiati_per_regione_italia():
    '''
        index	Date	RegionName	TotalDeaths	TotalConfirmed	Population	%Deaths	%Confirmed
    0	2	2020-03-31	Lombardy	6818.0	42161.0	10078012.0	0.07	0.42
    1	6	2020-03-31	Emilia-Romagna	1538.0	13531.0	4446220.0	0.03	0.30
    2	0	2020-03-31	Piemont	749.0	8712.0	4377941.0	0.02	0.20
    3	9	2020-03-31	Marche	417.0	3684.0	1541692.0	0.03	0.24
    4	3	2020-03-31	Veneto	413.0	8724.0	4865380.0	0.01	0.18
    5	5	2020-03-31	Liguria	397.0	3217.0	1557533.0	0.03	0.21
    6	7	2020-03-31	Tuscany	231.0	4412.0	3742437.0	0.01	0.12
    7	10	2020-03-31	Lazio	150.0	2914.0	5897635.0	0.00	0.05
    8	20	2020-03-31	Trentino-Alto Adige	147.0	1682.0	1070340.0	0.01	0.16
    9	13	2020-03-31	Campania	125.0	1952.0	5869029.0	0.00	0.03
    10	4	2020-03-31	Friuli Venezia Giulia	107.0	1501.0	1216524.0	0.01	0.12
    11	11	2020-03-31	Abruzzo	102.0	1345.0	1307919.0	0.01	0.10
    12	14	2020-03-31	Apulia	91.0	1712.0	4063888.0	0.00	0.04
    13	17	2020-03-31	Sicily	76.0	1555.0	5029615.0	0.00	0.03
    14	19	2020-03-31	South Tyrol	74.0	1325.0	530009.0	0.01	0.25
    15	1	2020-03-31	Aosta Valley	50.0	584.0	126933.0	0.04	0.46
    16	8	2020-03-31	Umbria	33.0	1051.0	889001.0	0.00	0.12
    17	16	2020-03-31	Calabria	31.0	647.0	1980533.0	0.00	0.03
    18	18	2020-03-31	Sardinia	28.0	682.0	1651793.0	0.00	0.04
    19	12	2020-03-31	Molise	9.0	134.0	308493.0	0.00	0.04
    20	15	2020-03-31	Basilicata	5.0	214.0	575902.0	0.00	
    '''

    data_total = pd.read_csv('https://open-covid-19.github.io/data/data.csv')

    # Aggiungiamo percentuale confermati e morti
    data_italy = data_total[data_total["CountryCode"]=="IT"] # seleziona italia
    update_date = data_italy["Date"].max()
    arr_region_names = data_italy["RegionName"].dropna().unique()
    #df = pd.DataFrame(columns=['Date','RegionName', 'TotalDeaths', "TotalConfirmed", "Population", "%Deaths", "%Confirmed"])
    df = pd.DataFrame(columns=['Data','Regione', 'Morti', "Contagiati", "Popolazione"])
    i=0
    for name in arr_region_names:
        temp_deaths = data_italy[data_italy["RegionName"]==name]["Deaths"].iloc[-1]
        temp_confirmed = data_italy[data_italy["RegionName"]==name]["Confirmed"].iloc[-1]
        temp_polulation = data_italy[data_italy["RegionName"]==name]["Population"].unique()[0]
        temp_perc_deaths = np.round((temp_deaths/temp_polulation)*100,2)
        temp_perc_confirmed = np.round((temp_confirmed/temp_polulation)*100,2)
        #df.loc[i] = [update_date, name, temp_deaths, temp_confirmed,temp_polulation,temp_perc_deaths,temp_perc_confirmed]
        df.loc[i] = [update_date,name, temp_deaths, temp_confirmed,temp_polulation]
        i+=1
    df = df.sort_values(by="Morti", ascending=False)
    df = df.reset_index()
    return df

def dati_morti_contagiati_italia():
    '''
    Italia Date	 Morti	Contagiati	Popolazione	% Polazione Infetta
    0	[2020-03-31]	101739.0	11591.0	61126829.0	0.
    '''
    
    df = dati_morti_contagiati_per_regione_italia()

    # Aggiornamneto ad oggi 
    update_date = df["Data"].unique()
    td = df["Morti"].sum()
    tc = df["Contagiati"].sum()
    perc =  np.round((df["Contagiati"].sum()/df["Popolazione"].sum())*100,2)
    tp = df["Popolazione"].sum()
    df_tot= pd.DataFrame(data=[[update_date, td, tc, tp, perc]], columns=['Data', 'Morti', 'Contagiati' , 'Popolazione', '% Polazione Infetta'])
    return df_tot

#external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets= [dbc.themes.SOLAR]

# Bootstrap Theme https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

'''
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'admin'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
'''

# data morti contagiati per regione
dmcpri = dati_morti_contagiati_per_regione_italia()
# data morti contagiati
dmci = dati_morti_contagiati_italia()
# data andamento in italia morti e contagiati
dai = dati_andamento_italia()


app.layout = html.Div(children=[
    html.H1(children='Covid 19 Analisi in Italia',className="text-center"),
    html.H2(children='Morti e Contagiati Totali'),
    html.Div([
        dbc.Row([
            # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("N. Morti"),
                        dbc.CardBody(
                            [
                                html.H2(dmci["Morti"], className="card-title text-center"),
                            ]
                        ),
                    ],color="dark", inverse=True)),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("N. Contagiati"),
                        dbc.CardBody(
                            [
                                html.H2(dmci["Contagiati"], className="card-title text-center"),
                            ]
                        ),
                    ],color="info", inverse=True))
            ]),
    ]),
    html.Div([
        dcc.Graph(
            id='grafico-andamento-italia',
            figure={
                    'data': [
                        {'x': dai["Data"], 'y': dai["Morti"], 'name': 'Morti', 'mode': "lines+markers"},
                        {'x': dai["Data"], 'y': dai["Contagiati"], 'name': 'Contagiati','mode': "lines+markers"},
                    ],
                    'layout': {
                        'title': "COVID-19 Andamento dei Morti e dei Contagiati" 
                    }
                }),
    ]),
    html.H2(children='Morti e Contagiati Per Regione'),
    html.Div([   
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in ["Data","Morti","Contagiati","Popolazione"]],
            data=dmcpri.iloc[:,1:6].to_dict('records'),
            style_as_list_view=False,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'textAlign': 'left',
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
            },  
        ),
    ], id='table-layout',style={
        'padding' : '0px 15px'
    }),
    html.Div([
        dcc.Graph(
                id='morti-contagiati',
                figure={
                    'data': [
                        {'x': dmcpri["Regione"], 'y': dmcpri["Morti"].T, 'type': 'bar', 'name': 'Morti'},
                         {'x': dmcpri["Regione"], 'y': dmcpri["Contagiati"].T, 'type': 'bar', 'name': 'Contagiati'}
                    ],
                    'layout': {
                        'title':  dmcpri["Data"].max() + ' COVID-19 Morti-Contagiati:' 
                    }
                }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)



