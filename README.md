[![Coverage Status](https://coveralls.io/repos/github/BONSAMURAIS/bonsai_api/badge.svg?branch=master)](https://coveralls.io/github/BONSAMURAIS/bonsai_api?branch=master) [![Build Status](https://travis-ci.org/BONSAMURAIS/bonsai_api.svg?branch=master)](https://travis-ci.org/BONSAMURAIS/bonsai_api)

https://ci.appveyor.com/api/projects/status/github/BONSAMURAIS/bonsai_api
# Bonsai API
## Documentation
See [documentation](https://bonsamurais.github.io/bonsai_api/build/html/index.html).

## What is it?
This is a Flask API using Flask-RESTful that serves requests on the BONSAI graph database and LCA results.

The idea is to give users easy-to-use endpoints to quickly query data from the BONSAI database but also seamlessly integrate LCA calculaiton routines in their own applications.

For example, using a Python interpreter:

    import requests
    r = requests.post('http://api.bonsai.uno/do_lca/',
        json={"functional unit": [("http://rdf.bonsai.uno/someUri1",1.0,"kilogram"), ("http://rdf.bonsai.uno/someUri2",1.0,"kilogram")],
        "method":"CML 2001", "algorithm":"attributional"})
    r.json()
    
would output:
```json
    [
      {"uri": "http://rdf.bonsai.uno/someUri1", "label": "Electricity production, coal"}: {
        "Global Warming Potential 100a": [
            {"impact": 0.102, "unit": "kg CO2-eq."}
        ],
        "Acidification": [
            {"impact": 1.2e-5, "unit": "kg SO2-eq."}
        ]
      },
      {"uri": "http://rdf.bonsai.uno/someUri2", "label": "Electricity production, nuclear"}: {
        "Global Warming Potential 100a": [
            {"impact": 0.02, "unit": "kg CO2-eq."}
        ],
        "Acidification": [
            {"impact": 1.2e-2, "unit": "kg SO2-eq."}
        ]
      }
    ]
```
    

We foresee **bonsai_api** to work together with:
* **bonsai_web_app**, a server-based LCA calculation module that receives requests from bonsai_api,
* **bonsai_web_interface**, a graphical user interface to make and visualize LCA calculations
* **the BONSAI database**


![alt text](https://github.com/BONSAMURAIS/bonsai_api/blob/master/docs/bonsai_app_flow_diagram.png)


## Install
Clone the repository

    git clone https://github.com/BONSAMURAIS/bonsai_api

Create a virtual environment and activate it

    python3 -m venv venv
    . venv/bin/activate

Or on Windows cmd

    py -3 -m venv venv
    venv\Scripts\activate.bat

## Install bonsai_api

    pip install -e .

Or if you are using the master branch, install Flask from source before installing bonsai_web_api

    pip install -e ../..
    pip install -e .

## Run
Linux/MacOS

Set the environment variables

    export FLASK_APP=bonsai_api
    export FLASK_ENV=development

Run local server
    
    flask run

Or on Windows cmd

    set FLASK_APP=bonsai_api
    set FLASK_ENV=development
    flask run

Open http://127.0.0.1:5000 in a browser.

## Test
    pip install '.[test]'
    pytest -v

## Run with coverage report

    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
