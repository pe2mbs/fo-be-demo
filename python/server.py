#!/usr/bin/python3
#
# Python and Flask serving Angular
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
"""Python and Flask serving Angular"""

from os import system
from sys import exit, argv
from config import loadSettings, angular_path
from getopt import getopt, GetoptError
from flask import Flask
from flask_cors import CORS
from api.contacts import ApiContacts
from angular import AngularLoader, RegexConverter

__version__ = '0.1'
__author__  = 'Marc Bertens-Nguyen <m.bertens@pe2mbs.nl'
__license__ = 'GPLv2'
__date__    = '2018'

app = Flask( __name__, 
             static_url_path = "",
             static_folder = angular_path + "/" )

# Setup the Angular application
app.url_map.converters[ 'regex' ] = RegexConverter
AngularLoader.register( app )

# Setup the API's
ApiContacts.register( app )

def usage():
    banner()
    print( """

-h / --help                  This help page.
-c / --configuration <name>  Selecting the executing configuration.
                             may be 'dev' or 'production' or any other configured in Angliar CLI.
    """ )


def banner():
    print( """
{app} version {ver}, Copyright (C) {year} {author}
{app} comes with ABSOLUTELY NO WARRANTY; for details
type `server.py --help'.  This is free software, and you are welcome
to redistribute it under certain conditions; type `server.py --help' for details.
""".format( app = __doc__, ver = __version__, year = __date__, author = __author__ ) )


def main():
    configuration = 'dev'
    try:
        opts, args = getopt( argv[1:], "hc:", [ "help", "configuration=" ] )

    except GetoptError as err:
        # print help information and exit:
        print( str( err ) )  # will print something like "option -a not recognized"
        usage()
        exit( 2 )

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            exit()

        elif o in ("-c", "--configuration"):
            configuration = a

        else:
            assert False, "unhandled option"

    verbose = (configuration == 'dev')
    settings = loadSettings( configuration )
    if verbose:
        banner()
        print( "Running ng build." )

    if configuration == 'dev':
        system( 'ng build' )

    else:
        system( 'ng build --configuration ' + configuration )

    if verbose:
        print( "Starting the web server." )

    if settings[ 'debug' ]:
        CORS( app )

    app.run( **settings )
    return


if __name__ == "__main__":
    main()
