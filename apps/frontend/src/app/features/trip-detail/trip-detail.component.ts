import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { TripApiService, TripResponse } from '../../core/services/trip_api.service';
import { WorkflowProgressComponent } from '../workflow/workflow-progress/workflow-progress.component';
import { ItineraryViewComponent } from '../itinerary/itinerary-view/itinerary-view.component';
import { Itinerary, TripDay, ItineraryItem } from '../../core/models/itinerary.model';

interface PackingCategory {
  category: string;
  icon: string;
  items: { name: string; checked: boolean }[];
}

@Component({
  selector: 'app-trip-detail',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    WorkflowProgressComponent,
    ItineraryViewComponent,
  ],
  templateUrl: './trip-detail.component.html',
  styleUrls: ['./trip-detail.component.css']
})
export class TripDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private tripApi = inject(TripApiService);

  tripId: string | null = null;
  trip: TripResponse | null = null;
  loading = true;
  activeTab: 'workflow' | 'itinerary' | 'preparation' = 'workflow';
  workflowDone = false;
  shareCopied = false;

  itinerary: Itinerary | null = null;
  packingList: PackingCategory[] = [];

  private itineraryHistory: string[] = [];

  ngOnInit(): void {
    this.tripId = this.route.snapshot.paramMap.get('tripId');
    if (this.tripId) {
      this.loadTrip(this.tripId);
    }
  }

  loadTrip(tripId: string): void {
    this.loading = true;
    this.tripApi.getTrip(tripId).subscribe({
      next: (trip) => {
        this.trip = trip;
        this.loading = false;
        this.initItinerary(trip);
        this.initPackingList(trip);
      },
      error: (err) => {
        console.error('Failed to load trip', err);
        this.loading = false;
      }
    });
  }

  onWorkflowCompleted(): void {
    this.workflowDone = true;
    if (this.trip && !this.itinerary) {
      this.initItinerary(this.trip);
    }
    // Smoothly auto-transition to itinerary tab so the user sees the generated schedule immediately
    setTimeout(() => {
      if (this.activeTab === 'workflow') {
        this.activeTab = 'itinerary';
      }
    }, 1200);
  }

  onDecisionMade(decision: string): void {
    if (this.trip) {
      if (!this.trip.preferences) {
        this.trip.preferences = {};
      }
      this.trip.preferences.pace = decision.toLowerCase();
      this.initItinerary(this.trip);
    }
    setTimeout(() => {
      this.activeTab = 'itinerary';
    }, 500);
  }

  shareTrip(): void {
    if (!this.tripId) return;

    this.tripApi.createShare(this.tripId).subscribe({
      next: (res) => {
        const shareUrl = `${window.location.origin}/share/${res.token}`;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(shareUrl).then(() => {
            this.showShareToast();
          }).catch(() => {
            prompt('Copy this share link:', shareUrl);
          });
        } else {
          prompt('Copy this share link:', shareUrl);
        }
      },
      error: () => {
        const fallbackUrl = window.location.href;
        navigator.clipboard?.writeText(fallbackUrl);
        this.showShareToast();
      }
    });
  }

  private showShareToast(): void {
    this.shareCopied = true;
    setTimeout(() => {
      this.shareCopied = false;
    }, 3000);
  }

  onReplan(event: { targetDay: number; instruction: string }): void {
    if (!this.itinerary) return;
    this.saveSnapshot();

    const targetDay = this.itinerary.days.find(d => d.day_index === event.targetDay);
    if (!targetDay) return;

    if (event.instruction.startsWith('Remove')) {
      const titleToRemove = event.instruction.replace('Remove ', '').replace(' from the schedule', '');
      targetDay.items = targetDay.items.filter(item => item.title !== titleToRemove);
    } else if (event.instruction.startsWith('Replace')) {
      const titleToReplace = event.instruction.replace('Replace ', '').replace(' with something else in the same area', '');
      const idx = targetDay.items.findIndex(item => item.title === titleToReplace);
      if (idx !== -1) {
        targetDay.items[idx] = {
          title: `Alternative Experience: Local Highlights & Culture`,
          item_type: 'Activity',
          start_time: targetDay.items[idx].start_time,
          end_time: targetDay.items[idx].end_time,
          location: `${this.trip?.destination || 'City'} Historic Center`,
          description: 'Custom curated activity suggested by AI Agent to match your preferences.',
          is_locked: false
        };
      }
    }
  }

  onUndo(): void {
    if (this.itineraryHistory.length > 0) {
      const prev = this.itineraryHistory.pop();
      if (prev) {
        this.itinerary = JSON.parse(prev);
      }
    }
  }

  private saveSnapshot(): void {
    if (this.itinerary) {
      this.itineraryHistory.push(JSON.stringify(this.itinerary));
    }
  }

  private initItinerary(trip: TripResponse): void {
    const dest = trip.destination || 'Destination';
    const numDays = Math.min(Math.max(trip.duration_days || 3, 1), 7);
    const startDate = trip.start_date ? new Date(trip.start_date) : new Date();

    const sampleDays: TripDay[] = [];

    const templates = [
      {
        theme: 'Arrival & Neighborhood Immersion',
        items: [
          { title: `Welcome to ${dest} & Hotel Check-in`, item_type: 'Logistics', start_time: '14:00', end_time: '15:30', location: 'City Center', description: 'Arrive, drop luggage, and refresh after transit.', is_locked: true },
          { title: 'Historic District Walking Tour', item_type: 'Activity', start_time: '16:00', end_time: '18:30', location: 'Old Quarter', description: 'Explore iconic streets, architecture, and local artisan shops.', is_locked: false },
          { title: 'Authentic Local Dinner & Night Market', item_type: 'Dining', start_time: '19:00', end_time: '21:00', location: 'Downtown Food Alley', description: 'Savor regional culinary specialties and vibrant atmosphere.', is_locked: false },
        ]
      },
      {
        theme: 'Iconic Landmarks & Cultural Highlights',
        items: [
          { title: 'Morning Heritage Landmark Visit', item_type: 'Attraction', start_time: '09:00', end_time: '12:00', location: 'National Museum & Gardens', description: 'Beat the crowds for an immersive cultural experience.', is_locked: false },
          { title: 'Scenic Lunch with City View', item_type: 'Dining', start_time: '12:30', end_time: '14:00', location: 'Riverfront Terrace', description: 'Relaxed dining featuring fresh seasonal ingredients.', is_locked: false },
          { title: 'Art & Design Gallery Exploration', item_type: 'Attraction', start_time: '14:30', end_time: '17:30', location: 'Modern Arts District', description: 'Curated exhibits of contemporary local masters.', is_locked: false },
        ]
      },
      {
        theme: 'Nature, Panoramic Vistas & Sunset',
        items: [
          { title: 'Scenic Lookout & Morning Trail', item_type: 'Nature', start_time: '08:30', end_time: '12:00', location: 'Overlook Park', description: 'Gentle morning hike with breathtaking skyline views.', is_locked: false },
          { title: 'Local Farmers Market & Casual Eateries', item_type: 'Dining', start_time: '12:30', end_time: '14:00', location: 'Market Square', description: 'Try street food treats and fresh seasonal snacks.', is_locked: false },
          { title: 'Golden Hour Cruise or Rooftop Lounge', item_type: 'Leisure', start_time: '17:30', end_time: '20:00', location: 'Observation Deck', description: 'Unwind with sunset refreshments over the cityscape.', is_locked: false },
        ]
      },
      {
        theme: 'Hidden Gems & Artisan Crafts',
        items: [
          { title: 'Traditional Craft Workshop & Tasting', item_type: 'Experience', start_time: '10:00', end_time: '12:30', location: 'Artisan Workshop', description: 'Hands-on discovery of local traditions and specialties.', is_locked: false },
          { title: 'Boutique Shopping & Café Break', item_type: 'Leisure', start_time: '14:00', end_time: '16:30', location: 'Bohemian Quarter', description: 'Independent boutiques, books, and specialty coffee.', is_locked: false },
          { title: 'Chef-Curated Tasting Menu', item_type: 'Dining', start_time: '19:30', end_time: '22:00', location: 'Fine Dining District', description: 'Memorable culinary journey featuring top regional dishes.', is_locked: false },
        ]
      }
    ];

    for (let i = 0; i < numDays; i++) {
      const dayDate = new Date(startDate);
      dayDate.setDate(dayDate.getDate() + i);
      const tmpl = templates[i % templates.length];

      sampleDays.push({
        day_index: i + 1,
        date: dayDate.toISOString().split('T')[0],
        theme_or_area: `${tmpl.theme}`,
        items: tmpl.items.map(it => ({ ...it }))
      });
    }

    this.itinerary = { days: sampleDays };
  }

  private initPackingList(trip: TripResponse): void {
    const dest = trip.destination || 'International';

    this.packingList = [
      {
        category: 'Essentials & Documents',
        icon: '🛂',
        items: [
          { name: 'Passport with at least 6 months validity', checked: true },
          { name: `Visa requirements checked for ${dest}`, checked: false },
          { name: 'Travel Insurance confirmation & emergency contacts', checked: false },
          { name: 'Copies of bookings, tickets, and reservations', checked: false },
        ]
      },
      {
        category: 'Tech & Connectivity',
        icon: '🔌',
        items: [
          { name: 'Universal travel power adapter', checked: false },
          { name: 'High-capacity power bank for day trips', checked: false },
          { name: 'eSIM / International roaming setup', checked: false },
          { name: 'Noise-canceling earphones for flight/transit', checked: false },
        ]
      },
      {
        category: 'Clothing & Comfort',
        icon: '👟',
        items: [
          { name: 'Comfortable walking shoes (10,000+ daily steps)', checked: true },
          { name: 'Lightweight weather-resistant layer / jacket', checked: false },
          { name: 'Daypack or crossbody bag with anti-theft zipper', checked: false },
          { name: 'Compact travel umbrella or rain poncho', checked: false },
        ]
      },
      {
        category: 'Health & Personal Care',
        icon: '💊',
        items: [
          { name: 'Prescription medications & basic first-aid kit', checked: false },
          { name: 'Reusable water bottle with filter compatibility', checked: false },
          { name: 'Sunscreen and travel-sized toiletries', checked: false },
          { name: 'Hand sanitizer & travel wipes', checked: true },
        ]
      }
    ];
  }
}
