#
# Configuration for the 'Python and Flask serving Angular'
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
from json import load
from os.path import join, abspath, dirname, basename, isfile, splitext, isdir
from glob import iglob

project_dir     = abspath( join( dirname( abspath( __file__ ) ), '..' ) )
angular_path    = abspath( join( project_dir, "dist", basename( project_dir ) ) + "/" )
source_path     = abspath( join( project_dir, "src", "app" ) )


def getFiles( path, monitor_ext ):
    files = []
    for filename in iglob( path + '/*', recursive = True ):
        if isfile( filename ):
            #print( filename )
            if splitext( filename )[1] in monitor_ext:
                files.append( filename )

        elif isdir( filename ):
            files.extend( getFiles( filename, monitor_ext ) )

    return files


def loadSettings( configuration ):
    global source_path, angular_path, project_dir

    with open( "server.json", "r" ) as stream:
        data = load( stream )

    data = data[ configuration ]
    if data[ 'debug' ]:
        if 'extra_files' in data:
            data[ 'extra_files' ] = getFiles( source_path,
                                              data[ 'extra_files' ] )

    if 'project_dir' in data:
        project_dir     = abspath( data[ 'project_dir' ] )
        angular_path    = abspath( join( project_dir, "dist", basename( project_dir ) ) + "/" )
        source_path     = abspath( join( project_dir, "src", "app" ) )
        del data['project_dir']

    if 'angular_path' in data:
        angular_path    = abspath( data[ 'angular_path' ] ) + "/"
        del data[ 'angular_path' ]

    if 'source_path' in data:
        source_path     = abspath( data[ 'source_path' ] )
        del data['source_path']

    return data

