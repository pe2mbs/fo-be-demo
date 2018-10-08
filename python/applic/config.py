# -*- coding: utf-8 -*-
"""Configuration module for the 'Main Angular application package'."""
#
# Configuration module for the 'Main Angular application package'.
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
import os
import errno
import copy
import yaml
import json
from flask import Config as BaseConfig


class Config( BaseConfig ):
    """Flask config enhanced with a `from_yaml` method."""
    def from_file( self, config_file, silent=False ):
        """Load the configuration from a file, currently JSON and YAML formats
        are supported

        :param config_file:     the filename of the JSON or YAML file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        ext = os.path.splitext( config_file )[ 1 ]
        if ext == '.json':
            result = self.from_json( config_file )

        elif ext == '.yml':
            result = self.from_yaml( config_file )

        else:
            raise Exception( "Could not load file type: '%s'" % ( ext ) )

        return result

    def from_yaml( self, config_file, silent=False ):
        """Load the configuration from a file, currently YAML formats
        are supported

        :param config_file:     the filename of the YAML file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        # Get the Flask environment variable, if not exist assume development.
        env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' )
        self[ 'ENVIRONMENT' ] = env.lower()
        try:
            with open( config_file ) as f:
                c = yaml.load( f )

        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False

            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        return self._modify( c.get( env, c ) )

    def from_json( self, config_file, silent=False ):
        """Load the configuration from a file, currently JSON formats
        are supported

        :param config_file:     the filename of the JSON file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        # Get the Flask environment variable, if not exist assume development.
        env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' )
        self[ 'ENVIRONMENT' ] = env.lower()
        try:
            with open( config_file ) as f:
                c = json.load( f )

        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False

            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        # Get the environment segment
        segment = copy.copy( c.get( env, c ) )
        #self.__dump( segment )
        if 'inport' in segment:
            # Get the import segment
            c = copy.copy( c.get( segment[ 'inport' ], {} ) )
            # join the selected segment and imported segment, making sure that
            # the selected segment has priority over the imported segement
            c.update( segment )
            segment = c

        return self._modify( segment )

    def _modify( self, c ):
        """Internal updater to fix PATH's and DATABASE uri

        :param c:
        :return:
        """
        for key in c.keys():
            if key.isupper():
                # Is the variable '**PATH**' in the name and starts with a dot.
                if "PATH" in key and c[ key ].startswith( '.' ):
                    # Resolve the path to a full path
                    self[ key ] = os.path.abspath( os.path.join( self.root_path, c[ key ] ) )

                else:
                    self[ key ] = c[ key ]

        #
        if 'DATABASE' in c:
            database_cfg = c[ 'DATABASE' ]
            engine = database_cfg[ 'ENGINE' ]
            if engine == 'sqlite':
                # For Sqlite the connect string is different, contains path and database filename
                database_cfg[ 'APP_PATH' ] = self[ 'APP_PATH' ]
                db_uri = '{ENGINE}:///{APP_PATH}/{SCHEMA}'.format( **database_cfg )

            else:
                # For other databases
                if 'HOST' not in database_cfg:
                    database_cfg[ 'HOST' ] = 'localhost'

                if 'PORT' not in database_cfg:
                    # 'HOST_ADDRESS' set to 'HOST' variable
                    database_cfg[ 'HOST_ADDRESS' ] = database_cfg[ 'HOST' ]

                else:
                    # 'HOST_ADDRESS' set to 'HOST' and 'PORT' variable
                    database_cfg[ 'HOST_ADDRESS' ] = '{HOST}:{PORT}'.format( **database_cfg )

                if 'USERNAME' in database_cfg and 'PASSWORD' in database_cfg:
                    # Include username and password into the 'HOST_ADDRESS'
                    database_cfg[ 'HOST_ADDRESS' ] = '{USERNAME}:{PASSWORD}@{HOST_ADDRESS}'.format( **database_cfg )

                elif 'USERNAME' in database_cfg:
                    # Include username into the 'HOST_ADDRESS'
                    database_cfg[ 'HOST_ADDRESS' ] = '{USERNAME}@{HOST_ADDRESS}'.format( **database_cfg )

                db_uri = '{ENGINE}://{HOST_ADDRESS}/{SCHEMA}'.format( **database_cfg )


            self[ 'SQLALCHEMY_DATABASE_URI' ] = db_uri

        if self[ 'DEBUG' ]:
            self.__dump()

        return True

    def __dump( self, segment = None ):
        logger = logging.getLogger( 'flask.app' )
        if segment is None:
            segment = self
            logger.debug( "Dump configuration." )

        else:
            logger.debug( "Dump segment configuration." )

        for key in sorted( segment.keys() ):
            logger.debug( "%-30s : %s" % ( key, segment[ key ] ) )

        return