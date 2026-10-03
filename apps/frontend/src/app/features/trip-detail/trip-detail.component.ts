import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-trip-detail',
  standalone: true,
  template: `
    <div class="card" style="margin-top: 2rem;">
      <h2>Trip Details</h2>
      <p style="color: #94a3b8;">Trip ID: {{ tripId }}</p>
    </div>
  `,
})
export class TripDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  tripId: string | null = null;

  ngOnInit(): void {
    this.tripId = this.route.snapshot.paramMap.get('tripId');
  }
}
