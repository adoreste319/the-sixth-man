import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(
    private http: HttpClient
  ) { }

  getPlayers(): Promise<any> {
    let url = environment.apiUrl + 'players'
    return this.http.get(url).toPromise();
  }

  getInput(data): Promise<any> {
    let url = environment.apiUrl + 'inputs'
    return this.http.post(url, data).toPromise();
  }

  simulatePick(): Promise<any> {
    let url = environment.apiUrl + 'draft'
    return this.http.get(url).toPromise();
  }

  pickPlayer(data): Promise<any> {
    let url = environment.apiUrl + 'draft'
    return this.http.post(url, data).toPromise();
  }

  getTeams(): Promise<any> {
    let url = environment.apiUrl + 'teams'
    return this.http.get(url).toPromise();
  }
}
