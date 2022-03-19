import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-account-page',
  templateUrl: './account-page.component.html',
  styleUrls: ['./account-page.component.css']
})
export class AccountPageComponent implements OnInit {

  constructor(
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.apiService.getAccounts().subscribe(
      response => {
        console.warn(response);
      }
    );
  }

}