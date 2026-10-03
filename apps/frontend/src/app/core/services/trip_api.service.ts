import { Injectable, inject } from '@angular/core';
import { ApiClientService } from './api_client.service';
import { Observable } from 'rxjs';

export interface TripCreatePayload {
  origin?: string;
  destination: string;
  start_date?: string;
  end_date?: string;
  duration_days: number;
  preferences?: {
    budget?: string;
    pace?: string;
    interests?: string[];
  };
}

export interface TripResponse {
  id: string;
  title: string;
  destination: string;
  duration_days: number;
  status: string;
}

@Injectable({
  providedIn: 'root',
})
export class TripApiService {
  private api = inject(ApiClientService);

  getHealth(): Observable<{ status: string }> {
    return this.api.get<{ status: string }>('/health');
  }

  createTrip(payload: TripCreatePayload): Observable<TripResponse> {
    return this.api.post<TripResponse>('/trips', payload);
  }

  getTrip(tripId: string): Observable<TripResponse> {
    return this.api.get<TripResponse>(`/trips/${tripId}`);
  }
}
