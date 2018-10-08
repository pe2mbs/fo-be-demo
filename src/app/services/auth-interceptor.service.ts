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

  intercept( req: HttpRequest<any>, 
              next: HttpHandler): Observable<HttpEvent<any>> {
      console.log( 'intercept.req ', req );
      console.log( 'intercept.next ', next );
      if ( !req.url.endsWith( '/auth' ) )
      {
        const clonedRequest = req.clone( {
          headers: req.headers.set(
              'Authorization', 'JWT ' + this.authService.getToken() )
        } );
        console.log( 'new headers', clonedRequest.headers.keys() );
        return next.handle( clonedRequest );
      }
      return next.handle( req );
  }
}
