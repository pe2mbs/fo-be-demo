# -*- coding: utf-8 -*-
"""Angular base API for the 'Main Angular application package'."""
#
# Angular base API for the 'Main Angular application package'
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
import os
from flask import Blueprint, send_from_directory, current_app
from werkzeug.routing import BaseConverter


class RegexConverter( BaseConverter ):
    def __init__( self, url_map, *items ):
        super( RegexConverter, self ).__init__( url_map )
        self.regex = items[ 0 ]


blueprint   = Blueprint( 'angular', __name__ )
logger      = None


def registerAngular( app, cors ):
    # Set the logger for the oldangular module
    app.url_map.converters[ 'regex' ] = RegexConverter
    app.register_blueprint( blueprint )
    return


@blueprint.route( '/' )
def index():
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info( "Angular dist (%s) : %s" % ( env, angular_path ) )
    try:
        if not os.path.isfile(os.path.join( angular_path, "index.html" ) ):
            current_app.logger.info( "Python says file not found" )

        return send_from_directory( angular_path, "index.html" )

    except Exception as exc:
        current_app.logger.error( exc )
        raise


@blueprint.route( r"/<regex('\w\.(js|css)'):path>" )
def angular_src( path ):
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info("Angular dist (%s) : %s" % ( env, angular_path ) )
    return send_from_directory( angular_path, path )
