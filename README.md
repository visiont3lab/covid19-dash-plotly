# covid19-dash-plotly

Dashboard using Dash Plotly Library

    * [Website](https://covid19-dash-plotly.herokuapp.com/)
    * https://covid19-dash-plotly.herokuapp.com/

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
    ```

    Useful output:
    Creating ⬢ covid19-dash-plotly... done  
    https://covid19-dash-plotly.herokuapp.com/ | https://git.heroku.com covid19-dash-plotly.git

* Heroku Update

    ```
    cd covid19-dash-plotly
    git add .  # add all the changes
    git commit -m 'a description of the changes'
    git push heroku master
    ```




## References

* [dash deploy](https://dash.plotly.com/deployment)
* [dash-heroku-template](https://github.com/plotly/dash-heroku-template)
* [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
* [heroku cli Logs](https://devcenter.heroku.com/articles/logging#view-logs)