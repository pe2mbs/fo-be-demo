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
