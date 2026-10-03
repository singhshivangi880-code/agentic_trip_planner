import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  standalone: true,
  template: `
    <div class="empty-box card">
      <h3>{{ title }}</h3>
      <p>{{ message }}</p>
    </div>
  `,
  styles: [`
    .empty-box {
      text-align: center;
      padding: 3rem;
      color: #94a3b8;
    }
  `]
})
export class EmptyStateComponent {
  @Input() title = 'No Data Available';
  @Input() message = 'Start by adding a new trip request.';
}
