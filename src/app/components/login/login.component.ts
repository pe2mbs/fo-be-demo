import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  public data: FormGroup;

  constructor( fb: FormBuilder, private auth: AuthService ) 
  { 
    this.data = fb.group( {
      'username': [ 'test' ], 
      'password': [ '12345678' ]
    } );
    return;
  }

  get username() 
  {
    return this.data.get( 'username' );
  }

  get passwd() 
  {
    return this.data.get( 'passwd' );
  }

  public ngOnInit(): void 
  {
    return;
  }

  public login( $event ): void
  {
    console.log( 'login' );
    this.auth.auth$( this.data.value ).subscribe( result => {
      console.log( 'login response: ', result );
    } );
    return;
  }

  public test( $event ): void
  {
    console.log( 'test' );
    this.auth.test$( this.data.value ).subscribe( result => {
      console.log( 'test response: ', result );
    } );
    return;
  }
}