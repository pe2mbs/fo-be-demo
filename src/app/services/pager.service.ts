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
import { PagerInfo } from './crud-backend.service';
@Injectable({
  providedIn: 'root'
})
export class PagerService 
{
  getPager( totalItems: number, currentPage: number = 1, 
            pageSize: number = 10 ): PagerInfo
  {
    // calculate total pages
    let totalPages = Math.ceil( totalItems / pageSize );

    // ensure current page isn't out of range
    if ( currentPage < 1 ) 
    { 
        currentPage = 1; 
    } 
    else if ( currentPage > totalPages ) 
    { 
        currentPage = totalPages; 
    }
     
    let startPage: number, endPage: number;
    if ( totalPages <= 10 ) 
    {
        // less than 10 total pages so show all
        startPage = 1;
        endPage = totalPages;
    } 
    else 
    {
        // more than 10 total pages so calculate start and end pages
        if ( currentPage <= 6 ) 
        {
            startPage = 1;
            endPage = 10;
        } 
        else if ( currentPage + 4 >= totalPages ) 
        {
            startPage = totalPages - 9;
            endPage = totalPages;
        } 
        else 
        {
            startPage = currentPage - 5;
            endPage = currentPage + 4;
        }
    }

    // calculate start and end item indexes
    let startIndex = ( currentPage - 1 ) * pageSize;
    let endIndex = Math.min( startIndex + pageSize - 1, totalItems - 1 );

    // create an array of pages to ng-repeat in the pager control
    let pages = Array.from( Array( ( endPage + 1 ) - startPage ).keys() )
                      .map( i => startPage + i );

    // return object with all pager properties required by the view
    return { totalItems:  totalItems,
             currentPage: currentPage,
             pageSize:    pageSize,
             totalPages:  totalPages,
             startPage:   startPage,
             endPage:     endPage,
             startIndex:  startIndex,
             endIndex:    endIndex,
             pages:       pages };
  }
}
