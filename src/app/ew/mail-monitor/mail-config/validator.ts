import { AsyncValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { MailConfigService } from './mail-config.service';
import { Observable, throwError } from 'rxjs';
import { map, tap, retry, catchError } from 'rxjs/operators';
import { HttpErrorResponse } from '@angular/common/http';

export class MissingParameterError extends Error {
    constructor(m: string) {
        super( m );

        // Set the prototype explicitly.
        Object.setPrototypeOf( this, MissingParameterError.prototype );
    }
}

function zip1(arrays) 
{
    return arrays[0].map( function( _, i )
    {
        return arrays.map( function( array ){ return array[ i ]; } );
    } );
}

function zip( arrays ) 
{
    return Array.apply( null, Array( arrays[ 0 ].length ) ).map( function( _, i ) {
        return arrays.map( function( array ){ return array[ i ]; } ); 
    } );
}

/*
*   Helper function: Clears a specific error from the form Input control
* 
*   @Param control:    Is the form Input control of Angular Material 
*   @Param errorName:  The error name to be removed.
*/ 
export function abstractControlRemoveError( control: AbstractControl, errorName: string ): void
{
    if ( control.hasError( errorName ) )
    {
        delete control.errors[ errorName ];
        let obj = control.errors;
        if ( obj.length === 0 )
        {
            control.setErrors( null );
        }
    }
    return;
}

/*
*   Helper function: Sets manually a error to the form Input control
* 
*   @param control:     Is the form Input control of Angular Material
*   @param whatToSet:   Is the error object to be set 
*/ 
export function abstractControlAppendError( control: AbstractControl, whatToSet: object ): void
{
    let errors = control.errors;
    const allRules = Object.assign( {}, errors, whatToSet );
    control.setErrors( allRules );
    return;
}


export class MailMonitor 
{
    static __timerId: any = null;

    static proxyAutoConfigValidator(userService: MailConfigService): AsyncValidatorFn 
    {
        return (control: AbstractControl): Promise<ValidationErrors | null> | Observable<ValidationErrors | null> => 
        {
            return userService.validateProxyService$( control.value ).pipe( 
                retry( 3 ),
                tap( data => console.log( 'validateProxyValidator Received: ', data ),
                     error => 
                {
                    console.log( 'Houston we have a problem: ', error );
                    console.error( error );
                } ),
                catchError( (err: HttpErrorResponse) => 
                {
                    console.error( err );
                    console.log( 'catchError ', err );
                    return throwError( err.error );
                } ),
                map( result => 
                {
      
                    return ( ( result && !result.result ) ? 
                               { 'proxyError' : true, 
                               'proxyMessage': result.message } : 
                               null );
                } ) 
            );
        };
    }
      
    static exchangeServerValidator( userService: MailConfigService ): AsyncValidatorFn 
    {
        return (control: AbstractControl): Promise<ValidationErrors | null> | Observable<ValidationErrors | null> =>
        {
            return userService.validateExchangeServer$( control.value ).pipe( 
                retry( 3 ),
                tap( data => console.log( 'validateExchangeServer Received: ', data ),
                     error => 
                {
                    console.log( 'Houston we have a problem: ', error );
                    console.error( error );
                } ),
                catchError( (err: HttpErrorResponse) => 
                {
                    console.error( err );
                    console.log( 'catchError ', err );
                    return throwError( err.error );
                } ),
                map( result => 
                {
                    return ( ( result && !result.result ) ? 
                               { 'exchangeError' : true,
                                 'exchangeMessage': result.message } : 
                               null );
                }
            ) 
            );
        };
    }
    
    static accountValidator( field_names: Array<string>,
                             userService: MailConfigService): AsyncValidatorFn 
    {
        return (AC: AbstractControl): Promise<ValidationErrors | null> | 
                                      Observable<ValidationErrors | null> =>
        {
            let fields: Array<AbstractControl> = new Array;
            let passwdFields: Array<AbstractControl> = new Array;
            field_names.forEach( field_name => {
                if ( field_name.toUpperCase().indexOf( 'PASSW' ) >= 0 )
                {
                    passwdFields.push( AC.get( field_name ) );
                }
                fields.push( AC.get( field_name ) );  
            } );
            console.log( 'passwdFields.length', passwdFields.length );
            if ( passwdFields.length !== 2 )
            {
                throw new MissingParameterError( 'There must be two password fields' );
            }
            if ( passwdFields[ 0 ].value === passwdFields[ 1 ].value )
            {
                let obj: object = {};
                zip( [ field_names, fields ] ).forEach( data => {
                    abstractControlRemoveError( data[ 1 ], 'passwordDontMatch' );
                    obj[ data[ 0 ] ] = data[ 1 ].value;
                } );
                // Passswords are equal, setup the Observer to the backend
                return userService.checkUserPassword$( obj );
            }
            fields.forEach( field => {
                abstractControlAppendError( field, { passwordDontMatch: true } );
            } );
            return new Observable( observer => {
                observer.next( { passwordDontMatch: true } );
                observer.complete();
            } );
        };
    }

    static __timerFunction( AC: AbstractControl ): void
    {
        // Has some loser forgot to set the AbstractControl ? 
        if ( AC == null )
        {
            throw new MissingParameterError( 'Missing the AbstractControl' );
        }
        let storageUsername = AC.get( 'storageUsername' );
        let storagePassword = AC.get( 'storagePassword' );          
        if ( storageUsername.value !== 'testUser' ||
                storagePassword.value !== 'abcd1234' ) 
        {
            console.log( 'false' );
            abstractControlAppendError( storageUsername, 
                                        { invalidUserOrPassword: true } );
            abstractControlAppendError( storagePassword, 
                                        { invalidUserOrPassword: true } );
        }
        else
        {
            abstractControlRemoveError( storageUsername, 'invalidUserOrPassword' );
            abstractControlRemoveError( storagePassword, 'invalidUserOrPassword' );
        }
        return;
    }

    static testStorageUserPassword( AC: AbstractControl ): void
    {
        let protocol = AC.get( 'storageProtocol' ).value;
        if ( [ 'https', 'ftps' ].indexOf( protocol ) >= 0 )
        {
            // Check if there is any data to care about
            if ( AC.get( 'storageUsername' ).value.length === 0 || 
                 AC.get( 'storagePassword' ).value.length === 0 )
            {
                if ( MailMonitor.__timerId !== null )
                {
                    clearTimeout( MailMonitor.__timerId );
                    MailMonitor.__timerId = null;
                }
                return;
            }
            // Is the timer running ?
            if ( MailMonitor.__timerId != null )
            {
                clearTimeout( MailMonitor.__timerId );
            }
            // (re-)Start the timer and inject the AbstractControl.
            MailMonitor.__timerId = setTimeout( 
                MailMonitor.__timerFunction.bind(null, AC), 2000 );
        }
        else if ( MailMonitor.__timerId !== null )
        {
            clearTimeout( MailMonitor.__timerId );
            MailMonitor.__timerId = null;
        }
        return;        
    }
}
