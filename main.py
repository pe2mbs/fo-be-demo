#!/usr/bin/python3
import os
import copy
import json
from flask import Flask, request, abort
from flask import send_from_directory
from werkzeug.routing import BaseConverter
from flask_cors import cross_origin, CORS

project_dir     = os.path.dirname( os.path.abspath( __file__ ) )
pachage_name    = os.path.basename( project_dir )
angular_path    = os.path.abspath( os.path.join( project_dir, "dist", pachage_name ) + "/" )
print( angular_path )

app = Flask( __name__, 
             static_url_path="", 
             static_folder = angular_path + "/" )
CORS( app )

class RegexConverter( BaseConverter ):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

contacts = [
        {   'id': 1,  
            'first_name': 'Marc',
            'last_name': 'Bertens',
            'phone': '+3161234567890',
            'email': 'm.bertens@pe2mbs.nl',
            'address': 'Charley Tooropstraat 12' 
        },
        {   'id': 2,  
            'first_name': 'Ernst',
            'last_name': 'Rijerse',
            'phone': '+3160987654321',
            'email': 'ernst.rijerse',
            'address': 'Eendrachtlaan 530' 
        }
]

app.url_map.converters['regex'] = RegexConverter

@app.route( "/" )
def angular():
    return send_from_directory( angular_path, "index.html" )


@app.route( r"/<regex('\w\.(js|css)'):path>" )
def angular_src( path ):
    return send_from_directory( angular_path, path )


@app.route( "/api/contacts", methods=['GET']  )
@cross_origin()
def apiContacts():
    global contacts
    return json.dumps( contacts )
    
def _getIndexById( id ):
    global contacts
    for idx in range( len( contacts ) ):
        if contacts[ idx ][ 'id' ] == id:
            return idx

    abort( 404 )    


@app.route( "/api/contact/<int:id>", methods = [ 'PUT', 'PATCH', 'DELETE' ] )
@cross_origin()
def apiContact( id ):
    record = {}
    print( "apiContact", id )
    global contacts
    if request.method == 'PUT':    # Add
        record = copy.copy( request.json )
        if id == 0: 
            print( 'add new record' )
            
            record[ 'id' ] = len( contacts )+1
            contacts.append( record )

        else:
            print( 'update existing record' )
            idx = _getIndexById( id )
            record[ 'id' ] = id
            contacts[ idx ] = record


    elif request.method == 'PATCH':    # Edit
        idx = _getIndexById( id )
        contacts[ idx ].update( request.json )
        record = contacts[ idx ]

    elif request.method == 'DELETE':    # Delete record
        idx = _getIndexById( id )
        record = contacts[ idx ]
        del contacts[ idx ]

    else:
        abort( 401 )

    print( json.dumps( contacts, indent=4 ) )

    return json.dumps( { 'result': 'OK',
                         'command': request.method,
                         'record': record } )

# jwt.decode(encoded, 'secret', algorithms=['HS256'])

def main( clearText = False ):
    if not clearText:
        settings = { 'host': "127.0.0.1",
                     'port': 6443,
                     'debug': True,
                     'ssl_context': ( os.path.join( 'cert', 'dev.angular.crt' ), 
                                      os.path.join( 'cert', 'dev.angular.key' ) ) }
    else:
        settings = { 'host': "127.0.0.1",
                     'port': 6080,
                     'debug': True }

    app.run( **settings )
    return


if __name__ == "__main__":
    main( True )
