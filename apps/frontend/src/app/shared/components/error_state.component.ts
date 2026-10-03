import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-error-state',
  standalone: true,
  template: `
    <div class="error-box card">
      <h3 style="color: #ef4444;">{{ title }}</h3>
      <p>{{ message }}</p>
    </div>
  `,
  styles: [`
    .error-box {
      border-left: 4px solid #ef4444;
      padding: 1.5rem;
    }
  `]
})
export class ErrorStateComponent {
  @Input() title = 'Something went wrong';
  @Input() message = 'Failed to load data. Please try again.';
}
