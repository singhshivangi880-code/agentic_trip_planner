import { Component, inject, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TripApiService, TripCreatePayload } from '../../core/services/trip_api.service';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  validation?: {
    is_valid: boolean;
    flags?: string[];
    suggestions?: string[];
  };
  tripData?: {
    origin?: string;
    destination?: string;
    duration_days?: number;
    start_date?: string;
    end_date?: string;
    pace?: string;
    budget?: string;
    interests?: string[];
  };
  showCard?: boolean;
  suggestedReplies?: string[];
}

@Component({
  selector: 'app-trip-new',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './trip-new.component.html',
  styleUrls: ['./trip-new.component.css']
})
export class TripNewComponent implements OnInit, AfterViewChecked {
  @ViewChild('scrollContainer') private scrollContainer?: ElementRef;
  @ViewChild('chatInput') private chatInput?: ElementRef;

  private tripApi = inject(TripApiService);
  private router = inject(Router);

  userInput = '';
  isThinking = false;
  generatingTrip = false;
  
  currentWorkingTrip: any = {
    origin: '',
    destination: '',
    duration_days: 7,
    pace: 'balanced',
    budget: 'moderate',
    interests: []
  };

  messages: ChatMessage[] = [
    {
      role: 'assistant',
      content: `👋 **Welcome to your AI Travel Co-Pilot!**\n\nWhere are you dreaming of escaping to? Tell me your thoughts freely—where you're departing from, where you'd like to go, travel dates, or just the vibe you're imagining (e.g. *"I want to plan a 14-day trip to Japan from Pune, love street food, history, and photography"*).\n\nI will check location feasibility, flag any typos, and craft an authentic day-by-day plan with you.`,
      suggestedReplies: [
        '14 days in Japan from Pune',
        '7 days in Paris & Rome from Mumbai',
        '5 days relaxing in Bali',
        'Test typo check (from "pube")'
      ]
    }
  ];

  ngOnInit(): void {}

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  private scrollToBottom(): void {
    if (this.scrollContainer) {
      try {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      } catch (err) {}
    }
  }

  onEnterPress(event: Event): void {
    const keyEvent = event as KeyboardEvent;
    if (!keyEvent.shiftKey) {
      event.preventDefault();
      this.submitMessage();
    }
  }

  sendUserMessage(text: string): void {
    this.userInput = text;
    this.submitMessage();
  }

  applySuggestion(sug: string): void {
    this.userInput = `Yes, I mean ${sug}.`;
    this.submitMessage();
  }

  submitMessage(): void {
    const text = this.userInput.trim();
    if (!text || this.isThinking) return;

    // Add user message to UI
    this.messages.push({
      role: 'user',
      content: text
    });
    this.userInput = '';
    this.isThinking = true;

    const historyPayload = this.messages.map(m => ({
      role: m.role,
      content: m.content
    }));

    this.tripApi.agentChat({
      message: text,
      history: historyPayload,
      current_trip: this.currentWorkingTrip
    }).subscribe({
      next: (res) => {
        this.isThinking = false;

        // Update working trip state if agent extracted new data
        if (res.extracted_trip) {
          if (res.extracted_trip.origin) this.currentWorkingTrip.origin = res.extracted_trip.origin;
          if (res.extracted_trip.destination) this.currentWorkingTrip.destination = res.extracted_trip.destination;
          if (res.extracted_trip.duration_days) this.currentWorkingTrip.duration_days = res.extracted_trip.duration_days;
          if (res.extracted_trip.pace) this.currentWorkingTrip.pace = res.extracted_trip.pace;
          if (res.extracted_trip.budget) this.currentWorkingTrip.budget = res.extracted_trip.budget;
          if (res.extracted_trip.interests?.length) this.currentWorkingTrip.interests = res.extracted_trip.interests;
        }

        // Add agent response
        this.messages.push({
          role: 'assistant',
          content: res.reply,
          validation: res.validation,
          tripData: res.show_embedded_card ? { ...this.currentWorkingTrip } : undefined,
          showCard: res.show_embedded_card,
          suggestedReplies: res.suggested_replies || []
        });
      },
      error: (err) => {
        console.error('Agent chat error:', err);
        this.isThinking = false;
        this.messages.push({
          role: 'assistant',
          content: 'I had a momentary connection hiccup. Could you repeat that or clarify your destination?'
        });
      }
    });
  }

  confirmAndGenerateTrip(tripData: any): void {
    if (!tripData.destination) {
      alert('Please specify a destination.');
      return;
    }

    this.generatingTrip = true;

    // Default dates if none provided
    const startDate = tripData.start_date || new Date(Date.now() + 86400000 * 30).toISOString().split('T')[0];
    const duration = tripData.duration_days || 7;
    const endDate = new Date(new Date(startDate).getTime() + (duration - 1) * 86400000).toISOString().split('T')[0];

    const payload: TripCreatePayload = {
      origin: tripData.origin || 'Pune',
      destination: tripData.destination,
      duration_days: duration,
      start_date: startDate,
      end_date: endDate,
      preferences: {
        budget: tripData.budget || 'moderate',
        pace: tripData.pace || 'balanced',
        interests: tripData.interests?.length ? tripData.interests : ['Highlights', 'Culture']
      }
    };

    this.tripApi.createTrip(payload).subscribe({
      next: (created) => {
        this.messages.push({
          role: 'assistant',
          content: `🚀 **Itinerary generated for ${created.title}!** Opening your interactive travel guide...`
        });
        setTimeout(() => {
          this.router.navigate(['/trip', created.id]);
        }, 800);
      },
      error: (err) => {
        this.generatingTrip = false;
        console.error('Error creating trip from chat:', err);
        alert('Failed to generate trip. Please verify details.');
      }
    });
  }

  formatMessage(text: string): string {
    if (!text) return '';
    // Format bold and line breaks
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\n\n/g, '<br><br>');
    formatted = formatted.replace(/\n/g, '<br>');
    return formatted;
  }
}
