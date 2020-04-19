# coding=utf-8 

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

def plot_totale_casi_provincia(df, lista_input, radio_buttom_value="Mostra Solo Primi 10"):
    # lista_input è una lista che può conteneure sia nomi di regioni che di province
    # plot_number numero di grafici da plottare All o 10

    lista = []
    if isinstance(lista_input, list)==False:
        lista.append(lista_input)
    else:
        lista = lista_input   

    nomi_regioni = get_nomi_regioni(df)
    #nomi_province = get_nomi_province(df) # nomi di tutte le province

    lista_province_to_plot = []
    for nome in lista:
        if (nome!="Tutte"):
            if (nome not in lista_province_to_plot):
                if (nome in nomi_regioni):
                    # Il nome è di una regione
                    nomi_province = get_nomi_province(df, regione=nome)
                    lista_province_to_plot.extend(nomi_province)
                else: #if (nome in nomi_province):    
                    lista_province_to_plot.append(nome)
        else:
            lista_province_to_plot = get_nomi_province(df)
    
    my_dict={}
    order = []
    my_dict["data"] = df["data"].unique()
    for nome in lista_province_to_plot:
        my_dict[nome] = list(df[df["denominazione_provincia"]==nome]["totale_casi"])
        order.append(df[df["denominazione_provincia"]==nome]["totale_casi"].max())

    # Ottieni la lista delle province ordinata (dal minore dei casi  in su) per la lengenda
    lista_ordinata_province_to_plot = []
    idxs = np.argsort(np.array(order))
    list_totale_casi_province_max = np.sort(np.array(order))
    for idx  in idxs:
        lista_ordinata_province_to_plot.append(lista_province_to_plot[idx])
    # Inverti l'ordine vogliamo dal peggiore de casi al meno peggio
    lista_ordinata_province_to_plot = lista_ordinata_province_to_plot[::-1 ]
    list_totale_casi_province_max = list_totale_casi_province_max[::-1]
    temp_df = pd.DataFrame(my_dict)

    # Prendi solo primi 10
    select = 10
    if radio_buttom_value!="Mostra Tutti":
        if (len(lista_ordinata_province_to_plot)>select):
            lista_ordinata_province_to_plot = lista_ordinata_province_to_plot[0:select]
            list_totale_casi_province_max = list_totale_casi_province_max[0:select]


    fig_line = go.Figure()
    for nome in lista_ordinata_province_to_plot:
        # Plot l'andamento del totale dei casi in una provincia
        xx = temp_df["data"].values.tolist()
        yy = temp_df[nome].values.tolist()
   
        fig_line.add_trace(go.Scatter(
                x = xx,
                y = yy,
                name=nome,
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
        
    fig_line.update_layout(
        #title=dict(
        #    text ="Totale Casi Province" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
       # ),
        legend=dict(
            orientation="v",
            #y = 1.1,
            #x = 0,
        ),
        xaxis = dict(
            title="data",
            gridcolor="cyan",
            #gridwidth=5,
            #color="red"
            #linecolor="red",
            zeroline=False,
            #fixedrange=True,  # Zoom option disabled
        ),
        yaxis = dict(
            title="totale casi",
            gridcolor="cyan",
            #gridwidth=5,
            #linecolor = "red",
            zeroline=False,
            #zerolinecolor="cyan",
            fixedrange=True,         
        ),
        dragmode="pan", #Type: enumerated , one of ( "zoom" | "pan" | "select" | "lasso" | "orbit" | "turntable" | False
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        hovermode='x',  #['x', 'y', 'closest', False]
        plot_bgcolor = "rgb(44,44,44)",
        paper_bgcolor="rgb(33, 33, 33)",
        margin={"t": 50},
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )

    fig_pie = go.Figure()
    
    fig_pie.add_trace(go.Pie(
                labels= lista_ordinata_province_to_plot,
                values= list_totale_casi_province_max,
                textposition='outside',
                textinfo='percent+label', #value
                #direction='clockwise',
                #hoverinfo='label+percent', 
                showlegend=False,
                #hole=.2,
                #textfont=dict(
                #    color="orange",
                #    size=20
                #),
            )
        )
    
    fig_pie.update_layout(
        #title=dict(
        #    text ="Totale Casi %" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        paper_bgcolor="rgb(33, 33, 33)",
        #margin={"t":200, "b": 200}
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )

    #print("Dictionary Representation of A Graph Object:\n" + str(fig.to_dict()))
    #print("\n\nJSON Representation of A Graph Object:\n" + str(fig.to_json()))
    return fig_line, fig_pie

def plot_regioni(df,lista_regioni_to_plot,lista_keys_to_plot=None, plot_style=None ):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    if plot_style=="area_plot":
        plot_style_string = "tozeroy"
    else: 
        plot_style_string = "none"

    lista = []
    if isinstance(lista_regioni_to_plot, list)==False:
        lista.append(lista_regioni_to_plot)
    else:
        lista = lista_regioni_to_plot   

    if lista_keys_to_plot==None:
        lista_keys_to_plot = ['deceduti', 'variazione_totale_positivi','terapia_intensiva'] # list(df.keys()[6:-2]) 
 
    fig_reg = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    for nome_regione in lista:
        for nome_key_to_plot in lista_keys_to_plot:
            my_dict[nome_key_to_plot] = list(df[df["denominazione_regione"]==nome_regione][nome_key_to_plot])

            xx = my_dict["data"]
            yy = my_dict[nome_key_to_plot]
    
            fig_reg.add_trace(go.Scatter(
                    x = xx,
                    y = yy,
                    #legendgroup=nome_regione,
                    name=nome_regione + " (" +nome_key_to_plot + ")",
                    mode="lines", #+markers",
                    showlegend=True,
                    #marker=dict(
                    #    symbol="circle-dot",
                    #    size=6,
                    #),
                    hoverlabel=dict(namelength=-1),
                    fill=plot_style_string, # tonexty
                    line=dict(
                        width=2,
                        #color="rgb(0,255,0)",
                        #dash="longdashdot"
                    )
                ),
            )
        
    fig_reg.update_layout(
        #title=dict(
        #    text ="Analisi Regionale" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        legend=dict(
            orientation="v",
            #traceorder="grouped",
            #y = 1.1,
            #x = 0,
        ),
        xaxis = dict(
            title="data",
            gridcolor="cyan",
            #gridwidth=5,
            #color="red"
            #linecolor="red",
            zeroline=False,
        ),
        yaxis = dict(
            title="numero",
            gridcolor="cyan",
            #gridwidth=5,
            #linecolor = "red",
            zeroline=False,
            #zerolinecolor="cyan",
            fixedrange=True,
        ),
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        dragmode="pan", #Type: enumerated , one of ( "zoom" | "pan" | "select" | "lasso" | "orbit" | "turntable" | False
        hovermode='x',  #['x unified', 'y', 'closest', False]
        plot_bgcolor = "rgb(44,44,44)",
        paper_bgcolor="rgb(33, 33, 33)",
        margin={"t":50, "b": 10},
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )
    return fig_reg

def plot_nazionale(df):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    fig = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    lista_keys_to_plot = list(df.keys()[2:-2])
    not_visible = ["variazione_totale_positivi","tamponi", "nuovi_positivi"]

    for nome_key_to_plot in lista_keys_to_plot:
        my_dict[nome_key_to_plot] = list(df[nome_key_to_plot])

        visible_str=True
        if (nome_key_to_plot in not_visible):
            visible_str="legendonly"

        xx = my_dict["data"]
        yy = my_dict[nome_key_to_plot]

        fig.add_trace(go.Scatter(
                x = xx,
                y = yy,
                #legendgroup=nome_regione,
                name=nome_key_to_plot,
                mode="lines+markers",
                showlegend=True,
                visible=visible_str,
                marker=dict(
                    symbol="circle",
                    size=4,
                ),
                hoverlabel=dict(namelength=-1),
                #fill="tozeroy", # tonexty
                line=dict(
                    width=1,
                    #color="rgb(0,255,0)",
                    #dash="longdashdot"
                )
            ),
        )
        
    fig.update_layout(
        #title=dict(
        #    text ="Analisi Regionale" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        legend=dict(
            orientation="v",
            #y = 1.1,
            #x = 0,
        ),
        xaxis = dict(
            title="data",
            gridcolor="cyan",
            #gridwidth=5,
            #color="red"
            #linecolor="red",
            zeroline=False,
        ),
        yaxis = dict(
            title="numero",
            gridcolor="cyan",
            #gridwidth=5,
            #linecolor = "red",
            zeroline=False,
            #zerolinecolor="cyan",
            fixedrange=True,
        ),
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        dragmode="pan", #Type: enumerated , one of ( "zoom" | "pan" | "select" | "lasso" | "orbit" | "turntable" | False
        hovermode='x',  #['x unified', 'y', 'closest', False]
        plot_bgcolor = "rgb(44,44,44)",
        paper_bgcolor="rgb(33, 33, 33)",
        margin={"t":50, "b": 10}
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )
    return fig

def plot_variazione_nazionale(df):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    fig = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    lista_keys_to_plot = ["variazione_totale_positivi", "nuovi_positivi"]

    for nome_key_to_plot in lista_keys_to_plot:
        my_dict[nome_key_to_plot] = list(df[nome_key_to_plot])

        xx = my_dict["data"]
        yy = my_dict[nome_key_to_plot]

        fig.add_trace(go.Scatter(
                x = xx,
                y = yy,
                #legendgroup=nome_regione,
                name=nome_key_to_plot,
                mode="lines+markers",
                showlegend=True,
                marker=dict(
                    symbol="circle",
                    size=6,
                ),
                hoverlabel=dict(namelength=-1),
                fill="tozeroy", # tonexty
                line=dict(
                    width=1,
                    #color="rgb(0,255,0)",
                    #dash="longdashdot"
                )
            ),
        )
        
    fig.update_layout(
        #title=dict(
        #    text ="Analisi Regionale" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        legend=dict(
            orientation="h",
            y = 1.1,
            x = 0,
        ),
        xaxis = dict(
            title="data",
            gridcolor="cyan",
            #gridwidth=5,
            #color="red"
            #linecolor="red",
            zeroline=False,
        ),
        yaxis = dict(
            title="numero",
            gridcolor="cyan",
            #gridwidth=5,
            #linecolor = "red",
            zeroline=False,
            #zerolinecolor="cyan",
            fixedrange=True,
        ),
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        dragmode="pan", #Type: enumerated , one of ( "zoom" | "pan" | "select" | "lasso" | "orbit" | "turntable" | False
        hovermode='x',  #['x unified', 'y', 'closest', False]
        plot_bgcolor = "rgb(44,44,44)",
        paper_bgcolor="rgb(33, 33, 33)",
        margin={"t":50, "b": 10}
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )
    return fig

def plot_map(df,data=None):
    # https://plotly.com/~EndlessRain/62.py
    # https://plotly.com/python/scattermapbox/
    # Cloropeth
    #token = "pk.eyJ1IjoibWFudWVscnVjY2kiLCJhIjoiY2s5MDR4aXRzMDI0ZjNnbWxtbDhnYXFiaCJ9._Rqe5z-nLG3QhOh9P4ZqLw"
    if data==None:
        ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    else:
        ultima_data_aggiornamento = data
    num_max = df["totale_casi"].max()
    temp_df = df[(df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!="In fase di definizione/aggiornamento")]
    temp_df.sort_values(by="totale_casi",ascending=True, inplace=True)
    
    nomi_province = temp_df["denominazione_provincia"] #[-40:]
 
    fig = go.Figure()
    #scale = temp_df["totale_casi"].max()
    count = 1
    for nome in nomi_province:
        row = temp_df[temp_df["denominazione_provincia"]==nome]
        num_casi = row["totale_casi"].values[0]
        size=5
        if (num_casi*30)/num_max > 5: 
            size=(num_casi*50)/num_max +size

        fig.add_trace(go.Scattermapbox(
            lon = row['long'],
            lat = row['lat'],
            text = row["totale_casi"],
            name = str((len(nomi_province)+1 - count)) + ". " +  nome + " " + str(num_casi),
            hoverinfo='text',
            hovertext= str((len(nomi_province)+1 - count)) + ". " +  nome + ": " + str(num_casi),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size= size,  # 20:num_max = x : val
                color="rgb(255,0,0)",
                opacity=0.8,
                ),
            )
        )
        count +=1
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            #accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=41,  # ROme
                lon=12
            ),
            pitch=0,
            zoom=4,
            style="carto-darkmatter",
        ),
        legend_font_color = "white",
        legend_traceorder = "reversed",
        paper_bgcolor="rgb(33, 33, 33)",
        transition_duration=0,
        margin={"r":10,"t":30,"l":20,"b":30}
    )
    return fig

def get_nomi_regioni(df):
    nomi_regioni = list(df["denominazione_regione"].unique())
    nomi_regioni.sort()
    return nomi_regioni

def get_nomi_province(df, regione=None):
    
    # Nomi delle prime num provincie per numero di casi 
    ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    # Dataframe regione scelta e ultima data aggiornamento
    el = 'In fase di definizione/aggiornamento'
    if regione==None:
        temp = df[(df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!=el)] 
    else:
        temp = df[(df["denominazione_regione"]==regione) & (df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!=el)]
    # Ordina dal più grande al più piccolo
    temp.sort_values(by="totale_casi",ascending=False, inplace=True)
    nomi_province = list(temp["denominazione_provincia"]) #[0:num])

    # Nomi pronvicie 
    #nomi_province = list(df["denominazione_provincia"].unique())
    return nomi_province

def get_data_provincia(df, provincia="Bologna", regione="Emilia-Romagna"):
    # Estrai i dati relativi alla regione=regione e provincia=pronvincia
    df_choice = df[ (df["denominazione_regione"]==regione) & (df["denominazione_provincia"]==provincia)]
    df_fin = df_choice[["data", "denominazione_regione","denominazione_provincia","lat","long","totale_casi"]]
    return df_fin

def get_info_data(df):
    # Usiamo dataset andamento nazionale
    totale_positivi  = df.tail(1)["totale_positivi"].values[0]
    dimessi_guariti  = df.tail(1)["dimessi_guariti"].values[0]
    deceduti  = df.tail(1)["deceduti"].values[0]
    nuovi_positivi  = df.tail(1)["nuovi_positivi"].values[0]
    totale_casi  = df.tail(1)["totale_casi"].values[0]
    return totale_positivi,dimessi_guariti,deceduti,nuovi_positivi,totale_casi
    

'''
def get_nomi_province(df, regione="Emilia-Romagna"):
    # Nomi pronvince data una regione
    nomi_province  = list(df[df["denominazione_regione"]==regione]["denominazione_provincia"].unique())
    el = 'In fase di definizione/aggiornamento'
    if el in nomi_province:
        nomi_province.remove(el)

    # Nomi pronvicie 
    #nomi_province = list(df["denominazione_provincia"].unique())
    nomi_province.sort()
    return nomi_province

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
'''

def plot_maphgf(df,data=None, fig=None):
    # https://plotly.com/~EndlessRain/62.py
    # https://plotly.com/python/scattermapbox/
    # Cloropeth
    #token = "pk.eyJ1IjoibWFudWVscnVjY2kiLCJhIjoiY2s5MDR4aXRzMDI0ZjNnbWxtbDhnYXFiaCJ9._Rqe5z-nLG3QhOh9P4ZqLw"
    if data==None:
        ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    else:
        ultima_data_aggiornamento = data
    num_max = df["totale_casi"].max()
    temp_df = df[(df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!="In fase di definizione/aggiornamento")]
    temp_df.sort_values(by="totale_casi",ascending=True, inplace=True)
    
    nomi_province = temp_df["denominazione_provincia"] #[-20:]
    
    if fig==None:
        fig = go.Figure()
        #scale = temp_df["totale_casi"].max()
        count = 1
        for nome in nomi_province:
            row = temp_df[temp_df["denominazione_provincia"]==nome]
            num_casi = row["totale_casi"].values[0]
            size=5
            if (num_casi*30)/num_max > 1: 
                size=(num_casi*30)/num_max 

            fig.add_traces(go.Scattermapbox(
                lon = row['long'],
                lat = row['lat'],
                text = row["totale_casi"],
                name = str((len(nomi_province)+1 - count)) + ". " +  nome + " " + str(num_casi),
                hoverinfo='text',
                hovertext= str((len(nomi_province)+1 - count)) + ". " +  nome + ": " + str(num_casi),
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size= size,  # 20:num_max = x : val
                    color="rgb(255,0,0)"
                    ),
                )
            )
            count +=1

        fig.update_layout(
            hovermode='closest',
            mapbox=dict(
                #accesstoken=token,
                bearing=1,
                center=go.layout.mapbox.Center(
                    lat=41,  # ROme
                    lon=12
                ),
                pitch=0,
                zoom=3,
                style="carto-darkmatter",
            ),
            legend_font_color = "white",
            legend_traceorder = "reversed",
            paper_bgcolor="rgb(33, 33, 33)",
            #margin={"r":0,"t":0,"l":0,"b":0}
        )
    else:
        #scale = temp_df["totale_casi"].max()
        count = 1
        for nome in nomi_province:
            row = temp_df[temp_df["denominazione_provincia"]==nome]
            num_casi = row["totale_casi"].values[0]
            size=5
            if (num_casi*30)/num_max > 1: 
                size=(num_casi*30)/num_max 

            fig.add_traces(go.Scattermapbox(
                lon = row['long'],
                lat = row['lat'],
                text = row["totale_casi"],
                name = str((len(nomi_province)+1 - count)) + ". " +  nome + " " + str(num_casi),
                hoverinfo='text',
                hovertext= str((len(nomi_province)+1 - count)) + ". " +  nome + ": " + str(num_casi),
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size= size,  # 20:num_max = x : val
                    color="rgb(255,0,0)"
                    ),
                )
            )
            count +=1

    return fig

def plot_mapp(df):
    # settings https://docs.mapbox.com/mapbox-gl-js/style-spec/root/
    token = "pk.eyJ1IjoibWFudWVscnVjY2kiLCJhIjoiY2s5MDR4aXRzMDI0ZjNnbWxtbDhnYXFiaCJ9._Rqe5z-nLG3QhOh9P4ZqLw"
   
    ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    temp_df = df[(df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!="In fase di definizione/aggiornamento")]
    center = temp_df[temp_df["denominazione_provincia"]=="Roma"][["lat","long"]].values[0]
    print(center)
    fig = px.scatter_mapbox(temp_df, lat="lat", lon="long", hover_name="denominazione_provincia", hover_data=["totale_casi"],
                        color_discrete_sequence=["fuchsia"],
                        #center={"lat": 45.5517, "lon": -73.7073},
                        mapbox_style="carto-positron",  #"dark",  # mapbox_style="carto-darkmatter",
                        #mapbox_accesstoken=token,
                        center = {"lat": center[0], "lon": center[1]},
                        zoom=4.5) #, height=300)
 
    #"open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" or "stamen-watercolor"
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


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