# Funzione fa il plot
# Funzione che mi calcola la tabella data, totale casi
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

def plot_totale_casi_provincia(dfs):
    # dfs is a list of dataframe

    fig = go.Figure()

    for df in dfs:
        # Plot l'andamento del totale dei casi in una provincia
        xx = df["data"].values.tolist()
        yy = df["totale_casi"].values.tolist()
        nome_provincia = list(df["denominazione_provincia"].unique())[0]
        
        fig.add_trace(go.Scatter(
                x = xx,
                y = yy,
                name=nome_provincia,
                mode="lines+markers",
                showlegend=True,
                marker=dict(
                    symbol="circle-dot",
                    size=6,
                ),
                line=dict(
                    width=1,
                    #color="rgb(0,255,0)",
                    #dash="longdashdot"
                )
            )
        )
        
    fig.update_layout(
        title=dict(
            text ="Totale Casi Province ",
            y = 0.9,
            x = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        #legend=dict(
        #    y = 0.9,
        #    x = 0.03,
        #),
        xaxis_title="data",
        yaxis_title="totale casi",
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="orange", #"#7f7f7f", 
        ),
        hovermode='x',  #['x', 'y', 'closest', False]
        plot_bgcolor = "rgb(10,10,10)",
        paper_bgcolor="rgb(0,0,0)"
    )
    return fig

def get_nomi_regioni(df):
    nomi_regioni = list(df["denominazione_regione"].unique())
    nomi_regioni.sort()
    return nomi_regioni

def get_nomi_provincie(df, regione="Emilia-Romagna"):
    # Nomi pronvince data una regione
    nomi_province  = list(df[df["denominazione_regione"]==regione]["denominazione_provincia"].unique())
    el = 'In fase di definizione/aggiornamento'
    if el in nomi_province:
        nomi_province.remove(el)

    # Nomi pronvicie 
    #nomi_province = list(df["denominazione_provincia"].unique())
    nomi_province.sort()
    return nomi_province

def get_nomi_provincie_max(df, num, regione="Emilia-Romagna"):
    # Nomi delle prime num provincie per numero di casi 
    ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    # Dataframe regione scelta e ultima data aggiornamento
    temp = df[(df["denominazione_regione"]==regione) & (df["data"]==ultima_data_aggiornamento)]
    # Ordina dal più grande al più piccolo
    temp.sort_values(by="totale_casi",ascending=False, inplace=True)
    nomi_province = list(temp["denominazione_provincia"][0:num])

    # Nomi pronvicie 
    #nomi_province = list(df["denominazione_provincia"].unique())
    return nomi_province

def get_data_provincia(df, provincia="Bologna", regione="Emilia-Romagna"):
    # Estrai i dati relativi alla regione=regione e provincia=pronvincia
    df_choice = df[ (df["denominazione_regione"]==regione) & (df["denominazione_provincia"]==provincia)]
    df_fin = df_choice[["data", "denominazione_regione","denominazione_provincia","lat","long","totale_casi"]]
    return df_fin

def es1(df,provincia,regione):
    # Plottare l'andamento nel tempo dei contagiati della propria provincia. 
    # Input proivincia e regione associata alla provincia
    df_fin = get_data_provincia(df, provincia, regione)
    #display(df_fin.tail(4))
    fig = plot_totale_casi_provincia([df_fin])
    #fig.show()
    return fig

def es2(df,regione):
    # Comparare l'andamento nel tempo dei contagiati di ogni provincia della nostra regione (Emilia-Romagna).
    
    nomi_province = get_nomi_provincie(df, regione) # Nomi di tutte le province
    nomi_province = get_nomi_provincie_max(df, 30, regione)  # Nomi delle prime 3 provincie per numero di casi 
    #print(nomi_province)

    df_fin_vec = []
    for nome_provincia in nomi_province:
        df_fin = get_data_provincia(df, nome_provincia, regione)
        df_fin_vec.append(df_fin)
    fig = plot_totale_casi_provincia(df_fin_vec)
    #fig.show()
    return fig

def es3(df,regione):
    #https://plotly.com/python/pie-charts/#pie-chart-with-plotly-express
    # https://plotly.com/python-api-reference/generated/plotly.express.pie.html
    ultima_data_aggiornamento = list(df.tail(1)["data"])[0]

    df_choice = df[(df["denominazione_regione"]==regione) & (df["denominazione_provincia"]!='In fase di definizione/aggiornamento') & (df["data"]==ultima_data_aggiornamento) ]
    #display(df_choice.tail())

    # https://plotly.com/python/builtin-colorscales/
    # template plotly https://plotly.com/python/templates/
    # https://plotly.com/python/reference/#pie
    # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    fig = px.pie(df_choice,
                values='totale_casi', 
                names='denominazione_provincia', 
                title='Totale casi Province',
                color_discrete_sequence=px.colors.sequential.Plotly3,
                hover_data=['denominazione_provincia'], labels={'denominazione_provincia':'provincia'}, 
                #template="plotly_dark",
                hole=0.3
                )       
        
    #fig.update_traces(textposition='outside', textinfo='label+percent')
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(
            color="orange",
            size=20
        ),
    ) #percent+value+label

    fig.update_layout(
            title=dict(
            text ="Totale Casi Province",
            y = 0.9,
            x = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="orange", #"#7f7f7f", 
        ),
        paper_bgcolor="rgb(0,0,0)"
    )
    #fig.show()
    return fig