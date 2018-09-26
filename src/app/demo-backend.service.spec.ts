import { TestBed } from '@angular/core/testing';

import { DemoBackendService } from './demo-backend.service';

describe('DemoBackendService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DemoBackendService = TestBed.get(DemoBackendService);
    expect(service).toBeTruthy();
  });
});
