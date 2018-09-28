import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { PagerService } from './services/pager.service';
import { ContactBackendService } from './services/contact-backend.service';
import { PaginationComponent } from './pagination/pagination.component';

@NgModule({
  declarations: [
    AppComponent,
    PaginationComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [ PagerService,
               ContactBackendService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
