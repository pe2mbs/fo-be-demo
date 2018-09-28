import { environment } from '../../environments/environment';
import { Injectable } from '@angular/core';
import { Observable, throwError} from 'rxjs';
import { finalize, tap, map, catchError, retry } from 'rxjs/operators';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';

export interface PagerInfo
{
  totalItems:  number;
  currentPage: number;
  pageSize:    number;
  totalPages:  number;
  startPage:   number;
  endPage:     number;
  startIndex:  number;
  endIndex:    number;
  pages:       Array<number>;
}

export interface PagerData<T>
{
  pagerInfo: PagerInfo;
  pagedItems?: Array<T>;
}

export class CrudBackendService<T> {
  private api: string;
  constructor( api: string, private  httpClient:  HttpClient )
  {
    this.api = environment.backend;
    this.api += api;
    console.log( this.api );
    if ( !this.api.endsWith( '/' ) )
    {
      this.api += '/';
    }
    console.log( this.api );
  }

  /*
  *   Retrieves all records from the collection on the server.
  * 
  *   :returns:       An Observable to the array of records
  * 
  *   TODO: This is not a good solution for very big collections.
  *         For very big collections a different function must be
  *         implemented.
  */
  public getList$(): Observable<Array<T>>
  {
    console.log( 'getList "' + this.api + 'list"()' );
    return this.httpClient.get<Array<T>>( this.api + 'list' ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res;
      } ) );
  }

  public getPagedList$( offset: number, count: number ): Observable<PagerData<T>>
  {
    console.log( 'getPagedList "' + this.api + 'list"( ' + offset + ', ' + count + ' )' );
    let params = new HttpParams().set( 'offset', String( offset ) )
                                 .set( 'count', String( count ) );
    return this.httpClient.get<PagerData<T>>( this.api + 'paged', { params } ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res;
      } ) );
  }
  /*
  *   Adds a new record to the collection on the server.
  * 
  *   :param record:  Object that represents the record of the database
  *                   the 'id' of the record should not be present.
  *   :returns:       An Observable to the newly added record.
  */
 public add$( record: T ): Observable<T>
  {
    console.log( 'Add PUT (new)"' + this.api + '"' );
    return this.httpClient.put<T>( this.api + '0', record ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res[ 'record' ];
      } ) );
  }

  /*
  *   Edit a complete record in the collection on the server.
  * 
  *   :param record:  Object that represents the record of the database.
  *   :param id:      The identification of the record in the database.
  *   :returns:       An Observable to the edited record.
  */
  public edit$( record: T, id?: number ): Observable<T>
  {
    if ( id == null )
    {
      id = record[ 'id' ];
    }
    console.log( 'Edit PUT "' + this.api + id + '"' );
    return this.httpClient.put<T>( this.api + id, record ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res[ 'record' ];
      } ) );
  }

  /*
  *   Edit some fields in the record in the collection on the server.
  * 
  *   :param record:  Object that represents the record of the database
  *                   Only the altered field shall be present.
  *   :param id:      The identification of the record in the database.
  *   :returns:       An Observable to the edited record.
  */
  public alter$( record: T, id?: number ): Observable<T>
  {
    if ( id == null )
    {
      id = record[ 'id' ];
    }
    console.log( 'Patch API "' + this.api + id + '"' );
    return this.httpClient.patch<T>( this.api + id, record ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res[ 'record' ];
      } ) );
  }

  /*
  *   Delete a record in the collection on the server.
  * 
  *   :param id:      The identification of the record in the database.
  *   :returns:       An Observable to the deleted record.
  */
  public delete$( id: number ): Observable<T>
  {
    console.log( 'Delete API "' + this.api + id + '"' );
    return this.httpClient.delete<T>( this.api + id ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( 'Received: ', data ),
        error => console.log( 'Houston we have a problem: ', error )
      ),
      catchError( (err: HttpErrorResponse) => {
        console.log( 'catchError ', err );
        return throwError( err.error );
      }),
      map( res => {
        console.log( 'map ', res );
        return res[ 'record' ];
      } ) );
  }
}

