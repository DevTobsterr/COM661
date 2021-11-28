import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppCreatePostComponent } from './app-create-post.component';

describe('AppCreatePostComponent', () => {
  let component: AppCreatePostComponent;
  let fixture: ComponentFixture<AppCreatePostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AppCreatePostComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppCreatePostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
