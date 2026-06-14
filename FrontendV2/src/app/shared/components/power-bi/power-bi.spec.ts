import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PowerBi } from './power-bi';

describe('PowerBi', () => {
  let component: PowerBi;
  let fixture: ComponentFixture<PowerBi>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PowerBi],
    }).compileComponents();

    fixture = TestBed.createComponent(PowerBi);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
