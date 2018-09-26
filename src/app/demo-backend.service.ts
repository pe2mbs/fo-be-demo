import { environment } from '../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable( { providedIn: 'root' } )
export class DemoBackendService {

  constructor( private  httpClient:  HttpClient ) { }

  getContacts()
  {
    console.log( 'Retrieve list "' + environment.backend + '/contacts"' );
    return this.httpClient.get( environment.backend + '/contacts' );
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
      response => { console.log( response ); }
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
      response => { console.log( response ); }
    );
  }

  patch()
  {
    console.log( 'Patch clicked' );
    const record = { last_name: 'Bertens-Nguyen' };
    this.httpClient.patch( environment.backend + '/contact/1', record ).subscribe(
      response => { console.log( response ); }
    );
  }

  delete()
  {
    console.log( 'Delete clicked' );
    const params = new HttpParams( { fromString: 'id=3'});
    this.httpClient.delete( environment.backend + '/contact/3', {params} ).subscribe(
      response => { console.log( response ); }
    );
  }
}
