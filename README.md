# covid19-dash-plotly

Dashboard using Dash Plotly Library

* [Website](https://covid19-dash-plotly.herokuapp.com/)
* https://covid19-dash-plotly.herokuapp.com/

Data collected from:

* [Dati COVID-19 Italia](https://github.com/pcm-dpc/COVID-19)
  * [Dati andamento nazionale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv)
  * [Dati andamento regionale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv)
  * [Dati andamento provinciale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv)
  
* [Covid World Data](https://github.com/open-covid-19/data)



## Setup

*   Python setup
    
    ```
    cd covid19-dash-plotly
    virtualenv env # creates a virtualenv called "env"
    source env/bin/activate # uses the virtualenv
    pip install -r requirements.txt
    ```

* Heroku Setup
    
    ```
    cd covid19-dash-plotly
    heroku login -i 
    git init
    git add .
    git commit -m "Initial app"
    heroku create covid19-dash-plotly
    heroku git:remote -a covid19-dash-plotly
    git push heroku master
    heroku ps:scale web=1  # start web dyno see Procfile
    heroku logs --tail # check logs
    heroku ps:scale web=0 # stop app
    heroku ps -a covid19-dash-plotly # remaining hours check

    ```

    Useful output:
    Creating ⬢ covid19-dash-plotly... done  
    https://covid19-dash-plotly.herokuapp.com/ | https://git.heroku.com/covid19-dash-plotly.git

* Heroku Update

    ```
    cd covid19-dash-plotly
    git add .  # add all the changes
    git commit -m 'a description of the changes'
    git push heroku master
    ```

* Link to Github
    
    Create a repository from github called "covid19-dash-plotly"
    
    ```
    git remote add origin https://github.com/visiont3lab/covid19-dash-plotly.git
    git push -u origin master
    ```
    
    Use heroku website to connect your heroku app with the created github repo. It will allow to have automatic deploy on push and code diffs.
    Enable automatic deploy

## Bugs
* [ ] Design del telefono non robusto. Quando clicco su una figura zoom automaticatemte. Bisognerebbe aggiunbgere le touch gesture.
* [ ] Dropdown hover color non visibile. Non trovo il css per cambiarlo.
* [ ] Pie plot con tanti valori causa diverse label che escono dal grafico. 


## TODO
 * [ ] Aggiungere refresh dei dati giornaliero
 * [ ] Sviluppare dockerfile per applicazione server senza heroku
 * [ ]  Aggiugnere spiegazione per ogni parametro. Premessa: non sono certo di cosa si voglia intendere con "tamponi" o "casi positivi"
 * [ ] Nel terzo grafico rendere disponibile cliccare "nuovi tamponi" (il delta fra due istanti di tempo successivi).Così da poter mettere a paragone la relazione fra nuovi positivi e nuovi tamponi
 * [ ] Comunque ho letto un articolo di recente che diceva che i dati ISTAT sarebbero più affidabili. Possibilita di confronto tra dati instat e protezione civile.
 * [ ] Analizzare la probabilità che una persona venga contagiata.
 * [ ] Analizzare i dati mondiali
 * [ ] Svilupapre una simulazione su come il virus si diffonde e le probabilità di contagio

## References

* [dash deploy](https://dash.plotly.com/deployment)
* [dash-heroku-template](https://github.com/plotly/dash-heroku-template)
* [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
* [heroku cli Logs](https://devcenter.heroku.com/articles/logging#view-logs)
