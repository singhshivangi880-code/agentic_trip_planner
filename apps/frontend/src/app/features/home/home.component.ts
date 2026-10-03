import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  template: `
    <div class="card" style="text-align: center; margin-top: 3rem;">
      <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">AI-Powered Agentic Trip Planner</h1>
      <p style="color: #94a3b8; max-width: 600px; margin: 0 auto 2rem auto;">
        Plan complete multi-city trips with real-time web research, autonomous agent orchestration, and printable travel guides.
      </p>
      <a routerLink="/trip/new" class="btn-primary" style="text-decoration: none; display: inline-block;">
        Plan New Trip
      </a>
    </div>
  `,
})
export class HomeComponent {}
