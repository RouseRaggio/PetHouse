import { TestBed } from '@angular/core/testing';

import { VeterinarioChat } from './veterinario-chat';

describe('VeterinarioChat', () => {
  let service: VeterinarioChat;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VeterinarioChat);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
