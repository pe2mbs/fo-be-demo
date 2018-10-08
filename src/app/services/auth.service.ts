import { environment } from '../../environments/environment';
import { Injectable, OnInit } from '@angular/core';
import { Observable, throwError} from 'rxjs';
import { finalize, tap, map, catchError, retry } from 'rxjs/operators';
import {  HttpClient, 
          HttpParams, 
          HttpErrorResponse, 
          HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService implements OnInit {
  private token;

  constructor( private http: HttpClient )  
  { 
    return;
  }

  ngOnInit(): void 
  {
    console.log( 'call auth$( user1, 123456 )' );
    this.auth$( 'user1', '123456' ).subscribe( result => {
      console.log( 'TOKEN: ', result[ 'access_token' ] );
      this.token = result[ 'access_token' ];
    } );
  }

  public auth$( user: string, password: string ): Observable<string>
  {
    const credentials = { username: user, 
                          password: password };
    const headers = new HttpHeaders().set( 'Content-Type', 'application/json' );

    console.log( 'auth ' + environment.backend + '/auth', credentials, headers );
    return this.http.post<string>( environment.backend + '/auth',
                                    credentials, { headers } 
    ).pipe(
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

  public getToken(): string
  {
    return this.token;
  }

}
