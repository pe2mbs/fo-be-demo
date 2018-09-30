#
# Angular loader for the 'Python and Flask serving Angular'
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
from flask_classy import FlaskView, route
from flask import send_from_directory
from werkzeug.routing import BaseConverter
import config

class RegexConverter( BaseConverter ):
    def __init__( self, url_map, *items ):
        super( RegexConverter, self ).__init__( url_map )
        self.regex = items[ 0 ]


class AngularLoader( FlaskView ):
    route_base  = '/'
    def index( self ):
        return send_from_directory( config.angular_path, "index.html" )

    @route( r"/<regex('\w\.(js|css)'):path>" )
    def angular_src( self, path ):
        return send_from_directory( config.angular_path, path )