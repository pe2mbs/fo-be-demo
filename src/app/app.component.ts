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
import { Component, OnInit } from '@angular/core';
import { UserRecord, ContactBackendService } from './services/contact-backend.service';
import { PagerData, PagerInfo } from './services/crud-backend.service';
import { PagerService } from './services/pager.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements  OnInit {
  title = 'fo-be-test';
  itemsPerPage = 10;
  // pager object
  pager: PagerInfo;
  // paged items
  pagedItems: Array<UserRecord>;

  constructor( private  apiService: ContactBackendService )
  {
    return;
  }

  ngOnInit()
  {
    console.log( 'get contacts' );
    this.setPage();
  }
 
  setPage( page: number = 1 ) 
  {
    console.log( 'page', page );
    this.apiService.getPagedList$( page, this.itemsPerPage ).subscribe( ( data: PagerData<UserRecord> ) => {
      this.pagedItems = data.pagedItems;
      this.pager      = data.pagerInfo;
      console.log( 'pager', this.pager );
    } );
  }

  addRecord()
  {
    const record: UserRecord = {
      first_name: 'Ernst',
      last_name: 'Rijerse',
      phone: '+3160987654321',
      email: 'ernst.rijerse',
      address: 'Eendrachtlaan 530'
    };
    this.apiService.add$( record ).subscribe( data => {
      if ( this.pagedItems.length < this.itemsPerPage )
      {
        this.setPage( this.pager.totalPages );
      }
      else
      {
        this.setPage( this.pager.totalPages + 1 );
      }
    } );
  }

  delRecord( id: number )
  {
    this.apiService.delete$( id ).subscribe( data => {
      console.log( 'Deleted record: ', data );
      this.setPage( this.pager.currentPage );
    } );
  }

  editRecord()
  {
    const id: number = 3;
    const record: UserRecord = {
      id: 3,
      first_name: 'Ernst',
      last_name: 'Rijerse',
      phone: '+3160987654321',
      email: 'ernst.rijerse',
      address: 'Eendrachtlaan 530'
    };
    this.apiService.edit$( record, id ).subscribe( data => {
      console.log( 'Record edited: ', data );
      this._updateRecord( id, data );
    } );
  }

  patchRecord()
  {
    const id: number = 3;
    const record: UserRecord = {
      email: 'ernst.rijerse@equensworldline.com',
    };
    this.apiService.alter$( record, id ).subscribe( data => {
      console.log( 'Record altered: ', data );
      this._updateRecord( id, data );
    } );
  }

  _updateRecord( id: number, data )
  {
    for ( let i = 0; i < this.pagedItems.length; i++ )
    {
      if ( this.pagedItems[ i ].id === id ) 
      {
        this.pagedItems[ i ] = data;
        return;
      }
    }
  }

  _getRecordIdx( id: number )
  {
    for ( let i = 0; i < this.pagedItems.length; i++ )
    {
      if ( this.pagedItems[ i ].id === id ) 
      {
        return i;
      }
    }
    return null;
  }
}
