import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UsPhoneComponent } from './us-phone.component';

describe('UsPhoneComponent', () => {
  let component: UsPhoneComponent;
  let fixture: ComponentFixture<UsPhoneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UsPhoneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UsPhoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
