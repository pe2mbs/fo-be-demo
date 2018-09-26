import { Component, OnInit } from '@angular/core';
import { DemoBackendService } from './demo-backend.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements  OnInit {
  title = 'fo-be-test';
  private  contacts:  Array<object> = [];

  constructor( private  apiService:  DemoBackendService )
  {
    return;
  }

  ngOnInit()
  {
    console.log( 'get contacts' );
    this.getRecords();
  }

  getRecords()
  {
    this.apiService.getContacts().subscribe((data:  Array<object>) => {
      this.contacts  =  data;
    } );
  }

  addRecord()
  {
    this.apiService.add();
  }

  delRecord()
  {
    this.apiService.delete();
  }

  editRecord()
  {
    this.apiService.edit();
  }

  patchRecord()
  {
    this.apiService.patch();
  }
}
