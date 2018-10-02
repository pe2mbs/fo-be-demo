#
# Contacts API for the 'Python and Flask serving Angular'
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
import copy
import json
from flask import request, abort
from flask_classy import FlaskView, route
from flask_cors import cross_origin
from api.pager import getPager


class ApiContacts( FlaskView ):
    route_base = '/api/contact'

    @route( '/list', methods=['GET'] ) #<--- Adding route
    @cross_origin()
    def apiContacts( self ):
        global contacts
        return json.dumps( self.contacts )

    @route( "/paged", methods=['GET']  )
    @cross_origin()
    def apiPagedContacts( self ):
        global contacts
        offset = request.args.get( 'offset' )
        count = request.args.get( 'count' )
        if offset is None or count is None:
            abort( 428 )

        pagerInfo = getPager( len( self.contacts ), int( offset ), int( count ) )
        pagedItems = self.contacts[ pagerInfo[ 'startIndex' ]:
                                    pagerInfo[ 'endIndex' ] + 1 ]

        return json.dumps( { 'pagedItems': pagedItems,
                             'pagerInfo': pagerInfo } )

    @route( "/<int:id>", methods = [ 'GET', 'PUT', 'PATCH', 'DELETE' ] )
    @cross_origin()
    def apiContact( self, id ):
        record = {}
        print( "apiContact", id )
        global contacts
        if request.method == 'GET':    # Get
            idx = self._getIndexById( id, 410 )
            record = self.contacts[ idx ]

        elif request.method == 'PUT':    # Add of full edit
            record = copy.copy( request.json )
            if id == 0:
                print( 'add new record' )

                record[ 'id' ] = len( self.contacts )+1
                self.contacts.append( record )

            else:
                print( 'update existing record' )
                idx = self._getIndexById( id, 410 )
                record[ 'id' ] = id
                self.contacts[ idx ] = record


        elif request.method == 'PATCH':    # Alter field
            idx = self._getIndexById( id, 410 )
            self.contacts[ idx ].update( request.json )
            record = self.contacts[ idx ]

        elif request.method == 'DELETE':    # Delete record
            idx = self._getIndexById( id, 410 )
            record = self.contacts[ idx ]
            del self.contacts[ idx ]

        else:
            abort( 401 )

        return json.dumps( { 'result': 'OK',
                             'command': request.method,
                             'record': record } )

    def _getIndexById( self, id, result_code = 404 ):
        for idx in range( len( self.contacts ) ):
            if self.contacts[ idx ][ 'id' ] == id:
                return idx

        abort( result_code )

    contacts = [
        {
            "id": 1,
            "first_name": "Porter",
            "last_name": "Greer",
            "phone": "+31-6-1969-6146",
            "email": "aliquam.adipiscing@arcu.ca",
            "address": "Ap #320-8295 Donec Rd.",
            "city": "Norfolk County",
            "postal": "893450",
            "country": "Aruba",
            "create_dt": "2019-03-29T09:08:58-07:00"
        },
        {
            "id": 2,
            "first_name": "Harlan",
            "last_name": "Sparks",
            "phone": "+31-6-1340-6196",
            "email": "neque.sed@nequenonquam.org",
            "address": "7640 Ultrices, Street",
            "city": "Malbaie",
            "postal": "76914",
            "country": "Barbados",
            "create_dt": "2018-08-22T22:37:10-07:00"
        },
        {
            "id": 3,
            "first_name": "Rashad",
            "last_name": "Hahn",
            "phone": "+31-9-3950-5411",
            "email": "Phasellus@velitQuisque.org",
            "address": "6862 Morbi Av.",
            "city": "Osgoode",
            "postal": "75473",
            "country": "Palestine, State of",
            "create_dt": "2019-08-02T07:51:08-07:00"
        },
        {
            "id": 4,
            "first_name": "Charles",
            "last_name": "Parrish",
            "phone": "+31-1-5492-7783",
            "email": "risus@nisiCumsociis.com",
            "address": "5508 Justo Av.",
            "city": "Haßloch",
            "postal": "43831",
            "country": "Turkmenistan",
            "create_dt": "2018-11-30T21:05:20-08:00"
        },
        {
            "id": 5,
            "first_name": "Michael",
            "last_name": "Powers",
            "phone": "+31-6-3797-2405",
            "email": "varius@fames.com",
            "address": "8300 Placerat, Av.",
            "city": "Nice",
            "postal": "93554",
            "country": "Saint Lucia",
            "create_dt": "2019-03-14T23:07:49-07:00"
        },
        {
            "id": 6,
            "first_name": "Gareth",
            "last_name": "Gomez",
            "phone": "+31-3-2924-7522",
            "email": "scelerisque@Fusce.com",
            "address": "P.O. Box 702, 7058 Velit Street",
            "city": "Gijón",
            "postal": "B3X 8BI",
            "country": "Jordan",
            "create_dt": "2019-04-20T13:23:20-07:00"
        },
        {
            "id": 7,
            "first_name": "Jelani",
            "last_name": "Parsons",
            "phone": "+31-6-0426-8594",
            "email": "rutrum.lorem.ac@feugiat.ca",
            "address": "840-5988 Suspendisse Street",
            "city": "Passau",
            "postal": "63255",
            "country": "Dominican Republic",
            "create_dt": "2017-06-23T22:43:48-07:00"
        },
        {
            "id": 8,
            "first_name": "Talon",
            "last_name": "Bryant",
            "phone": "+31-2-0606-4030",
            "email": "nonummy.Fusce@nuncrisus.com",
            "address": "234-3451 Curabitur Avenue",
            "city": "Toruń",
            "postal": "393243",
            "country": "Austria",
            "create_dt": "2018-01-02T09:06:48-08:00"
        },
        {
            "id": 9,
            "first_name": "Timothy",
            "last_name": "Nixon",
            "phone": "+31-2-0070-8601",
            "email": "et@nuncQuisque.ca",
            "address": "Ap #605-3228 Lorem. Ave",
            "city": "North Cowichan",
            "postal": "8942",
            "country": "Korea, South",
            "create_dt": "2017-08-02T09:27:49-07:00"
        },
        {
            "id": 10,
            "first_name": "Xenos",
            "last_name": "Humphrey",
            "phone": "+31-2-2763-2027",
            "email": "dis.parturient.montes@esttempor.net",
            "address": "P.O. Box 605, 1921 Nunc Avenue",
            "city": "Tourcoing",
            "postal": "22570",
            "country": "Solomon Islands",
            "create_dt": "2019-05-03T00:35:24-07:00"
        },
        {
            "id": 11,
            "first_name": "Abbot",
            "last_name": "Schroeder",
            "phone": "+31-2-1170-3425",
            "email": "ultrices.iaculis.odio@ligulaAliquam.ca",
            "address": "229-1571 Laoreet Rd.",
            "city": "Pomarico",
            "postal": "95088",
            "country": "Guyana",
            "create_dt": "2018-10-11T13:23:02-07:00"
        },
        {
            "id": 12,
            "first_name": "Wylie",
            "last_name": "Hernandez",
            "phone": "+31-8-0268-9579",
            "email": "nibh@Proinnon.co.uk",
            "address": "887-2826 Quis Avenue",
            "city": "Cumnock",
            "postal": "13386",
            "country": "Kuwait",
            "create_dt": "2019-08-05T10:53:56-07:00"
        },
        {
            "id": 13,
            "first_name": "Brian",
            "last_name": "Gilbert",
            "phone": "+31-7-6194-0581",
            "email": "molestie.dapibus.ligula@purussapiengravida.edu",
            "address": "P.O. Box 511, 2654 Etiam Avenue",
            "city": "Lolol",
            "postal": "3817",
            "country": "Maldives",
            "create_dt": "2017-05-09T01:00:20-07:00"
        },
        {
            "id": 14,
            "first_name": "Steven",
            "last_name": "Vance",
            "phone": "+31-4-5758-7375",
            "email": "nunc.ullamcorper@vestibulum.com",
            "address": "2239 Accumsan St.",
            "city": "Walhain-Saint-Paul",
            "postal": "58697",
            "country": "Heard Island and Mcdonald Islands",
            "create_dt": "2018-01-20T15:32:06-08:00"
        },
        {
            "id": 15,
            "first_name": "Jordan",
            "last_name": "Gross",
            "phone": "+31-9-9646-8611",
            "email": "turpis.egestas@interdumligulaeu.co.uk",
            "address": "Ap #736-5954 Tortor Road",
            "city": "Honolulu",
            "postal": "61113",
            "country": "Solomon Islands",
            "create_dt": "2018-05-29T08:48:53-07:00"
        },
        {
            "id": 16,
            "first_name": "Ignatius",
            "last_name": "Weaver",
            "phone": "+31-3-7171-3436",
            "email": "gravida.mauris.ut@magnanecquam.org",
            "address": "998-1671 Sollicitudin Street",
            "city": "Gonda",
            "postal": "2898",
            "country": "Gabon",
            "create_dt": "2018-07-25T00:50:42-07:00"
        },
        {
            "id": 17,
            "first_name": "Kasper",
            "last_name": "Baker",
            "phone": "+31-8-5757-1246",
            "email": "pretium.et@ullamcorpereu.net",
            "address": "208-2023 Libero Road",
            "city": "Lodelinsart",
            "postal": "89833",
            "country": "Yemen",
            "create_dt": "2018-08-09T19:35:01-07:00"
        },
        {
            "id": 18,
            "first_name": "Cade",
            "last_name": "Norton",
            "phone": "+31-5-7353-2858",
            "email": "tempus.mauris.erat@vulputate.edu",
            "address": "Ap #476-4785 In Rd.",
            "city": "Rulles",
            "postal": "060523",
            "country": "Macedonia",
            "create_dt": "2017-03-07T11:25:58-08:00"
        },
        {
            "id": 19,
            "first_name": "Calvin",
            "last_name": "Hicks",
            "phone": "+31-2-2178-0485",
            "email": "Donec.felis.orci@risusa.com",
            "address": "8882 Metus. Rd.",
            "city": "Palmilla",
            "postal": "442749",
            "country": "China",
            "create_dt": "2017-01-21T17:34:40-08:00"
        },
        {
            "id": 20,
            "first_name": "Aaron",
            "last_name": "Munoz",
            "phone": "+31-7-6323-3880",
            "email": "cursus.Nunc.mauris@sed.ca",
            "address": "646 Et Rd.",
            "city": "Fatehpur",
            "postal": "143299",
            "country": "Moldova",
            "create_dt": "2019-08-10T13:34:52-07:00"
        },
        {
            "id": 21,
            "first_name": "Caleb",
            "last_name": "Combs",
            "phone": "+31-8-1706-0750",
            "email": "diam.Pellentesque.habitant@loremauctor.ca",
            "address": "P.O. Box 753, 4227 Dictum St.",
            "city": "Porirua",
            "postal": "0274 VW",
            "country": "New Zealand",
            "create_dt": "2018-04-12T07:17:50-07:00"
        },
        {
            "id": 22,
            "first_name": "Nasim",
            "last_name": "Frost",
            "phone": "+31-2-1958-9796",
            "email": "at.iaculis.quis@Curae.org",
            "address": "Ap #849-1470 Ligula. St.",
            "city": "Bloomington",
            "postal": "357201",
            "country": "Denmark",
            "create_dt": "2017-05-22T21:34:53-07:00"
        },
        {
            "id": 23,
            "first_name": "Declan",
            "last_name": "Barnes",
            "phone": "+31-3-0726-0620",
            "email": "ut.sem.Nulla@nislNullaeu.org",
            "address": "7836 Eu Avenue",
            "city": "Exeter",
            "postal": "5896",
            "country": "Andorra",
            "create_dt": "2019-01-14T00:18:54-08:00"
        },
        {
            "id": 24,
            "first_name": "Elvis",
            "last_name": "Hess",
            "phone": "+31-3-4766-7112",
            "email": "Nunc.laoreet@facilisisloremtristique.edu",
            "address": "P.O. Box 809, 6907 At Street",
            "city": "Tirrases",
            "postal": "90225",
            "country": "Botswana",
            "create_dt": "2017-11-30T05:39:37-08:00"
        },
        {
            "id": 25,
            "first_name": "Benjamin",
            "last_name": "Lambert",
            "phone": "+31-9-2081-4114",
            "email": "dictum.eleifend@dapibusquamquis.com",
            "address": "7199 Commodo St.",
            "city": "Sint-Lambrechts-Woluwe",
            "postal": "97293-803",
            "country": "Argentina",
            "create_dt": "2019-07-26T19:56:22-07:00"
        },
        {
            "id": 26,
            "first_name": "Kirk",
            "last_name": "Nash",
            "phone": "+31-6-0382-1369",
            "email": "neque.sed@Sed.org",
            "address": "P.O. Box 195, 1011 A, Rd.",
            "city": "Trazegnies",
            "postal": "268909",
            "country": "Macao",
            "create_dt": "2017-10-16T03:23:43-07:00"
        },
        {
            "id": 27,
            "first_name": "Amal",
            "last_name": "Carr",
            "phone": "+31-3-3476-1531",
            "email": "felis@dignissimtemporarcu.org",
            "address": "P.O. Box 546, 8231 Ultrices Ave",
            "city": "Cuddalore",
            "postal": "536675",
            "country": "Ukraine",
            "create_dt": "2017-08-22T09:21:53-07:00"
        },
        {
            "id": 28,
            "first_name": "Wylie",
            "last_name": "Meyer",
            "phone": "+31-3-4061-7202",
            "email": "et@adipiscinglobortis.com",
            "address": "718-4006 Facilisis. Street",
            "city": "Quintero",
            "postal": "16482",
            "country": "Liberia",
            "create_dt": "2019-01-19T22:29:46-08:00"
        },
        {
            "id": 29,
            "first_name": "Driscoll",
            "last_name": "Salas",
            "phone": "+31-5-5444-9107",
            "email": "nascetur.ridiculus.mus@dictumsapienAenean.ca",
            "address": "P.O. Box 871, 4019 At Road",
            "city": "Gandhidham",
            "postal": "344953",
            "country": "Benin",
            "create_dt": "2017-04-11T11:24:49-07:00"
        },
        {
            "id": 30,
            "first_name": "Logan",
            "last_name": "Austin",
            "phone": "+31-1-4216-2265",
            "email": "Lorem.ipsum@auctor.org",
            "address": "2310 Luctus Rd.",
            "city": "Valpelline",
            "postal": "7540",
            "country": "Mozambique",
            "create_dt": "2019-02-15T07:14:23-08:00"
        },
        {
            "id": 31,
            "first_name": "Colton",
            "last_name": "Beach",
            "phone": "+31-8-1897-2632",
            "email": "Fusce@mitempor.edu",
            "address": "P.O. Box 104, 6809 Cursus St.",
            "city": "Quilpué",
            "postal": "20335",
            "country": "Norway",
            "create_dt": "2017-10-31T14:28:06-07:00"
        },
        {
            "id": 32,
            "first_name": "Quentin",
            "last_name": "Byers",
            "phone": "+31-4-9155-7522",
            "email": "feugiat.tellus.lorem@diamloremauctor.edu",
            "address": "3364 Convallis Ave",
            "city": "Paternopoli",
            "postal": "731489",
            "country": "Congo, the Democratic Republic of the",
            "create_dt": "2017-05-30T13:50:08-07:00"
        },
        {
            "id": 33,
            "first_name": "Ferdinand",
            "last_name": "Best",
            "phone": "+31-3-2909-2130",
            "email": "velit.justo@vestibulum.org",
            "address": "695-8619 Quis Ave",
            "city": "Mobile",
            "postal": "35-604",
            "country": "Mauritania",
            "create_dt": "2019-02-10T21:11:31-08:00"
        },
        {
            "id": 34,
            "first_name": "Barclay",
            "last_name": "Gutierrez",
            "phone": "+31-6-6931-1275",
            "email": "Quisque.nonummy.ipsum@NullainterdumCurabitur.co.uk",
            "address": "P.O. Box 665, 9085 Diam Av.",
            "city": "Huissen",
            "postal": "4236",
            "country": "Turkmenistan",
            "create_dt": "2019-01-07T20:50:26-08:00"
        },
        {
            "id": 35,
            "first_name": "Gray",
            "last_name": "Hopkins",
            "phone": "+31-8-4827-5727",
            "email": "tortor.Nunc.commodo@sit.org",
            "address": "8922 Lacus. Av.",
            "city": "Recogne",
            "postal": "8864",
            "country": "Spain",
            "create_dt": "2018-02-27T08:51:40-08:00"
        },
        {
            "id": 36,
            "first_name": "Rooney",
            "last_name": "Townsend",
            "phone": "+31-2-9627-6937",
            "email": "justo.sit.amet@facilisis.net",
            "address": "436-8515 Lorem St.",
            "city": "San Costantino Calabro",
            "postal": "518852",
            "country": "Laos",
            "create_dt": "2018-02-21T06:34:55-08:00"
        },
        {
            "id": 37,
            "first_name": "Clark",
            "last_name": "Riley",
            "phone": "+31-8-2840-3825",
            "email": "sed.hendrerit.a@euismodenim.net",
            "address": "744-4532 Id, Street",
            "city": "Gojra",
            "postal": "09719",
            "country": "Bhutan",
            "create_dt": "2017-09-08T03:51:50-07:00"
        },
        {
            "id": 38,
            "first_name": "Norman",
            "last_name": "Sanford",
            "phone": "+31-4-9409-2440",
            "email": "dui.quis.accumsan@hendreritconsectetuercursus.edu",
            "address": "P.O. Box 293, 2284 Vel Rd.",
            "city": "Gießen",
            "postal": "40812",
            "country": "Saint Martin",
            "create_dt": "2019-03-22T03:15:00-07:00"
        },
        {
            "id": 39,
            "first_name": "Shad",
            "last_name": "Simpson",
            "phone": "+31-3-8696-4070",
            "email": "facilisis@Nuncacsem.com",
            "address": "Ap #853-7643 Fringilla, Ave",
            "city": "Marke",
            "postal": "93914",
            "country": "Taiwan",
            "create_dt": "2017-03-01T22:14:14-08:00"
        },
        {
            "id": 40,
            "first_name": "Logan",
            "last_name": "Ellison",
            "phone": "+31-1-7679-6138",
            "email": "scelerisque@ornareliberoat.edu",
            "address": "114-8414 Et St.",
            "city": "Huissen",
            "postal": "72363",
            "country": "Venezuela",
            "create_dt": "2018-06-07T03:05:49-07:00"
        },
        {
            "id": 41,
            "first_name": "Zachary",
            "last_name": "Rojas",
            "phone": "+31-4-4641-5931",
            "email": "odio.vel@magnaa.com",
            "address": "P.O. Box 292, 8893 Nullam St.",
            "city": "Lidingo",
            "postal": "C6C 6R1",
            "country": "Mexico",
            "create_dt": "2017-07-12T03:14:35-07:00"
        },
        {
            "id": 42,
            "first_name": "Matthew",
            "last_name": "Waters",
            "phone": "+31-3-2502-5402",
            "email": "amet.ante@lobortismaurisSuspendisse.com",
            "address": "Ap #373-748 Cursus Rd.",
            "city": "Sundrie",
            "postal": "3045",
            "country": "Czech Republic",
            "create_dt": "2017-03-16T14:50:12-07:00"
        },
        {
            "id": 43,
            "first_name": "Kirk",
            "last_name": "Perry",
            "phone": "+31-9-6117-5469",
            "email": "non.magna.Nam@risusatfringilla.co.uk",
            "address": "753-6730 Vestibulum St.",
            "city": "Musselburgh",
            "postal": "Y0C 1B8",
            "country": "Christmas Island",
            "create_dt": "2018-05-14T23:27:13-07:00"
        },
        {
            "id": 44,
            "first_name": "Henry",
            "last_name": "Moody",
            "phone": "+31-3-5955-9218",
            "email": "dolor.sit@non.co.uk",
            "address": "Ap #528-2021 Diam Avenue",
            "city": "Fort Simpson",
            "postal": "33479",
            "country": "Mauritania",
            "create_dt": "2017-01-18T08:40:10-08:00"
        },
        {
            "id": 45,
            "first_name": "Charles",
            "last_name": "Sanders",
            "phone": "+31-6-5380-9250",
            "email": "ipsum@asollicitudin.co.uk",
            "address": "278-5880 Tincidunt Street",
            "city": "Penhold",
            "postal": "4506 HC",
            "country": "Heard Island and Mcdonald Islands",
            "create_dt": "2017-09-28T22:59:03-07:00"
        },
        {
            "id": 46,
            "first_name": "Chase",
            "last_name": "Solomon",
            "phone": "+31-8-0401-5427",
            "email": "rutrum@Maecenasornare.net",
            "address": "Ap #980-4484 Ut, Avenue",
            "city": "Calvera",
            "postal": "38721",
            "country": "Mongolia",
            "create_dt": "2017-12-27T12:20:50-08:00"
        },
        {
            "id": 47,
            "first_name": "Geoffrey",
            "last_name": "Whitehead",
            "phone": "+31-4-6960-4426",
            "email": "molestie.in.tempus@ac.net",
            "address": "8645 Tellus. Road",
            "city": "Wambeek",
            "postal": "54645-030",
            "country": "Japan",
            "create_dt": "2017-02-12T16:22:30-08:00"
        },
        {
            "id": 48,
            "first_name": "Zachary",
            "last_name": "Stark",
            "phone": "+31-9-3452-5916",
            "email": "euismod.ac.fermentum@rutrumjusto.edu",
            "address": "P.O. Box 821, 8250 Ipsum. Road",
            "city": "Zweibrücken",
            "postal": "70423",
            "country": "Seychelles",
            "create_dt": "2018-04-29T20:18:29-07:00"
        },
        {
            "id": 49,
            "first_name": "David",
            "last_name": "Nielsen",
            "phone": "+31-5-4093-4452",
            "email": "venenatis@ultricessit.net",
            "address": "560-1114 Penatibus Road",
            "city": "Marzabotto",
            "postal": "23841",
            "country": "Nigeria",
            "create_dt": "2017-09-27T23:14:14-07:00"
        },
        {
            "id": 50,
            "first_name": "Lionel",
            "last_name": "Mccoy",
            "phone": "+31-6-1158-9803",
            "email": "netus.et@interdum.co.uk",
            "address": "7639 Lorem, Av.",
            "city": "Spy",
            "postal": "18932-125",
            "country": "Sudan",
            "create_dt": "2017-03-19T23:41:35-07:00"
        },
        {
            "id": 51,
            "first_name": "Yuli",
            "last_name": "Mcconnell",
            "phone": "+31-3-9432-1606",
            "email": "enim.gravida@apurusDuis.net",
            "address": "P.O. Box 818, 2380 Duis St.",
            "city": "Blaenau Ffestiniog",
            "postal": "396302",
            "country": "Angola",
            "create_dt": "2017-04-04T21:45:52-07:00"
        },
        {
            "id": 52,
            "first_name": "Mannix",
            "last_name": "Roy",
            "phone": "+31-8-0717-2118",
            "email": "mus.Aenean.eget@necmetus.ca",
            "address": "P.O. Box 172, 136 Lectus Rd.",
            "city": "Halesowen",
            "postal": "1945",
            "country": "Samoa",
            "create_dt": "2018-12-18T07:30:49-08:00"
        },
        {
            "id": 53,
            "first_name": "Marshall",
            "last_name": "Camacho",
            "phone": "+31-3-7284-2446",
            "email": "rutrum@nulla.co.uk",
            "address": "P.O. Box 303, 8824 Nunc. Street",
            "city": "Leipzig",
            "postal": "408418",
            "country": "Central African Republic",
            "create_dt": "2017-05-20T14:34:48-07:00"
        },
        {
            "id": 54,
            "first_name": "Henry",
            "last_name": "Huff",
            "phone": "+31-7-1022-9606",
            "email": "mauris@tellus.org",
            "address": "P.O. Box 190, 2729 Venenatis Rd.",
            "city": "Renaico",
            "postal": "826717",
            "country": "Romania",
            "create_dt": "2018-07-06T01:13:52-07:00"
        },
        {
            "id": 55,
            "first_name": "Lionel",
            "last_name": "Mckenzie",
            "phone": "+31-8-6713-1137",
            "email": "dictum.placerat@nisimagnased.co.uk",
            "address": "Ap #231-2366 Et, Av.",
            "city": "Swansea",
            "postal": "51775",
            "country": "Kuwait",
            "create_dt": "2018-12-17T04:04:36-08:00"
        },
        {
            "id": 56,
            "first_name": "Keaton",
            "last_name": "Giles",
            "phone": "+31-3-1715-6662",
            "email": "Ut@in.net",
            "address": "P.O. Box 429, 4481 Nibh St.",
            "city": "Lions Bay",
            "postal": "6031",
            "country": "Malawi",
            "create_dt": "2017-01-23T15:00:32-08:00"
        },
        {
            "id": 57,
            "first_name": "Grady",
            "last_name": "Mendoza",
            "phone": "+31-1-7788-5716",
            "email": "velit.justo.nec@utdolordapibus.edu",
            "address": "P.O. Box 468, 9503 Dolor Road",
            "city": "Pembroke",
            "postal": "404793",
            "country": "Sao Tome and Principe",
            "create_dt": "2018-09-22T09:54:07-07:00"
        },
        {
            "id": 58,
            "first_name": "Kennedy",
            "last_name": "Day",
            "phone": "+31-3-2625-4768",
            "email": "ante.Maecenas@odio.co.uk",
            "address": "9535 Consequat St.",
            "city": "Nurdağı",
            "postal": "67303",
            "country": "Djibouti",
            "create_dt": "2018-07-23T21:05:58-07:00"
        },
        {
            "id": 59,
            "first_name": "Cullen",
            "last_name": "Daniel",
            "phone": "+31-3-7975-7131",
            "email": "aliquet.odio@eumetus.com",
            "address": "P.O. Box 354, 9258 Suspendisse Avenue",
            "city": "Chemnitz",
            "postal": "01274",
            "country": "Kyrgyzstan",
            "create_dt": "2019-06-20T03:02:19-07:00"
        },
        {
            "id": 60,
            "first_name": "Grady",
            "last_name": "Ramsey",
            "phone": "+31-9-5501-1759",
            "email": "mauris@imperdietornare.org",
            "address": "6917 Nullam Av.",
            "city": "Pucón",
            "postal": "305858",
            "country": "El Salvador",
            "create_dt": "2019-05-17T16:22:21-07:00"
        },
        {
            "id": 61,
            "first_name": "Ferris",
            "last_name": "Wilson",
            "phone": "+31-3-8634-5875",
            "email": "ac.mattis.velit@pellentesquetellussem.org",
            "address": "1704 Sodales Street",
            "city": "Ararat",
            "postal": "793971",
            "country": "Sint Maarten",
            "create_dt": "2019-03-31T15:56:30-07:00"
        },
        {
            "id": 62,
            "first_name": "Isaac",
            "last_name": "Lawrence",
            "phone": "+31-2-7838-6653",
            "email": "sapien@metusIn.edu",
            "address": "586-6340 Tincidunt St.",
            "city": "Ammanford",
            "postal": "26761",
            "country": "Syria",
            "create_dt": "2019-04-25T17:26:34-07:00"
        },
        {
            "id": 63,
            "first_name": "Fuller",
            "last_name": "Mooney",
            "phone": "+31-3-9003-3342",
            "email": "erat.semper@Proinsedturpis.edu",
            "address": "633-711 Ligula. Street",
            "city": "Coleville Lake",
            "postal": "73645",
            "country": "Iran",
            "create_dt": "2019-08-21T22:54:52-07:00"
        },
        {
            "id": 64,
            "first_name": "Rafael",
            "last_name": "Mcleod",
            "phone": "+31-2-6182-8786",
            "email": "ullamcorper.viverra.Maecenas@ad.co.uk",
            "address": "P.O. Box 608, 3143 Orci St.",
            "city": "Bellevue",
            "postal": "38646",
            "country": "Maldives",
            "create_dt": "2019-03-03T13:43:51-08:00"
        },
        {
            "id": 65,
            "first_name": "Amal",
            "last_name": "Rivera",
            "phone": "+31-6-9982-3906",
            "email": "Integer.vitae.nibh@euismodurna.ca",
            "address": "Ap #836-2287 Id St.",
            "city": "Shipshaw",
            "postal": "36-401",
            "country": "Bahrain",
            "create_dt": "2017-07-30T04:48:36-07:00"
        },
        {
            "id": 66,
            "first_name": "Cain",
            "last_name": "Barker",
            "phone": "+31-3-8602-4085",
            "email": "Phasellus.ornare@Sedcongueelit.net",
            "address": "366-729 Lorem, Road",
            "city": "FerriŽres",
            "postal": "53215",
            "country": "Saint Helena, Ascension and Tristan da Cunha",
            "create_dt": "2018-11-05T13:26:55-08:00"
        },
        {
            "id": 67,
            "first_name": "Baxter",
            "last_name": "Chaney",
            "phone": "+31-8-0759-1988",
            "email": "ac.mattis@leo.com",
            "address": "P.O. Box 139, 4589 Nunc Avenue",
            "city": "Kitchener",
            "postal": "98626",
            "country": "Malta",
            "create_dt": "2017-07-22T19:43:17-07:00"
        },
        {
            "id": 68,
            "first_name": "Jackson",
            "last_name": "Stevenson",
            "phone": "+31-9-4608-9896",
            "email": "quis.arcu@tortornibh.com",
            "address": "P.O. Box 766, 7920 Sapien. Road",
            "city": "Ospedaletto d'Alpinolo",
            "postal": "86148",
            "country": "Denmark",
            "create_dt": "2017-11-08T12:06:41-08:00"
        },
        {
            "id": 69,
            "first_name": "Oren",
            "last_name": "Hale",
            "phone": "+31-7-2047-9075",
            "email": "vitae@Morbiquis.co.uk",
            "address": "9384 Nunc Rd.",
            "city": "Klemskerke",
            "postal": "25742-803",
            "country": "Kenya",
            "create_dt": "2017-01-28T20:29:08-08:00"
        },
        {
            "id": 70,
            "first_name": "Lyle",
            "last_name": "Caldwell",
            "phone": "+31-1-1970-2590",
            "email": "nec@Vivamusnibhdolor.ca",
            "address": "9860 Metus. Street",
            "city": "Tarragona",
            "postal": "70811",
            "country": "Antigua and Barbuda",
            "create_dt": "2017-02-06T04:33:25-08:00"
        },
        {
            "id": 71,
            "first_name": "Tanner",
            "last_name": "Johns",
            "phone": "+31-7-1106-4800",
            "email": "nisl@nequeNullamut.ca",
            "address": "P.O. Box 624, 537 In, Street",
            "city": "Montoggio",
            "postal": "64-748",
            "country": "Palau",
            "create_dt": "2019-09-09T19:47:25-07:00"
        },
        {
            "id": 72,
            "first_name": "Bert",
            "last_name": "Dunlap",
            "phone": "+31-9-6634-2578",
            "email": "vitae.sodales.nisi@euerosNam.net",
            "address": "P.O. Box 843, 8503 At Avenue",
            "city": "Isnes",
            "postal": "60171-683",
            "country": "Gabon",
            "create_dt": "2018-11-07T21:21:36-08:00"
        },
        {
            "id": 73,
            "first_name": "Raymond",
            "last_name": "Hinton",
            "phone": "+31-9-7775-6191",
            "email": "Suspendisse@telluslorem.org",
            "address": "3006 Aliquam Av.",
            "city": "Laramie",
            "postal": "35588",
            "country": "Mauritius",
            "create_dt": "2017-03-21T04:07:16-07:00"
        },
        {
            "id": 74,
            "first_name": "Chandler",
            "last_name": "Gentry",
            "phone": "+31-2-9217-9728",
            "email": "rutrum.lorem.ac@Ut.com",
            "address": "Ap #328-2414 Lacus, Rd.",
            "city": "Cuglieri",
            "postal": "K4C 8L0",
            "country": "Germany",
            "create_dt": "2017-12-24T15:26:07-08:00"
        },
        {
            "id": 75,
            "first_name": "Holmes",
            "last_name": "Rocha",
            "phone": "+31-3-0283-9172",
            "email": "eu@sodalesatvelit.edu",
            "address": "P.O. Box 132, 8090 Nisl. Ave",
            "city": "Katsina",
            "postal": "334678",
            "country": "Turkey",
            "create_dt": "2018-04-17T15:16:53-07:00"
        },
        {
            "id": 76,
            "first_name": "Holmes",
            "last_name": "Farmer",
            "phone": "+31-9-4078-7574",
            "email": "vel.mauris.Integer@enimSuspendissealiquet.ca",
            "address": "Ap #619-5377 Magna Av.",
            "city": "Southwell",
            "postal": "31776",
            "country": "Comoros",
            "create_dt": "2019-09-15T04:36:01-07:00"
        },
        {
            "id": 77,
            "first_name": "Mason",
            "last_name": "Hampton",
            "phone": "+31-3-3560-7106",
            "email": "Nulla.eu.neque@vitaeposuere.edu",
            "address": "562-7142 Nec Road",
            "city": "Fiuminata",
            "postal": "7704 EB",
            "country": "Mozambique",
            "create_dt": "2018-02-19T00:28:30-08:00"
        },
        {
            "id": 78,
            "first_name": "Hiram",
            "last_name": "Ramos",
            "phone": "+31-7-3060-3635",
            "email": "mauris.Suspendisse@sagittis.net",
            "address": "Ap #401-4399 Consectetuer Ave",
            "city": "Melton Mowbray",
            "postal": "820792",
            "country": "Montenegro",
            "create_dt": "2018-08-09T03:46:56-07:00"
        },
        {
            "id": 79,
            "first_name": "Branden",
            "last_name": "Vinson",
            "phone": "+31-5-5662-2385",
            "email": "et.rutrum.non@vestibulum.com",
            "address": "P.O. Box 875, 2548 Ultrices. Road",
            "city": "Munger",
            "postal": "4336",
            "country": "Belarus",
            "create_dt": "2018-04-05T23:09:13-07:00"
        },
        {
            "id": 80,
            "first_name": "Cairo",
            "last_name": "Koch",
            "phone": "+31-4-0874-1957",
            "email": "Aliquam.ultrices.iaculis@Morbiaccumsanlaoreet.net",
            "address": "Ap #308-8057 Est, Rd.",
            "city": "Chañaral",
            "postal": "277702",
            "country": "Nauru",
            "create_dt": "2018-01-26T05:39:19-08:00"
        },
        {
            "id": 81,
            "first_name": "Jackson",
            "last_name": "Pruitt",
            "phone": "+31-3-0614-2105",
            "email": "pede.et.risus@lorem.com",
            "address": "P.O. Box 114, 1684 Consectetuer St.",
            "city": "Nalinnes",
            "postal": "59-709",
            "country": "Iran",
            "create_dt": "2017-04-19T19:24:36-07:00"
        },
        {
            "id": 82,
            "first_name": "Yoshio",
            "last_name": "Lyons",
            "phone": "+31-1-9508-1750",
            "email": "eleifend@adipiscing.ca",
            "address": "5193 Quisque Ave",
            "city": "Fort Collins",
            "postal": "4812",
            "country": "Suriname",
            "create_dt": "2019-04-10T06:06:31-07:00"
        },
        {
            "id": 83,
            "first_name": "Raymond",
            "last_name": "Hyde",
            "phone": "+31-3-4983-5453",
            "email": "Ut@vellectus.net",
            "address": "856-9331 Tincidunt Avenue",
            "city": "Nashville",
            "postal": "68-498",
            "country": "Antarctica",
            "create_dt": "2018-09-30T01:42:16-07:00"
        },
        {
            "id": 84,
            "first_name": "Duncan",
            "last_name": "Tyler",
            "phone": "+31-7-8512-1759",
            "email": "dictum.mi@odio.com",
            "address": "3205 Ad St.",
            "city": "Evansville",
            "postal": "81224",
            "country": "Turkey",
            "create_dt": "2018-12-11T15:13:42-08:00"
        },
        {
            "id": 85,
            "first_name": "Carter",
            "last_name": "Stafford",
            "phone": "+31-7-4991-8546",
            "email": "ac@pedeNunc.com",
            "address": "894-2006 At, Street",
            "city": "Boninne",
            "postal": "46950-953",
            "country": "Estonia",
            "create_dt": "2017-12-03T06:12:10-08:00"
        },
        {
            "id": 86,
            "first_name": "Wang",
            "last_name": "Leblanc",
            "phone": "+31-3-4608-7374",
            "email": "Morbi.sit@mattisvelit.ca",
            "address": "1570 Aenean Street",
            "city": "Eckville",
            "postal": "657986",
            "country": "Congo (Brazzaville)",
            "create_dt": "2017-02-27T02:14:37-08:00"
        },
        {
            "id": 87,
            "first_name": "Jerry",
            "last_name": "Boone",
            "phone": "+31-3-2107-2904",
            "email": "nunc.nulla@pretiumetrutrum.com",
            "address": "P.O. Box 805, 5557 Tristique Road",
            "city": "Matagami",
            "postal": "4710",
            "country": "Ghana",
            "create_dt": "2019-07-27T13:26:11-07:00"
        },
        {
            "id": 88,
            "first_name": "Anthony",
            "last_name": "Kirk",
            "phone": "+31-3-0732-6291",
            "email": "vel.nisl.Quisque@erateget.edu",
            "address": "P.O. Box 450, 1708 Vehicula Street",
            "city": "Herenthout",
            "postal": "L4B 0W2",
            "country": "Guinea",
            "create_dt": "2019-03-31T22:00:10-07:00"
        },
        {
            "id": 89,
            "first_name": "Jarrod",
            "last_name": "Ellison",
            "phone": "+31-5-5233-2940",
            "email": "arcu.Vestibulum.ante@liberoet.edu",
            "address": "Ap #576-8633 Convallis Street",
            "city": "Anderlues",
            "postal": "24797-732",
            "country": "Tanzania",
            "create_dt": "2018-09-20T20:24:26-07:00"
        },
        {
            "id": 90,
            "first_name": "Nathan",
            "last_name": "Holt",
            "phone": "+31-2-1460-4888",
            "email": "at.arcu@vitaerisusDuis.com",
            "address": "6459 Lobortis St.",
            "city": "Norderstedt",
            "postal": "22160-914",
            "country": "Tokelau",
            "create_dt": "2017-03-10T00:36:26-08:00"
        },
        {
            "id": 91,
            "first_name": "Kyle",
            "last_name": "Curtis",
            "phone": "+31-3-9431-1050",
            "email": "lorem.lorem@accumsan.net",
            "address": "P.O. Box 337, 4581 Lorem St.",
            "city": "Athus",
            "postal": "9601",
            "country": "Maldives",
            "create_dt": "2018-03-03T02:11:29-08:00"
        },
        {
            "id": 92,
            "first_name": "Sean",
            "last_name": "Maldonado",
            "phone": "+31-9-8495-9176",
            "email": "purus.mauris@purusactellus.co.uk",
            "address": "9784 Elit St.",
            "city": "Londrina",
            "postal": "10004",
            "country": "Burkina Faso",
            "create_dt": "2018-01-29T13:31:47-08:00"
        },
        {
            "id": 93,
            "first_name": "Marsden",
            "last_name": "Mercer",
            "phone": "+31-6-6793-6079",
            "email": "non.feugiat.nec@Suspendisse.net",
            "address": "Ap #214-6958 Et, St.",
            "city": "Niort",
            "postal": "22-913",
            "country": "Tokelau",
            "create_dt": "2018-05-21T06:18:45-07:00"
        },
        {
            "id": 94,
            "first_name": "Rigel",
            "last_name": "Mcintyre",
            "phone": "+31-9-5157-3450",
            "email": "nec@dignissimMaecenas.org",
            "address": "3265 Pede St.",
            "city": "Grangemouth",
            "postal": "0989",
            "country": "Saint Helena, Ascension and Tristan da Cunha",
            "create_dt": "2019-08-15T08:03:49-07:00"
        },
        {
            "id": 95,
            "first_name": "Fitzgerald",
            "last_name": "Morrison",
            "phone": "+31-4-6215-2722",
            "email": "Aliquam@arcu.ca",
            "address": "724-6777 Nulla Rd.",
            "city": "Santipur",
            "postal": "09662",
            "country": "Faroe Islands",
            "create_dt": "2017-06-18T03:31:53-07:00"
        },
        {
            "id": 96,
            "first_name": "Vernon",
            "last_name": "Campos",
            "phone": "+31-4-5152-0403",
            "email": "Curabitur.vel@ultricessitamet.ca",
            "address": "P.O. Box 220, 7565 Pharetra St.",
            "city": "Daska",
            "postal": "816007",
            "country": "Comoros",
            "create_dt": "2019-04-16T17:04:35-07:00"
        },
        {
            "id": 97,
            "first_name": "Ahmed",
            "last_name": "Leblanc",
            "phone": "+31-7-2924-0487",
            "email": "non@morbitristique.net",
            "address": "Ap #979-6674 Egestas. St.",
            "city": "Slijpe",
            "postal": "2554",
            "country": "Guyana",
            "create_dt": "2018-06-08T23:03:09-07:00"
        },
        {
            "id": 98,
            "first_name": "Kamal",
            "last_name": "Bradley",
            "phone": "+31-3-3696-8455",
            "email": "In@sagittis.net",
            "address": "892-9325 Nullam Ave",
            "city": "Latronico",
            "postal": "432723",
            "country": "Ethiopia",
            "create_dt": "2018-06-10T03:11:04-07:00"
        },
        {
            "id": 99,
            "first_name": "Hamish",
            "last_name": "Barr",
            "phone": "+31-8-4025-7021",
            "email": "congue@etnetus.ca",
            "address": "652-8161 Aenean Av.",
            "city": "Schönebeck",
            "postal": "798313",
            "country": "Uruguay",
            "create_dt": "2019-02-25T00:42:27-08:00"
        },
        {
            "id": 100,
            "first_name": "Kato",
            "last_name": "Blackburn",
            "phone": "+31-7-8734-0215",
            "email": "placerat@Nunc.ca",
            "address": "984-4265 Donec Avenue",
            "city": "Sagar",
            "postal": "33233",
            "country": "Guernsey",
            "create_dt": "2018-08-21T08:30:50-07:00"
        }
    ]

