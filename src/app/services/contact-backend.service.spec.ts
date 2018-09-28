import { TestBed } from '@angular/core/testing';

import { ContactBackendService } from './contact-backend.service';

describe('ContactBackendService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ContactBackendService = TestBed.get(ContactBackendService);
    expect(service).toBeTruthy();
  });
});
