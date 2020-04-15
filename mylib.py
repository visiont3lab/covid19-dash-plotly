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
  return list(df["denominazione_regione"].unique())

def get_nomi_province(df,regione):
    temp = df[df["denominazione_regione"]==regione]
    #ultima_data = list(a.tail(1)["data"])[0]
    ultima_data = temp.tail(1)["data"].values[0]
    nomi_province = list(temp[temp["data"]==ultima_data]["denominazione_provincia"])
    nomi_province.remove('In fase di definizione/aggiornamento')
    return nomi_province

def get_andamento_province(df,regione):
    nomi_province = get_nomi_province(df, regione)
    my_dict={}
    my_dict["data"] = df["data"].unique()
    for nome in nomi_province:
        my_dict[nome] = list(df[df["denominazione_provincia"]==nome]["totale_casi"])
    df_filt = pd.DataFrame(my_dict)
    fig = px.line(df_filt)
  

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
regione ="Emilia-Romagna"
provincia = "Bologna"

nomi_province = get_nomi_province(df, regione)
my_dict={}
my_dict["data"] = df["data"].unique()
for nome in nomi_province:
    my_dict[nome] = list(df[df["denominazione_provincia"]==nome]["totale_casi"])
df_filt = pd.DataFrame(my_dict)