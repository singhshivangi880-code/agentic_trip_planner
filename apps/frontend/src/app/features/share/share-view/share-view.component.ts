import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ItineraryViewComponent } from '../../itinerary/itinerary-view/itinerary-view.component';
import { Itinerary } from '../../../core/models/itinerary.model';

@Component({
  selector: 'app-share-view',
  standalone: true,
  imports: [CommonModule, ItineraryViewComponent],
  template: `
    <div class="share-page">
      <header class="share-header">
        <h1>Trip Planner</h1>
        <p>You've been invited to view an itinerary!</p>
      </header>

      <div *ngIf="loading" class="loading-state">
        <p>Loading itinerary...</p>
      </div>
      
      <div *ngIf="error" class="error-state">
        <p>❌ {{ error }}</p>
      </div>

      <app-itinerary-view 
        *ngIf="itinerary" 
        [itinerary]="itinerary" 
        [readonly]="true">
      </app-itinerary-view>
    </div>
  `,
  styles: [`
    .share-page {
      min-height: 100vh;
      background: #f8fafc;
      padding-bottom: 3rem;
    }
    .share-header {
      background: #0288d1;
      color: white;
      padding: 2rem 1rem;
      text-align: center;
      margin-bottom: 2rem;
    }
    .share-header h1 { margin: 0 0 0.5rem 0; }
    .share-header p { margin: 0; opacity: 0.9; }
    .loading-state, .error-state {
      text-align: center;
      padding: 3rem;
      font-size: 1.2rem;
    }
    .error-state { color: #d32f2f; }
  `]
})
export class ShareViewComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private http = inject(HttpClient);
  
  itinerary: Itinerary | null = null;
  loading = true;
  error = '';

  ngOnInit() {
    const token = this.route.snapshot.paramMap.get('token');
    if (!token) {
      this.error = 'No share token provided.';
      this.loading = false;
      return;
    }

    this.http.get<any>(`/api/v1/share/${token}`).subscribe({
      next: (data) => {
        this.itinerary = data;
        this.loading = false;
      },
      error: (err) => {
        if (err.status === 404) this.error = 'This share link is invalid or has been revoked.';
        else if (err.status === 410) this.error = 'This share link has expired.';
        else this.error = 'Failed to load itinerary. Please try again later.';
        this.loading = false;
      }
    });
  }
}
