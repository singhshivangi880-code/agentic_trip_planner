import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Itinerary, TripDay, ItineraryItem } from '../../../core/models/itinerary.model';

@Component({
  selector: 'app-itinerary-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './itinerary-view.component.html',
  styleUrls: ['./itinerary-view.component.css']
})
export class ItineraryViewComponent {
  @Input() itinerary: Itinerary | null = null;
  @Input() readonly: boolean = false;
  @Output() replanRequest = new EventEmitter<{targetDay: number, instruction: string}>();
  @Output() undoRequest = new EventEmitter<void>();

  onRemove(dayIndex: number, item: ItineraryItem) {
    this.replanRequest.emit({
      targetDay: dayIndex,
      instruction: `Remove ${item.title} from the schedule`
    });
  }

  onReplace(dayIndex: number, item: ItineraryItem) {
    this.replanRequest.emit({
      targetDay: dayIndex,
      instruction: `Replace ${item.title} with something else in the same area`
    });
  }

  onToggleLock(item: ItineraryItem) {
    item.is_locked = !item.is_locked;
  }
}
