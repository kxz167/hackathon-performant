import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AccountPageComponent } from './account-page/account-page.component';
import { SummaryPageComponent } from './summary-page/summary-page.component';
import { VisualizePageComponent } from './visualize-page/visualize-page.component';
import { HistoryPageComponent } from './history-page/history-page.component';
import { InputPageComponent } from './input-page/input-page.component';
import { HttpClientModule } from '@angular/common/http'
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    AccountPageComponent,
    SummaryPageComponent,
    VisualizePageComponent,
    HistoryPageComponent,
    InputPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
