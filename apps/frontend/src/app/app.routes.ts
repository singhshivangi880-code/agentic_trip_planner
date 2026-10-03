import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { TripNewComponent } from './features/trip-new/trip-new.component';
import { TripDetailComponent } from './features/trip-detail/trip-detail.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'trip/new', component: TripNewComponent },
  { path: 'trip/:tripId', component: TripDetailComponent },
  { path: 'trip/:tripId/itinerary', component: TripDetailComponent },
  { path: 'trip/:tripId/preparation', component: TripDetailComponent },
  { path: '**', redirectTo: '' },
];
