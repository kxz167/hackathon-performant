import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_api-service/api.service';

@Component({
  selector: 'app-visualize-page',
  templateUrl: './visualize-page.component.html',
  styleUrls: ['./visualize-page.component.scss']
})
export class VisualizePageComponent implements OnInit {

  visAccount = false;

  constructor(
    private apiService:ApiService
  ) { }

  stockGData :any;
  pgd_pl : any;
  pgd_plp : any;
  pgd_quantity : any;

  ngOnInit(): void {
    this.apiService.getPositionGraphData().subscribe(
      (response: any) => {
        let all_data = response["graphdata"];
        this.pgd_pl = all_data[1];
        this.pgd_plp = all_data[2];
        this.pgd_quantity = all_data[3]
        this.stockGData = response["graphdata"];

        this.multi = [
          {
            "name": "Profits and Losses",
            "series": this.pgd_pl
          },
          {
            "name": "Profit loss percentages",
            "series": this.pgd_plp
          },
          {
            "name": "Quantity",
            "series": this.pgd_quantity
          }
        ]
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
  showYAxisLabel: boolean = true;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Year';
  yAxisLabel: string = 'Population';
  timeline: boolean = true;

  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };
  schemed = 'forest';

  multi: any;
}
