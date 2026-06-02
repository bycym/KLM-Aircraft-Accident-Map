import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import * as L from 'leaflet';

import { AccidentApiService, AccidentPoint, AccidentYearResponse } from './accident-api.service';
import { getRuntimeConfig } from './runtime-config';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  private readonly api = inject(AccidentApiService);
  years: number[] = [];
  selectedYear = 2019;
  response: AccidentYearResponse | null = null;
  loading = false;
  error = '';
  private map?: L.Map;
  private markers = L.layerGroup();
  private readonly tileUrl = getRuntimeConfig().tileUrl;

  ngOnInit(): void {
    this.api.getYears().subscribe({
      next: (response) => {
        console.log(`>>>>>>> years: ${response.years}`)
        this.years = response.years;
      },
      error: () => {
        this.error = 'Unable to load available years.';
      },
    });
    this.loadAccidents();
  }

  loadAccidents(): void {
    this.loading = true;
    this.error = '';

    this.api.getAccidents(this.selectedYear).subscribe({

      next: (response) => {
        this.response = response;
        this.loading = false;

        this.renderMap(response.accidents);
      },

      error: () => {
        this.loading = false;
        this.error = 'Unable to load accident data.';
        this.renderMap([]);
      },
    });
    //this.loading = false;
  }

  onYearChange(): void {
    this.loadAccidents();
  }

  get hasNoMappableData(): boolean {
    return !!this.response && this.response.total_count > 0 && this.response.accidents.length === 0;
  }

  popupText(accident: AccidentPoint): string {
    return [
      accident.event_date,
      accident.location,
      accident.country,
      accident.injury_severity,
      accident.aircraft_category,
      accident.make,
      accident.model,
      accident.investigation_type,
      accident.accident_number,
    ]
      .filter(Boolean)
      .join(' | ');
  }

  private renderMap(accidents: AccidentPoint[]): void {
    if (!this.map) {
      this.map = L.map('map', { center: [20, 0], zoom: 2 });
      L.tileLayer(this.tileUrl, { attribution: '&copy; OpenStreetMap contributors' }).addTo(this.map);
      this.markers.addTo(this.map);
    }
    this.markers.clearLayers();
    if (accidents.length === 0) {
      this.map.setView([20, 0], 2);
      return;
    }
    const bounds = L.latLngBounds([]);
    for (const accident of accidents) {
      const marker = L.marker([accident.latitude, accident.longitude]).bindPopup(this.popupText(accident));
      marker.addTo(this.markers);
      bounds.extend([accident.latitude, accident.longitude]);
    }
    this.map.fitBounds(bounds, { padding: [24, 24], maxZoom: 8 });
  }
}
