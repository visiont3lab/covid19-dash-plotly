# covid19-dash-plotly

Dashboard using Dash Plotly Library

* [Website](https://covid19-dash-plotly.herokuapp.com/)
* https://covid19-dash-plotly.herokuapp.com/

Data collected from:

* [Dati COVID-19 Italia](https://github.com/pcm-dpc/COVID-19)
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

## TODO

* [ ] Analyze italian data based on "Province", "Comuni" and "Città". Add the possibility to search a specific "Comune,Città,Provincia"
* [ ] Create a world interactive map showing how the virus has spread in the world (timeline)
* [ ] Develop a simulation describing how the virus spread
* [ ] Add covid19 useful information and updates  


## References

* [dash deploy](https://dash.plotly.com/deployment)
* [dash-heroku-template](https://github.com/plotly/dash-heroku-template)
* [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
* [heroku cli Logs](https://devcenter.heroku.com/articles/logging#view-logs)
