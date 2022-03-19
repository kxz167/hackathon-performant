import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-input-page',
  templateUrl: './input-page.component.html',
  styleUrls: ['./input-page.component.scss']
})
export class InputPageComponent implements OnInit {

  constructor(
    private apiService: ApiService,
    private fb: FormBuilder
  ) { }
  
  // FORMS:
  transactionForm = this.fb.group({
    account: ['', Validators.required],
    price: ['', Validators.compose([
      Validators.required, 
      Validators.pattern('^\\d*(.\\d{1,2})?$')
    ])],
    date: ['', Validators.required],
    quantity: ['', Validators.compose([
      Validators.required, 
      Validators.pattern('^-?\\d+$')
    ])],
    ticker: ['', Validators.pattern('^[A-Z]+$')]
  });

  accounts: any;

  ngOnInit(): void {
    this.apiService.getAccounts().subscribe(
      (response: any) => {
        console.warn(response);
        this.accounts = response['accounts'];
      }
    );
  }

  onSubmit(){
    console.warn(this.transactionForm.value);
    this.apiService.makeTransaction(this.transactionForm.value).subscribe(
      (response:any) => {
        console.warn(response);
        if(response.status == "good"){
          this.transactionForm.reset();
        }
      }
    )
  }
}
