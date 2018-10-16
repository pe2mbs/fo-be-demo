import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService 
{
  constructor( private authService: AuthService )  
  {
    return;
  }

  intercept( req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> 
  {
    if ( !req.url.endsWith( '/login' ) )
    {
      const token = 'Token ' + this.authService.getToken();
      const obj = { setHeaders: { Authorization: token } };
      return next.handle( req.clone( obj ) );
    }
    return next.handle( req );
  }
}
