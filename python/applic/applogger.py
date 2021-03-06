# -*- coding: utf-8 -*-
"""logger API for the 'Main Angular application package'"""
#
# logger API for the 'Main Angular application package'
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
import logging
from functools import wraps\

logObject = None


def getLogger( root = 'flask.app' ):
    """Gets the logger instance

    :param root:    The name of the logger instance
    :return:        Logger class
    """
    return logging.getLogger( root )


def appLogger( func ):
    """Decorator to log the entry of a function/procedure/route

    :param func:    the functions being called
    :return:        the decorator wrapper function
    """
    @wraps( func )
    def wrapper( *args, **kwargs ):
        global logObject
        if logObject is None:
            logObject = logging.getLogger( 'flask.app' )

        if logObject.level == logging.DEBUG:
            argList = ', '.join( args )
            kwargList = ', '.join( [ '{0} = {1}'.format( key, value ) for key, value in kwargs.items() ] )
            argList = ( argList if len( argList ) == 0 else ", " ) + kwargList
            if len( argList ) > 0:
                argList = ' ' + argList + ' '

            logObject.debug( "entrty:%s(%s)" % ( func.__name__, argList ) )

            result = func( *args, **kwargs )

            logObject.debug( "exit:%s => %s" % ( func.__name__, repr( result ) ) )
            return result

        return func( *args, **kwargs )

    return wrapper
