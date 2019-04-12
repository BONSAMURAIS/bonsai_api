import os
from flask import Flask, request, make_response, abort, jsonify
import connexion


from SPARQLWrapper import SPARQLWrapper, JSON
import json


"""Search for activities."""
def getSearchActivityByLabel(substring):
    """Returns a list of one or several activities in the BONSAI database for which the label contains the specified substring.
    
    .. :quickref: Search activities query; Get list of activities that match search criteria.
    
    **Example request**:
    
    .. sourcecode:: http
    
      GET /v1/activities/by_label/alu HTTP/1.1
      Host: https://api.bonsai.uno
      Accept: application/json
      
    **Example response**:
    
    .. sourcecode:: http
    
      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
        [
            {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUO", "label": "Mining of aluminium ores and concentrates"}, {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUW", "label": "Re-processing of secondary aluminium into new aluminium"}
        ]

    :resheader Content-Type: application/json
    :status 200: Activity found
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
                    FILTER(regex(str(?label), '"""+str(substring)+"""' ) )
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



def getSearchActivityByUri(substring):
    
    """Returns a list of one or several activities in the BONSAI database for which the URI contains the specified substring.
    
    .. :quickref: Search activities query; Get list of activities that match search criteria.
    
    **Example request**:
    
    .. sourcecode:: http
    
      GET /v1/activities/by_uri/ALU HTTP/1.1
      Host: https://api.bonsai.uno
      Accept: application/json
      
    **Example response**:
    
    .. sourcecode:: http
    
      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
        [
            {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUO", "label": "Mining of aluminium ores and concentrates"}, {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUW", "label": "Re-processing of secondary aluminium into new aluminium"}
        ]

    :resheader Content-Type: application/json
    :status 200: Activity found
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
                    FILTER(regex(str(?uri), '"""+str(substring)+"""' ) )
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


#@app.route('/activities/', methods = ['GET'])
def getActivities():
    """Returns a list of activities contained in the BONSAI database.
    
    .. :quickref: Activities list query; Get list of available activities.
    
    **Example request**:
    
    .. sourcecode:: http
    
      GET /v1/activities/ HTTP/1.1
      Host: https://api.bonsai.uno
      Accept: application/json
      
    **Example response**:
    
    .. sourcecode:: http
    
      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
      [
        {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_FAUX", "label": "Activities auxiliary to financial intermediation (67)"},
        {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ORGA", "label": "Activities of membership organisation n.e.c. (91)"},
        {"uri": "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_TAIR", "label": "Air transport (62)"}
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
#@app.route('/activities/get_relations/<path:parameter>', methods = ['GET'])
def getActivityRelations(URI):
    """Returns a list of activity flows that are *input of* and *output of* the specified activity.
    
    .. :quickref: Flows list query; Get list of flows related to a specified activity.
    
    **Example request**:
    
    .. sourcecode:: http
    
      GET /v1/activities/get_relations/http://rdf.bonsai.uno/activitytype/core/eg HTTP/1.1
      Host: https://api.bonsai.uno
      Accept: application/json
      
    **Example response**:
    
    .. sourcecode:: http
    
      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
      [
          {
            "isInputOf": [
              {
                "label": "some label",
                "uri": "some URI"
              }
            ],
            "isOutputOf": [
              {
                "label": "some other label",
                "uri": "some other URI"
              }
            ],
            "label": "Electricity grid",
            "uri": "http://rdf.bonsai.uno/activitytype/core/eg"
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

#@app.route('/do_lca/', methods = ['POST'])
def postDoLCA():
    """Returns a list of impacts for one or several functional units specified.
    
    .. :quickref: LCA results query; Get impacts for a specified functional unit.
    
    **Example request**:
    
    .. sourcecode:: http
    
      POST /v1/do_lca/ HTTP/1.1
      Host: https://api.bonsai.uno


    :reqheader Accept: application/json
    :<json string URI: specifies the URI of the activity
    :<json number amount: specifies the amount of the reference flow
    :<json string unit: specifies the unit of the reference flow
    :<json string method: specifies the impact method (e.g., "CML 2001")
    :<json string algorithm: specifies the linking algorithm (e.g., "attributional")

    **Example response**:
    
    .. sourcecode:: http
    
      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json
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
    :resheader Content-Type: application/json
    :status 200: Activity found
    :status 400: Bad request on client side (e.g., invalid parameters)
    :status 404: Resource does not exist in the database
    :status 500: Internal server error
    :returns: :class:`flask.response_class`
    """


    return abort(make_response(jsonify(message="Sorry, this resource is not yet implemented."), 404))

from swagger_ui_bundle import swagger_ui_3_path
options = {'swagger_path': swagger_ui_3_path}


connexion_app = connexion.App(__name__,  options=options)
connexion_app.add_api('swagger.yaml', strict_validation=True)
app = connexion_app.app


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

