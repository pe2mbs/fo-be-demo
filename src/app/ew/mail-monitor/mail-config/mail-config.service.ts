import { Injectable, OnInit } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { finalize, tap, map, catchError, retry, delay } from 'rxjs/operators';
import { of } from 'rxjs';

import {  HttpClient, 
          HttpParams, 
          HttpErrorResponse, 
          HttpHeaders } from '@angular/common/http';
import { environment } from '../../../../environments/environment.dev';
import { MailConfig } from './mail-config';

export interface CheckProxyResult
{
  result: boolean;
  message: string;
}

export interface CheckAccountResult
{
  result: boolean;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class MailConfigService 
{
  constructor( private http: HttpClient ) 
  { 
    return;
  }

  public getMailConfig$(): Observable<MailConfig>
  {
    const headers = new HttpHeaders().set( 'Content-Type', 'application/json' );
    console.log( 'getMailConfig$ ' + environment.backend + '/mail/config' );
    return this.http.get<MailConfig>( environment.backend + '/mail/config' ).pipe(
      retry( 3 ),
      tap(
        data => console.log( 'Received: ', data ),
        error => {
          console.log( 'Houston we have a problem: ', error );
          console.error( error );
        }
      ),
      catchError( (err: HttpErrorResponse) => {
        console.error( err );
        console.log( 'catchError ', err );
        return throwError( err.error );
      } ),
      map( res => {
        console.log( 'map ', res );
        return res;
      } ) );
  }

  public updateMailConfig$( active: boolean,
                            pacFile: string,
                            webmailServer: string,
                            dasId: string,
                            dasPassword: string,
                            storageLocation: string ): Observable<boolean>
  {

    return;
  }

  checkUserPassword$( obj: object )
  {
    console.log( 'checkUserPassword$( ', obj, ' )' );
    return this.http.post<CheckAccountResult>( environment.backend + '/mail/check_account', obj );
  }

  public validateProxyService$( proxyService: string ): Observable<CheckProxyResult>
  {
    if ( proxyService.startsWith( 'http' ) && proxyService.endsWith( '.pac' ) )
    {
      return this.http.post<CheckProxyResult>( environment.backend + '/mail/check_proxy', proxyService );
    }
    return new Observable( observer => {
      observer.next( { result: false, message: 'The proxy URL must start with a valid Web address and end with .pac' } );
      observer.complete();
    } );
  }

  public validateExchangeServer$( exchangeServer: string ): Observable<CheckProxyResult>
  {
    let data = new HttpParams().set( 'exchangeServer', exchangeServer );
    return this.http.post<CheckProxyResult>( environment.backend + '/mail/check_exchange_server', 
                                              exchangeServer );
  }
}
