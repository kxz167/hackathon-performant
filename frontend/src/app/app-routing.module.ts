import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccountPageComponent } from './account-page/account-page.component';
import { HistoryPageComponent } from './history-page/history-page.component';
import { InputPageComponent } from './input-page/input-page.component';
import { SummaryPageComponent } from './summary-page/summary-page.component';
import { VisualizePageComponent } from './visualize-page/visualize-page.component';

const routes: Routes = [
  {
    path: 'visualize',
    component: VisualizePageComponent
  },
  {
    path: 'history',
    component: HistoryPageComponent
  },
  {
    path: 'input',
    component: InputPageComponent
  },
  {
    path: 'account',
    component: AccountPageComponent,
  },
  {
    path: '',
    component: SummaryPageComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
