import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TripApiService, TripCreatePayload } from '../../core/services/trip_api.service';

@Component({
  selector: 'app-trip-new',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  template: `
    <div class="card" style="max-width: 600px; margin: 2rem auto; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
      <h2>Plan Your Next Trip</h2>
      <p style="color: #94a3b8; margin-bottom: 2rem;">Enter where you want to go and what you love.</p>

      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <div style="margin-bottom: 1rem;">
          <label style="display: block; margin-bottom: 0.5rem;">Origin</label>
          <input type="text" formControlName="origin" style="width: 100%; padding: 0.5rem;" placeholder="e.g. Pune">
        </div>

        <div style="margin-bottom: 1rem;">
          <label style="display: block; margin-bottom: 0.5rem;">Destination*</label>
          <input type="text" formControlName="destination" style="width: 100%; padding: 0.5rem;" placeholder="e.g. Japan">
          <div *ngIf="form.get('destination')?.invalid && form.get('destination')?.touched" style="color: red; font-size: 0.8rem; margin-top: 0.25rem;">
            Destination is required.
          </div>
        </div>

        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
          <div style="flex: 1;">
            <label style="display: block; margin-bottom: 0.5rem;">Start Date*</label>
            <input type="date" formControlName="startDate" style="width: 100%; padding: 0.5rem;">
          </div>
          <div style="flex: 1;">
            <label style="display: block; margin-bottom: 0.5rem;">End Date*</label>
            <input type="date" formControlName="endDate" style="width: 100%; padding: 0.5rem;">
          </div>
        </div>
        <div *ngIf="form.errors?.['dateRange']" style="color: red; font-size: 0.8rem; margin-bottom: 1rem;">
            End date must be after start date.
        </div>

        <div style="margin-bottom: 1rem;">
          <label style="display: block; margin-bottom: 0.5rem;">Budget</label>
          <select formControlName="budget" style="width: 100%; padding: 0.5rem;">
            <option value="">Any</option>
            <option value="budget">Budget</option>
            <option value="moderate">Moderate</option>
            <option value="luxury">Luxury</option>
          </select>
        </div>

        <div style="margin-bottom: 1rem;">
          <label style="display: block; margin-bottom: 0.5rem;">Pace</label>
          <select formControlName="pace" style="width: 100%; padding: 0.5rem;">
            <option value="">Any</option>
            <option value="relaxed">Relaxed</option>
            <option value="balanced">Balanced</option>
            <option value="packed">Packed</option>
          </select>
        </div>

        <div style="margin-bottom: 2rem;">
          <label style="display: block; margin-bottom: 0.5rem;">Interests (comma separated)</label>
          <input type="text" formControlName="interests" style="width: 100%; padding: 0.5rem;" placeholder="food, history, nature">
        </div>

        <div *ngIf="error()" style="color: red; margin-bottom: 1rem; font-size: 0.9rem;">{{ error() }}</div>

        <button type="submit" [disabled]="form.invalid || submitting()" style="padding: 0.75rem 1.5rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">
          {{ submitting() ? 'Submitting...' : 'Create Trip' }}
        </button>
      </form>
    </div>
  `,
})
export class TripNewComponent {
  private fb = inject(FormBuilder);
  private tripApi = inject(TripApiService);
  private router = inject(Router);

  submitting = signal(false);
  error = signal<string | null>(null);

  form = this.fb.group({
    origin: [''],
    destination: ['', Validators.required],
    startDate: ['', Validators.required],
    endDate: ['', Validators.required],
    budget: [''],
    pace: [''],
    interests: [''],
  }, { validators: this.dateRangeValidator });

  dateRangeValidator(control: AbstractControl): ValidationErrors | null {
    const start = control.get('startDate')?.value;
    const end = control.get('endDate')?.value;
    if (start && end && new Date(start) > new Date(end)) {
      return { dateRange: true };
    }
    return null;
  }

  onSubmit() {
    if (this.form.invalid) return;

    this.submitting.set(true);
    this.error.set(null);

    const val = this.form.value;
    
    // ponytail: derive duration_days since it's required by backend, one line logic
    const durationDays = Math.max(1, Math.ceil((new Date(val.endDate!).getTime() - new Date(val.startDate!).getTime()) / 86400000));

    const payload: TripCreatePayload = {
      origin: val.origin || undefined,
      destination: val.destination as string,
      start_date: val.startDate as string,
      end_date: val.endDate as string,
      duration_days: durationDays,
      preferences: {
        budget: val.budget || undefined,
        pace: val.pace || undefined,
        interests: val.interests ? val.interests.split(',').map((i: string) => i.trim()).filter((i: string) => i) : undefined,
      }
    };

    this.tripApi.createTrip(payload).subscribe({
      next: (trip) => {
        this.router.navigate(['/trip', trip.id]);
      },
      error: (err) => {
        this.submitting.set(false);
        this.error.set(err.error?.message || 'Failed to create trip. Please try again.');
      }
    });
  }
}
