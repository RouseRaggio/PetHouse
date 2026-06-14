import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PetModal } from './pet-modal';

describe('PetModal', () => {
  let component: PetModal;
  let fixture: ComponentFixture<PetModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PetModal],
    }).compileComponents();

    fixture = TestBed.createComponent(PetModal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
