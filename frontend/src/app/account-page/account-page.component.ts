import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-account-page',
  templateUrl: './account-page.component.html',
  styleUrls: ['./account-page.component.css']
})
export class AccountPageComponent implements OnInit {

  constructor(
    private apiService: ApiService,
    private fb: FormBuilder
  ) { }
  
  // FORMS:
  fundForm = this.fb.group({
    account: ['', Validators.required],
    amount: ['', Validators.compose([
      Validators.required, 
      Validators.pattern('^-?\\d*(.\\d{1,2})?$')
    ])],
    date: ['', Validators.required]
  });

  accounts: any;

  ngOnInit(): void {
    this.updateAccounts();
  }

  updateAccounts(){
    this.apiService.getAccounts().subscribe(
      (response: any) => {
        console.warn(response);
        this.accounts = response['accounts'];
      }
    );
  }

  onSubmit(){
    console.warn(this.fundForm.value);
    this.apiService.fundAccount(this.fundForm.value).subscribe(
      (response:any) => {
        console.warn(response);
        if(response.status == "good"){
          this.fundForm.reset();
          this.updateAccounts();
        }
      }
    )
  }
}
