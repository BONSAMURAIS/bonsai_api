[![Coverage Status](https://coveralls.io/repos/github/BONSAMURAIS/bonsai_api/badge.svg?branch=master&service=github)](https://coveralls.io/github/BONSAMURAIS/bonsai_api?branch=master&service=github) [![Build Status](https://travis-ci.org/BONSAMURAIS/bonsai_api.svg?branch=master)](https://travis-ci.org/BONSAMURAIS/bonsai_api) [![Build Status](https://ci.appveyor.com/api/projects/status/github/BONSAMURAIS/bonsai_api)]

# Bonsai API
## Documentation
See [API specifications](https://api.bonsai.uno/v1/ui/) and [documentation](https://bonsamurais.github.io/bonsai_api/build/html/index.html).

## What is it?
This is a Flask API using Flask-RESTful that serves requests on the BONSAI graph database and LCA results.

The idea is to give users easy-to-use endpoints to quickly query data from the BONSAI database but also seamlessly integrate LCA calculaiton routines in their own applications.

For example, using a Python interpreter:

    import requests
    r = requests.post('http://api.bonsai.uno/v1/do_lca/',
        json={"functional unit": [("http://rdf.bonsai.uno/someUri1",1.0,"kilogram"), ("http://rdf.bonsai.uno/someUri2",1.0,"kilogram")],
        "method":"CML 2001", "algorithm":"attributional"})
    r.json()
    
would output:
```json
    [
      {
        "label":"Manufacture of cement, lime and plaster",
        "uri":"http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_CMNT",
        "activityType":"",
        "algorithm": "attributional",
        "impacts":	{
                "amount":650.8,
                "impact_name":	"GWP100a",
                "unit":	"kg CO2-eq."
            }
        }
    ]
```
    

We foresee **bonsai_api** to work together with:
* **bonsai_web_app**, a server-based LCA calculation module that receives requests from bonsai_api,
* **bonsai_web_interface**, a graphical user interface to make and visualize LCA calculations
* **the BONSAI database**


![alt text](https://github.com/BONSAMURAIS/bonsai_api/blob/master/bonsai_app_flow_diagram.png)


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

### Docker

The docker image uses [gunicorn](https://gunicorn.org/) to serve the application.

Build the image with:

    docker build . -t bonsai_api

The minimal command line to run the image would look like:

    docker run -p 5000:5000 bonsai_api


Running on another port (say, 8080) on the host, and displaying DEBUG logs from gunicorn:

    docker run -e GUNICORN_CMD_ARGS="--log-level DEBUG" -p 8080:5000 bonsai_api


Running the application as a docker container and naming the container `bonsai_api`:

    docker run -d --name bonsai_api -e GUNICORN_CMD_ARGS="--log-level DEBUG" -p 8080:5000 bonsai_api

To see the output logs from this conatiner:

    docker logs bonsai_api

To _follow_ the logs from the container (must do `CTL-C` to stop the logs from showing in the terminal, *but* the service will continue to run!)

    docker logs -f bonsai_api

To stop the background service:
    
    docker stop bonsai_api

### Linux/MacOS

Set the environment variables

    export FLASK_APP=bonsai_api
    export FLASK_ENV=development

Run local server
    
    flask run

### Windows cmd

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
