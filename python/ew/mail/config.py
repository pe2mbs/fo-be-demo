import requests
import requests.exceptions
import json
from flask import Blueprint, request

blueprintApi = Blueprint( 'auth', __name__ )


def registerApi( app, cors ):
    if app.config.get( "ALLOW_CORS_ORIGIN", False ):
        app.logger.info( "Allowing CORS" )
        origins = app.config.get( 'CORS_ORIGIN_WHITELIST', '*' )
        cors.init_app( blueprintApi,
                       origins = origins )

    app.register_blueprint( blueprintApi )
    return


@blueprintApi.route( "/api/mail/config", methods=[ 'GET', 'PUT' ] )
def getMailConfig():
    if request.method == 'GET':
        return json.dumps( {
            'active':           True,
            'pacFile':          'http://127.0.0.1:5000/static/proxy.pac',
            'webmailServer':    'https://webmail.it-solutions.atos.net',
            'dasId':            'G123456',
            'dasPassword':      '1234567890',
            'storageLocation':  '\\\\sts10039\\external\\test\\input',
            'storageProtocol':  'share',
            'storageUsername':  '',
            'storagePassword':  ''
        } )

    elif request.method == 'PUT':
        return ""

    raise Exception( "Invalid request" )

@blueprintApi.route( "/api/mail/check_proxy", methods=[ 'POST' ] )
def checkMailProxy():
    serverAddress = request.json()[ 'proxyService' ]
    print( "proxyService: %s" % ( serverAddress ) )
    try:
        r = requests.get( n )
        data = r.text

        if ( 'application/x-ns-proxy-autoconfig' in r.headers[ 'content-type' ] and
             'function' in data and 'FindProxyForURL' in data ):
            return json.dumps( { 'result': True,
                                 'message': '' } )

        print( "r.status_code %i" % ( r.status_code ) )
        print( "r.content-type %s" % ( r.headers[ 'content-type' ] ) )
        print( "r.encoding %s" % ( r.encoding ) )
        return json.dumps( { 'result': False,
                             'message': 'Failed proxy: %s' % ( requests.codes[ r.status_code ] ) } )
    except Exception as exc:
        return json.dumps( { 'result': False,
                             'message': str( exc ) } )


@blueprintApi.route( "/api/mail/check_exchange_server", methods=[ 'POST' ] )
def checkExchangeServer():
    serverAddress = request.json()[ 'exchangeServer' ]
    print( "exchangeServer: %s" % ( serverAddress ) )
    try:
        r = requests.get( serverAddress )
        data = r.text

        if 'Microsoft' in data and 'Exchange' in data:
            return json.dumps( { 'result': True,
                                 'message': '' } )

        print( "r.status_code %i" % ( r.status_code ) )
        print( "r.content-type %s" % ( r.headers[ 'content-type' ] ) )
        print( "r.encoding %s" % ( r.encoding ) )
        return json.dumps( { 'result': False,
                         'message': 'Failed proxy: %s' % ( requests.codes[ r.status_code ] ) } )

    except requests.exceptions.ConnectionError as e:
        return json.dumps( { 'result': False,
                             'message': 'Could not connect to address' } )
    except Exception as exc:
        return json.dumps( { 'result': False,
                             'message': str( exc ) } )


@blueprintApi.route( "/api/mail/check_account", methods=[ 'POST' ] )
def checkAccount():
    accountData = request.json()
    print( "checkAccount: %s" % ( repr( accountData ) ) )


