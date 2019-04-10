API Documentation
=================

**bonsai_api** allows users to quickly query data from the BONSAI graph database. It is an *application programming interface* (API) based on *representational state transfer* (REST) services. It requires simple resource-oriented URLs, returns JSON-encoded responses and uses standard HTTP response codes. Queries on activities are using the GET method. Queries on LCA calculations are using the POST method. They do not require authentication.

Objective
---------
The API should become the intermediary between the database, the LCA calculation module and the users. Upon completion, **bonsai_api** is destined to be queried by users' own applications as well as providing data to the Bonsai graphical user interface.

How to use it?
--------------

From a Python environment, querying the first 5 products in the BONSAI database, sorted by label, would look like:

    .. highlight:: python
    .. code-block:: python

        import requests
        r = requests.get('https://api.bonsai.uno/products/', params = {'lim':5, "sort":"label"})
        r.json()
        
Or from a console, for example using curl:
    .. code-block:: console
        
        curl http://127.0.0.1:5000/activities/?lim=5&sort=label

Both would print out:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
        {'label': 'Activities auxiliary to financial intermediation (67)',
          'uri': 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_FAUX'},
        {'label': 'Activities of membership organisation n.e.c. (91)',
          'uri': 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ORGA'},
        {'label': 'Air transport (62)',
          'uri': 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_TAIR'},
        {'label': 'Aluminium production',
          'uri': 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_ALUM'},
        {'label': 'Animal products nec',
          'uri': 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/A_OANP'}
      ]




Summary of queries
------------------

.. qrefflask:: bonsai_api:app
  :undoc-static:

API Details
-----------

.. autoflask:: bonsai_api:app
  :undoc-static: