import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-history-page',
  templateUrl: './history-page.component.html',
  styleUrls: ['./history-page.component.css']
})
export class HistoryPageComponent implements OnInit {
  
  constructor(
    private apiService: ApiService,
    private fb: FormBuilder
  ) { }

  transactions: any;

  ngOnInit(): void {
    this.apiService.getTransactions().subscribe(
      (response: any) => {
        console.warn(response);
        this.transactions = response['transactions'];
      }
    );
  }

}
