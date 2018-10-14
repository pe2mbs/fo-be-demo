/*
* Python and Flask serving Angular
* Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HashLocationStrategy, LocationStrategy } from '@angular/common';

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule, MatCheckboxModule, MatInputModule, MatCardModule, MatSlideToggleModule } from '@angular/material';

import { AppComponent } from './app.component';
import { PagerService } from './services/pager.service';
import { ContactBackendService } from './services/contact-backend.service';
import { PaginationComponent } from './pagination/pagination.component';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TableSelectionExampleComponent } from './example/table-selection-example/table-selection-example.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSortModule } from '@angular/material';
import { RouterModule, Routes } from '@angular/router';
import { APP_BASE_HREF } from '@angular/common';
import { AuthInterceptorService } from './services/auth-interceptor.service';
import { MailMonitorComponent } from './ew/mail-monitor/mail-monitor.component';
import { MailConfigComponent } from './ew/mail-monitor/mail-config/mail-config.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MailConfigService } from './ew/mail-monitor/mail-config/mail-config.service';
import { PasswordComponent } from './components/password/password.component';
import { UsPhoneComponent } from './components/us-phone/us-phone.component';

const appRoutes: Routes = [
  { path: 'example-table', component: TableSelectionExampleComponent },
  { path: 'mail-monitor', component: MailMonitorComponent },
  { path: 'mail-config', component: MailConfigComponent },
  { path: '**', redirectTo: '/' }
];

@NgModule({
  declarations: [
    AppComponent,
    TableSelectionExampleComponent,
    MailMonitorComponent,
    MailConfigComponent,
    PasswordComponent,
    UsPhoneComponent,
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatCheckboxModule,
    MatTableModule,
    MatInputModule,
    MatIconModule,
    MatCardModule,
    MatToolbarModule,
    MatSelectModule,
    MatSortModule,
    MatSlideToggleModule,
    MatProgressSpinnerModule,
    MatPaginatorModule
  ],
  providers: [ { provide: APP_BASE_HREF, useValue : '/' },
               { provide: LocationStrategy, useClass: HashLocationStrategy },
               { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true },
               MailConfigService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
