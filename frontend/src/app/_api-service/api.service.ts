import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(
    private http: HttpClient
  ) { }

  getAccounts(){
    return  this.http.get(environment.apiUrl + "/account/get-accounts");
  }

  fundAccount(data:any){
    return this.http.post(environment.apiUrl + "/account/fund-account", data);
  }

  getTransactions(){
    return this.http.get(environment.apiUrl + "/position/get-transactions");
  }

  makeTransaction(data:any){
    return this.http.post(environment.apiUrl + "/position/make-transaction", data);
  }

  getPositionGraphData(ticker:any){
    return this.http.get(environment.apiUrl + "/position/graph-data", ticker)
  }

  getPositionTicks(){
    return this.http.get(environment.apiUrl + "/position/ticks")
  }
}
