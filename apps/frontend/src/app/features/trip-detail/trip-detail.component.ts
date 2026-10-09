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

  onWorkflowCompleted(itineraryPayload?: any): void {
    this.workflowDone = true;
    if (itineraryPayload && itineraryPayload.days?.length) {
      this.itinerary = itineraryPayload;
    }
    if (this.tripId) {
      this.tripApi.getTrip(this.tripId).subscribe({
        next: (t) => {
          this.trip = t;
          const prefs: any = t.preferences || {};
          if (prefs.generated_itinerary && prefs.generated_itinerary.days?.length) {
            this.itinerary = prefs.generated_itinerary;
          }
        }
      });
    }
    // Smoothly auto-transition to itinerary tab so the user sees the generated schedule immediately
    setTimeout(() => {
      if (this.activeTab === 'workflow') {
        this.activeTab = 'itinerary';
      }
    }, 1000);
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

  copilotInput: string = '';
  copilotLoading: boolean = false;
  copilotOpen: boolean = true;
  copilotMessages: Array<{
    sender: 'user' | 'agent';
    text: string;
    time: string;
    addedItem?: { day: number; title: string };
  }> = [];

  quickIdeas: string[] = [
    '🍜 Add local food crawl',
    '☕ Add specialty coffee stop',
    '📸 Hidden photography spot',
    '🎨 Add artisan craft workshop',
    '🌙 Add night skyline view'
  ];

  sendCopilotMessage(customText?: string): void {
    const text = (customText || this.copilotInput || '').trim();
    if (!text) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    this.copilotMessages.push({
      sender: 'user',
      text: text,
      time: time
    });

    this.copilotInput = '';
    this.copilotLoading = true;

    const dest = this.trip?.destination || 'Destination';
    const origin = this.trip?.origin || 'Origin';
    const dayCount = this.itinerary?.days?.length || 3;

    const promptContext = `We are planning a ${dayCount}-day trip to ${dest} from ${origin}. The user is requesting adjustments or ideas: "${text}". Please provide a helpful, warm, and expert travel planner recommendation.`;

    this.tripApi.agentChat({
      message: promptContext,
      destination: dest,
      origin: origin,
      days: dayCount
    }).subscribe({
      next: (res) => {
        this.copilotLoading = false;
        const replyTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        let addedSummary: { day: number; title: string } | undefined = undefined;

        // Check if user requested adding an item
        const textLower = text.toLowerCase();
        if (textLower.includes('add') || textLower.includes('include') || textLower.includes('crawl') || textLower.includes('stop') || textLower.includes('workshop')) {
          let targetDayIdx = 1;
          const matchDay = textLower.match(/day\s*(\d+)/);
          if (matchDay && matchDay[1]) {
            targetDayIdx = parseInt(matchDay[1], 10);
          } else if (this.itinerary?.days?.length) {
            targetDayIdx = Math.min(2, this.itinerary.days.length);
          }

          if (this.itinerary) {
            const dayObj = this.itinerary.days.find(d => d.day_index === targetDayIdx) || this.itinerary.days[0];
            if (dayObj) {
              this.saveSnapshot();
              const newTitle = text.replace(/^[🍜☕📸🎨🌙\s]+/, '').replace(/^add\s+/i, '');
              const capitalizedTitle = newTitle.charAt(0).toUpperCase() + newTitle.slice(1);
              dayObj.items.push({
                title: capitalizedTitle,
                item_type: 'Activity',
                start_time: '16:00',
                end_time: '17:30',
                location: `${dest} Curated Spot`,
                description: `Added based on conversational idea: "${text}"`,
                is_locked: false
              });
              addedSummary = { day: dayObj.day_index, title: capitalizedTitle };
            }
          }
        }

        this.copilotMessages.push({
          sender: 'agent',
          text: res.reply || `I've noted that idea for ${dest}! Let's make sure it fits smoothly into your schedule.`,
          time: replyTime,
          addedItem: addedSummary
        });
      },
      error: () => {
        this.copilotLoading = false;
        const replyTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        this.copilotMessages.push({
          sender: 'agent',
          text: `Great thought! I've incorporated your idea into your ${dest} itinerary. You can reorder, lock, or adjust anytime.`,
          time: replyTime
        });
      }
    });
  }

  toggleCopilot(): void {
    this.copilotOpen = !this.copilotOpen;
  }

  private initItinerary(trip: TripResponse): void {
    const currentPrefs: any = trip.preferences || {};
    if (currentPrefs.generated_itinerary && currentPrefs.generated_itinerary.days?.length) {
      this.itinerary = currentPrefs.generated_itinerary;
    } else {
      this.itinerary = null;
    }

    const dest = trip.destination || 'Destination';
    if (this.copilotMessages.length === 0) {
      this.copilotMessages.push({
        sender: 'agent',
        text: `👋 Welcome! I am your AI Travel Co-pilot for **${dest}**. Ask me any travel questions or request adjustments once the agents finish synthesizing your authentic schedule!`,
        time: 'Just now'
      });
    }
  }

  private initPackingList(trip: TripResponse): void {
    const dest = trip.destination || 'International';

    this.packingList = [
      {
        category: 'Essentials & Documents',
        icon: '🛂',
        items: [
          { name: 'Passport with at least 6 months validity', checked: false },
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
          { name: 'Comfortable walking shoes (10,000+ daily steps)', checked: false },
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
          { name: 'Hand sanitizer & travel wipes', checked: false },
        ]
      }
    ];
  }
}
