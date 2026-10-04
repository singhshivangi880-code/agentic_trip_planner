export interface ItineraryItem {
  title: string;
  item_type: string;
  start_time: string;
  end_time: string;
  location: string;
  description: string;
  booking_ref?: string;
  is_locked: boolean;
}

export interface TripDay {
  day_index: number;
  date: string;
  theme_or_area: string;
  items: ItineraryItem[];
}

export interface Itinerary {
  days: TripDay[];
}
