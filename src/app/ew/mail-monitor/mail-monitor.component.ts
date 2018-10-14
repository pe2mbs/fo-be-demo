import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-mail-monitor',
  templateUrl: './mail-monitor.component.html',
  styleUrls: ['./mail-monitor.component.scss']
})
export class MailMonitorComponent implements OnInit {
  test: FormGroup;

  constructor( fb: FormBuilder ) 
  { 
    this.test = fb.group( {
      'oldPassword': [ 'test' ],
      'newPassword': [ 'tset' ],
      'retypePassword': [ 'tset' ]
    } );
  }

  ngOnInit() {
  }

}
