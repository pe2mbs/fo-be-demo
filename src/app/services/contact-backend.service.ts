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
