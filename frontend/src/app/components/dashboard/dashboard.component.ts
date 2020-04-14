import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Player, Players } from '../../models/dashhboard';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  players: Players = new Players();
  homeActive: boolean = true;
  resultsActive: boolean = false;
  myDraftActive: boolean = false;
  draftSheetActive: boolean = false;
  userActive: boolean = false;

  constructor(
    private dashboardService: DashboardService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    console.log("Loading page...");
    this.dashboardService.getPlayers().then(res => {
      console.log(res);
      this.players = res;
    });
  }

  getActive(value: string) {
    if (value === 'mydraft') {
      return this.myDraftActive ? 'navbar-active' : '';
    } else if (value === 'draftsheet') {
      return this.draftSheetActive ? 'navbar-active' : '';
    } else if (value === 'results') {
      return this.resultsActive ? 'navbar-active' : '';
    }
  }

  setActive(value: string) {
    if (value === 'mydraft') {
      this.myDraftActive = true;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.userActive = false;
    } else if (value === 'draftsheet') {
      this.draftSheetActive = true;
      this.myDraftActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.userActive = false;
    } else if (value === 'results') {
      this.resultsActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.homeActive = false;
      this.userActive = false;
    } else if (value === 'home') {
      this.homeActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.userActive = false;
    } else if (value === 'user') {
      this.userActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.homeActive = false;
    }
  }

}
