# -*- coding: utf-8 -*-
"""Angular base module, containing the app factory function.
for the 'Main Angular application package'"""
#
# Angular base module, containing the app factory function.
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import json
import logging
import importlib
from logging.config import dictConfig
from os.path import join
from applic.angular import registerAngular

from applic import commands
from applic.exceptions import InvalidUsage
from applic.extensions import bcrypt, cache, db, migrate, jwt, cors, Flask


def createApp( root_path, config_file, module = None ):
    """An application factory, as explained here:
       http://flask.pocoo.org/docs/patterns/appfactories/.

        :param root_path:   The the root path of the application.
        :param config_file: The configuration file to be used.
        :param module:       The actual application module.

        :return:            The application object.
    """
    # Setup logging for the application
    with open( join( root_path, 'logging.json' ) ) as stream:
        logDict = json.load( stream )

    dictConfig( logDict )
    app = Flask( __name__.split( '.' )[ 0 ],
                 static_url_path    = "",
                 root_path          = root_path,
                 static_folder      = root_path )

    app.logger.info( "Starting Flask application, loading configuration." )
    app.config.fromFile( join( root_path, config_file ) )
    app.logger.setLevel( logging.DEBUG if app.config[ 'DEBUG' ] else logging.ERROR )
    app.logger.log( app.logger.level,
                    "Logging Flask application: %s" % ( logging._levelToName[ app.logger.level ] ) )

    app.logger.info( "AngularPath : %s" % ( app.config[ 'ANGULAR_PATH' ] ) )
    app.static_folder   = join( root_path, app.config[ 'ANGULAR_PATH' ] ) + "/"
    app.url_map.strict_slashes = False
    if module is None:
        module = importlib.import_module( app.config[ 'API_MODULE' ] )

    registerExtensions( app, module )
    registerBluePrints( app, module )
    registerErrorHandlers( app, module )
    registerShellContext( app, module )
    registerCommands( app, module )
    return app


def registerExtensions( app, module ):
    """Register Flask extensions.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    app.logger.info( "Registering extensions" )
    bcrypt.init_app( app )
    cache.init_app( app )
    db.init_app( app )
    migrate.init_app( app, db )
    jwt.init_app( app )
    # Set the auth callbacks
    if hasattr( module, 'jwt_identity' ):
        jwt.user_loader_callback_loader( module.jwt_identity )

    if hasattr( module, 'identity_loader' ):
        jwt.user_identity_loader( module.identity_loader )

    if hasattr( module, 'registerExtensions' ):
        module.registerExtensions( app, db )

    return


def registerBluePrints( app, module ):
    """Register Flask blueprints.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    app.logger.info( "Registering blueprints" )
    if not app.config.get( "ALLOW_CORS_ORIGIN", False ):
        app.logger.info( "NOT allowing CORS" )

    registerAngular( app, cors )
    if hasattr( module, 'registerApi' ):
        module.registerApi( app, cors )

    return


def registerErrorHandlers( app, module ):
    """Register Flask error handler.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    app.logger.info( "Registering error handler" )

    if hasattr( module, 'registerErrorHandler' ):
        module.registerErrorHandler( app )

    else:
        def errorhandler( error ):
            response = error.to_json()
            response.status_code = error.status_code
            return response

        app.errorhandler( InvalidUsage )( errorhandler )

    return


def registerShellContext( app, module ):
    """Register shell context objects.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    app.logger.info( "Registering SHELL context" )
    if hasattr( module, 'registerShellContext' ):
        module.registerShellContext( app, db )

    else:
        app.shell_context_processor( { 'db': db } )

    return


def registerCommands( app, module ):
    """Register Click commands.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    app.logger.info( "Registering commands" )
    app.cli.add_command( commands.test )
    app.cli.add_command( commands.lint )
    app.cli.add_command( commands.clean )
    app.cli.add_command( commands.urls )
    app.cli.add_command( commands.runsslCommand )
    if hasattr( module, 'registerCommands' ):
        module.registerCommands( app )

    return
