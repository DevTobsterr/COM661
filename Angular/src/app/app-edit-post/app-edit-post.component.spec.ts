import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppEditPostComponent } from './app-edit-post.component';

describe('AppEditPostComponent', () => {
  let component: AppEditPostComponent;
  let fixture: ComponentFixture<AppEditPostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AppEditPostComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppEditPostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
