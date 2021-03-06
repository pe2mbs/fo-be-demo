import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MatExPasswordComponent } from './password.component';

describe('MatExPasswordComponent', () => {
  let component: MatExPasswordComponent;
  let fixture: ComponentFixture<MatExPasswordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MatExPasswordComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MatExPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
