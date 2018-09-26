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

"""
200: OK
201: Aangemaakt
202: Aanvaard
203: Niet-gemachtigde informatie
204: Geen inhoud
205: Inhoud opnieuw instellen
206: Gedeeltelijke inhoud
207: Meerdere-Statussen

400: Foute aanvraag
401: Niet geautoriseerd
402: Betalende toegang
403: Verboden toegang
404: Niet gevonden
405: Methode niet toegestaan
406: Niet aanvaardbaar
407: Authenticatie op de proxyserver verplicht
408: Aanvraagtijd verstreken
409: Conflict
410: Verdwenen
411: Lengte benodigd
412: Niet voldaan aan vooraf gestelde voorwaarde
413: Aanvraag te groot
414: Aanvraag-URL te lang
415: Media-type niet ondersteund
416: Aangevraagd gedeelte niet opvraagbaar
417: Niet voldaan aan verwachting
418: I'm a teapot (gedefinieerd in RFC 2324[1], maar bedoeld als aprilgrap: zie HTCPCP)
422: Aanvraag kan niet verwerkt worden
423: Afgesloten
424: Gefaalde afhankelijkheid
426: Upgrade nodig
428: Voorwaarde nodig
429: Te veel requests
431: Headers van de aanvraag te lang
450: Geblokkeerd door Windows Parental Controls (niet-officiële HTTP-statuscode)
451: Toegang geweigerd om juridische redenen.[2] De code is een toespeling op de roman Fahrenheit 451.
494: Request Header Too Large (Nginx), Deze header lijkt op header 431 maar wordt gebruikt door nginx
495: Cert Error (Nginx), Wordt gebruikt door Nginx om een normale fout van een certificaat error in de logboeken te onderscheiden.
496: No Cert (Nginx), Wordt gebruikt door Nginx om een normale fout van een missend certificaat in de logboeken te onderscheiden
497: HTTP to HTTPS (Nginx): Interne code van Nginx om aan te geven dat er een http aanvraag is op een https port
498: Token expired/invalid (Esri): Een code van 498 geeft aan dat het token verlopen of ongeldig is.
499: Token required (Esri): Wordt weggegeven door Esri dat er een token nodig is wanneer er geen is gegeven

500: Interne serverfout
501: Niet geïmplementeerd
502: Bad Gateway
503: Dienst niet beschikbaar
504: Gateway Timeout
505: HTTP-versie wordt niet ondersteund
509: Bandbreedte overschreden (niet-officiële HTTP-statuscode)
510: Niet verlengd
511: Netwerkauthenticatie vereist
"""

def _getIndexById( id, result_code = 404 ):
    global contacts
    for idx in range( len( contacts ) ):
        if contacts[ idx ][ 'id' ] == id:
            return idx

    abort( result_code )    


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
        idx = _getIndexById( id, 410 )
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
