import { Injectable, NgZone } from '@angular/core';
import { Subject, Observable } from 'rxjs';

export interface WorkflowEvent {
  type: 'agent_started' | 'agent_completed' | 'agent_failed' | 'checkpoint_required' | 'workflow_completed';
  agent_name?: string;
  message: string;
  data?: any;
  itinerary?: any;
}

@Injectable({
  providedIn: 'root'
})
export class WorkflowSseService {
  private eventSource: EventSource | null = null;
  private eventSubject = new Subject<WorkflowEvent>();
  
  constructor(private zone: NgZone) {}

  connect(tripId: string, force: boolean = false): Observable<WorkflowEvent> {
    this.disconnect();
    
    const url = force 
      ? `/api/v1/trips/${tripId}/workflow/stream?force=true`
      : `/api/v1/trips/${tripId}/workflow/stream`;
    this.eventSource = new EventSource(url);

    this.eventSource.onmessage = (event) => {
      this.zone.run(() => {
        try {
          const data: WorkflowEvent = JSON.parse(event.data);
          this.eventSubject.next(data);
        } catch (e) {
          console.error('Error parsing SSE data', e);
        }
      });
    };

    this.eventSource.onerror = (error) => {
      this.zone.run(() => {
        console.error('SSE Error:', error);
      });
    };

    return this.eventSubject.asObservable();
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
