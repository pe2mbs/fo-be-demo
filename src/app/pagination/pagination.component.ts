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
import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';
import { PagerInfo } from '../services/crud-backend.service';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent implements OnInit {
  @Input( 'pager' )       pager: PagerInfo; // the pager object
  @Output( 'goPage' )     goPage = new EventEmitter<number>();

  constructor() { }

  ngOnInit() {
  }

  onPage( n: number ): void 
  {
    this.goPage.emit( n );
  }

  onPrev(): void 
  {
    this.goPage.emit( this.pager.currentPage - 1 );
  }

  onNext( next: boolean ): void 
  {
    this.goPage.emit( this.pager.currentPage + 1 );
  }

  onLastPage(): void 
  {
    this.goPage.emit( this.pager.totalPages );
  }

  onFirstPage(): void 
  {
    this.goPage.emit( 1 );
  }
}
