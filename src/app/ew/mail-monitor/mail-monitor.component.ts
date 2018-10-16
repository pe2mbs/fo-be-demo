import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-mail-monitor',
  templateUrl: './mail-monitor.component.html',
  styleUrls: ['./mail-monitor.component.scss']
})
export class MailMonitorComponent implements OnInit 
{
  messages = [
    { sender: 'Bob van der Moesel',
      subject: 'IP ING RAT',
      logo: 'header-image-ing',
      status: 'Message(s) send',
      numberOfTests: 10,
      message: `The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan.
      A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally
      bred for hunting.`
    },
    { sender: 'Jeroen',
      subject: 'IP RAB RAT',
      logo: 'header-image-rabo',
      status: 'Message(s) send',
      numberOfTests: 1,
      message: ''
    },
    { sender: 'Roaland van der Niet',
      subject: 'IP ABN RAT',
      logo: 'header-image-abnamro',
      status: 'Message(s) send',
      numberOfTests: 2,
      message: ''
    }

  ];
  




  constructor( fb: FormBuilder ) 
  { 
    return;
  }

  ngOnInit() {
  }

}
