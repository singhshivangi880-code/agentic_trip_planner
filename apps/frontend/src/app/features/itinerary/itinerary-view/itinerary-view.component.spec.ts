import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ItineraryViewComponent } from './itinerary-view.component';

describe('ItineraryViewComponent', () => {
  let component: ItineraryViewComponent;
  let fixture: ComponentFixture<ItineraryViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ItineraryViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ItineraryViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should toggle lock status', () => {
    const item = { title: 'Test', item_type: 'Activity', start_time: '10:00', end_time: '11:00', location: 'Here', description: 'Desc', is_locked: false };
    component.onToggleLock(item);
    expect(item.is_locked).toBeTrue();
    component.onToggleLock(item);
    expect(item.is_locked).toBeFalse();
  });

  it('should emit replanRequest on remove', () => {
    spyOn(component.replanRequest, 'emit');
    const item = { title: 'Test', item_type: 'Activity', start_time: '10:00', end_time: '11:00', location: 'Here', description: 'Desc', is_locked: false };
    component.onRemove(1, item);
    expect(component.replanRequest.emit).toHaveBeenCalledWith({
      targetDay: 1,
      instruction: 'Remove Test from the schedule'
    });
  });
});
