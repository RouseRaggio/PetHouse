import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Petcard } from './pet-card';

describe('Petcard', () => {
  let component: Petcard;
  let fixture: ComponentFixture<Petcard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Petcard],
    }).compileComponents();

    fixture = TestBed.createComponent(Petcard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
