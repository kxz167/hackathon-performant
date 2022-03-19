import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-visualize-page',
  templateUrl: './visualize-page.component.html',
  styleUrls: ['./visualize-page.component.scss']
})
export class VisualizePageComponent implements OnInit {

  //Forms:
  posOptForm = this.fb.group({
    pl: [''],
    plp: [''],
    quantity: ['']
  });

  updateGraphSeries(){
    console.warn(this.posOptForm.value);
    let newSeries: any[] = []
    for (let key in this.posOptForm.value){
      if(this.posOptForm.value[key]){
        newSeries.push(this.seriesDict[key]);
      }
    }
    // this.posOptForm.value.forEach((value:any) => {
    //   console.warn(value);
    //   if(value){
    //     newSeries.push()
    //   }
    // });
    this.multi = newSeries;
  }


  visAccount = false;

  constructor(
    private apiService:ApiService,
    private fb : FormBuilder
  ) { }

  stockGData :any;
  pgd_pl : any;
  pgd_plp : any;
  pgd_quantity : any;

  seriesDict :any = {};

  dateParser = (pair:any) => ({
    'name': new Date(pair["name"]), 
    'value': pair['value']
  });

  ngOnInit(): void {
    this.multi = []

    this.apiService.getPositionGraphData().subscribe(
      (response: any) => {
        let all_data = response["graphdata"];
        this.stockGData = response["graphdata"];
        this.pgd_pl = 
        {
          "name": "Profits and Losses",
          "series": all_data[1].map(this.dateParser)
        };
        this.seriesDict["pl"] = this.pgd_pl;


        this.pgd_plp = {
          "name": "Profit loss percentages",
          "series": all_data[2].map(this.dateParser)
        };
        this.seriesDict["plp"] = this.pgd_plp;


        this.pgd_quantity = {
          "name": "Quantity",
          "series": all_data[3].map(this.dateParser)
        };
        this.seriesDict["quantity"] = this.pgd_quantity;

      }
    )
  }

  //CHART STUFF:
  // view: any = [700, 900];

  // options
  legend: boolean = true;
  showLabels: boolean = true;
  animations: boolean = true;
  xAxis: boolean = true;
  yAxis: boolean = true;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Date';
  timeline: boolean = true;

  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };
  schemed = 'forest';

  multi: any;
}
