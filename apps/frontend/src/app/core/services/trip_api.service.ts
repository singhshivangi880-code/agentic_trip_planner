import { Injectable, inject } from '@angular/core';
import { ApiClientService } from './api_client.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

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
  origin?: string;
  start_date?: string;
  end_date?: string;
  duration_days: number;
  status: string;
  workflow_status?: string;
  preferences?: {
    budget?: string;
    pace?: string;
    interests?: string[];
    group_composition?: string;
  };
}

@Injectable({
  providedIn: 'root',
})
export class TripApiService {
  private api = inject(ApiClientService);

  private http = inject(HttpClient);

  getHealth(): Observable<{ status: string }> {
    return this.http.get<{ status: string }>('/health');
  }

  createTrip(payload: TripCreatePayload): Observable<TripResponse> {
    return this.api.post<TripResponse>('/trips', payload);
  }

  getTrip(tripId: string): Observable<TripResponse> {
    return this.api.get<TripResponse>(`/trips/${tripId}`);
  }

  submitDecision(tripId: string, payload: { decision_id: string; selected_option: string; context?: string }): Observable<any> {
    return this.api.post<{ status: string; message: string }>(`/trips/${tripId}/decisions`, payload);
  }

  createShare(tripId: string): Observable<{ token: string; expires_at: string }> {
    return this.api.post<{ token: string; expires_at: string }>('/share/', { trip_id: tripId });
  }

  agentChat(payload: { message: string; history?: any[]; current_trip?: any; destination?: string; origin?: string; days?: number }): Observable<any> {
    return this.api.post<any>('/agent/chat', payload);
  }
}
