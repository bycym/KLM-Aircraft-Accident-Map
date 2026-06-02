import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

import { AccidentApiService } from './accident-api.service';
import { AppComponent } from './app.component';

class FakeApi {
  years = [2018, 2019];
  accidentsResponse = { year: 2019, total_count: 1, unmapped_count: 0, accidents: [] };
  getYears() {
    return of({ years: this.years });
  }
  getAccidents(year: number) {
    return of({ ...this.accidentsResponse, year });
  }
}

interface RenderMapHost {
  renderMap(accidents: unknown[]): void;
}

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let component: AppComponent;
  let api: FakeApi;

  beforeEach(async () => {
    api = new FakeApi();
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [{ provide: AccidentApiService, useValue: api }],
    }).compileComponents();
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    spyOn(component as unknown as RenderMapHost, 'renderMap');
  });

  it('uses backend years in the dropdown', () => {
    fixture.detectChanges();

    expect(component.years).toEqual([2018, 2019]);
  });

  it('reloads accidents when the selected year changes', () => {
    const getAccidents = spyOn(api, 'getAccidents').and.callThrough();
    component.selectedYear = 2018;

    component.onYearChange();

    expect(getAccidents).toHaveBeenCalledWith(2018);
  });
});
