import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { MailConfigService, CheckProxyResult } from './mail-config.service';
import { map } from 'rxjs/operators';
import { MailMonitor } from './validator';
import { environment } from '../../../../environments/environment.dev';

@Component({
  selector: 'app-mail-config',
  templateUrl: './mail-config.component.html',
  styleUrls: ['./mail-config.component.scss']
})
export class MailConfigComponent implements OnInit {
  parts: FormGroup;
  hideDas1 = true;
  hideDas2 = true;
  hideStorage1 = true;
  hideStorage2 = true;
  proxyOke  = false;
  protocols = [ { value: 'local', name: 'LOCAL' },
                { value: 'share', name: 'SHARE' },
                { value: 'nfs',   name: 'NFS'   },
                { value: 'ftps',  name: 'FTPS'  },
                { value: 'https', name: 'HTTPS' } ];

  constructor( public fb: FormBuilder, 
               private mailConfigService: MailConfigService ) 
  { 
    this.parts =  fb.group( {
      'active':           [ false ],
      'pacFile':          [ '',
                            [ Validators.required ],
                            MailMonitor.proxyAutoConfigValidator( this.mailConfigService ) ],
      'webmailServer':    [ '',
                            [ Validators.required ],
                            MailMonitor.exchangeServerValidator( this.mailConfigService ) ],
      'dasId':            [ '',
                            [ Validators.required, Validators.minLength( 6 ) ] ],
      'dasPassword1':     [ '',
                            [ Validators.required ] ],
      'dasPassword2':     [ '',
                            [ Validators.required ] ],
      'storageLocation':  [ '',
                            [ Validators.required ] ],
      'storageProtocol':  [ 'share' ],
      'storageUsername':  [ '' ],
      'storagePassword1': [ '' ],
      'storagePassword2': [ '' ]
    }, {
      validator: [ MailMonitor.accountValidator( [ 'dasId', 'dasPassword1', 'dasPassword2' ], 
                                                  this.mailConfigService ),
                   MailMonitor.accountValidator( [ 'storageUsername', 'storagePassword1', 'storagePassword2' ], 
                                                  this.mailConfigService ) ]
    } );
  }

  public ngOnInit(): void
  {
    this.mailConfigService.getMailConfig$().subscribe( data => {
      this.parts.get('active').setValue( data.active );
      this.parts.get('pacFile').setValue( data.pacFile );
      this.parts.get('webmailServer').setValue( data.webmailServer );
      this.parts.get('dasId').setValue( data.dasId );
      this.parts.get('dasPassword1').setValue( data.dasPassword );
      this.parts.get('dasPassword2').setValue( data.dasPassword );
      this.parts.get('storageLocation').setValue( data.storageLocation );
      this.parts.get('storageProtocol').setValue( data.storageProtocol );
      this.parts.get('storageUsername').setValue( data.storageUsername );
      this.parts.get('storagePassword1').setValue( data.storagePassword );
      this.parts.get('storagePassword2').setValue( data.storagePassword );
    } );
    return;
  }

  public needStorageUser()
  {
    return ( [ 'ftps', 'https' ].indexOf( this.storageProtocol.value ) >= 0 );
  }

  get storageUsername() 
  {
    return this.parts.get('storageUsername');
  }

  get storagePassword1() 
  {
    return this.parts.get('storagePassword1');
  }

  get storagePassword2() 
  {
    return this.parts.get('storagePassword2');
  }

  get storageProtocol() 
  {
    return this.parts.get('storageProtocol');
  }

  get pacFile() 
  {
    return this.parts.get('pacFile');
  }

  get active() 
  {
    return this.parts.get('active');
  }

  get webmailServer() 
  {
    return this.parts.get('webmailServer');
  }

  get dasId() 
  {
    return this.parts.get('dasId');
  }

  get dasPassword1() 
  {
    return this.parts.get('dasPassword1');
  }

  get dasPassword2() 
  {
    return this.parts.get('dasPassword2');
  }

  get storageLocation() 
  {
    return this.parts.get('storageLocation');
  }

  public update( $event ): void
  {
    console.log( this.parts );

    this.mailConfigService.updateMailConfig$(
      this.active.value,
      this.pacFile.value,
      this.webmailServer.value,
      this.dasId.value,
      this.dasPassword1.value,
      this.storageLocation.value
    ).subscribe( result => {
      console.log( result );
    } );
  }  
}
