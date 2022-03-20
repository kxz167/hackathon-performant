import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-summary-page',
  templateUrl: './summary-page.component.html',
  styleUrls: ['./summary-page.component.scss']
})
export class SummaryPageComponent implements OnInit {

  constructor(
    private apiService: ApiService
  ) { }


  summaryValues:any;

  ngOnInit(): void {
    this.apiService.getAccountSummary().subscribe(
      (response: any) => {
        console.warn(response);
        this.summaryValues = response["summary"];
      }
    )
  }

}
