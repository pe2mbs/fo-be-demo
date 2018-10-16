import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MatExPhoneComponent } from './phone.component';

describe('MatExPhoneComponent', () => {
  let component: MatExPhoneComponent;
  let fixture: ComponentFixture<MatExPhoneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MatExPhoneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MatExPhoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
