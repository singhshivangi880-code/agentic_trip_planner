import { Injectable } from '@angular/core';
import { Itinerary, TripDay, ItineraryItem } from '../models/itinerary.model';

@Injectable({
  providedIn: 'root'
})
export class AuthenticItineraryService {

  generateItinerary(params: {
    destination: string;
    origin?: string;
    durationDays: number;
    startDate?: string;
    pace?: string;
    interests?: string[];
  }): Itinerary {
    const destLower = params.destination.toLowerCase();
    const startDate = params.startDate ? new Date(params.startDate) : new Date();
    const daysCount = Math.min(Math.max(params.durationDays || 3, 1), 14);

    let dayPlans: { theme: string; area: string; items: ItineraryItem[] }[] = [];

    if (destLower.includes('united states') || destLower.includes('usa') || destLower.includes('america') || destLower.includes('new york') || destLower.includes('california')) {
      dayPlans = this.getUSAPlans(params);
    } else if (destLower.includes('japan') || destLower.includes('tokyo') || destLower.includes('kyoto') || destLower.includes('osaka')) {
      dayPlans = this.getJapanPlans(params);
    } else if (destLower.includes('france') || destLower.includes('paris')) {
      dayPlans = this.getParisPlans(params);
    } else if (destLower.includes('italy') || destLower.includes('rome') || destLower.includes('florence')) {
      dayPlans = this.getItalyPlans(params);
    } else if (destLower.includes('switzerland') || destLower.includes('zurich') || destLower.includes('interlaken')) {
      dayPlans = this.getSwissPlans(params);
    } else if (destLower.includes('bali') || destLower.includes('indonesia')) {
      dayPlans = this.getBaliPlans(params);
    } else {
      dayPlans = this.getGeneralPlans(params);
    }

    const days: TripDay[] = [];
    for (let i = 0; i < daysCount; i++) {
      const curDate = new Date(startDate);
      curDate.setDate(curDate.getDate() + i);
      const plan = dayPlans[i % dayPlans.length];

      days.push({
        day_index: i + 1,
        date: curDate.toISOString().split('T')[0],
        theme_or_area: `${plan.theme} (${plan.area})`,
        items: plan.items.map(it => ({ ...it }))
      });
    }

    return { days };
  }

  private getUSAPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Arrival, Midtown Skyline & Broadway Night',
        area: 'Midtown Manhattan, New York',
        items: [
          { title: 'JFK/Newark Airport Arrival & Hotel Check-in', item_type: 'Logistics', start_time: '14:00', end_time: '15:30', location: 'Midtown Manhattan', description: 'Arrive in NYC, transfer to hotel, and refresh.', is_locked: true },
          { title: 'Central Park Walk & Fifth Avenue Architecture', item_type: 'Attraction', start_time: '16:00', end_time: '18:00', location: 'Central Park South', description: 'Stroll past Bethesda Terrace, the Bow Bridge, and iconic Fifth Avenue storefronts.', is_locked: false },
          { title: 'Classic New York Dinner at Joe’s Pizza or Carmine’s', item_type: 'Dining', start_time: '18:30', end_time: '19:45', location: 'Times Square / Theater District', description: 'Authentic thin-crust New York slice or family-style Italian before the show.', is_locked: false },
          { title: 'Broadway Musical Performance', item_type: 'Culture', start_time: '20:00', end_time: '22:30', location: 'Broadway Theater District', description: 'World-renowned theater production in the glowing heart of Manhattan.', is_locked: true }
        ]
      },
      {
        theme: 'Lady Liberty, Financial District & Brooklyn Bridge Sunset',
        area: 'Lower Manhattan & DUMBO, New York',
        items: [
          { title: 'Statue of Liberty & Ellis Island Morning Ferry', item_type: 'Heritage', start_time: '09:00', end_time: '12:00', location: 'Battery Park', description: 'Cruise past the iconic symbol of freedom with breathtaking harbor views.', is_locked: true },
          { title: 'Wall Street & 9/11 Memorial Reflecting Pools', item_type: 'Heritage', start_time: '12:30', end_time: '14:30', location: 'World Trade Center', description: 'Pay homage at the memorial pools and admire the soaring Oculus architecture.', is_locked: false },
          { title: 'Sunset Pedestrian Walk Across Brooklyn Bridge', item_type: 'Activity', start_time: '16:00', end_time: '18:00', location: 'Brooklyn Bridge', description: 'Walk across the historic 1883 suspension bridge as golden hour lights up the Manhattan skyline.', is_locked: false },
          { title: 'Dinner in DUMBO overlooking Manhattan Waterfront', item_type: 'Dining', start_time: '18:30', end_time: '21:00', location: 'DUMBO, Brooklyn', description: 'Artisanal dinner and craft cocktails with panoramic views of the illuminated bridges.', is_locked: false }
        ]
      },
      {
        theme: 'High Line Park, Chelsea Market & SoHo Style',
        area: 'Chelsea, Meatpacking & SoHo, New York',
        items: [
          { title: 'The High Line Elevated Stroll & Hudson Yards', item_type: 'Nature', start_time: '09:30', end_time: '11:30', location: 'Chelsea / Meatpacking', description: 'Repurposed elevated freight rail line transformed into a lush urban botanical path.', is_locked: false },
          { title: 'Chelsea Market Artisanal Food Crawl', item_type: 'Dining', start_time: '12:00', end_time: '14:00', location: 'Chelsea Market', description: 'Fresh Maine lobster rolls, artisanal tacos, and gourmet chocolate samples.', is_locked: false },
          { title: 'SoHo Cast-Iron Architecture & Independent Boutiques', item_type: 'Activity', start_time: '14:30', end_time: '17:30', location: 'SoHo Historic District', description: 'Browse world-class art galleries, design studios, and historic cobblestone streets.', is_locked: false },
          { title: 'Dinner at Balthazar or Minetta Tavern in Greenwich Village', item_type: 'Dining', start_time: '18:30', end_time: '21:00', location: 'Greenwich Village', description: 'Iconic French brasserie or legendary black label burgers in a historic literary haven.', is_locked: false }
        ]
      },
      {
        theme: 'Masterpiece Art & Summit Sky Observatory',
        area: 'Museum Mile & Grand Central, New York',
        items: [
          { title: 'The Metropolitan Museum of Art (The Met)', item_type: 'Attraction', start_time: '09:30', end_time: '13:00', location: 'Museum Mile, Upper East Side', description: '5,000 years of global art, from Temple of Dendur to European Masters.', is_locked: true },
          { title: 'Upper East Side Café Lunch & Madison Avenue Walk', item_type: 'Dining', start_time: '13:30', end_time: '15:00', location: 'Upper East Side', description: 'Relaxed bistro lunch and classic New York streetscape.', is_locked: false },
          { title: 'Summit One Vanderbilt 360° Glass Observation', item_type: 'Experience', start_time: '16:00', end_time: '18:30', location: 'Grand Central', description: 'Multi-sensory mirror art installations and panoramic views looking down at the Empire State Building.', is_locked: true },
          { title: 'Grand Central Oyster Bar or Flatiron Craft Dinner', item_type: 'Dining', start_time: '19:00', end_time: '21:30', location: 'Midtown East', description: 'Historic vaulted tiled dining hall serving fresh Atlantic oysters.', is_locked: false }
        ]
      },
      {
        theme: 'Greenwich Village Vibes & Washington Square Sunset',
        area: 'West Village & Washington Square, New York',
        items: [
          { title: 'Washington Square Park & West Village Brownstones', item_type: 'Culture', start_time: '10:00', end_time: '12:30', location: 'Greenwich Village', description: 'Iconic marble memorial arch, street musicians, chess masters, and historic tree-lined avenues.', is_locked: false },
          { title: 'Artisan Pastrami or Bagel Lunch at Katz’s Delicatessen', item_type: 'Dining', start_time: '13:00', end_time: '14:30', location: 'Lower East Side', description: 'Legendary hand-carved pastrami on rye served since 1888.', is_locked: false },
          { title: 'Greenwich Village Jazz Club or Comedy Cellar Experience', item_type: 'Nightlife', start_time: '19:00', end_time: '22:00', location: 'MacDougal Street', description: 'Intimate subterranean venue featuring top global stand-up or live acoustic jazz.', is_locked: false }
        ]
      }
    ];
  }

  private getJapanPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Arrival & Shinjuku Neon Nightlife',
        area: 'Shinjuku & Shibuya, Tokyo',
        items: [
          { title: 'Tokyo Haneda/Narita Arrival & Shinkansen Suica Setup', item_type: 'Logistics', start_time: '14:00', end_time: '15:30', location: 'Tokyo Central Station', description: 'Pick up pocket Wi-Fi, charge Suica transit pass, and check into your hotel.', is_locked: true },
          { title: 'Tokyo Metropolitan Gov Building Observation Deck', item_type: 'Attraction', start_time: '16:30', end_time: '18:00', location: 'Nishi-Shinjuku', description: 'Enjoy panoramic sunset views of the Tokyo metropolis stretching toward Mt. Fuji.', is_locked: false },
          { title: 'Dinner at Omoide Yokocho (Memory Lane)', item_type: 'Dining', start_time: '18:30', end_time: '20:30', location: 'Shinjuku West Gate', description: 'Authentic yakitori skewers, craft highballs, and retro post-war alley atmosphere.', is_locked: false },
          { title: 'Golden Gai Micro-Bars Exploration', item_type: 'Nightlife', start_time: '21:00', end_time: '22:30', location: 'Kabukicho, Shinjuku', description: 'Historic labyrinth of 200 tiny themed bars packed into six narrow alleys.', is_locked: false }
        ]
      },
      {
        theme: 'Historic Asakusa & Akihabara Otaku Culture',
        area: 'Asakusa & Taito-ku, Tokyo',
        items: [
          { title: 'Senso-ji Temple & Nakamise-dori Shopping Street', item_type: 'Heritage', start_time: '09:00', end_time: '11:30', location: 'Asakusa', description: 'Tokyo’s oldest Buddhist temple founded in 645 AD. Taste fresh melonpan and ningyo-yaki.', is_locked: false },
          { title: 'Traditional Tempura Lunch at Daikokuya', item_type: 'Dining', start_time: '12:00', end_time: '13:30', location: 'Asakusa', description: 'Famous sesame oil tempura bowls served since the Meiji era.', is_locked: false },
          { title: 'Akihabara Electric Town & Retro Gaming', item_type: 'Culture', start_time: '14:30', end_time: '17:30', location: 'Chiyoda, Akihabara', description: 'Browse Super Potato, multi-floor anime complexes, and cutting-edge electronics megastores.', is_locked: false },
          { title: 'Craft Ramen Dinner at Kanda Matsuya or Fuunji', item_type: 'Dining', start_time: '18:30', end_time: '20:00', location: 'Kanda/Shinjuku', description: 'Rich dipping tsukemen ramen with intense bonito and pork broth.', is_locked: false }
        ]
      },
      {
        theme: 'Spiritual Serenity & Pop Culture Crossroads',
        area: 'Harajuku & Shibuya, Tokyo',
        items: [
          { title: 'Meiji Jingu Shrine Sacred Forest Walk', item_type: 'Heritage', start_time: '09:00', end_time: '11:00', location: 'Yoyogi Park, Shibuya', description: 'Peaceful stroll through 170 acres of evergreen sacred forest and giant cedar torii gates.', is_locked: false },
          { title: 'Takeshita Street & Cat Street Vintage Boutiques', item_type: 'Activity', start_time: '11:30', end_time: '13:30', location: 'Harajuku', description: 'Vibrant youth fashion, quirky street desserts, and sleek indie boutiques along Cat Street.', is_locked: false },
          { title: 'Shibuya Crossing & Shibuya Sky 360° Rooftop', item_type: 'Attraction', start_time: '16:00', end_time: '18:30', location: 'Shibuya Scramble Square', description: 'Experience the world’s busiest pedestrian crossing from street level and from the open-air rooftop observatory.', is_locked: false },
          { title: 'Izakaya Feast & Craft Beer in Nonbei Yokocho', item_type: 'Dining', start_time: '19:00', end_time: '21:30', location: 'Shibuya', description: 'Sashimi platters, gyoza, and local Japanese microbrews.', is_locked: false }
        ]
      },
      {
        theme: 'Seafood Markets & Digital Sensory Art',
        area: 'Tsukiji & Toyosu, Tokyo',
        items: [
          { title: 'Tsukiji Outer Market Food Crawl', item_type: 'Dining', start_time: '08:30', end_time: '11:00', location: 'Tsukiji, Chuo', description: 'Fresh sea urchin (uni), melt-in-your-mouth Wagyu skewers, tamagoyaki egg omelettes, and matcha lattes.', is_locked: false },
          { title: 'teamLab Planets Immersive Digital Art', item_type: 'Experience', start_time: '12:00', end_time: '14:30', location: 'Toyosu Waterfront', description: 'Wade barefoot through water and walk among digital projections of floating flowers and infinite crystal rooms.', is_locked: true },
          { title: 'Ginza Luxury Shopping & Itoya Stationery Haven', item_type: 'Leisure', start_time: '15:30', end_time: '18:00', location: 'Ginza, Chuo', description: '12 floors of artisan Japanese stationery, department stores, and flagship architecture.', is_locked: false },
          { title: 'Omakase Sushi Dinner at Ginza Kyubey or Sukiyabashi', item_type: 'Dining', start_time: '19:00', end_time: '21:00', location: 'Ginza', description: 'Authentic Edomae sushi seasoned by master chefs.', is_locked: false }
        ]
      },
      {
        theme: 'Bullet Train to Kyoto & Fushimi Inari Torii Gates',
        area: 'Fushimi & Gion, Kyoto',
        items: [
          { title: 'Tokaido Shinkansen Bullet Train (Tokyo ➔ Kyoto)', item_type: 'Logistics', start_time: '08:30', end_time: '11:00', location: 'Tokyo Station', description: 'Ride the world-famous Nozomi high-speed train at 285 km/h with Mt. Fuji views.', is_locked: true },
          { title: 'Fushimi Inari Taisha Thousand Vermilion Torii Gates', item_type: 'Heritage', start_time: '13:00', end_time: '16:00', location: 'Fushimi-ku, Kyoto', description: 'Ascend the sacred mountain trails through thousands of vibrant orange torii gates dedicated to the god of rice and commerce.', is_locked: false },
          { title: 'Historic Gion Geisha District Evening Atmosphere', item_type: 'Culture', start_time: '17:30', end_time: '19:30', location: 'Gion, Higashiyama', description: 'Lantern-lit preservation district with preserved wooden machiya merchant houses.', is_locked: false },
          { title: 'Traditional Kyoto Kaiseki Dinner along Pontocho Alley', item_type: 'Dining', start_time: '20:00', end_time: '22:00', location: 'Pontocho, Kamogawa River', description: 'Multi-course seasonal dining on riverside wooden terraces overlooking the Kamo River.', is_locked: false }
        ]
      },
      {
        theme: 'Golden Pavilions & Bamboo Forest Sanctuary',
        area: 'Arashiyama & Kinkaku-ji, Kyoto',
        items: [
          { title: 'Arashiyama Bamboo Grove & Tenryu-ji Zen Garden', item_type: 'Nature', start_time: '08:00', end_time: '11:00', location: 'Ukyo-ku, Kyoto', description: 'Beat the crowds to experience towering bamboo stalks swaying in the morning breeze.', is_locked: false },
          { title: 'Iwatayama Monkey Park Scenic Summit', item_type: 'Activity', start_time: '11:30', end_time: '13:00', location: 'Arashiyama', description: 'Short scenic hike with wild Japanese macaques and breathtaking views over Kyoto valley.', is_locked: false },
          { title: 'Kinkaku-ji (The Famous Golden Pavilion)', item_type: 'Heritage', start_time: '14:30', end_time: '16:30', location: 'Kita-ku, Kyoto', description: 'Breathtaking Zen temple whose top two floors are completely covered in pure gold leaf reflecting onto mirror pond.', is_locked: false },
          { title: 'Nishiki Market Street Food Tasting', item_type: 'Dining', start_time: '18:00', end_time: '20:30', location: 'Nakagyo-ku, Kyoto', description: '“Kyoto’s Kitchen”: taste dashi omelets, octopus skewers, sesame crackers, and pickled vegetables.', is_locked: false }
        ]
      },
      {
        theme: 'Dotonbori Street Food & Osaka Castle Day Trip',
        area: 'Namba & Chuo-ku, Osaka',
        items: [
          { title: 'Morning Transit from Kyoto to Osaka', item_type: 'Logistics', start_time: '09:00', end_time: '09:45', location: 'Hankyu/JR Kyoto Line', description: 'Quick 30-minute train ride to Japan’s vibrant gastronomic capital.', is_locked: false },
          { title: 'Osaka Castle & Turret Grounds', item_type: 'Heritage', start_time: '10:30', end_time: '13:00', location: 'Chuo-ku, Osaka', description: 'Iconic 16th-century fortress surrounded by stone moats and lush parklands.', is_locked: false },
          { title: 'Dotonbori Canal Walk & Glico Running Man', item_type: 'Attraction', start_time: '14:30', end_time: '17:30', location: 'Namba, Osaka', description: 'Electric streets filled with giant mechanical crab signs, neon towers, and buzzing crowds.', is_locked: false },
          { title: 'Kuidaore Street Feast: Takoyaki & Okonomiyaki', item_type: 'Dining', start_time: '18:00', end_time: '21:00', location: 'Dotonbori', description: 'Crispy piping-hot octopus balls, savory Japanese cabbage pancakes, and kushikatsu fried skewers.', is_locked: false }
        ]
      }
    ];
  }

  private getParisPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Iconic Landmarks & Eiffel Tower Sunset',
        area: '7th & 8th Arrondissement, Paris',
        items: [
          { title: 'Hotel Check-in & Artisan Boulangerie Croissant', item_type: 'Logistics', start_time: '14:00', end_time: '15:30', location: 'Saint-Germain-des-Prés', description: 'Unpack, refresh, and sample fresh buttery croissants and café au lait.', is_locked: true },
          { title: 'Champ de Mars & Eiffel Tower Ascent', item_type: 'Attraction', start_time: '16:30', end_time: '19:00', location: 'Champ de Mars', description: 'Ascend to the summit for breathtaking 360-degree views over the Seine and Parisian boulevards.', is_locked: false },
          { title: 'Classic French Bistro Dinner at Chez Janou', item_type: 'Dining', start_time: '19:30', end_time: '21:30', location: 'Le Marais', description: 'Confit de canard, provençal herbs, and legendary unlimited chocolate mousse.', is_locked: false }
        ]
      },
      {
        theme: 'World-Class Art & Royal Gardens',
        area: '1st & 6th Arrondissement, Paris',
        items: [
          { title: 'Louvre Museum Masterpieces & Glass Pyramid', item_type: 'Attraction', start_time: '09:00', end_time: '12:30', location: 'Rue de Rivoli', description: 'Explore the Mona Lisa, Winged Victory, and French crown jewels with fast-track entry.', is_locked: false },
          { title: 'Tuileries Garden Stroll & Angelina Hot Chocolate', item_type: 'Leisure', start_time: '13:00', end_time: '14:30', location: 'Place de la Concorde', description: 'Relax in green iron chairs by the grand fountain with thick African hot chocolate.', is_locked: false },
          { title: 'Musée d’Orsay Impressionist Masterpieces', item_type: 'Attraction', start_time: '15:00', end_time: '17:30', location: 'Quai d’Orsay', description: 'Former Beaux-Arts railway station housing Monet, Van Gogh, and Renoir.', is_locked: false },
          { title: 'Seine River Sunset Cruise with Bateaux Parisiens', item_type: 'Activity', start_time: '18:30', end_time: '20:00', location: 'Port de la Bourdonnais', description: 'Glide under historic stone bridges as the Eiffel Tower sparkles at dusk.', is_locked: false }
        ]
      },
      {
        theme: 'Bohemian Heights & Montmartre Alleyways',
        area: '18th Arrondissement, Paris',
        items: [
          { title: 'Sacré-Cœur Basilica & Panoramic Butte View', item_type: 'Heritage', start_time: '09:30', end_time: '11:30', location: 'Montmartre', description: 'Pristine white travertine dome atop the highest point in Paris.', is_locked: false },
          { title: 'Place du Tertre Artists & Secret Vineyards', item_type: 'Culture', start_time: '12:00', end_time: '14:00', location: 'Montmartre Village', description: 'Watch portrait painters and discover hidden cobblestone alleys of Picasso and Renoir.', is_locked: false },
          { title: 'Le Marais Vintage Boutiques & Jewish Quarter Pastries', item_type: 'Activity', start_time: '15:00', end_time: '18:00', location: 'Rue des Rosiers', description: 'Art galleries, high-fashion concept stores, and legendary falafel at L’As du Fallafel.', is_locked: false }
        ]
      }
    ];
  }

  private getItalyPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Ancient Roman Empire & Colosseum Glory',
        area: 'Historic Center, Rome',
        items: [
          { title: 'Colosseum & Gladiatorial Arena Tour', item_type: 'Heritage', start_time: '09:00', end_time: '11:30', location: 'Piazza del Colosseo', description: 'Walk through the 2,000-year-old amphitheater and underground hypogeum.', is_locked: true },
          { title: 'Roman Forum & Palatine Hill Ruins', item_type: 'Heritage', start_time: '12:00', end_time: '14:00', location: 'Via dei Fori Imperiali', description: 'The beating heart of ancient Roman political and commercial life.', is_locked: false },
          { title: 'Authentic Roman Lunch at Armando al Pantheon', item_type: 'Dining', start_time: '14:30', end_time: '16:00', location: 'Salita de’ Crescenzi', description: 'Legendary Cacio e Pepe, Carbonara, and artichokes alla giudia.', is_locked: false },
          { title: 'Pantheon & Trevi Fountain Evening Gelato Stroll', item_type: 'Attraction', start_time: '17:00', end_time: '19:30', location: 'Trevi & Campo Marzio', description: 'Toss a coin into the Trevi Fountain and gaze up through the oculus of the Pantheon.', is_locked: false }
        ]
      },
      {
        theme: 'Vatican Treasures & Trastevere Evenings',
        area: 'Vatican City & Trastevere, Rome',
        items: [
          { title: 'Vatican Museums & Sistine Chapel Ceiling', item_type: 'Attraction', start_time: '08:30', end_time: '12:00', location: 'Vatican City', description: 'Michelangelo’s legendary frescoes and the Gallery of Maps.', is_locked: true },
          { title: 'St. Peter’s Basilica & Michelangelo’s Pietà', item_type: 'Heritage', start_time: '12:30', end_time: '14:00', location: 'Piazza San Pietro', description: 'Climb the dome for a panoramic look over St. Peter’s Square.', is_locked: false },
          { title: 'Trastevere Cobblestone Walk & Wine Tasting', item_type: 'Culture', start_time: '16:30', end_time: '19:00', location: 'Trastevere', description: 'Ivy-draped ochre alleyways, bohemian plazas, and local aperitivo.', is_locked: false },
          { title: 'Rustic Trattoria Dinner at Da Enzo al 29', item_type: 'Dining', start_time: '19:30', end_time: '21:30', location: 'Trastevere', description: 'Crispy fried zucchini blossoms and decadent tiramisu.', is_locked: false }
        ]
      }
    ];
  }

  private getSwissPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Alpine Lakes & Lucerne Heritage',
        area: 'Lucerne & Lake Geneva',
        items: [
          { title: 'Chapel Bridge & Historic Old Town Walking Tour', item_type: 'Heritage', start_time: '09:30', end_time: '12:00', location: 'Lucerne', description: '14th-century covered wooden bridge and medieval painted guild houses.', is_locked: false },
          { title: 'Steamboat Cruise on Lake Lucerne with Fondue', item_type: 'Dining', start_time: '12:30', end_time: '15:00', location: 'Lake Lucerne', description: 'Gliding past snowcapped summits while enjoying Gruyère cheese fondue.', is_locked: false },
          { title: 'Mount Pilatus Golden Round Trip Cogwheel Railway', item_type: 'Nature', start_time: '15:30', end_time: '18:30', location: 'Kriens / Alpnachstad', description: 'The steepest cogwheel railway in the world climbing to 2,132m peaks.', is_locked: true }
        ]
      },
      {
        theme: 'Valley of 72 Waterfalls & Jungfraujoch Summit',
        area: 'Lauterbrunnen & Interlaken, Bernese Oberland',
        items: [
          { title: 'Lauterbrunnen Valley & Staubbach Falls Trail', item_type: 'Nature', start_time: '09:00', end_time: '11:30', location: 'Lauterbrunnen', description: 'Dramatic cliff walls inspired Tolkien’s Rivendell, with 300m cascading waterfalls.', is_locked: false },
          { title: 'Jungfraujoch Top of Europe High-Alpine Station', item_type: 'Attraction', start_time: '12:00', end_time: '16:00', location: 'Jungfrau Region', description: 'Ice Palace, Sphinx Observatory, and permanent snow atop Europe at 3,454 meters.', is_locked: true },
          { title: 'Swiss Alpine Dinner with Raclette & Rösti', item_type: 'Dining', start_time: '18:30', end_time: '21:00', location: 'Interlaken Old Town', description: 'Golden crispy potato rösti with melted mountain cheese and cured bresaola.', is_locked: false }
        ]
      }
    ];
  }

  private getBaliPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    return [
      {
        theme: 'Cultural Heart & Emerald Rice Terraces',
        area: 'Ubud, Central Bali',
        items: [
          { title: 'Tegallalang Rice Terraces & Jungle Swing', item_type: 'Nature', start_time: '08:30', end_time: '11:00', location: 'Tegallalang, Ubud', description: 'Layered UNESCO green paddies bathed in soft morning light.', is_locked: false },
          { title: 'Sacred Monkey Forest Sanctuary Walk', item_type: 'Nature', start_time: '11:30', end_time: '13:30', location: 'Padangtegal, Ubud', description: 'Moss-covered stone temples and playful long-tailed macaques.', is_locked: false },
          { title: 'Organic Balinese Garden Lunch & Spa Treatment', item_type: 'Dining', start_time: '14:00', end_time: '17:00', location: 'Campuhan, Ubud', description: 'Farm-to-table Nasi Campur followed by a rejuvenating flower-bath massage.', is_locked: false }
        ]
      },
      {
        theme: 'Ocean Cliffs & Dramatic Sunset Fire Dance',
        area: 'Uluwatu & Jimbaran, Southern Bali',
        items: [
          { title: 'Uluwatu Cliffside Temple & Coastal Views', item_type: 'Heritage', start_time: '15:00', end_time: '17:30', location: 'Uluwatu Cliff', description: 'Perched 70 meters above roaring Indian Ocean swells.', is_locked: false },
          { title: 'Kecak & Fire Dance Performance at Sunset', item_type: 'Culture', start_time: '18:00', end_time: '19:30', location: 'Uluwatu Amphitheater', description: 'Chanting choir of 50+ performers depicting the Ramayana epic as the sun sets into the ocean.', is_locked: true },
          { title: 'Candlelit Beachfront Grilled Seafood Dinner', item_type: 'Dining', start_time: '20:00', end_time: '22:00', location: 'Jimbaran Bay', description: 'Fresh lobster, red snapper, and jumbo prawns grilled over coconut husks on the sand.', is_locked: false }
        ]
      }
    ];
  }

  private getGeneralPlans(params: any): { theme: string; area: string; items: ItineraryItem[] }[] {
    const dest = params.destination;
    return [
      {
        theme: `Arrival & City Center Orientation`,
        area: `${dest} Central District`,
        items: [
          { title: `Welcome to ${dest}: Hotel Check-in & Orientation`, item_type: 'Logistics', start_time: '14:00', end_time: '15:30', location: 'City Center', description: 'Unpack, refresh, and get oriented with a local transit card.', is_locked: true },
          { title: `Historic Plaza & Walking Exploration`, item_type: 'Activity', start_time: '16:00', end_time: '18:30', location: 'Old Quarter', description: `Discover landmark architecture, vibrant squares, and street vendors in ${dest}.`, is_locked: false },
          { title: `Welcome Dinner featuring Regional Specialties`, item_type: 'Dining', start_time: '19:00', end_time: '21:00', location: 'Downtown Dining Quarter', description: 'Enjoy handpicked culinary delights and local hospitality.', is_locked: false }
        ]
      },
      {
        theme: `Iconic Landmarks & Cultural Highlights`,
        area: `${dest} Heritage Quarter`,
        items: [
          { title: `Morning Cultural Landmark & Guided Experience`, item_type: 'Heritage', start_time: '09:00', end_time: '12:00', location: 'National Landmark District', description: 'Early access to the most famous museum or monument in the city.', is_locked: false },
          { title: `Terrace Lunch with Scenic Views`, item_type: 'Dining', start_time: '12:30', end_time: '14:00', location: 'Riverside / Hillside', description: 'Seasonal local ingredients and refreshing beverages.', is_locked: false },
          { title: `Artisan Markets & Craft Discovery`, item_type: 'Culture', start_time: '14:30', end_time: '17:30', location: 'Artisan Quarter', description: 'Connect with local creators and discover handcrafted treasures.', is_locked: false },
          { title: `Sunset Vista & Evening Dining`, item_type: 'Dining', start_time: '18:30', end_time: '21:00', location: 'Panoramic Viewpoint', description: 'Unwind with sunset views over the skyline.', is_locked: false }
        ]
      },
      {
        theme: `Nature, Hidden Gems & Local Lifestyle`,
        area: `${dest} Outer District`,
        items: [
          { title: `Scenic Morning Excursion or Nature Trail`, item_type: 'Nature', start_time: '08:30', end_time: '12:00', location: 'Green Belt / Botanical Gardens', description: 'Escape the bustle for fresh air, scenic lookout points, and photography.', is_locked: false },
          { title: `Famous Food Market Lunch Crawl`, item_type: 'Dining', start_time: '12:30', end_time: '14:30', location: 'Central Market', description: 'Sample street food favorites and specialty delicacies.', is_locked: false },
          { title: `Leisure Evening & Sunset Farewell`, item_type: 'Leisure', start_time: '17:00', end_time: '20:30', location: 'Promenade / Waterfront', description: 'Celebrate the journey with drinks and regional entertainment.', is_locked: false }
        ]
      }
    ];
  }
}
