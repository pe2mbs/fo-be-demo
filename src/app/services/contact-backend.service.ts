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
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CrudBackendService } from './crud-backend.service';

export interface UserRecord
{
  id?: number;
  first_name?: string;
  last_name?: string;
  phone?: string;
  email?: string;
  address?: string;
}

@Injectable( { providedIn: 'root' } )
export class ContactBackendService extends CrudBackendService<UserRecord>
{
  constructor( httpClient:  HttpClient )
  {
    super( '/contact', httpClient );
    return;
  }
}
