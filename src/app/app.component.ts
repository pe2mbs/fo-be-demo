/*
* Python and Flask serving Angular
* Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
import { Component } from '@angular/core';
import { AuthService } from './services/auth.service';
import { ContactBackendService } from './services/contact-backend.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent 
{
  constructor( private auth: AuthService, private contact: ContactBackendService )
  {
    console.log( 'AppComponent' );
    return;
  }
}
