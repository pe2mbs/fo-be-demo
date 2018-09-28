import { TestBed } from '@angular/core/testing';

import { CrudBackendService } from './crud-backend.service';

interface Dummy
{
  id?: number;
}

describe('CrudBackendService<Dummy>', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CrudBackendService<Dummy> = TestBed.get( CrudBackendService );
    expect(service).toBeTruthy();
  });
});
