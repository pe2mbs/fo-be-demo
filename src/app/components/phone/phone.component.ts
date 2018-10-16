import { Component, ElementRef, OnDestroy, Input } from '@angular/core';
import { MatFormFieldControl } from '@angular/material';
import { coerceBooleanProperty } from '@angular/cdk/coercion';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subject } from 'rxjs';
import { FocusMonitor } from '@angular/cdk/a11y';

/** Data structure for holding telephone number. */
export class PhoneNumber
{
  constructor( public area: string, 
               public exchange: string, 
               public subscriber: string ) 
  {
    return;
  }
}

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'mat-form-field-ex-phone',
  templateUrl: './phone.component.html',
  styleUrls: ['./phone.component.scss'],
  providers: [{provide: MatFormFieldControl, useExisting: MatExPhoneComponent}],
  // tslint:disable-next-line:use-host-property-decorator
  host: {
    '[class.floating]': 'shouldLabelFloat',
    '[id]': 'id',
    '[attr.aria-describedby]': 'describedBy',
  }
})
export class MatExPhoneComponent implements MatFormFieldControl<PhoneNumber>, OnDestroy  {

  static nextId           = 0;
  public areaLength       = 4;
  public exchangeLength   = 2;
  public subscriberLength = 8;
  private _countryCode    = 528;

  parts: FormGroup;
  stateChanges            = new Subject<void>();
  focused                 = false;
  ngControl               = null;
  errorState              = false;
  controlType             = 'mat-form-field-ex-phone';
  id                      = `mat-form-field-ex-phone-${MatExPhoneComponent.nextId++}`;
  describedBy             = '';

  get empty() 
  {
    const {value: {area, exchange, subscriber}} = this.parts;
    return !area && !exchange && !subscriber;
  }

  get shouldLabelFloat() 
  { 
    return this.focused || !this.empty; 
  }

  @Input()
  get placeholder(): string 
  { 
    return this._placeholder; 
  }
  set placeholder( value: string ) 
  {
    this._placeholder = value;
    this.stateChanges.next();
    return;
  }
  private _placeholder: string;

  @Input()
  get required(): boolean 
  { 
    return this._required; 
  }
  set required(value: boolean) {
    this._required = coerceBooleanProperty(value);
    this.stateChanges.next();
    return;
  }
  private _required = false;

  @Input()
  get disabled(): boolean 
  { 
    return this._disabled; 
  }
  set disabled(value: boolean) 
  {
    this._disabled = coerceBooleanProperty(value);
    this.stateChanges.next();
    return;
  }
  private _disabled = false;

  @Input()
  get value(): PhoneNumber | null 
  {
    const { value: { area, exchange, subscriber } } = this.parts;
    if ( area.length === 3 && 
         exchange.length === 3 && 
         subscriber.length === 4 ) 
    {
      return new PhoneNumber( area, exchange, subscriber );
    }
    return null;
  }
  set value( tel: PhoneNumber | null ) 
  {
    const { area, exchange, subscriber } = tel || new PhoneNumber( '', '', '' );
    this.parts.setValue( { area, exchange, subscriber } );
    this.stateChanges.next();
    return;
  }

  constructor( fb: FormBuilder, 
               private fm: FocusMonitor, 
               private elRef: ElementRef<HTMLElement> ) 
  {
    this.parts = fb.group( {
      area:       '',
      exchange:   '',
      subscriber: '',
    } );

    fm.monitor( elRef.nativeElement, true ).subscribe( origin => {
      this.focused = !!origin;
      this.stateChanges.next();
    } );
    return;
  }

  ngOnDestroy() {
    this.stateChanges.complete();
    this.fm.stopMonitoring(this.elRef.nativeElement);
  }

  setDescribedByIds(ids: string[]) {
    this.describedBy = ids.join(' ');
  }

  onContainerClick(event: MouseEvent) {
    if ((event.target as Element).tagName.toLowerCase() !== 'input') 
    {
      // tslint:disable-next-line:no-non-null-assertion
      this.elRef.nativeElement.querySelector( 'input' )!.focus();
    }
  }
}
