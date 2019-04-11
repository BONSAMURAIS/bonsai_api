import os
from flask import Flask, request, make_response, abort, jsonify
import connexion


from SPARQLWrapper import SPARQLWrapper, JSON
import json


"""Search for activities."""
def getSearchActivityByLabel(substring):

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

    
    return abort(make_response(jsonify(message="Sorry, this resource is not yet implemented."), 404))

    """Requests LCA from the LCA calculation module (**NOT IMPLEMENTED YET**) and returns results (**NOT IMPLEMENTED YET**)."""

#@app.route('/do_lca/', methods = ['POST'])
def postDoLCA():


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

