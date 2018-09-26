import { environment } from '../environments/environment';
import { Injectable } from '@angular/core';
import { Observable} from 'rxjs';
import { finalize, tap, map, catchError, retry } from 'rxjs/operators';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable( { providedIn: 'root' } )
export class DemoBackendService {

  constructor( private  httpClient:  HttpClient ) { }

  getContacts(): Observable<Array<Object>>
  {
    console.log( 'Retrieve list "' + environment.backend + '/contacts"' );
    return this.httpClient.get<Array<Object>>( environment.backend + '/contacts' ).pipe(
      retry( 3 ),
      tap( // Log the result or error
        data => console.log( data ),
        error => console.log( error)
      ),
      map( res => {
        return res;
      } ) );
  }

  add()
  {
    console.log( 'Add clicked "' + environment.backend + '/contact"' );
    const record = {  first_name: 'Ernst',
                      last_name: 'Rijerse',
                      phone: '+3160987654321',
                      email: 'ernst.rijerse',
                      address: 'Eendrachtlaan 530' };
    this.httpClient.put( environment.backend + '/contact/0', record ).subscribe(
      data => { console.log( data ); },
      error => { console.log( error ); }
    );
  }

  edit()
  {
    console.log( 'Edit clicked' );
    const record = {  phone: '+3161234567890',
                      email: 'm.bertens@pe2mbs.n',
                      first_name: 'Marc',
                      last_name: 'Bertens',
                      address: 'Charley Tooropstraat 12' };
    this.httpClient.put( environment.backend + '/contact/1', record ).subscribe(
      data => { console.log( data ); },
      error => { console.log( error ); }
    );
  }

  patch()
  {
    console.log( 'Patch clicked' );
    const record = { last_name: 'Bertens-Nguyen' };
    this.httpClient.patch( environment.backend + '/contact/1', record ).subscribe(
      data => { console.log( data ); },
      error => { console.log( error ); }
    );
  }

  delete()
  {
    console.log( 'Delete clicked' );
    const params = new HttpParams( { fromString: 'id=3'});
    this.httpClient.delete( environment.backend + '/contact/3', {params} ).subscribe(
      data => { console.log( data ); },
      error => { console.log( error ); }
    );
  }
}
