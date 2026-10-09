import { Injectable } from '@angular/core';

export interface LocationValidationResult {
  isValid: boolean;
  normalizedName?: string;
  country?: string;
  flagEmoji?: string;
  warning?: string;
  error?: string;
  suggestions?: string[];
  isVagueCountry?: boolean;
  recommendedCities?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class LocationValidatorService {
  // Curated database of known cities, airports, countries, and common typos
  private knownLocations: Record<string, { name: string; country: string; flag: string; type: 'city' | 'country'; topCities?: string[] }> = {
    // India
    'pune': { name: 'Pune', country: 'India', flag: '🇮🇳', type: 'city' },
    'mumbai': { name: 'Mumbai', country: 'India', flag: '🇮🇳', type: 'city' },
    'delhi': { name: 'New Delhi', country: 'India', flag: '🇮🇳', type: 'city' },
    'new delhi': { name: 'New Delhi', country: 'India', flag: '🇮🇳', type: 'city' },
    'bengaluru': { name: 'Bengaluru', country: 'India', flag: '🇮🇳', type: 'city' },
    'bangalore': { name: 'Bengaluru', country: 'India', flag: '🇮🇳', type: 'city' },
    'hyderabad': { name: 'Hyderabad', country: 'India', flag: '🇮🇳', type: 'city' },
    'chennai': { name: 'Chennai', country: 'India', flag: '🇮🇳', type: 'city' },
    'kolkata': { name: 'Kolkata', country: 'India', flag: '🇮🇳', type: 'city' },
    'goa': { name: 'Goa', country: 'India', flag: '🇮🇳', type: 'city' },

    // Japan
    'japan': { name: 'Japan', country: 'Japan', flag: '🇯🇵', type: 'country', topCities: ['Tokyo', 'Kyoto', 'Osaka', 'Hiroshima', 'Hokkaido'] },
    'tokyo': { name: 'Tokyo', country: 'Japan', flag: '🇯🇵', type: 'city' },
    'kyoto': { name: 'Kyoto', country: 'Japan', flag: '🇯🇵', type: 'city' },
    'osaka': { name: 'Osaka', country: 'Japan', flag: '🇯🇵', type: 'city' },
    'hiroshima': { name: 'Hiroshima', country: 'Japan', flag: '🇯🇵', type: 'city' },
    'sapporo': { name: 'Sapporo', country: 'Japan', flag: '🇯🇵', type: 'city' },
    'nara': { name: 'Nara', country: 'Japan', flag: '🇯🇵', type: 'city' },

    // Europe
    'france': { name: 'France', country: 'France', flag: '🇫🇷', type: 'country', topCities: ['Paris', 'Nice', 'Lyon', 'Marseille'] },
    'paris': { name: 'Paris', country: 'France', flag: '🇫🇷', type: 'city' },
    'italy': { name: 'Italy', country: 'Italy', flag: '🇮🇹', type: 'country', topCities: ['Rome', 'Florence', 'Venice', 'Milan'] },
    'rome': { name: 'Rome', country: 'Italy', flag: '🇮🇹', type: 'city' },
    'florence': { name: 'Florence', country: 'Italy', flag: '🇮🇹', type: 'city' },
    'venice': { name: 'Venice', country: 'Italy', flag: '🇮🇹', type: 'city' },
    'switzerland': { name: 'Switzerland', country: 'Switzerland', flag: '🇨🇭', type: 'country', topCities: ['Zurich', 'Lucerne', 'Interlaken', 'Geneva'] },
    'zurich': { name: 'Zurich', country: 'Switzerland', flag: '🇨🇭', type: 'city' },
    'interlaken': { name: 'Interlaken', country: 'Switzerland', flag: '🇨🇭', type: 'city' },
    'london': { name: 'London', country: 'United Kingdom', flag: '🇬🇧', type: 'city' },
    'united kingdom': { name: 'United Kingdom', country: 'United Kingdom', flag: '🇬🇧', type: 'country', topCities: ['London', 'Edinburgh', 'Manchester'] },
    'spain': { name: 'Spain', country: 'Spain', flag: '🇪🇸', type: 'country', topCities: ['Barcelona', 'Madrid', 'Seville'] },
    'barcelona': { name: 'Barcelona', country: 'Spain', flag: '🇪🇸', type: 'city' },
    'madrid': { name: 'Madrid', country: 'Spain', flag: '🇪🇸', type: 'city' },

    // Southeast Asia & Americas & Middle East
    'bali': { name: 'Bali', country: 'Indonesia', flag: '🇮🇩', type: 'city' },
    'indonesia': { name: 'Indonesia', country: 'Indonesia', flag: '🇮🇩', type: 'country', topCities: ['Bali', 'Jakarta', 'Yogyakarta'] },
    'singapore': { name: 'Singapore', country: 'Singapore', flag: '🇸🇬', type: 'city' },
    'thailand': { name: 'Thailand', country: 'Thailand', flag: '🇹🇭', type: 'country', topCities: ['Bangkok', 'Phuket', 'Chiang Mai'] },
    'bangkok': { name: 'Bangkok', country: 'Thailand', flag: '🇹🇭', type: 'city' },
    'phuket': { name: 'Phuket', country: 'Thailand', flag: '🇹🇭', type: 'city' },
    'dubai': { name: 'Dubai', country: 'United Arab Emirates', flag: '🇦🇪', type: 'city' },
    'vietnam': { name: 'Vietnam', country: 'Vietnam', flag: '🇻🇳', type: 'country', topCities: ['Hanoi', 'Da Nang', 'Ho Chi Minh City'] },
    'new york': { name: 'New York', country: 'United States', flag: '🇺🇸', type: 'city' },
    'san francisco': { name: 'San Francisco', country: 'United States', flag: '🇺🇸', type: 'city' },
    'usa': { name: 'United States', country: 'United States', flag: '🇺🇸', type: 'country', topCities: ['New York', 'San Francisco', 'Los Angeles'] },
  };

  // Known typos & fuzzy redirects
  private typoMap: Record<string, string[]> = {
    'pube': ['Pune', 'Phuket', 'Dubai'],
    'puna': ['Pune'],
    'delh': ['New Delhi'],
    'delhy': ['New Delhi'],
    'mubai': ['Mumbai'],
    'bombay': ['Mumbai'],
    'banglore': ['Bengaluru'],
    'japn': ['Japan', 'Tokyo'],
    'tokio': ['Tokyo'],
    'kyto': ['Kyoto'],
    'parsi': ['Paris'],
    'rom': ['Rome'],
    'swis': ['Switzerland', 'Zurich'],
    'singapor': ['Singapore'],
    'duba': ['Dubai']
  };

  validateLocation(rawInput: string, isOrigin = false): LocationValidationResult {
    if (!rawInput || !rawInput.trim()) {
      return {
        isValid: false,
        error: isOrigin ? 'Departure city is required.' : 'Destination is required.'
      };
    }

    const clean = rawInput.trim().toLowerCase();

    // Check direct match
    if (this.knownLocations[clean]) {
      const info = this.knownLocations[clean];
      const res: LocationValidationResult = {
        isValid: true,
        normalizedName: info.name,
        country: info.country,
        flagEmoji: info.flag
      };

      if (!isOrigin && info.type === 'country') {
        res.isVagueCountry = true;
        res.recommendedCities = info.topCities || [];
        res.warning = `${info.name} is a country with diverse regions. A standard trip typically focuses on ${res.recommendedCities.slice(0, 3).join(', ')}.`;
      }

      return res;
    }

    // Check known typo mapping
    if (this.typoMap[clean]) {
      const suggestions = this.typoMap[clean];
      return {
        isValid: false,
        error: `"${rawInput}" was not recognized as a valid location.`,
        suggestions: suggestions,
        warning: `Did you mean ${suggestions.join(' or ')}?`
      };
    }

    // Fuzzy partial match among known locations
    const candidates = Object.keys(this.knownLocations).filter(k => 
      k.includes(clean) || clean.includes(k) || this.levenshteinDistance(k, clean) <= 2
    );

    if (candidates.length > 0) {
      const suggestions = candidates.map(c => this.knownLocations[c].name);
      return {
        isValid: false,
        error: `"${rawInput}" seems like a typo.`,
        suggestions: Array.from(new Set(suggestions)).slice(0, 3),
        warning: `Did you mean ${suggestions[0]}?`
      };
    }

    // If completely unknown string
    // If it's pure gibberish (e.g. "asdfgh", "xyz123", length < 3)
    if (clean.length < 3 || /[^a-zA-Z\s-]/.test(clean)) {
      return {
        isValid: false,
        error: `"${rawInput}" does not look like a real city or destination.`,
        suggestions: ['Pune', 'Mumbai', 'Tokyo', 'Paris']
      };
    }

    // Otherwise, treat as an unlisted but syntactically possible destination, with a gentle validation note
    const capitalized = rawInput.trim().replace(/\b\w/g, l => l.toUpperCase());
    return {
      isValid: true,
      normalizedName: capitalized,
      flagEmoji: '📍',
      warning: `"${capitalized}" is not in our primary verified airport directory, but we can plan a trip there!`
    };
  }

  validateTripPair(origin: string, destination: string): { isValid: boolean; error?: string } {
    const normOrigin = origin.trim().toLowerCase();
    const normDest = destination.trim().toLowerCase();

    if (normOrigin === normDest) {
      return {
        isValid: false,
        error: `Origin and destination cannot be identical ("${origin}"). Please choose a different destination to travel to.`
      };
    }

    return { isValid: true };
  }

  private levenshteinDistance(a: string, b: string): number {
    const matrix: number[][] = [];
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
          );
        }
      }
    }
    return matrix[b.length][a.length];
  }
}
