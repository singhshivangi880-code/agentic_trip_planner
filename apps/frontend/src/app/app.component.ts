import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <nav style="background-color: var(--surface-dark); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 1rem 2rem;">
      <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
        <a routerLink="/" style="font-size: 1.25rem; font-weight: 700; color: white; text-decoration: none;">
          🌐 Agentic Trip Planner
        </a>
        <div style="display: flex; gap: 1.5rem;">
          <a routerLink="/trip/new" style="color: var(--text-muted); text-decoration: none;">New Trip</a>
        </div>
      </div>
    </nav>
    <main class="container">
      <router-outlet></router-outlet>
    </main>
  `,
})
export class AppComponent {
  title = 'AI-Powered Agentic Trip Planner';
}
