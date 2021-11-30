import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppEditCommentComponent } from './app-edit-comment.component';

describe('AppEditCommentComponent', () => {
  let component: AppEditCommentComponent;
  let fixture: ComponentFixture<AppEditCommentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AppEditCommentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppEditCommentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
