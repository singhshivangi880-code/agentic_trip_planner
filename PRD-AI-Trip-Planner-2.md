# Product Requirements Document: AI-Powered Agentic Trip Planner

> **Version:** 1.2  
> **Status:** Discovery Complete — Ready for Technical Design  
> **Date:** October 2026  

---

## Revision Notes (v1.1 and v1.2)

This revision resolves two internal contradictions, closes five product gaps, and adds supporting requirements drawn from the companion Functional Requirements Document. No existing requirement has been removed. Changes are additive or clarify the original text.

| Area | Change | Where |
|---|---|---|
| Contradiction: origin city | Origin city and nationality are captured at the start (one-tap, skippable, saved to the profile) instead of only during refinement | 9.2A, 9.3, 9.4, Journey 1 |
| Contradiction: day trips | Day-trip decisions are always put to the user as a choice with a recommendation; the plan shows the recommended option as provisional until confirmed | 20.3, Journey 1 |
| Gap: trains and buses | Flights, trains and buses are all supported for getting to and from the destination, not only between cities | 24.1, FR-9, Journey 5 |
| Gap: existing bookings | Users can tell the product about bookings already made; these become fixed anchors | 24.8, 9.3, 21.3, 22.1 |
| Gap: packing | Packing is a weather-aware, tick-off checklist | 24.5, 26.3 |
| Gap: discovery | Discovery uses budget, dates, travel time and best time to visit, and supports comparison | 10.5 |
| Gap: experiences | Experiences are first-class, detailed itinerary items, not just app mentions | 11.4, 19.1 |
| Additions from the Functional Requirements Document | Accounts, privacy, readiness checklist, feedback and reporting, undo, KPIs, non-functional requirements, data sources, data model, risks | 38 |
| Decision round (v1.2) | Open product decisions resolved and recorded; affected sections updated | 37.1 |

---

## 1. Product Overview

The AI-Powered Agentic Trip Planner is a consumer travel-planning product that helps travellers research, plan, and organize complete trips using real-time information from the internet.

The product acts as a **knowledgeable local friend** — it researches destinations autonomously, synthesizes information from scattered sources, builds realistic day-by-day itineraries, recommends flights, trains and buses, accommodation, restaurants, attractions, and experiences, and produces a polished interactive travel guide with an exportable printable magazine.

The product is **agentic**: it performs multi-source research, reasons over information, makes planning decisions, identifies trade-offs, asks the user when decisions require human judgment, and replans intelligently when constraints change.

The product is a **planning tool, not a booking platform**. It recommends and informs. It may provide links to booking sites but does not handle transactions. Travellers can tell the product about bookings they have already made, and the product plans around them.

---

## 2. Problem Statement

Planning a trip today is a fragmented, time-consuming process. A traveller researching a destination typically consults 5–10 different sources — search engines, travel blogs, review platforms, social media, YouTube, forums, maps — spending 8–15+ hours across multiple sessions to assemble a coherent plan.

The problems with this process:

1. **Information is scattered.** Useful knowledge lives across dozens of sources with no single synthesized view.
2. **Recommendations are generic.** Most travel content surfaces the same popular attractions with little personalization.
3. **Planning is manual.** The user must assemble logistics — routing, timing, proximity, meal breaks, opening hours — by hand.
4. **Output is messy.** The result is bookmarks, screenshots, notes, and spreadsheets that are hard to use while travelling.
5. **Real-time information is hard to find.** Opening hours change, prices increase, attractions close temporarily, and events happen on specific dates — none of which is reflected in static travel content.

The product solves all five problems by performing the research, reasoning, and planning work that the traveller currently does manually — and producing a usable, beautiful, and trustworthy trip plan.

---

## 3. Product Vision

**Be the one place a traveller goes to plan an entire trip — from "I want to go somewhere" to "here's your complete, personalized, printable travel guide."**

The product should deliver the experience of having a well-travelled, knowledgeable friend who:

- Knows the destination deeply — the famous highlights *and* the places only locals know
- Understands your interests, pace, budget, and travel style
- Does all the research for you and synthesizes it
- Builds a realistic, executable plan — not a wish list
- Tells you what to pack, what visa you need, what apps to download
- Gives you honest advice — including what to skip and what to watch out for
- Hands you a beautiful travel guide you can carry with you

---

## 4. Target Users

### Primary audience

The product is designed for a **broad consumer audience** across all travel-experience levels. The majority of users are expected to be **relatively inexperienced planners** — people who find trip planning overwhelming, time-consuming, or tedious and want the product to do the heavy lifting.

A smaller cohort will be **moderately experienced or experienced travellers** who are capable of planning themselves but want a faster, smarter tool that surfaces things they wouldn't find on their own and saves them hours of research.

### User archetypes

| Archetype | Description | Primary need |
|---|---|---|
| **First-timer** | Has never visited the destination; doesn't know where to start | Comprehensive guidance — what to see, where to stay, how to get around |
| **Time-pressed planner** | Knows they want to travel but has limited time to research | Speed — a good plan quickly, refined as needed |
| **Discovery-seeker** | Wants more than the obvious tourist attractions; values unique, local experiences | Depth — genuinely interesting, offbeat recommendations they can't find on TripAdvisor |
| **Group organizer** | Planning a trip for family, friends, or others | Balancing multiple people's needs; shareable plan |
| **Gift planner** | Planning a trip for someone else (parents, partner, friend) | Ability to plan for a different traveller's preferences |

### The product treats all users at the same level

There are no separate "beginner" or "expert" modes. The product adapts through the user's stated interests, preferences, and refinement interactions rather than through explicit experience-level segmentation.

---

## 5. User Needs

| Need | Description |
|---|---|
| **Consolidated research** | All relevant destination information in one place, synthesized and organized |
| **Personalized recommendations** | Suggestions that reflect the traveller's interests, pace, budget, and group composition — not a generic list |
| **Discovery of the non-obvious** | Experiences, places, and moments that the traveller wouldn't find through standard search |
| **Realistic planning** | An itinerary that a real human can actually follow — with sensible timing, geography, rest, and meals |
| **Complete trip coverage** | Not just "what to do" but also how to get there, where to stay, where to eat, what to pack, what documents to prepare |
| **Trustworthy information** | Accurate, current details — or honest acknowledgment when information can't be verified |
| **Beautiful, usable output** | A travel guide worth reading and carrying — not chatbot text or a spreadsheet |
| **Easy modification** | The ability to change the plan without starting over |
| **Offline reference** | A printable guide that works without connectivity while travelling |

---

## 6. Jobs to Be Done

| Job | Situation | Outcome |
|---|---|---|
| **Plan a complete trip from scratch** | "I want to visit Japan for 10 days. I don't know where to start." | A complete multi-city itinerary with flights, hotels, restaurants, activities, and a printable guide |
| **Discover what's worth seeing** | "I'm going to Lisbon. What should I actually do there beyond the obvious?" | A curated mix of must-see highlights and genuinely offbeat local experiences, with explanations of why each is worth visiting |
| **Build a realistic day-by-day plan** | "I have 4 days in Rome. How do I organize my time?" | A balanced, geographically optimized, time-aware itinerary with meals, rest, and practical logistics |
| **Plan a trip for someone else** | "My parents are visiting Barcelona. They're in their 60s, love history and food." | A plan tailored to someone else's preferences, saved as a traveller profile for future trips |
| **Modify a plan when things change** | "We added a day" / "Remove that museum" / "Make it more relaxed" | Intelligent replanning that preserves good decisions and adapts to the change |
| **Get a travel guide I can carry** | "I want something I can print and use on the trip without internet." | A polished, printable travel magazine with all the information needed to execute the plan |
| **Prepare for travel logistics** | "What do I need to know before I go?" | Visa requirements, packing essentials, recommended apps, local transport guidance, currency/tipping info |

---

## 7. Core User Journeys

### Journey 1: First-time complete trip planning

```
User opens product
  → Enters freeform intent: "10 days in Japan, I love food and temples"
  → Sees tappable interest tags; selects "Food," "History," "Culture"
  → Product asks two quick, skippable questions: "Where are you travelling from?" and "Which passport will you travel on?" (saved to the traveller profile so they are asked only once)
  → Product generates the complete plan (guests see the outline and Day 1 as a preview, then sign in to see the rest; Section 37.1):
      - Suggested ways to get there from the user's origin city (flights, trains or buses, whichever fits best)
      - Recommended cities: Tokyo (4 days), Kyoto (4 days), Osaka (2 days; shown as a choice, see below)
      - Hotel area recommendations per city
      - Day-by-day itinerary with attractions, experiences, meals, time-of-day notes
      - Tourist highlights + offbeat local experiences
      - Weather-aware packing checklist, visa info, recommended apps
  → Product presents the Osaka decision as a choice: "Osaka is about 30 minutes from Kyoto by train. I'd recommend a day trip so you avoid a hotel change, or you can stay 2 nights there. Which do you prefer?" (the day-trip option is shown as "Proposed" until confirmed)
  → User picks the day trip; product replans only the affected days (Kyoto-based for 6 days, including two Osaka day trips)
  → User reviews interactive guide
  → Product suggests refinement: "I included several temple visits — would you like more variety?"
  → User: "Add more street food experiences, make Day 3 more relaxed"
  → Product replans affected days
  → User exports printable magazine
  → User shares plan link with travel companion
```

### Journey 2: Quick single-city plan

```
User enters: "3 days in Lisbon"
  → Product asks: "What kind of experiences are you most excited about?"
  → User taps: "Food," "Architecture," "Local culture"
  → Product generates 3-day Lisbon itinerary
  → Includes named restaurants, neighborhood walks, local markets, major landmarks
  → User locks Belém Tower on Day 2, removes a recommended museum
  → Product replans Day 2 around locked attraction, fills gap with nearby alternative
```

### Journey 3: Planning for someone else

```
User enters: "Plan a trip for my parents to Prague, 5 days. They're in their 60s, love classical music and history. Moderate pace."
  → Product creates plan tailored to the described preferences
  → Product saves traveller profile "Parents" for future use
  → User reviews, adjusts, exports, and shares the guide with parents
```

### Journey 4: Impossible or constrained request

```
User enters: "1 day in all of Japan"
  → Product responds honestly: "One day isn't enough to experience multiple cities in Japan. Here's what I'd recommend instead:"
      - Option A: "Spend your day in Tokyo — here's a packed single-day itinerary"
      - Option B: "If you have flexibility, even 3 days would let you experience Tokyo and a day trip to Kamakura"
  → User selects Option A
  → Product generates focused single-day Tokyo plan
```

### Journey 5: Trip by train with an existing booking

```
User enters: "4 days in Prague from Vienna. I've already booked a hotel near Wenceslas Square for the first 3 nights."
  → Product records the hotel as a fixed anchor (Section 24.8)
  → Product asks for nationality only if it does not already have it (for entry requirements)
  → Product compares ways to get from Vienna to Prague:
      - Train: about 4 hours, centre to centre, comfortable, recommended
      - Bus: slightly longer, usually the cheapest
      - Flight: shorter in the air but slower door to door once airport transfers and security are counted
  → User picks the train; product recommends reserving a seat, names the stations and explains how to reach the hotel
  → Product builds the 4-day plan around the booked hotel and suggests where to stay for the 4th night
  → Product includes a guided evening food tour with meeting point, duration, what's included and how to book
  → Product notes that it cannot verify the booking details the user provided
```

---

## 8. Product Principles

These principles guide product decisions when requirements conflict or when the team faces trade-offs.

### 8.1 Be a knowledgeable friend, not a search engine

The product should feel like advice from someone who knows the destination — opinionated, curated, and honest. It should not feel like search results, a database query, or a generic AI response.

### 8.2 Quality over quantity

A plan with 5 excellent, well-explained recommendations per day is better than a plan with 15 superficial ones. The product should prioritize depth and quality of each recommendation over coverage.

### 8.3 Honest over impressive

If the product can't find genuinely offbeat recommendations, it should say so. If information can't be verified, it should tell the user to verify directly. If a request is unrealistic, it should say why and suggest alternatives. The product should never fake quality, fabricate "hidden gems," or pad itineraries with mediocre content.

### 8.4 Executable over aspirational

Every itinerary must be something a real human can physically follow. Timing, geography, fatigue, meals, opening hours, and logistics must be realistic. A beautiful but impractical plan is a product failure.

### 8.5 Fast to value, deep on demand

The product should generate a useful plan quickly with minimal input, then allow the user to refine and deepen progressively. It should never require a lengthy questionnaire before showing any output. Origin city and nationality are one-tap, skippable questions saved to the profile; they must not block the first plan. Guests see the preview described in Section 37.1 before signing in.

### 8.6 Stable on edit

When the user makes a change, the product should modify the minimum necessary to accommodate the change while preserving decisions the user has already implicitly or explicitly accepted. The plan should not completely regenerate on every small edit.

### 8.7 Prescriptive, not alarming

Warnings, safety notes, and practical advice should be delivered as helpful, friendly guidance — the way a friend would tell you "bring cash, they don't take cards" — not as liability disclaimers or alarming alerts.

---

## 9. User Inputs and Traveller Preferences

### 9.1 Initial input

The product accepts **freeform natural-language input** describing the travel intent. The product must parse and understand a wide variety of input forms, including but not limited to:

| Input type | Example |
|---|---|
| Specific city + duration | "5 days in Barcelona" |
| Country or region | "A week in Portugal" |
| Multiple cities | "10 days — Tokyo, Kyoto, and Osaka" |
| Open-ended destination | "Beach vacation in Southeast Asia, 10 days" |
| Layover / short stop | "6-hour layover in Istanbul" |
| Planning for others | "My parents are visiting Berlin for 3 days, they love history" |
| Interest-rich | "I want a foodie trip to Tokyo with lots of street food and local markets" |
| Minimal | "Lisbon, 4 days" |

When the input specifies a **country or region** rather than a specific city, the product should perform destination discovery — recommending specific cities or destinations within that region before building the itinerary.

When the input is **open-ended** (no specific destination), the product should suggest destinations that match the stated preferences.

### 9.2 Interest capture

After the initial input, the product should capture the user's interests to personalize the first output. Interest capture follows a **dual approach**:

1. **Infer from the freeform input** — if the user says "foodie trip to Tokyo," the product infers food as a primary interest without asking.
2. **Show tappable interest tags** — when the input does not express clear interests (e.g., "Lisbon, 4 days"), the product presents a set of selectable interest categories alongside or immediately after the input.

**Interest categories** (indicative, not exhaustive):

- Food & Dining
- History
- Art & Museums
- Architecture
- Nature & Outdoors
- Adventure
- Local Culture
- Shopping
- Nightlife
- Photography
- Relaxation / Wellness
- Family Activities
- Workshops & Classes
- Festivals & Events

The user should be able to select **multiple interests** and skip the selection entirely (in which case the product generates a balanced default plan).

Interest capture must remain **lightweight** — it should feel like a quick personalization step, not a survey. It must not create friction or delay the first output.

### 9.2A Essential logistics inputs: origin city and nationality

Two inputs are needed early because the first plan depends on them: **origin city** (where the traveller starts from) and **nationality / passport** (for visa and entry guidance). Both are captured at the start rather than left to refinement.

- **Lightweight.** They are presented as two quick, optional questions in the same step as the interest tags. They are inferred from freeform input where possible (e.g. "from Pune", "travelling on an Indian passport") and never asked twice.
- **Saved.** Once given, they are stored in the user's account and traveller profile as defaults for future trips. When planning for someone else, the product asks for that person's nationality, since their visa needs may differ from the planner's.
- **Skippable.** If the user skips them, the product still generates the full itinerary without delay. The getting-there and visa sections show a prompt instead (e.g. "Add your starting city to see the best way to get there"). Once supplied, only the affected sections are updated; the itinerary is not regenerated.
- **Layovers.** Nationality also drives transit-visa notes for layover itineraries.

### 9.3 Additional inputs accepted during refinement

After the first plan is generated, the product should accept the following as conversational or structured input during the refinement phase:

| Input | Effect |
|---|---|
| Origin city / starting location | Normally captured at the start (Section 9.2A); editable here. Enables flight, train and bus suggestions and arrival planning |
| Travel dates (specific or approximate) | Enables seasonality-aware recommendations, event detection |
| Budget level (budget / moderate / luxury) | Adjusts hotel, restaurant, and experience recommendations |
| Travel pace (relaxed / balanced / packed) | Adjusts number of activities per day |
| Group composition (solo / couple / family / friends / group size) | Adjusts recommendation suitability |
| Children's ages | Adjusts for child-friendly activities |
| Dietary restrictions | Adjusts restaurant recommendations |
| Mobility or physical constraints | Adjusts for physical accessibility (future scope; see Section 29) |
| Places already visited | Excludes from recommendations |
| Places explicitly requested | Includes and plans around them |
| Places explicitly rejected | Excludes and replaces |
| Accommodation preferences (area, type) | Adjusts hotel recommendations |
| Nationality / passport | Normally captured at the start (Section 9.2A); editable here. Enables visa and entry guidance |
| Preferred way of getting there | e.g. "I'd rather take the train" or "no night buses"; adjusts the transport comparison (Section 24.1) |
| Existing bookings | Flights, trains, buses, hotels, tours, tickets or reservations already made (Section 24.8); treated as fixed anchors |
| Weather preference | e.g. "somewhere warm", "avoid monsoon"; used in destination discovery (Section 10.5) and packing |

### 9.4 Traveller profiles

The product should support **saved traveller profiles**. When a user plans a trip for someone else (or for themselves), the product should:

1. **Ask for relevant preferences** the first time.
2. **Save the profile** (name, interests, pace, dietary restrictions, group composition defaults, home city, nationality).
3. **Reuse the profile** for future trip planning — the user can say "plan this for Mom" and the saved profile is applied.

Profiles must be editable and deletable. A user can have multiple saved profiles (e.g., "Me," "Parents," "Family with kids").

---

## 10. Destination Discovery

### 10.1 City-level input

When the user provides a specific city, the product proceeds directly to research and planning for that city.

### 10.2 Country or region-level input

When the user provides a country, region, or vague geographic intent (e.g., "a week in Portugal," "Southeast Asia," "somewhere warm in Europe"):

1. The product should **research and recommend specific destinations** within that geography.
2. Recommendations should be personalized based on stated interests and travel style.
3. Each suggested destination should include a brief explanation of **what makes it worth visiting** and **how it differs** from the other suggestions, along with the decision data in Section 10.5.
4. The user should be able to **select one or multiple destinations** from the suggestions.
5. For multi-destination selections, the product proceeds to multi-city planning (see Section 20).

### 10.3 Open-ended input

When the user provides no specific geography (e.g., "I want a beach vacation for a week"):

1. The product should suggest **specific destinations** matching the described intent.
2. Suggestions should span different regions/countries where appropriate to give the user genuine choice.
3. Each suggestion should explain **why it matches** the user's stated preferences.

### 10.4 Destination knowledge limitations

If the product cannot find sufficient information about a requested destination to build a quality plan:

- It must **honestly say so** rather than generating a plan padded with low-quality or fabricated content.
- It should suggest **nearby or alternative destinations** where it can provide better guidance.
- It should explain what it *can* provide for the requested destination and what gaps exist.

### 10.5 Discovery criteria, decision data and comparison

Destination discovery (Sections 10.2 and 10.3) is guided by the criteria below and presents the data a traveller needs to choose between options.

**Criteria used to rank suggestions.** All are optional, inferred from the freeform input where possible, and offered as tappable chips rather than a form (Section 8.5):

- Budget level
- Travel dates, month, or "flexible"
- Trip length
- Origin city (Section 9.2A), used for travel time and cost of getting there
- Interests and travel style
- Weather or climate preference
- Group composition and trip type (e.g. honeymoon, family, solo)
- Visa ease for the traveller's nationality
- Crowd tolerance

**Decision data shown with each suggestion.** Subject to the "verify directly" rules in Section 16:

| Data | Description |
|---|---|
| **Best time to visit** | Month-by-month suitability (weather, crowds, price level, notable events), with a clear verdict for the user's dates and a better alternative month where relevant |
| **Typical cost** | Approximate cost per day for the selected budget level and a rough trip total, marked as approximate |
| **Getting there** | Modes available from the user's origin (flight, train, bus), approximate door-to-door travel time and a cost band |
| **Weather for the dates** | Typical conditions for the travel dates (forecast when the dates are close enough) |
| **Visa ease** | Indicative entry requirements for the user's nationality (verify with official sources) |
| **Crowd level and seasonality** | Whether the dates fall in peak, shoulder or low season |
| **Suggested trip length** | How many days the destination deserves |
| **Why it matches** | The explanation required in Sections 10.2 and 10.3 |

**Comparison.** The user can shortlist up to four destinations and view them side by side on the data above. The product gives an opinionated recommendation with trade-offs, in line with Section 8.1. Selecting one or more destinations proceeds to planning (Section 20 for multi-city).

**Refinement.** The user can adjust discovery with prompts such as "cheaper," "closer," "warmer," "less crowded" or "different month." Results are re-ranked, not regenerated from scratch.

**Inspiration.** For open-ended input, the product can also offer seasonal and themed ideas (e.g. long weekends, food trails, beaches) and a "surprise me" option that respects the stated constraints.

**Honesty.** If reliable cost, weather or travel-time data cannot be found for a destination, that data point is omitted and flagged rather than guessed.

---

## 11. Tourist Attraction Recommendations

### 11.1 Definition

A **tourist attraction** is defined as a place or experience that meets either or both of the following criteria:

- **High visitor volume**: The place attracts significant tourist traffic.
- **Standard list presence**: The place appears on mainstream "top things to do" lists, major travel publications, and widely referenced travel guides for the destination.

### 11.2 Recommendation behaviour

- Tourist attractions should be included in the plan by default, prioritized based on the user's interests, available time, and the product's editorial judgment.
- The product should **not simply reproduce a "top 10" list**. It should curate based on the specific traveller's interests, available time, and the product's assessment of experience quality.
- Each tourist attraction recommendation must include context that goes beyond the name and generic description (see Section 11.3).
- The product should apply **editorial judgment** about which famous attractions are genuinely worth the time and which are overrated — and should be willing to recommend skipping or limiting time at a famous place if it doesn't match the traveller.

### 11.3 Information per tourist attraction

Each tourist attraction recommendation should provide **adaptive information** based on the type of attraction. For a structured formal attraction (museum, monument, park), the recommendation should include:

| Information | Requirement |
|---|---|
| **What it is** | A substantive description — not a one-line definition but an explanation of what makes it notable |
| **Why visit** | Specific reasons this attraction is worth the traveller's time, tailored to their interests |
| **Who it's best for** | Interest types, group types, age ranges that would most enjoy it |
| **Who it's not ideal for** | Honest guidance about who might want to skip it and why |
| **What to see/do there** | Specific highlights within the attraction — what to focus on, what to skip if short on time |
| **Honest trade-offs** | Queue expectations, crowd levels, whether the reality matches the hype |
| **How to get there** | Practical directions from likely previous location in the itinerary |
| **Approximate travel time** | From the previous planned activity |
| **Opening hours** | Current hours; marked "verify directly" if uncertain |
| **Entry fees** | Current pricing; marked "verify directly" if uncertain |
| **Booking requirements** | Whether advance booking is needed, how far in advance, and relevant apps/websites |
| **What's included with tickets** | If a ticket includes access to multiple areas, guided tours, etc. |
| **Expected visit duration** | Recommended time to spend |
| **Best time to visit** | Time of day, day of week, season — with explanation |
| **Practical tips** | What to bring, what to wear, what to expect |
| **Restrictions** | Photography rules, dress codes, age restrictions, prohibited items |
| **Current status** | Any known temporary closures, renovations, or schedule changes; marked "verify directly" if uncertain |
| **Prescriptive warnings** | Scam alerts, tourist-trap avoidance, safety-relevant notes — in a friendly, prescriptive tone |
| **Apps for tickets/access** | If there's a specific app for booking or accessing the attraction |

**Not all fields apply to all attractions.** The product must adapt the information shown based on the type of experience. An open-air market does not need "entry fees" or "booking requirements." A sunset walk does not need "opening hours." The product should never display empty or N/A fields; it should simply omit inapplicable information.

### 11.4 Experiences and activities

**Experiences are first-class itinerary items.** Guided tours, food tours, cooking classes, workshops, adventure and nature activities, wellness sessions, performances, festivals and local events are planned and presented like attractions and meals. They are not reduced to a mention of an app or booking site. Each experience:

- Occupies a time slot and counts toward the day's pacing (Section 19.3)
- Has travel time from the previous activity
- Can be locked, swapped, moved, rejected or marked as visited (Section 22.1)
- Is ranked under Section 14 and classified as tourist or offbeat under Sections 11 and 12
- Appears in the printable magazine with full detail (Section 26.3)

**Information per experience.** Adaptive, as in Section 11.3. Applicable fields are shown and the rest omitted:

| Information | Requirement |
|---|---|
| **What it is and what happens** | A substantive description of what the traveller actually does, not just a title |
| **Why it's worth it** | Specific reasons for this traveller's interests |
| **Type** | Guided tour, class, workshop, adventure, wellness, performance, event or festival, excursion, or self-guided moment |
| **Who runs it** | Operator or venue type and signals of reputability |
| **Duration and schedule** | Typical start times, days it runs, seasonal availability |
| **Group size and format** | Private or shared, typical group size, languages offered |
| **What's included and not included** | Equipment, food, transport, tickets, guide |
| **Approximate price** | Per person, marked "verify directly" where uncertain |
| **How to book** | Whether booking is needed, how far in advance, the operator's website or phone, and the cancellation policy where known. The product links out and does not process the booking |
| **Meeting point and logistics** | Where to meet, how to get there, when to arrive, what to bring and wear |
| **Difficulty, fitness and age suitability** | Honest guidance on who it suits and who should skip it |
| **Weather and season dependence** | What happens in poor weather and the backup option (Section 19.7) |
| **Safety and ethics** | Safety notes; flags for animal-welfare concerns, overcrowded operators or low-benefit-to-community tours |
| **Honest trade-offs** | Upselling, tourist-trap risk, group size, whether reality matches the hype |
| **Free or self-guided alternative** | Where one exists, so the traveller can choose |
| **Fit with the day** | What comes before and after, and the energy it requires |

**Bookable and non-bookable experiences.** The product distinguishes experiences that need advance booking from free or self-guided ones. An experience that needs significant advance booking follows the "ask the user" rule in Section 21.1. If the traveller has already booked it, it appears as a booked, fixed item (Section 24.8).

**Events and festivals.** Local events, festivals and seasonal happenings that overlap the travel dates are surfaced as experiences, with a note when they affect crowds, prices or closures.

---

## 12. Offbeat / Hidden-Gem Recommendations

### 12.1 Definition

An **offbeat or hidden-gem experience** is defined as a place, activity, or moment that meets the following criteria:

- **Known primarily to locals** — not prominently featured in mainstream travel guides, major review platforms, or standard tourist itineraries.
- **A type of experience tourists rarely have** — it offers something genuinely different from the standard tourist experience: a local market, a neighborhood ritual, a family-run workshop, a specific street at a specific time, a local swimming spot, a community event.

### 12.2 Classification integrity

The product must maintain **honest classification**:

- A moderately popular attraction that simply isn't the #1 tourist sight must **not** be labeled as a "hidden gem."
- If the product cannot find genuinely offbeat recommendations for a destination, it must **honestly acknowledge this** rather than relabeling less-famous tourist attractions.
- The product should **explain why** it has classified something as offbeat (e.g., "This neighborhood bakery doesn't appear on any major travel sites — it was found through local food blogs and community recommendations").

### 12.3 Offbeat recommendation quality

- Offbeat recommendations should be **genuinely interesting and worth the traveller's time** — not obscure for the sake of obscurity.
- They should provide an experience that **adds something the tourist attractions don't** — local perspective, cultural depth, authenticity, novelty, or a memorable moment.
- The product should explain **what makes the experience special** and **what to expect** — because the user can't verify an unknown place through their own prior knowledge.

### 12.4 Balance between tourist and offbeat

- The initial plan should include **both tourist and offbeat recommendations by default**.
- The default balance should lean toward tourist attractions for unfamiliar destinations (the user needs to see the highlights) with meaningful offbeat additions.
- Users should be able to **adjust the balance** during refinement (e.g., "more offbeat," "fewer tourist traps," "I want only local experiences").

### 12.5 Information per offbeat recommendation

Offbeat recommendations follow the same **adaptive information depth** as tourist attractions (Section 11.3) but with additional emphasis on:

- **Why it's offbeat** — the classification explanation
- **What to expect** — since the user likely has no prior mental model of this place
- **How to find it** — offbeat places may not have obvious signage or Google Maps presence
- **Confidence level** — if information about the place is limited, the product should note this honestly

---

## 13. Recommendation Personalization

### 13.1 Core personalization principle

Changing a meaningful input or constraint should produce a **materially different plan** — not the same plan with different wording. Two users with different interests visiting the same city for the same duration should receive meaningfully different itineraries, not identical plans with minor substitutions.

### 13.2 Factors that should influence recommendations

The following factors, when provided by the user, should materially change which recommendations are included, how they are prioritized, and how the itinerary is structured:

| Factor | Impact |
|---|---|
| **Interests** (food, history, art, nature, etc.) | Determines which types of experiences are prioritized and which are deprioritized or excluded |
| **Travel pace** (relaxed / balanced / packed) | Changes the number of activities per day and the amount of buffer/exploration time |
| **Budget** (budget / moderate / luxury) | Affects hotel recommendations, restaurant selections, and whether expensive paid attractions are included |
| **Group composition** (solo / couple / family / friends) | Affects the type of experiences recommended (nightlife for friends, family-friendly for kids) |
| **Children's ages** | Strongly affects recommendations — toddler-friendly is different from teenager-friendly |
| **Dietary restrictions** | Directly affects restaurant recommendations |
| **Available time** | Shorter trips prioritize must-sees; longer trips include more offbeat and niche experiences |
| **Places already visited** | Excluded from recommendations |
| **Places explicitly rejected** | Excluded; product learns what the user doesn't want |
| **Season of travel** | Affects seasonally dependent activities, weather-sensitive outdoor experiences, and local events |

### 13.3 Personalization without explicit input

When the user provides minimal input (destination + days + a few interests), the product should still produce a personalized-feeling plan by:

- Curating a **diverse mix** rather than dumping all attractions
- Including editorial commentary that demonstrates **knowledge and opinion**
- Structuring the days **intelligently** (geography, timing, pacing) rather than randomly
- Including both tourist and offbeat recommendations by default
- Adapting language, tone, and emphasis to the stated interests

---

## 14. Recommendation Ranking and Prioritization

### 14.1 Ranking philosophy

The product should rank and prioritize recommendations like a **knowledgeable local friend**, not like a popularity algorithm. This means:

- A famous attraction is not automatically the top priority if it doesn't match the user's interests.
- A lesser-known experience may be ranked above a famous one if it's uniquely aligned with what the user cares about.
- The product should be willing to recommend **skipping** or **limiting time** at a popular attraction when it conflicts with the user's interests or available time.

### 14.2 Ranking factors

The product should consider the following factors when deciding what to include and how to prioritize, roughly in order of importance:

1. **Alignment with user's stated interests** — the strongest signal
2. **Experience quality** — is this genuinely worth the time, regardless of fame?
3. **Time efficiency** — how much of the day does this consume relative to the value it delivers?
4. **Geographic practicality** — does it fit logically into a day's routing?
5. **Uniqueness** — does this offer something the traveller can't get elsewhere?
6. **Cultural significance** — is this important for understanding the destination?
7. **Time-of-day suitability** — is there an optimal time that aligns with the itinerary?
8. **Seasonality and current availability** — is this experience at its best right now?
9. **Popularity and reputation** — general consensus on quality (but not the dominant factor)

### 14.3 Trade-off handling

When the product faces trade-offs between recommendations:

- A highly rated place that consumes half a day should be **evaluated against what the traveller would miss** — not automatically included because of its rating.
- An attraction that is geographically inefficient (far from the day's cluster) should be **deprioritized unless it's uniquely valuable** — in which case the product should plan a dedicated trip to that area.
- The product should **prefer depth over breadth** — spending quality time at fewer places is better than rushing through many.

### 14.4 The product should be able to explain its ranking

When a user asks why something was included, excluded, or ranked in a particular position, the product should provide a clear explanation (e.g., "I included this because it aligns with your interest in local food culture and it's best visited in the morning, which fits your Day 2 route. I excluded X because it requires a half-day commitment and doesn't match your stated interests.").

---

## 15. Real-Time Web Research

### 15.1 Core research behaviour

The product should research destinations and recommendations using **current information from the internet** rather than relying primarily on static or pre-stored travel data.

### 15.2 Research scope

For each destination and recommendation, the product should research:

- Current attraction information (hours, prices, status, booking requirements)
- Restaurant information (operating status, hours, cuisine, price range)
- Transportation options and logistics
- Accommodation areas and hotel options
- Local events, festivals, or seasonal activities relevant to the travel dates
- Temporary closures, renovations, or changes
- Visa requirements and travel advisories
- Practical travel information (currency, tipping, apps, transport cards)
- Offbeat and local experiences beyond mainstream travel content

### 15.3 Multi-source research

The product should consult **multiple sources** for important facts rather than relying on a single source. When facts are consistent across sources, the product should present them confidently. When facts conflict, see Section 16.

### 15.4 Research depth expectations

The product's research should go **beyond what a simple search query returns**:

- It should find information that requires following multiple links, reading local blogs, checking official websites, and synthesizing information across sources.
- For offbeat recommendations specifically, the product should research **local-language sources, community forums, food blogs, and niche travel content** — not just the first page of English-language search results.
- The product should discover **time-specific events, seasonal activities, and local happenings** that generic travel guides don't cover.

---

## 16. Information Freshness and Verification

### 16.1 Information confidence model

The product should internally assess the **confidence** of each piece of information it presents:

- **High confidence**: Information confirmed across multiple reliable sources or from an official source. Present it directly.
- **Moderate confidence**: Information from a single source or a source that may not be current. Present it with a note to "verify directly" with the venue/attraction.
- **Low confidence or conflicting**: Multiple sources disagree or no recent source is available. **Omit the specific data point** and advise the user to verify directly.

### 16.2 User-facing behaviour

- The product should **omit information it cannot verify** rather than guessing or presenting best-effort data.
- When a data point is omitted, the product should include a clear note: "Verify [hours/prices/availability] directly with [venue name] before visiting."
- The product should **never present uncertain information as established fact**.

### 16.3 Volatile information

The following types of information are inherently volatile and should always include a "verify directly" note unless sourced from an official website that appears current:

- Entry prices
- Opening hours (especially seasonal hours)
- Booking requirements
- Temporary closures or renovations
- Event schedules
- Restaurant operating status

### 16.4 Information that cannot be found

When the product cannot find specific information (e.g., prices for a small local attraction, hours for a neighborhood market):

- It should say so clearly: "Pricing information is not available online — check locally."
- It should **still recommend the place** if the experience value is high — missing details about a great recommendation are better than omitting the recommendation entirely.

---

## 17. Sources and Trust

### 17.1 Source visibility

The product presents information **in its own curated editorial voice**, without visible source attributions. It should read like a travel magazine, not a research report.

### 17.2 Product ownership of information

Because the product does not show sources, it **takes editorial ownership** of the information it presents. This means:

- The product must hold a high standard for what it presents as fact.
- When it's not confident, it must omit or qualify rather than state.
- The "verify directly" mechanism is the product's primary tool for managing information it can't stand behind completely.

### 17.3 Trust through honesty

Trust is established through the product's willingness to:

- Admit when it doesn't know something
- Admit when it can't find offbeat recommendations
- Admit when a plan isn't realistic
- Tell the user to verify volatile details themselves
- Provide honest trade-offs rather than only positive framing
- Explain why it's recommending or not recommending something

---

## 18. Geographic and Travel-Time Optimization

### 18.1 Geographic clustering

The product should group recommendations into **geographically sensible clusters** for each day. Attractions that are near each other should be visited on the same day to avoid unnecessary cross-city travel.

### 18.2 Routing intelligence

Daily itineraries should follow a **logical geographic flow** — the traveller should move through an area rather than zigzagging back and forth. The routing should account for:

- Walking distance between recommendations
- Public transit connections where walking isn't practical
- The general direction of travel through the day (e.g., north to south, centre to outskirts)

### 18.3 Geography is not the only optimization

The product must **not optimize purely for shortest travel distance**. The following factors should also influence routing:

| Factor | Influence |
|---|---|
| **Opening hours** | Some attractions must be visited at specific times, overriding geographic convenience |
| **Time-of-day suitability** | A sunset viewpoint must be in the evening regardless of geography |
| **Experience flow** | The emotional and energy arc of the day matters — don't cluster all intensive activities together |
| **Meal timing** | Lunch and dinner locations should align with where the traveller is at meal times |
| **Transportation availability** | Some areas are poorly connected; factor transit frequency and last-service times |

### 18.4 Travel time estimation

The product should provide **approximate travel times** between consecutive activities, noting the assumed mode of transport (walking, public transit, taxi/ride-share). Travel times should be realistic, accounting for:

- Actual walking distances (not straight-line)
- Transit wait times and connections
- General traffic conditions where relevant (e.g., "taxis in Bangkok during rush hour can take 45+ minutes for short distances")

### 18.5 Accommodation-aware planning

- The product should recommend **hotel areas or specific hotels** as part of the plan (see Section 24).
- Daily itineraries should consider the accommodation location as a **reasonable start and end point** for each day's activities.
- The product should recommend attractions **near the hotel** for partial days (arrival evening, departure morning).

---

## 19. Itinerary Generation

### 19.1 Day-by-day structure

The product should generate a **day-by-day itinerary** where each day includes:

- A coherent set of experiences, attractions, and meals — including bookable experiences (tours, classes, workshops, events) as full itinerary items with the detail in Section 11.4
- Geographic flow (clustered, logical routing)
- Time-of-day awareness (morning/afternoon/evening assignment)
- Meal breaks with restaurant recommendations
- Realistic timing including travel between locations
- Buffer time for exploration and spontaneity
- Notes on what makes this particular day's combination special

### 19.2 Default pacing

The default itinerary pacing is **balanced**:

- 3–4 main experiences/attractions per day
- Integrated meal breaks (lunch, dinner) with named restaurant recommendations
- Travel time between locations factored in
- Free/exploration time included — the day should not feel like a forced march
- Morning, afternoon, and evening sections with appropriate activities for each period

### 19.3 Adjustable pacing

Users should be able to change the pacing:

| Pace setting | Behaviour |
|---|---|
| **Relaxed** | 2 anchoring experiences per day; generous breathing room; time for wandering and spontaneous discovery; leisurely meals |
| **Balanced** | 3–4 main experiences; structured but comfortable; includes free time |
| **Packed** | 5–6 experiences; tightly scheduled; maximum coverage; minimal downtime |

Changing the pace should **trigger replanning** of the itinerary, not simply add or remove items from the same routing.

### 19.4 Time-of-day optimization

The product should assign activities to the **optimal time of day**:

- **Morning**: Markets, popular attractions (before crowds), east-facing viewpoints for light
- **Midday**: Indoor activities, museums, lunch
- **Afternoon**: Neighbourhood exploration, shopping, activities that work in any light
- **Late afternoon / sunset**: West-facing viewpoints, scenic walks, rooftop bars
- **Evening**: Dinner, nightlife (if relevant), illuminated landmarks, cultural performances

The product should explicitly note **time-specific experiences**: "Visit this market on Saturday morning — it only operates on weekends" or "The temple is most atmospheric at sunset when the monks chant."

### 19.5 Meal integration

- Every full day should include **lunch and dinner breaks** at realistic meal times.
- Each meal break should include **2–3 named restaurant or food recommendations** with:
  - Cuisine type
  - Approximate price range
  - Why it's recommended (e.g., "best street pad thai near this area" or "local favorite, no tourist crowd")
  - Location relative to the day's route
  - Dietary accommodation notes where relevant
- In addition to named restaurants, the product should provide **area and cuisine guidance** (e.g., "This neighborhood is excellent for seafood — look for restaurants along the harbor with outdoor seating").
- Restaurant recommendations should be consistent with the user's **budget level and dietary restrictions**.
- Named restaurants are limited to well-established places with a reliable track record. Where the product cannot confirm that a place is established and currently operating, it gives area and cuisine guidance instead of a name, so fewer than 2–3 names may be shown (Section 37.1).

### 19.6 Rest and human factors

The itinerary should account for:

- **Physical fatigue**: Don't schedule strenuous activities back-to-back
- **Decision fatigue**: Don't overload early days
- **Jet lag**: First day in a distant time zone should be lighter
- **Energy arc**: Build days with a natural rise and fall of energy
- **Rest breaks**: Especially for trips with children or elderly travellers

### 19.7 Weather-aware alternatives

Any day that depends on good weather (viewpoints, boat trips, hikes, open-air markets) should include a short **backup option** nearby, such as an indoor attraction or covered market. Alternatives are based on the weather for the travel dates (forecast when available, otherwise typical climate for the season) and appear as a brief "If it rains" note rather than a second itinerary.

---

## 20. Multi-Day and Multi-City Planning

### 20.1 Multi-day planning

For trips of multiple days, the product should:

- **Distribute experiences intelligently** across days rather than front-loading
- **Vary the character of each day** — avoid making every day feel identical
- **Build a narrative arc** over the trip — the sequence of days should feel intentionally designed
- **Consider the day of the week** — weekend activities, weekday-only experiences, Sunday closures

### 20.2 Arrival and departure days

- The product should plan **partial days** for arrival and departure:
  - **Arrival day**: Plan from the estimated arrival time, typically afternoon/evening. Recommend light activities — a neighbourhood walk, dinner, orientation.
  - **Departure day**: Plan for the morning until the estimated departure time. Recommend nearby, quick-visit experiences close to the accommodation or transit hub.
- The itinerary should display these as "Day 1: Arrive in [city]" and "Day N: Departure" with appropriate partial-day planning.
- The product should ask for or estimate **arrival/departure times** to plan these days correctly.

### 20.3 Multi-city holistic planning

When the user requests a multi-city trip, the product should provide **holistic planning** including:

| Capability | Detail |
|---|---|
| **Days-per-city recommendation** | The product should recommend how many days to allocate per city, with an explanation of why (e.g., "Kyoto has enough depth for 4 full days; Osaka's highlights can be covered in 2 days or as a day trip from Kyoto") |
| **User override** | The user can change the day allocation, triggering replanning |
| **Optimal city order** | The product should recommend the most logical city sequence based on geography, flight routes, and experience flow |
| **Inter-city transportation** | The product should recommend how to travel between cities (train, domestic flight, bus) with approximate duration and practical tips |
| **Day trips** | Where possible, the product should recommend day trips from a base city rather than moving accommodation, reducing packing/logistics overhead — but **must ask the user** before making this decision rather than assuming. The ask is presented at the moment it arises as a choice with the product's recommendation highlighted (Section 21.2). Until the user chooses, the plan shows the recommended option as provisional ("Proposed — confirm"), and only the affected days are replanned once the user decides. The user journeys follow this rule |
| **Adding/removing cities** | The product should proactively suggest cities the user should consider adding (e.g., "Nara is 45 minutes from Kyoto and worth a day") or note when a requested city may not be worth a separate stay |

### 20.4 Accommodation across cities

For multi-city trips, the product must plan **accommodation for each city segment**:

- Recommend a hotel area or specific hotels for each city where the traveller will stay overnight.
- When the traveller moves cities, the plan should account for **travel day logistics** — check-out, luggage, transit, check-in — and plan activities accordingly (lighter activity load on travel days).

---

## 21. Adaptive / Agentic Replanning

### 21.1 Agentic behaviour definition

The product behaves **agentically** — it performs research, makes decisions, and builds plans autonomously. However, it operates within boundaries:

| Behaviour | Autonomous or Ask? |
|---|---|
| Choosing which attractions to include/exclude | Autonomous |
| Deciding day-by-day ordering | Autonomous |
| Geographic grouping and routing | Autonomous |
| Setting visit durations and pacing | Autonomous |
| Balancing tourist vs. offbeat mix | Autonomous |
| Adding meal breaks and restaurant recommendations | Autonomous |
| Adding prescriptive warnings and practical tips | Autonomous |
| **Including a full-day excursion that dominates an entire day** | **Ask the user** |
| **Choosing between two equally good options that can't both fit** | **Ask the user — present as options** |
| **Recommending a day trip instead of a separate city stay** | **Ask the user** |
| **Suggesting adding or removing a city** | **Ask the user** |
| **Including an experience that requires significant advance booking** | **Ask the user** |
| **Skipping a famous attraction because it doesn't fit interests/time** | **Ask the user or explain in the plan** |

### 21.2 Trade-off presentation

When the product encounters a decision that requires user input, it should:

1. **Clearly describe the trade-off** — what each option gives and what it costs.
2. **Offer a recommendation** — the product should express its editorial opinion, not just present neutral options.
3. **Make it easy to choose** — suggested prompts/buttons, not open-ended questions.

Example: *"Day 2 has room for one more experience. I'd recommend Option A: the Tsukiji outer market for street food (aligns with your food interest), but Option B: the Meiji Shrine garden is also nearby and beautiful in autumn. Which do you prefer?"*

### 21.3 Replanning triggers

The following user actions should trigger **intelligent replanning**:

| Action | Replanning scope |
|---|---|
| Remove a recommendation | Replan the affected day — fill the gap, re-optimize timing |
| Add a specific place/experience | Replan the affected day or multiple days if needed to fit it in |
| Swap a recommendation for an alternative | Replan the affected day for timing and routing |
| Move a recommendation to a different day | Replan both the source and target days |
| Lock a recommendation | Preserve it; replan around it |
| Change the number of days | Replan the entire trip |
| Change interests or pace | Replan the entire trip |
| Change budget | Replan hotel and restaurant recommendations; adjust experience mix if needed |
| Ask for more/fewer offbeat experiences | Replan experience mix across the trip |
| Add or edit an existing booking | Re-anchor the affected days around the booking; replan only what conflicts |
| Change origin city, nationality, transport mode or arrival/departure time | Update the getting-there guidance, visa notes and the arrival/departure days only |

### 21.4 Stability during replanning

When replanning, the product should:

- **Preserve decisions the user has explicitly or implicitly accepted** — don't change everything when only one thing needs to change.
- **Minimize disruption** — change the minimum necessary to accommodate the edit while maintaining plan quality.
- **Explain what changed and why** — after replanning, briefly note what was modified and the reasoning.

---

## 22. User Editing and Control

### 22.1 Available editing actions

Users should be able to perform the following actions on the generated plan:

| Action | Description |
|---|---|
| **Remove** | Remove any recommendation from the plan |
| **Add** | Add a specific place, experience, or restaurant the user knows about |
| **Swap** | Request an alternative to a specific recommendation |
| **Move** | Move a recommendation to a different day |
| **Lock** | Fix a recommendation in place — replanning preserves it |
| **Reject** | Remove a recommendation and tell the product they don't want anything like it |
| **Reorder days** | Change the sequence of days |
| **Change days** | Add or remove days from the trip |
| **Change interests** | Update interest selections; triggers replanning |
| **Change pace** | Adjust the pacing level; triggers replanning |
| **Change budget** | Adjust budget level; triggers replanning |
| **Mark as visited** | Mark a place as already visited — exclude from future plans |
| **Ask for alternatives** | Request alternative recommendations for any slot |
| **Adjust offbeat balance** | Request more or fewer offbeat/local experiences |
| **Add existing booking** | Tell the product about a flight, train, bus, hotel, tour, ticket or reservation already made; it becomes a fixed anchor (Section 24.8) |
| **Freeform refinement** | Type any change request in natural language (e.g., "Make day 3 more relaxed," "Add more food experiences," "I don't like museums") |

### 22.2 Refinement prompts

After generating the initial plan, the product should **proactively suggest refinement options** through:

- **Tappable prompt chips** (e.g., "More food experiences," "Make it more relaxed," "Add offbeat places")
- **Contextual suggestions** based on the generated plan (e.g., "I included several museums — would you like more variety?")
- **An open text input** for freeform requests

The product should also accept freeform conversational input at any time.

---

## 23. Personalization and Memory

### 23.1 Within-session memory

During a planning session, the product should remember:

- All stated preferences and constraints
- All explicit decisions (locked, removed, accepted, rejected recommendations)
- Changes to interests, pace, or budget
- Reasons given for rejections (e.g., "I don't like museums" → deprioritize museums in alternatives)
- Clarifications and context provided during conversation

### 23.2 Cross-session persistence

The product should persist:

- **Traveller profiles** (for self and others)
- **Saved trip plans** (multiple active plans at different stages)
- **Past planning history** — the product may reference past trips to avoid repeating recommendations

### 23.3 Plan management

| Feature | Description |
|---|---|
| **Save plans** | All generated plans are saved and accessible later |
| **Multiple active plans** | Users can have several plans in different stages (draft, finalized, past) |
| **Duplicate a plan** | Create a variation of an existing plan (e.g., "Japan in spring" vs. "Japan in autumn") |
| **Share a plan** | Share a plan with others as a link or exportable document |
| **Upcoming trips** | Users can see their upcoming saved plans |
| **Undo and version history** | Undo the last replan or restore an earlier version of the plan |

---

## 24. Travel Logistics

### 24.1 Getting there and back: flights, trains and buses

The product should suggest **how to travel from the user's origin city to the destination and back** by flight, train, bus or another mode where relevant (e.g. ferry, self-drive). This applies to the main journey of the trip and not only to travel between cities within it. For flights:

- Recommend routes (direct vs. connecting where relevant)
- Indicate approximate timing for arrival/departure planning
- Provide practical notes (e.g., "Book domestic flights within Japan on [airline] — significantly cheaper than the bullet train for this route")
- Provide booking-site links for each option (Section 37.1)
- The product does **not** show real-time pricing or availability — it recommends routes and lets the user book independently

For multi-city trips, the product should recommend the optimal **arrival and departure airports or stations** (e.g., "Fly into Tokyo Narita, fly out of Osaka Kansai to avoid backtracking").

**Trains and buses.** For journeys where rail or road is practical, the product should:

- Recommend the route, the stations or terminals to use, and approximate journey time
- Note practical details: seat reservation requirements, ticket validity, luggage rules, overnight options that save a hotel night, and cross-border document checks
- Mention rail passes or travel cards when they are likely to save money, and say when they are not worth it
- Provide booking-site or operator links for each option, with the same no-transaction and no-live-pricing rules as flights
- Explain how to get from the arrival airport, station or terminal to the accommodation

**Choosing between modes.** Where more than one mode is realistic, the product compares them on door-to-door time, approximate cost band, comfort, reliability, luggage and environmental impact. It labels the options where helpful (fastest, best value, most comfortable, lowest carbon), gives plain reasoning, and makes an opinionated recommendation. Mixed journeys (e.g. train to an airport, then a flight) are supported. The user can state a preference ("I'd rather not fly") and the comparison adjusts. The chosen mode and arrival and departure times feed the arrival and departure days (Section 20.2) and the budget (Section 24.7). Inter-city legs within a trip (Section 20.3) use the same logic.

### 24.2 Accommodation recommendations

The product should recommend **where to stay** as part of the itinerary:

- Recommend **specific areas/neighborhoods** for accommodation, with explanations (e.g., "Shinjuku is well-connected by train and central for Day 1–3 activities; Gion in Kyoto is walking distance to most temples")
- Where possible, suggest **specific hotels or accommodation types** consistent with the user's budget
- For multi-city trips, recommend accommodation per city segment
- Account for the accommodation location in daily itinerary routing

The product assumes **no bookings have been made unless the user says otherwise** (Section 24.8) — by default it plans from scratch including accommodation.

### 24.3 Local transportation

The product should provide practical **local transportation guidance**:

- Recommended transport modes for the destination (metro, bus, taxi, walking, cycling)
- Transport cards or passes to purchase (e.g., "Get an ICOCA card at the airport for all trains and buses in Kansai")
- Relevant transport apps to download
- Approximate taxi/ride-share costs for common routes
- Walking feasibility notes for the destination

### 24.4 Visa and travel requirements

The product should provide:

- **Visa requirements** based on the user's nationality and destination
- **Application timeline** — how far in advance to apply
- **Required documents** — what's needed for the visa application
- **Entry requirements** — vaccination records, travel insurance, customs declarations where relevant
- Marked as "verify directly with the embassy/consulate" for all visa information, given its sensitivity

### 24.5 Packing essentials (weather-aware checklist)

The product should recommend **packing essentials** tailored to the destination and trip:

- Weather-appropriate clothing based on the expected weather for the travel dates (see below)
- Destination-specific items (e.g., "Bring a small towel — many Japanese restaurants provide hot towels but some don't"; "Comfortable walking shoes are essential — Lisbon is very hilly")
- Activity-specific items (e.g., "Bring swimwear for the onsen day trip"; "A light rain jacket — October in Kyoto is unpredictable")
- Electronics and adapters (plug types, voltage)
- Practical items (copies of documents, travel insurance info, emergency contacts)

**Weather basis.** The packing list uses the weather for the travel dates. When the dates are close enough for a reliable forecast, the product uses the forecast. Otherwise it uses typical climate for those dates (highs and lows, rainy days, humidity) and says which it is using. For multi-city trips, it accounts for differences between places (e.g. coast versus mountains). Each key item carries a short reason (e.g. "light rain jacket: October in Kyoto is often wet").

**Checklist behaviour.** Packing is presented as an interactive checklist, not a block of text:

- Items are grouped by category: documents, clothing, toiletries and health, electronics and adapters, activity-specific gear, and items for children
- The user can tick items off, change quantities, add custom items and remove items; progress is shown
- Separate lists per traveller for groups and saved profiles
- Carry-on-only and checked-luggage modes; if the user has told the product their baggage allowance (Section 24.8), it warns when the list is likely to exceed it
- Local rules where relevant: plug type and voltage, dress codes, restricted items, customs limits
- When dates, destinations or activities change, the list updates while preserving ticked and custom items (Section 8.6)
- Lists can be saved as a reusable template (e.g. "my standard toiletries")
- The printable magazine includes the checklist with tick boxes and the weather summary (Section 26.3)

### 24.6 Recommended apps

The product should recommend **apps the traveller should download** before the trip:

- **Country/city-specific apps**: Transportation apps, maps, translation apps, ride-hailing apps relevant to the destination
- **Attraction-specific apps**: Apps for booking tickets, audio guides, or accessing specific attractions
- **General travel apps**: Currency conversion, offline maps, language assistance
- Each app recommendation should briefly explain **why** it's useful

### 24.7 Budget estimation

The product should provide an **estimated budget summary** for the trip:

- Estimated daily costs broken down by category (accommodation, food, transport, activities)
- Total estimated trip cost
- Marked as approximate — actual costs may vary
- Aligned with the user's selected budget level (budget / moderate / luxury)
- Presented both as per-day ranges for the chosen budget level and as an itemised trip total by category (getting there, accommodation, food, experiences, local transport, miscellaneous), shown per person with a group total where relevant (Section 37.1)
- Shown in the user's preferred currency with an approximate conversion to the local currency, noting that rates are indicative
- Updated when the plan changes (days, pace, budget level, transport mode), and counting existing bookings at the cost the user provides, if any
- Accompanied by money tips: cards versus cash, ATM and foreign-exchange fees, and tipping norms

### 24.8 Existing bookings (user-provided)

The product assumes nothing is booked by default, but the user can tell it about bookings already made. This is **user-entered information, not a booking integration** (Section 35.2); the product does not connect to booking accounts, import emails or process transactions.

**What can be added.** Flights, trains, buses and ferries; accommodation; tours, experiences and tickets; restaurant reservations; car rental; and other fixed commitments.

**How it is entered.** In natural language (e.g. "I've booked a flight landing in Tokyo at 3 pm on 12 October") or through a simple form. Useful fields are type, provider, date and time, location, duration, an optional reference number and an optional cost. Users can edit or remove bookings at any time.

**How the product uses them.**

- Each booking becomes a **fixed anchor**, like a locked item (Section 22.1); the plan is built around it
- Booked transport sets the arrival and departure days and times (Section 20.2) and makes the product skip getting-there recommendations for that leg
- Booked accommodation becomes the start and end point for the days it covers; the product gives no hotel recommendations for those nights, but may suggest where to stay for any remaining nights and says honestly how the location shapes each day
- Booked tours, tickets and reservations are placed in the itinerary at their fixed times and shown with a "Booked" marker
- Booked costs feed the budget (Section 24.7), and a booked airline or flight feeds the baggage check in packing (Section 24.5)

**Sanity checks.** The product flags conflicts without changing the booking: overlapping commitments, a timed ticket on a day the venue is closed, a very short connection, or bookings outside the trip dates. It then suggests how to resolve them.

**Honesty.** The product cannot verify what the user enters and says so. Reference numbers are used only to populate the quick-reference card in the printable magazine (Section 26.3) and are excluded from shared views by default (Section 38.2).

---

## 25. Output / Travel Guide Experience

### 25.1 Primary output: Interactive digital guide

The primary output is an **interactive digital guide within a chat interface**:

- Users can browse, click, and interact with the plan
- Day-by-day structure with expandable sections
- Clickable recommendations with detailed information
- Interactive refinement — users can tap prompts, type changes, and modify the plan within the same interface
- The experience should feel like navigating a well-designed travel guide, not reading chat messages

### 25.2 Interactive features

| Feature | Description |
|---|---|
| **Day navigation** | Easily move between days of the itinerary |
| **Expand/collapse** | Show summary view or detailed view of each recommendation |
| **Quick actions** | Remove, swap, lock, move actions accessible on each recommendation |
| **Refinement chips** | Suggested modification prompts visible throughout |
| **Trip overview** | At-a-glance summary of the entire trip |
| **Freeform input** | Always-available text input for conversational refinement |
| **Packing checklist** | Tick-off checklist with weather summary (Section 24.5) |
| **Bookings** | View, add and edit existing bookings; booked items are marked in the itinerary (Section 24.8) |

### 25.3 Content voice

The product should write in a **warm, knowledgeable editorial voice** — like a well-written travel magazine or a message from a well-travelled friend:

- Substantive and informative, not flowery or generic
- Opinionated — willing to recommend, caution, and prioritize
- Practical — focused on what the traveller needs to know to act
- Personal — acknowledging the traveller's interests and adapting the narrative

The product should **not** write like:

- A chatbot ("Sure! Here are some suggestions!")
- A textbook ("Rome is the capital of Italy, known for its history.")
- A marketing brochure ("Discover the magic of...")
- A database query result (bare facts without context)

---

## 26. Printable Magazine Experience

### 26.1 Magazine as export

The printable magazine is an **export feature** — a downloadable, printable version of the plan designed to work as a standalone travel guide **without internet access**.

### 26.2 Magazine design principles

The printable magazine should feel like an **intentionally designed travel guide**, not a formatted printout of chat content:

- Clear visual hierarchy — headings, sections, emphasis
- Readable typography — designed for print consumption
- Information density appropriate for paper — enough detail to be useful, not so much that pages are overwhelming
- Logical page flow — the reader should be able to navigate it linearly or jump to specific days/sections
- Beautiful and worth carrying — a travel guide the user is proud to have, not embarrassed to pull out

### 26.3 Magazine sections

The printable magazine should include the following sections:

| Section | Content |
|---|---|
| **Cover page** | Destination name, trip dates, traveller name, a compelling description |
| **Destination overview** | Brief cultural/historical context — what makes this place special, what to expect |
| **Trip summary** | At-a-glance overview of all days (Day 1: Arrive, explore Gion; Day 2: Temples and tea ceremony...) |
| **Day-by-day itinerary** | Full detailed itinerary for each day — morning/afternoon/evening, with all recommendation details, restaurants, timing, and practical notes, including full experience details (meeting point, what's included, booking status) |
| **Packing and preparation** | Weather summary for the trip dates, printable packing checklist with tick boxes, visa info, travel documents needed, timeline for preparation |
| **Essential phrases** | Key local-language phrases with pronunciation guidance — greetings, "thank you," "where is...," "how much," "I'm allergic to...," dietary phrases |
| **Emergency information** | Local emergency numbers, nearest embassy/consulate, hospital information |
| **Quick-reference card** | Key addresses (hotel, airport, train station), important phone numbers, booking confirmation references (pre-filled from bookings the user has told the product about; otherwise user-fillable) |
| **Transportation guide** | How local transport works, cards/passes to buy, apps to download, taxi tips, and how to get to and from the destination (flight, train or bus options, stations and airports, arrival and departure logistics) |
| **Food guide** | Overview of local cuisine, must-try dishes, dining customs (tipping, ordering, meal times), dietary navigation tips |
| **Budget summary** | Estimated costs by category and total |
| **Recommended apps** | Apps to download with brief descriptions |
| **Personal notes** | Blank space for the traveller to annotate and add their own notes |
| **Trip recap / map** | Visual summary of all places visited across the trip |

### 26.4 Information richness

The printable magazine must be **self-contained and information-rich**:

- It should include **all the practical details** a traveller needs — the user should be able to navigate their trip using only the magazine, without going back online.
- Every recommendation should include sufficient detail: location description, directions, timing, practical tips.
- "Verify directly" notes should include the **venue's official website or phone number** where available, so the user can verify from the magazine.

### 26.5 Print readability

- Designed for standard paper sizes (A4 / Letter)
- Readable font sizes — no tiny text
- High contrast for readability
- Minimal ink usage considerations (avoid heavy dark backgrounds)
- Clear page breaks between logical sections

---

## 27. Maps and Geographic Context

### 27.1 Geographic context in the interactive guide

The interactive digital guide should provide **geographic context** for the itinerary:

- A visual or descriptive understanding of where recommendations are relative to each other
- Neighbourhood/area labels so the traveller understands the geography of the destination
- Travel time and distance between consecutive activities
- General orientation — what's north, south, central, outskirts

### 27.2 Geographic context in the printable magazine

The printable magazine should include:

- A **trip overview map** showing all locations across the trip
- **Per-day route context** — the traveller should understand the day's geographic flow
- **Neighbourhood descriptions** — so the traveller understands the character and location of each area

### 27.3 Map accuracy note

Maps, routes, and geographic representations should be **indicative and useful for orientation**, not GPS-precision navigation tools. The product should note that travellers should use a dedicated maps application for turn-by-turn navigation.

---

## 28. Edge Cases and Failure Scenarios

### 28.1 Unrealistic requests

| Scenario | Product behaviour |
|---|---|
| User requests 1 day for an entire country (e.g., "1 day in Japan") | Honestly explain that this isn't feasible. Suggest what *is* possible in 1 day (e.g., "You could have a great day in Tokyo — here's what I'd recommend"). Offer alternatives if more time is available. |
| User requests more days than the destination can fill (e.g., 10 days in a small town) | Honestly say the destination is best experienced in fewer days. Suggest a shorter stay and recommend nearby destinations to combine. Never pad with mediocre content. |
| User's interests conflict with budget (e.g., "luxury dining on a tight budget") | Flag the contradiction. Ask the user to adjust either the budget or interests. Suggest a compromise (e.g., "I can include one splurge dinner and recommend excellent affordable options for other meals"). |
| User wants too many specific attractions for the available time | Explain that fitting everything in isn't realistic. Present prioritized options and ask the user to choose. Show what would need to be cut. |

### 28.2 Information limitations

| Scenario | Product behaviour |
|---|---|
| Low-information destination | Acknowledge the limitation. Provide what's available. Suggest the user supplement with local inquiry upon arrival. Recommend nearby better-documented destinations if applicable. |
| Cannot find offbeat recommendations | Honestly state: "I wasn't able to find genuinely offbeat or local-only experiences for this destination. The recommendations below are well-known but excellent." Do not relabel tourist attractions as hidden gems. |
| Conflicting opening hours or prices across sources | Omit the specific conflicting data point. Note "verify directly" with the venue. Do not guess. |
| Temporary closure or renovation | If known, state it clearly: "[Attraction] is currently reported as closed for renovation. Verify status before planning to visit." Suggest an alternative. |
| Seasonal attraction outside season | Note that the attraction is seasonal and may not be available during the planned travel dates. Recommend alternatives. |

### 28.3 Planning edge cases

| Scenario | Product behaviour |
|---|---|
| Layover (a few hours only) | Plan a focused micro-itinerary. Factor in airport-to-city travel time, security re-entry time, and a buffer. Recommend only what's realistically achievable. Warn about cutting it too close. |
| Very long trip (3+ weeks) | Structure the trip into phases or segments. Vary the intensity. Include rest days. Avoid recommendation fatigue by varying the type and character of each segment. |
| Multi-city with tight inter-city connections | Account for travel days. Reduce activity load on travel days. Note connection logistics (luggage storage, check-out times). |
| User adds a locked recommendation that conflicts with others | Replan around the locked item. If it creates an irresolvable conflict (e.g., two places on opposite sides of the city at the same time), explain the conflict and ask the user to choose. |
| Weekend vs. weekday differences | Account for attractions that are closed on specific days. Note weekend-only markets, events, or experiences. Flag Sunday closures in destinations where they are common. |

### 28.4 Content quality failures

The product should be designed to avoid and detect the following quality failures:

| Failure | Mitigation |
|---|---|
| Repetitive recommendations (every day feels the same) | Vary the type and character of each day's recommendations |
| Generic descriptions (could apply to any destination) | Write destination-specific, detailed, opinionated content |
| Impractical timing (impossible to execute the day as planned) | Validate timing, distances, and opening hours during generation |
| Exhausting itinerary (too many activities, no breaks) | Enforce pacing constraints and include rest/meal/buffer time |
| Tourist traps presented positively | Apply honest trade-off analysis; warn about overpriced or disappointing attractions |
| Fake "hidden gems" | Apply strict offbeat classification criteria; admit when none are found |

---

## 29. Accessibility and Inclusivity

### 29.1 MVP scope

Detailed accessibility features (wheelchair access information, mobility-optimized routing, sensory disability accommodation) are **not in scope for the MVP**.

### 29.2 Future scope — accessibility

The following accessibility features should be considered for post-MVP development:

- Mobility accessibility information per recommendation (wheelchair access, elevator availability, terrain difficulty, step counts)
- Filtering recommendations by accessibility level
- Mobility-optimized routing (avoiding stairs, steep hills, long walks)
- Accessible restaurant recommendations
- Stroller-friendly itineraries for families with young children
- Elderly-traveller-friendly pacing and recommendations
- Hearing/vision accessibility information for attractions

### 29.3 Inclusivity in MVP

Even without dedicated accessibility features, the product should:

- Accept **group composition** that includes elderly travellers, young children, or mixed-ability groups and adjust the **pacing and recommendation types** accordingly
- Include **dietary restriction** support in restaurant recommendations
- Avoid **ableist language** or assumptions (not everyone can "hike to the top" or "walk for hours")

---

## 30. Notifications and Change Detection

### 30.1 MVP scope

The MVP does not include real-time notifications or push alerts about changes to a saved plan.

### 30.2 Future scope — change detection

Post-MVP, the product should consider:

- Re-checking volatile information (hours, closures, events) as the travel date approaches
- Notifying the user if a recommended attraction is now reported as closed or changed
- Detecting new events or festivals that align with the user's travel dates and interests
- Alerting the user to visa deadline reminders based on their travel dates

---

## 31. Quality Expectations

The product should be evaluated against the following quality dimensions. All are considered important:

### 31.1 Recommendation quality

- Recommendations are **genuinely interesting** — not the same list every travel blog produces
- Offbeat recommendations are **actually offbeat** — not relabeled popular spots
- The plan **feels personal** — two users with different interests for the same destination receive meaningfully different plans
- The product demonstrates **editorial knowledge and opinion** — it doesn't just list, it advises

### 31.2 Itinerary quality

- The itinerary is **executable** — a real human can follow it without running into timing conflicts, impossible logistics, or exhaustion
- Geographic routing is **sensible** — no unnecessary cross-city travel
- Pacing is **humane** — includes rest, meals, buffer time, and a natural energy arc
- Time-of-day assignments are **appropriate** — sunset activities in the evening, morning markets in the morning

### 31.3 Information quality

- Information is **accurate** — hours, prices, directions are correct when the user actually travels
- When accuracy can't be guaranteed, the product **says so** clearly
- Descriptions are **substantive and specific** — not generic filler that could apply to any destination
- Trade-offs and warnings are **honest and helpful**

### 31.4 Output quality

- The interactive guide is **beautiful, navigable, and usable** — it feels like a designed product
- The printable magazine is **worth printing and carrying** — it looks and reads like a professional travel guide
- The writing voice is **warm, knowledgeable, and editorial** — not robotic, generic, or overly enthusiastic

### 31.5 Efficiency quality

- The product **saves meaningful time** — hours of research compressed into minutes
- The first output is useful **immediately** with minimal input — time to value is short
- Refinement is **fast and intuitive** — changes don't require starting over

---

## 32. Trust, Transparency, and Limitations

### 32.1 Trust model

The product builds trust through:

- **Honesty about limitations** — admitting what it doesn't know
- **Accuracy of what it presents** — high standard for stated facts
- **"Verify directly" signals** — clear indication when the user should confirm details
- **Explanation of decisions** — ability to explain why recommendations were included or excluded
- **Offbeat integrity** — honest about when genuine offbeat recommendations aren't available
- **Prescriptive honesty** — honest trade-offs, tourist-trap warnings, practical scam advice

### 32.2 Product limitations

The product should be transparent about the following limitations:

- Information is researched from the internet and may not reflect the very latest changes
- Prices, hours, and availability are approximate and should be verified before visiting
- Restaurant recommendations are particularly volatile — the product should note this
- The product is a planning tool, not a booking service — all reservations must be made independently
- Visa information is indicative — the user should verify with official government sources
- Flight, train and bus suggestions are route and timing recommendations, not real-time booking with pricing
- Existing bookings entered by the user are taken as given; the product cannot verify them

---

## 33. Functional Requirements

### FR-1: Freeform input parsing
The product must accept and correctly interpret freeform natural-language travel intent across all supported input types (city, country, region, multi-city, open-ended, layover, planning for others).

### FR-2: Destination discovery
When the input specifies a region or country (not a specific city), the product must research and recommend specific destinations with explanations before building the itinerary. Suggestions must include the decision data and comparison capability in Section 10.5.

### FR-3: Interest capture
The product must support dual interest capture: inference from freeform input AND tappable interest tag selection. Origin city and nationality are captured in the same step (Section 9.2A).

### FR-4: Real-time research
The product must research destinations using current internet information, consulting multiple sources for important facts.

### FR-5: Tourist and offbeat classification
The product must classify recommendations as tourist or offbeat using the defined criteria and must explain offbeat classifications.

### FR-6: Adaptive recommendation depth
The product must adjust the information fields shown per recommendation based on the type of experience (formal attraction, informal experience, restaurant, moment/ritual).

### FR-7: Day-by-day itinerary generation
The product must generate a structured day-by-day itinerary with geographic clustering, time-of-day optimization, meal integration, and realistic pacing.

### FR-8: Multi-city holistic planning
The product must support multi-city trips including day allocation recommendations, optimal city ordering, inter-city transport, day trip suggestions (with user confirmation), and per-city accommodation.

### FR-9: Getting there and back (flights, trains and buses)
The product must suggest how to travel between the user's origin and the destination and back (flights, trains, buses and other modes where relevant), compare the realistic modes, and give practical timing and booking guidance (Section 24.1).

### FR-10: Accommodation recommendation
The product must recommend hotel areas or specific hotels per city, consistent with the user's budget.

### FR-11: Restaurant recommendation
The product must include meal breaks with 2–3 named restaurant recommendations per meal, plus area/cuisine guidance, consistent with the user's budget and dietary restrictions.

### FR-12: Agentic decision-making
The product must make planning decisions autonomously for standard trade-offs and pause to ask the user for high-impact decisions as defined in Section 21.1.

### FR-13: Intelligent replanning
All user edits must trigger intelligent replanning that preserves accepted decisions and re-optimizes affected portions of the itinerary.

### FR-14: Traveller profiles
The product must support creating, saving, editing, and deleting traveller profiles for the user and for others.

### FR-15: Plan management
The product must support saving, listing, duplicating, and accessing multiple trip plans.

### FR-16: Plan sharing
The product must support sharing a trip plan with others.

### FR-17: Interactive digital guide
The product must present the itinerary as an interactive, navigable digital guide within the chat interface with day navigation, expand/collapse, quick actions, and refinement prompts.

### FR-18: Printable magazine export
The product must export the plan as a printable magazine/travel guide containing all sections defined in Section 26.3, designed for print readability and offline use.

### FR-19: Visa and preparation information
The product must provide visa requirements, application timelines, packing essentials as a weather-aware tick-off checklist, recommended apps, and practical preparation guidance.

### FR-20: Budget estimation
The product must provide an estimated budget summary broken down by category.

### FR-21: Prescriptive warnings
The product must include practical warnings, scam alerts, and safety-relevant advice in a friendly, prescriptive tone.

### FR-22: Honest limitation handling
The product must honestly communicate when it cannot find offbeat recommendations, when a request is unrealistic, when a destination has insufficient information, or when constraints contradict.

### FR-23: Information uncertainty handling
The product must omit information it cannot verify and include "verify directly" guidance with venue contact information where possible.

### FR-24: Early capture of origin city and nationality
The product must capture origin city and nationality at the start (inferred or via quick optional prompts), save them to the traveller profile, and degrade gracefully when they are skipped (Section 9.2A).

### FR-25: Day-trip and city decisions
The product must present day-trip versus separate-stay decisions as a choice with a recommendation, show the recommended option as provisional until the user confirms, and replan only the affected days afterwards (Sections 20.3 and 21.1).

### FR-26: Existing bookings
The product must accept, display and plan around bookings the user reports (transport, accommodation, tours, tickets, reservations), flag conflicts, and never claim to have verified them (Section 24.8).

### FR-27: Experiences as itinerary items
The product must include experiences and activities as full itinerary items with the adaptive detail in Section 11.4, distinguishing bookable from free or self-guided options.

### FR-28: Discovery decision data and comparison
The product must support discovery by budget, dates, travel time, interests, weather and visa ease, show best-time-to-visit and cost data, and allow side-by-side comparison of shortlisted destinations (Section 10.5).

### FR-29: Weather-aware packing checklist
The product must generate a packing checklist based on the weather for the travel dates, with tick-off, custom items, per-traveller lists and a printable version (Section 24.5).

### FR-30: Accounts and privacy
The product must support account sign-up and login, guest use, data export and deletion, and the privacy controls in Sections 38.1 and 38.2.

### FR-31: Plan history and undo
The product must let users undo the last replan and restore earlier versions of a plan (Sections 23.3 and 38.4).

### FR-32: Feedback and error reporting
The product must let users report a problem with any recommendation and route reports to a review process (Section 38.5).

### FR-33: Readiness checklist and advisories
The product must provide a pre-trip readiness checklist and surface official travel advisories prominently (Section 38.3).

---

## 34. Non-Functional Product Expectations

### NFP-1: Time to first value
The product should generate a useful first plan within a reasonable time after the user provides their input and interests — the experience should feel responsive, not like a long wait. The target is a usable outline in about 15 seconds and the full plan in about 90 seconds, streamed progressively (Section 37.1, D8).

### NFP-2: Plan quality consistency
The product should produce consistently high-quality plans across different destinations, trip durations, and user profiles. Quality should not vary dramatically based on destination popularity.

### NFP-3: Research depth
The product's research should go beyond surface-level search results. For major destinations, the product should demonstrate knowledge comparable to an experienced travel writer. For minor destinations, it should honestly acknowledge limitations.

### NFP-4: Replanning speed
Edits and refinements should produce an updated plan quickly — not require re-running the entire research and planning process from scratch.

### NFP-5: Language quality
All generated content should be well-written, grammatically correct, and stylistically consistent — matching the warm, knowledgeable editorial voice defined in Section 25.3.

### NFP-6: Print output quality
The printable magazine should be visually polished and print-ready — not a raw HTML-to-PDF conversion.

### NFP-7: Scalability of destinations
The product should work for popular global destinations, moderately known cities, and less-known destinations — with honest quality scaling (better output for better-known destinations, honest limitations for obscure ones).

---

## 35. MVP Scope

### 35.1 MVP includes all core features

The MVP includes the complete feature set defined in this document:

- Freeform natural-language input with interest capture
- Destination discovery with budget, dates, travel-time and best-time-to-visit data, and comparison
- Flight, train and bus suggestions for getting to and from the destination
- Accommodation recommendations
- Tourist + offbeat recommendations with full adaptive detail
- Experience, activity, and moment recommendations (not just places), as full detailed itinerary items
- Day-by-day itinerary with time-of-day optimization and meal integration
- Multi-city holistic planning
- Agentic decision-making with user checkpoints
- Intelligent replanning on all user edits
- Traveller profiles (self + others)
- Plan saving, duplication, and sharing
- Interactive digital guide
- Printable magazine export with all sections
- Visa, weather-aware packing checklist, apps, and preparation information
- Budget estimation
- Prescriptive warnings and practical tips
- Existing bookings entered by the user, used as fixed anchors
- Supporting requirements in Section 38 (accounts, privacy, readiness checklist, undo, feedback and reporting, calendar export)

### 35.2 MVP excludes

The following are explicitly **out of scope for MVP**:

| Feature | Rationale |
|---|---|
| Booking integration | The product recommends and links; it does not handle transactions. (Bookings the user has already made can be entered manually; see Section 24.8) |
| Multiple language support | English only for MVP |
| Detailed accessibility features | Mobility routing, wheelchair access data, sensory disability accommodation — deferred to post-MVP |
| Real-time change notifications | No push alerts about changes to saved plans |
| Offline interactive guide | The interactive guide requires connectivity; the printable magazine serves as the offline reference |
| Collaborative real-time editing | Single-player planning; plans can be shared but not collaboratively edited |

### 35.3 Business model

- **Subscription-based** product in the long term
- **Fully free for all users in the MVP**; pricing and entitlements are decided after launch data (Section 37.1, D6). Usage limits apply to control cost
- No advertising revenue in MVP
- No affiliate/booking revenue in MVP (links provided for user convenience, not monetization)

---

## 36. Future Scope

The following features are identified for consideration post-MVP:

| Feature | Description |
|---|---|
| **Accessibility features** | Wheelchair access data, mobility-optimized routing, elderly/child-friendly filtering |
| **Multi-language support** | Generate plans in the user's preferred language |
| **Booking integration** | Connect to booking platforms for flights, hotels, restaurants, attractions |
| **Real-time notifications** | Alert users when saved plan details change (closures, price changes, events) |
| **Collaborative planning** | Multiple users editing and contributing to the same plan |
| **Offline interactive guide** | Downloadable offline version of the interactive guide (not just the magazine) |
| **Social features** | User reviews of the product's recommendations after travelling; community-contributed offbeat tips |
| **AI learning from feedback** | Improving recommendations based on user feedback and post-trip reviews |
| **Travel journal / trip diary** | Post-trip feature where users can record their experiences against the plan |
| **Calendar integration** | Live sync of trip plans with the user's calendar (one-time calendar export is in MVP, Section 38.4) |
| **Weather integration** | Weather for the travel dates already informs the packing checklist (MVP, Section 24.5). Future: real-time forecasting integrated into day-by-day planning and automatic replanning of outdoor activities |
| **Expense tracking** | Track actual spend against estimated budget during the trip, including splitting costs among a group |
| **Live in-trip replanning** | Adjust the plan during the trip for delays, closures or weather |
| **Near me now** | Suggest nearby food, experiences, ATMs and pharmacies during the trip |
| **Booking import** | Add bookings by forwarding confirmation emails or connecting accounts |
| **Group voting** | Group members vote on options within a shared plan (part of collaborative planning) |
| **Native mobile apps** | iOS and Android apps |
| **Partner and white-label use** | Embeddable planner for travel businesses |

---

## 37. Open Product Decisions

The following product decisions were identified during discovery but not fully resolved. Items marked **Resolved** were closed in the v1.2 decision round and are recorded in Section 37.1. The rest are design-phase items:

| Decision | Context |
|---|---|
| **Interest tag set** | The exact set and number of tappable interest tags at input needs to be defined. The list in Section 9.2 is indicative. |
| **Refinement prompt design** | The specific suggested refinement chips/prompts shown after initial plan generation need UX design. |
| **Plan sharing mechanics** | Whether sharing is link-based, in-app, view-only, or allows the recipient to duplicate and edit.**Resolved (37.1).** |
| **Traveller profile fields** | The exact data fields stored in a traveller profile need specification. |
| **Magazine visual design** | Layout, typography, cover design, section styling, and the overall visual identity of the printable magazine require design work. |
| **Budget estimation methodology** | How the product estimates costs (ranges, averages, per-person vs. per-group) needs definition.**Resolved (37.1).** |
| **Getting-there suggestion depth** | Whether flight, train and bus suggestions include airlines or operators, approximate price ranges, booking platform links, or just route/timing guidance.**Resolved (37.1).** |
| **Interactive guide component design** | The specific UI components for the interactive digital guide (cards, maps, expandable sections, quick actions) need detailed UX/UI design. |
| **"Verify directly" information** | What contact information (website, phone, address) should accompany "verify directly" notes — and how to obtain it reliably. |
| **Handling of restaurant volatility** | Named restaurant recommendations are the most likely to be outdated. Whether the product should flag restaurant info as more volatile, or limit to area guidance for less-known restaurants, needs consideration.**Resolved (37.1).** |
| **Existing booking input** | Exact fields and the balance between free text and a structured form for entering bookings (Section 24.8).**Resolved (37.1).** |
| **Subscription entitlements** | What is included in the subscription after the free launch period (e.g. number of plans, magazine exports, sharing) and how the transition is handled.**Resolved (37.1).** |
| **Launch markets** | Initial origin countries, currencies and destination coverage for launch, and how quality is communicated outside them.**Resolved (37.1).** |
| **Performance targets** | Concrete time-to-first-plan and replanning targets for technical design (Section 38.7).**Resolved (37.1).** |

### 37.1 Decision log (v1.2)

| # | Decision | Resolution | Effect on the PRD |
|---|---|---|---|
| D1 | Plan sharing | Anyone with the link can view; links are unlisted, view-only for recipients and revocable by the owner. Copying or editing a shared plan is not in the MVP | PRV-03, 38.2 |
| D2 | Getting-there depth | Route, timing, station and airport guidance, operators, and booking-site links for each option. No live pricing or availability | 24.1, FR-9 |
| D3 | Budget method | Per-day ranges by budget level plus an itemised trip total by category. Shown per person with a group total for multi-traveller trips (default applied) | 24.7 |
| D4 | Restaurants | Name only well-established places; give area and cuisine guidance for the rest. Remaining named restaurants still carry the volatility note | 19.5 meal integration, 16.3 |
| D5 | Launch coverage and language | Global destination coverage from day one with honest quality labels per destination. English only, with multi-currency display | NFP-7, 38.7 |
| D6 | Subscription | Fully free in the MVP; pricing and entitlements are decided after launch data. Because it is free, usage limits and rate limiting are needed to control cost | ACC-05, 38.7, 35.3 |
| D7 | Existing bookings input | Both plain language and a quick form | 24.8 |
| D8 | Speed target | Outline in about 15 seconds and the full plan in about 90 seconds, streamed progressively. Replanning targets are set in technical design | 38.7, 8.5 |
| D9 | Carrying the plan | Printable magazine PDF plus a mobile-friendly online guide that needs internet. No offline app in the MVP | 35.2 |
| D10 | MVP tiering | The whole PRD ships in one release. See the risk note below | 35.1 |
| D11 | Sign-in | Guests get a free snippet of the plan, then must sign in to see the full plan. The snippet is defined as the trip outline (destinations, day allocation, highlights) plus the first day in full (default applied; confirm in design) | ACC-02, 8.5 |

**Risk notes on these decisions.**

- **One-release MVP (D10).** This is the largest delivery risk. To manage it, build in internal milestones with feature flags, run a closed beta before public launch (Section 38.6 metrics as the gate), and keep the future-scope list in Section 36 firm.
- **Preview gate (D11) and speed (D8).** Generating a plan for visitors who may not sign in costs money. Limit guest generations per device and network, and consider generating the full plan only after sign-in while showing the outline immediately.
- **Free product with global coverage (D5, D6).** Cost per plan (Section 38.6) is the key number to watch in the prototype; set a ceiling before launch.

**Confirmed.** D11 (the snippet is the trip outline plus Day 1 in full) and the free-in-MVP model (D6) are confirmed, and NFP-1 keeps both the general "reasonable time" expectation and the specific targets in D8.

**Default applied.** D3 (budget shown per person with a group total) was not explicitly chosen and should be confirmed.

**Still to be defined in design.** Interest tag set, refinement chips, traveller profile fields, magazine visual design, interactive guide components, and the contact details attached to "verify directly" notes.

---

## 38. Additional Requirements (from the Functional Requirements Document)

These requirements add the supporting platform layer around the product's core planning experience. They are taken from the companion Functional Requirements Document and adapted to this PRD's scope. Items from that document that conflict with this PRD's scope (affiliate booking hand-offs, community reviews, real-time collaboration, push and price alerts, native apps, and live in-trip features) are not included in the MVP and are recorded in Section 36.

**Priority key:** M = Must, S = Should, C = Could.

### 38.1 Accounts and access

| ID | Requirement | Pri |
|---|---|---|
| ACC-01 | Sign up and log in with email, phone OTP, Google and Apple | M |
| ACC-02 | Guest preview: a user without an account sees a free snippet of the plan (the trip outline and the first day) and signs in to see the full plan and to save, share or export (Section 37.1) | M |
| ACC-03 | Account preferences: currency, units, home city and nationality as defaults for new trips | M |
| ACC-04 | Data export and account deletion, including all plans and traveller profiles | M |
| ACC-05 | Subscription status handling. Deferred: the product is fully free in MVP, and pricing and entitlements are decided after launch data (Section 37.1) | C |

### 38.2 Privacy and data protection

| ID | Requirement | Pri |
|---|---|---|
| PRV-01 | Explicit consent and cookie management; compliance with applicable privacy law (e.g. GDPR, DPDP, CCPA) | M |
| PRV-02 | Traveller profiles for other people (names, ages, dietary needs) are minimal, user-controlled and deletable | M |
| PRV-03 | Shared plan links are unlisted, not search-indexed, view-only for recipients, and revocable by the owner (Section 37.1) | M |
| PRV-04 | Booking reference numbers and personal documents are stored encrypted and excluded from shared views unless the owner chooses to include them | M |
| PRV-05 | Data minimisation and a defined retention policy | S |

### 38.3 Pre-trip readiness, advisories and safety

Extends Sections 24.4 to 24.6 and 26.3.

| ID | Requirement | Pri |
|---|---|---|
| RDY-01 | Readiness checklist with tick-off: passport validity, visa or e-visa, vaccinations and health entry rules, travel insurance, foreign exchange and cards, SIM or eSIM, copies of documents. All items are marked "verify with official sources" | M |
| RDY-02 | Official travel advisories and health alerts are surfaced prominently; destinations under severe advisories get a clear notice before planning proceeds | M |
| RDY-03 | Emergency numbers, embassy details and hospital information are available in the interactive guide as well as the magazine | S |
| RDY-04 | Local laws, customs and dress codes, plus safety notes for solo, women and LGBTQ+ travellers, in the prescriptive-not-alarming tone of Section 8.7 | S |
| RDY-05 | Connectivity guidance: eSIM and SIM options and offline-useful apps | S |

### 38.4 Itinerary enhancements

| ID | Requirement | Pri |
|---|---|---|
| ITN-01 | Calendar export (.ics) of the itinerary | S |
| ITN-02 | Digital PDF export of the plan, in addition to the printable magazine | S |
| ITN-03 | Undo of the last replan and version history of a plan | S |
| ITN-04 | Public-holiday, closure-day and local-event warnings for the travel dates | M |
| ITN-05 | Curated starter templates for popular trips that the user can adopt and personalise | C |
| ITN-06 | Merging of multiple traveller profiles for a group trip (e.g. parents and children) into one plan, with per-traveller packing lists | S |

### 38.5 Feedback, quality and moderation

| ID | Requirement | Pri |
|---|---|---|
| FBK-01 | "Report a problem" on every recommendation (closed, wrong hours or price, unsafe, mislabelled as offbeat) | M |
| FBK-02 | Thumbs up or down on recommendations and on the whole plan, with an optional reason | S |
| FBK-03 | Reports feed an internal review queue; confirmed errors are corrected and the affected data flagged | M |
| FBK-04 | Internal admin console with role-based access: review queue, per-destination quality dashboard (stale information, broken links, source failures), ranking and prompt configuration, blocklists, and usage and cost monitoring | S |
| FBK-05 | Periodic sampled accuracy audits of hours, prices and closures against official sources, tracked as a KPI | M |

### 38.6 Success metrics

Targets are set after a baseline is established.

| Metric | What it measures |
|---|---|
| Activation | Share of visitors who complete a first plan |
| Time to first plan | Time from input to the first usable plan |
| Plan engagement | Share of plans that are saved, edited, shared or exported |
| Refinement | Average edits per plan; share of replans accepted without reverting |
| Recommendation acceptance | Share of recommended items kept in the final plan, split by tourist and offbeat |
| Accuracy | Pass rate on sampled audits (hours, prices, closures) |
| Error reports | Reports per 1,000 recommendations viewed |
| Magazine exports | Share of plans exported as a magazine |
| Satisfaction | NPS or CSAT after a plan is completed |
| Return use | Users who plan a second trip |
| Cost per plan | Average compute and data cost to produce and refine a plan |

### 38.7 Additional non-functional requirements

| Category | Requirement |
|---|---|
| **Performance** | Progressive generation: a usable outline appears in about 15 seconds and the full plan in about 90 seconds, streamed as it is built. Replanning targets are set in technical design (Section 37.1) |
| **Availability** | 99.5% or higher; graceful degradation when a data source fails, by stating what is missing rather than guessing |
| **Scalability and cost** | Caching of research results with freshness windows by data type (e.g. hours, prices, restaurant status), and usage controls to keep cost per plan sustainable |
| **Security** | HTTPS, protection against the OWASP Top 10, encryption of personal data, rate limiting, defences against malicious instructions embedded in web content, and no storage of payment card data |
| **Accessibility of the product itself** | The application's own interface meets WCAG 2.1 AA (screen readers, contrast, keyboard use), separate from the destination accessibility features in Section 29 |
| **Responsiveness** | Mobile-first design; support for the latest two versions of major browsers |
| **Localisation readiness** | Support for local units, date formats and currencies; English only at launch with multi-currency display; additional languages after MVP |
| **Observability** | Logging, monitoring and alerting, plus audit trails for admin actions |
| **SEO and sharing** | Shared plans are not indexed; marketing pages are indexable |
| **Freshness** | Volatile data (Section 16.3) is re-checked at plan generation and internally stamped with the date last checked |

### 38.8 Candidate data sources and integrations

These supplement the web research in Section 15 to make volatile facts more reliable. The choice and licensing of sources is decided in technical design. Section 17 (no visible source attributions) is unaffected.

| Area | Examples |
|---|---|
| Maps, routing and travel times | Google Maps, Mapbox, OpenStreetMap |
| Places and venues | Google Places, Foursquare, official venue sites |
| Weather and climate | Forecast and historical climate providers |
| Visa and entry requirements | Government and official data sources |
| Travel advisories | National foreign-affairs advisories |
| Flights, trains and buses | Schedule data and operator sites |
| Experiences and tours | Operator sites and experience marketplaces |
| Currency | Exchange-rate provider |
| Authentication and email | OAuth providers, email service |
| Analytics and error monitoring | Product analytics, error tracking |

### 38.9 Core data model (conceptual)

- **User** has **TravellerProfiles** and **Trips**.
- **Trip** has **Days**, which have **ItineraryItems**. An item is an attraction, experience, meal, travel leg, existing booking or custom note, and can be locked, rejected or marked visited.
- **Trip** also has **Bookings** (user-entered), a **PackingList** with items per traveller, a **Budget**, a **ReadinessChecklist**, a **ShareLink** and **Versions**.
- **TravellerProfile** holds interests, pace, dietary needs, group defaults, home city and nationality.
- **Recommendation** records classification (tourist or offbeat), confidence level, "last checked" date and the reason it was included.
- **Report** and **Feedback** link a user to a recommendation.

### 38.10 Risks and mitigations

| Risk | Mitigation |
|---|---|
| Inaccurate or outdated information (hours, prices, closures, visas) | Confidence model (Section 16), "verify directly" notes, freshness stamps, accuracy audits, user reports |
| AI hallucination in itineraries or "hidden gems" | Validate against structured place and routing data; strict offbeat criteria (Section 12.2); omit what cannot be verified |
| Dependence on third-party data sources (cost, limits, outages) | Caching, multiple providers, graceful degradation |
| High cost of agentic research per plan | Cost monitoring, caching, usage limits, incremental replanning (Section 8.6) |
| Malicious or misleading web content influencing outputs | Content sanitisation and instruction-injection defences; multi-source corroboration |
| Legal and privacy exposure (visa advice, children's data, shared links) | Clear "verify with official sources" language, privacy controls (Section 38.2), early legal review |
| Quality varying by destination | Honest quality scaling (Section 34, NFP-7); clear limitation messages |
| Scope creep from a large MVP | Priorities in Section 38 and the future-scope list in Section 36 |

---

> **End of Product Requirements Document**  
> **Next step:** Technical Design Document based on these requirements.
