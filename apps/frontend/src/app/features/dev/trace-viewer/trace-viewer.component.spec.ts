import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TraceViewerComponent } from './trace-viewer.component';

describe('TraceViewerComponent', () => {
  let component: TraceViewerComponent;
  let fixture: ComponentFixture<TraceViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TraceViewerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TraceViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
