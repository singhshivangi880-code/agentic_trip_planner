import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-trace-viewer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="trace-viewer">
      <header class="header">
        <h1>Agent Observability Trace</h1>
        <p *ngIf="traceId">Trace ID: <code>{{ traceId }}</code></p>
      </header>

      <div *ngIf="loading" class="loading">Loading trace...</div>
      <div *ngIf="error" class="error">{{ error }}</div>

      <div class="timeline" *ngIf="traceData">
        <div class="span-card" *ngFor="let span of traceData.spans" [ngClass]="{'error-span': span.is_error}">
          
          <div class="span-header">
            <h3>
              <span class="status-icon">{{ span.is_error ? '❌' : '✅' }}</span>
              {{ span.operation_name }}
            </h3>
            <span class="duration">{{ span.duration_ms | number:'1.0-2' }} ms</span>
          </div>

          <div class="span-details">
            <p *ngIf="span.error_message" class="error-msg"><strong>Error:</strong> {{ span.error_message }}</p>
            
            <div class="tags" *ngIf="span.tags && (span.tags | keyvalue).length">
              <h4>Attributes</h4>
              <ul>
                <li *ngFor="let tag of span.tags | keyvalue">
                  <strong>{{ tag.key }}:</strong> {{ tag.value }}
                </li>
              </ul>
            </div>
            
            <div class="events" *ngIf="span.events && span.events.length">
              <h4>Events</h4>
              <ul>
                <li *ngFor="let event of span.events">
                  <div *ngFor="let field of event.fields | keyvalue">
                    <strong>{{ field.key }}:</strong> {{ field.value }}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .trace-viewer { padding: 2rem; max-width: 1200px; margin: 0 auto; font-family: monospace; }
    .header { margin-bottom: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 1rem; }
    .header h1 { font-family: sans-serif; margin-bottom: 0.5rem; }
    .loading, .error { text-align: center; padding: 2rem; font-size: 1.2rem; }
    .error { color: #d32f2f; }
    
    .timeline { display: flex; flex-direction: column; gap: 1rem; }
    .span-card { 
      border: 1px solid #e2e8f0; 
      border-radius: 8px; 
      padding: 1rem;
      background: #f8fafc;
      border-left: 4px solid #4caf50;
    }
    .span-card.error-span { border-left-color: #ef4444; background: #fef2f2; }
    
    .span-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .span-header h3 { margin: 0; font-size: 1.1rem; }
    .duration { font-weight: bold; background: #e2e8f0; padding: 0.25rem 0.5rem; border-radius: 4px; }
    
    .span-details h4 { margin: 1rem 0 0.5rem 0; font-size: 0.9rem; text-transform: uppercase; color: #64748b; }
    .span-details ul { margin: 0; padding-left: 1rem; }
    .span-details li { margin-bottom: 0.25rem; font-size: 0.9rem; }
    
    .error-msg { color: #b91c1c; font-weight: bold; }
  `]
})
export class TraceViewerComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private http = inject(HttpClient);

  traceId: string | null = null;
  traceData: any = null;
  loading = true;
  error = '';

  ngOnInit() {
    this.traceId = this.route.snapshot.paramMap.get('traceId');
    if (!this.traceId) {
      this.error = 'No trace ID provided.';
      this.loading = false;
      return;
    }

    this.http.get<any>(`/api/v1/dev/traces/${this.traceId}`).subscribe({
      next: (data) => {
        this.traceData = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Failed to load trace. Ensure Jaeger is running.';
        this.loading = false;
      }
    });
  }
}
