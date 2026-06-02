import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { getRuntimeConfig } from './runtime-config';


export interface AccidentPoint {
  event_id: string;
  latitude: number;
  longitude: number;
  event_date: string;
  location: string;
  country: string;
  injury_severity: string;
  aircraft_category: string;
  make: string;
  model: string;
  investigation_type: string;
  accident_number: string;
}

export interface YearsResponse {
  years: number[];
}

export interface AccidentYearResponse {
  year: number;
  total_count: number;
  unmapped_count: number;
  accidents: AccidentPoint[];
}

@Injectable({ providedIn: 'root' })
export class AccidentApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = getRuntimeConfig().apiBaseUrl.replace(/\/$/, '');

  getYears(): Observable<YearsResponse> {
    return this.http.get<YearsResponse>(`${this.apiBaseUrl}/years`);
  }

  getAccidents(year: number): Observable<AccidentYearResponse> {
    return this.http.get<AccidentYearResponse>(`${this.apiBaseUrl}/accidents?year=${year}`);
  }
}
