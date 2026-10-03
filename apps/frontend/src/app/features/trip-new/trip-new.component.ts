import { Component } from '@angular/core';

@Component({
  selector: 'app-trip-new',
  standalone: true,
  template: `
    <div class="card" style="max-width: 600px; margin: 2rem auto;">
      <h2>Plan Your Next Trip</h2>
      <p style="color: #94a3b8;">Enter where you want to go and what you love.</p>
    </div>
  `,
})
export class TripNewComponent {}
