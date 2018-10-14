import { Component, OnInit, Input, OnDestroy, ElementRef, HostBinding, Optional, Self } from '@angular/core';
import { FormBuilder, FormGroup, NgControl, Validators, AbstractControl } from '@angular/forms';
import { Subject } from 'rxjs';
import { MatFormFieldControl } from '@angular/material';
import { FocusMonitor } from '@angular/cdk/a11y';
import { coerceBooleanProperty } from '@angular/cdk/coercion';


@Component({
  // tslint:disable-next-line:component-selector
  selector: 'mat-ex-password',
  templateUrl: './password.component.html',
  styleUrls: ['./password.component.scss'],
  providers: [ { provide: MatFormFieldControl, 
                 useExisting: PasswordComponent } ],
  // tslint:disable-next-line:use-host-property-decorator
  host: {
    '[class.floating]':         'shouldLabelFloat',
    '[id]':                     'id',
    '[attr.aria-describedby]':  'describedBy',
  }                 
})
export class PasswordComponent implements MatFormFieldControl<string>, OnInit, OnDestroy {
  static nextId = 0;

  private _placeholder: string;
  private _required = false;
  private _disabled = false;
  public _width = '100%';
  public _padding_left = '0';
  public _padding_right = '0';
  public hint_text = 'Enter your password';
  public errorState = false;
  public controlType = 'app-password';
  public parts: FormGroup;
  public hide  = true;
  public focused = false;
  public stateChanges = new Subject<void>();

  @HostBinding() id = `app-password-${PasswordComponent.nextId++}`;

  @HostBinding( 'attr.aria-describedby' ) describedBy = '';
  setDescribedByIds( ids: string[] ): void
  {
    this.describedBy = ids.join(' ');
    return;
  }

  @HostBinding('class.floating')
  get shouldLabelFloat() 
  {
    return this.focused || !this.empty;
  }

  public onChange: any = () => { };
  public onTouched: any = () => { };

  @Input()
  get exStyle(): string
  {
    let _exStyle = this._width + ',' + this._padding_left + ',' + this._padding_right; 
    console.log( 'get exStyle = ', _exStyle );
    return _exStyle;
  }
  set exStyle( value: string )
  {
    let parts: Array<string> = value.split(',');
    console.log( 'set exStyle = ', value, parts.length, parts );
    if ( parts.length > 0 )
    {
      this._width = parts[ 0 ];
    }
    else
    {
      this._width = '100%';
    }
    if ( parts.length > 1 )
    {
      this._padding_left = parts[ 1 ];
    }
    else
    {
      this._padding_left = '0';
    }
    if ( parts.length > 2 )
    {
      this._padding_right = parts[ 2 ];
    }
    else
    {
      this._padding_right = '0';
    }
    console.log( 'set exStyle = ', this._width + ',' + 
                                   this._padding_left + ',' + 
                                   this._padding_right );
    return;
  }
  
  @Input()
  get placeholder() 
  {
    return this._placeholder;
  }
  set placeholder(plh) 
  {
    this._placeholder = plh;
    this.stateChanges.next();
  }

  @Input()
  get hint() 
  {
    return this.hint_text;
  }
  set hint(_hint: string ) 
  {
    this.hint_text = _hint;
    this.stateChanges.next();
  }

  @Input()
  get required() 
  {
    return this._required;
  }
  set required(req) 
  {
    this._required = coerceBooleanProperty( req );
    this.stateChanges.next();
  }
  
  @Input()
  get disabled() 
  {
    return this._disabled;
  }

  set disabled(dis) 
  {
    this._disabled = coerceBooleanProperty(dis);
    this.stateChanges.next();
  }


  @Input()
  get value(): string  
  {
    let AC = this.parts.get( 'password' );
    return ( AC.value );
  }
  set value( passwd: string ) 
  {
    this.parts.get( 'password' ).setValue( passwd );
  }

  constructor( fb: FormBuilder, 
                private fm: FocusMonitor, 
                private elRef: ElementRef<HTMLElement>,
                @Optional() @Self() public ngControl: NgControl ) 
  { 
    this.parts =  fb.group( {
      'password': [ '', [ Validators.required ] ]
    } );
    // Setting the value accessor directly (instead of using
    // the providers) to avoid running into a circular import.
    if ( this.ngControl != null ) 
    { 
      this.ngControl.valueAccessor = this; 
    }
    fm.monitor( elRef.nativeElement, true ).subscribe( origin => {
      this.focused = !!origin;
      this.stateChanges.next();
    } );
  }

  get password(): AbstractControl
  {
    return this.parts.get( 'password' );
  }

  public ngOnInit(): void
  {
    return;
  }
  
  public ngOnDestroy(): void
  {
    this.stateChanges.complete();
    this.fm.stopMonitoring( this.elRef.nativeElement );
    return;
  }

  public writeValue( value: string ): void 
  {
    if ( value )
    {
      this.parts.get( 'password' ).setValue( value );
    }
    return;
  }

  registerOnChange(fn) 
  {
    this.onChange = fn;
  }

  registerOnTouched(fn) 
  { 
    this.onTouched = fn;
  }

  get empty(): boolean
  {
    const {value: {password}} = this.parts;

    return !password;
  }

  public onContainerClick(event: MouseEvent): void 
  {
    if ( ( event.target as Element).tagName.toLowerCase() !== 'input' ) 
    {
      this.elRef.nativeElement.querySelector('input').focus();
    }
    return;
  } 
}
