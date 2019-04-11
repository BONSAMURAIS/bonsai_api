import os
from flask import Flask, request, make_response, abort, jsonify
import connexion
from connexion.resolver import RestyResolver

from SPARQLWrapper import SPARQLWrapper, JSON
import json

app = connexion.FlaskApp(__name__)
app.add_api('openapi-Swagger20.json', resolver=RestyResolver('bonsai_api'))

#app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

DATABASE='https://db.bonsai.uno/bonsai/query'
test_config = None

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)



# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

"""Search for activities."""

@app.route('/activities/by_label/<path:parameter>', methods = ['GET'])
def getSearchActivityByLabel(parameter):
    """Returns a list of one or several activities in the BONSAI database for which the label contains the specified substring.

    .. :quickref: Search activities query; Get list of activities that match search criteria.

    **Example request**:

    .. sourcecode:: http

      GET /search_activities/by_label/cement HTTP/1.1
      Host: api.bonsai.uno
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
          {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_CMNT", "name": "Manufacture of cement, lime and plaster"}
      ]

    :resheader Content-Type: application/json
    :status 200: Activity found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """


    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?uri  ?label
                WHERE {
                    ?uri a <http://ontology.bonsai.uno/core#ActivityType>;
                    rdfs:label ?label
                    FILTER(regex(str(?label), '"""+str(parameter)+"""' ) )
                    }
        """

    sparql = SPARQLWrapper("https://db.bonsai.uno/bonsai/query")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()

    activities = [{
        'uri': activity["uri"]["value"],
        'label':activity["label"]["value"]
    } for activity in response["results"]["bindings"]]

    if len(activities)>0:
        resp = make_response(json.dumps(activities), 200)
        resp.headers.extend({})

        return resp
    else:
        abort(make_response(jsonify(message="The specified substring is not contained in any label."), 404))


@app.route('/activities/by_uri/<path:parameter>', methods = ['GET'])
def getSearchActivityByUri(parameter):
    """Returns a list of one or several activities in the BONSAI database for which the URI contains the specified substring.

    .. :quickref: Search activities query; Get list of activities that match search criteria.

    **Example request**:

    .. sourcecode:: http

      GET /activities/by_uri/CEM HTTP/1.1
      Host: api.bonsai.uno
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
          {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_CMNT", "name": "Manufacture of cement, lime and plaster"}
      ]

    :resheader Content-Type: application/json
    :status 200: Activity found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """


    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?uri  ?label
                WHERE {
                    ?uri a <http://ontology.bonsai.uno/core#ActivityType>;
                    rdfs:label ?label
                    FILTER(regex(str(?uri), '"""+str(parameter)+"""' ) )
                    }
        """

    sparql = SPARQLWrapper("https://db.bonsai.uno/bonsai/query")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()

    activities = [{
        'uri': activity["uri"]["value"],
        'label':activity["label"]["value"]
    } for activity in response["results"]["bindings"]]

    if len(activities)>0:
        resp = make_response(json.dumps(activities), 200)
        resp.headers.extend({})

        return resp
    else:
        abort(make_response(jsonify(message="The specified substring is not contained in any URI."), 404))

# ActivityList
# shows a list of all activities in the Bonsai db, with an optional limit

@app.route('/activities/', methods = ['GET'])
def getActivities():
    """Returns a list of activities contained in the BONSAI database.

    .. :quickref: Activities list query; Get list of available activities.

    **Example request**:

    .. sourcecode:: http

      GET /search_activities/ HTTP/1.1
      Host: api.bonsai.uno
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
          {"uri": "http://rdf.bonsai.uno/activitytype/core/eg", "label": "Electricity grid"},
          {"uri": "http://rdf.bonsai.uno/activitytype/core/em", "label": "Market for electricity"},
          {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUM", "label": "Aluminium production"},
          ...
      ]

    :query sort: sorts by alphabetical order, based on URI or label. Possible values: sort=uri, sort=label.
    :query lim: limits the length of results, of type integer (e.g., 10). Possible values: between 0 and 1000. Defaults to 100.
    :resheader Content-Type: application/json
    :status 200: Activities found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """
    lim = request.args.get('lim', 100)

    try:
        lim = int(lim)
    except ValueError:
        abort(make_response(jsonify(message="The 'lim' parameter does not seem to be of type integer."), 400))
    if not lim>0 or not lim<1000:
        abort(make_response(jsonify(message="The 'lim' parameter is not defined within the accepted value range (>0 - <1000)."), 400))
    if not request.args.get('sort'):
        sort = "label"
    else:
        sort = request.args.get('sort')
    if sort!="uri" and sort!="label":
        abort(make_response(jsonify(message="The 'sort' parameter does not seem to be valid."), 400))

    query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?uri  ?label WHERE {
                    ?uri a <http://ontology.bonsai.uno/core#ActivityType>;
                    rdfs:label ?label
                    } order by asc(UCASE(str(?"""+sort+"""))) LIMIT """+str(lim)

    sparql = SPARQLWrapper(DATABASE)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()

    # Parse the response in a dicitonnary
    activities = [{
        'uri': activity["uri"]["value"],
        'label':activity["label"]["value"]
    } for activity in response["results"]["bindings"]]

    if not len(activities)>0:
        abort(make_response(jsonify(message="The resource does not seem to be found."), 404))

    resp = make_response(json.dumps(activities), 200)
    resp.headers.extend({})

    return resp

"""Activity relations query (**NOT IMPLEMENTED YET**)."""
@app.route('/activities/get_relations/<path:parameter>', methods = ['GET'])
def getActivityRelations(parameter):

    """Returns a list of activity flows that are *input of* and *output of* the specified activity.

    .. :quickref: Flows list query; Get list of flows related to a specified activity.

    **Example request**:

    .. sourcecode:: http

      GET /search_relations/http://rdf.bonsai.uno/activitytype/core/eg HTTP/1.1
      Host: api.bonsai.uno
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
          {
            "uri": "http://rdf.bonsai.uno/activitytype/core/eg",
            "label": "Electricity grid"
          },
          {
            "isInputOf": [
              {
                "uri": "http://rdf.bonsai.uno/activitytype/core/someUri1",
                "label": "Some label1"
              },
              {
                "uri": "http://rdf.bonsai.uno/activitytype/core/someUri2",
                "label": "Some label2"
              }
            ]
          },
          {
            "isOutputOf": [
              {
                "uri": "http://rdf.bonsai.uno/activitytype/core/someUri1",
                "label": "Some label3"
              },
              {
                "uri": "http://rdf.bonsai.uno/activitytype/core/someUri2",
                "label": "Some label4"
              }
            ]
          }
        ]

    :resheader Content-Type: application/json
    :status 200: Activity found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """
    return abort(make_response(jsonify(message="Sorry, this resource is not yet implemented."), 404))

    """Requests LCA from the LCA calculation module (**NOT IMPLEMENTED YET**) and returns results (**NOT IMPLEMENTED YET**)."""

@app.route('/do_lca/', methods = ['POST'])
def postDoLCA():

    """Returns a list of impacts for one or several functional units specified.

    .. :quickref: LCA results query; Get impacts for a specified functional unit.

    **Example request**:

    .. sourcecode:: http

      POST /do_lca/ HTTP/1.1
      Host: api.bonsai.uno

    .. sourcecode:: http

      GET /search_activities/ HTTP/1.1
      Host: api.bonsai.uno
      Accept: application/json


    :reqheader Accept: application/json
    :<json List[tuple] functional unit: specifies one or several functional units of format (string, float, string) (e.g., [("http://rdf.bonsai.uno/someUri1",1.0,"kilogram"), ("http://rdf.bonsai.uno/someUri2",1.0,"kilogram"),...])
    :<json string method: specifies the impact method (e.g., "CML 2001")
    :<json string algorithm: specifies the linking algorithm (e.g., "attributional")


    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
            {
                "uri": "someURI",
                "activityType": "sometype",
                "label": "whatever",
                "algorithm": "attributional",
                "impacts":
                        [
                            { "impact_name": "GWP100a", "amount": 1.05, "unit":"kg CO2-eq." },
                            { "impact_name": "Acidification potential", "amount": 1.02e-5, "unit":"kg SO2-eq." }
                        ]
            }
        ]
    :resheader Content-Type: application/json
    :status 200: Activity found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """
    return abort(make_response(jsonify(message="Sorry, this resource is not yet implemented."), 404))

