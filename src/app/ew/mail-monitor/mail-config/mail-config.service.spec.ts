import { TestBed } from '@angular/core/testing';

import { MailConfigService } from './mail-config.service';

describe('MailConfigService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MailConfigService = TestBed.get(MailConfigService);
    expect(service).toBeTruthy();
  });
});
