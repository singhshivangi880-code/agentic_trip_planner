# Technical Design Document
## AI-Powered Agentic Trip Planner

**Version:** 1.0  
**Status:** Technical Design  
**Language:** English  
**Frontend:** Angular  
**Backend:** Python / FastAPI  
**AI:** Google Gemini Models  
**Database:** PostgreSQL  
**Cache:** Redis  
**Deployment:** Google Cloud Platform  
**Containerisation:** Docker  
**Frontend Runtime:** Google Cloud Run  
**Backend Runtime:** Google Cloud Run  
**Repository:** Monorepo  
**Architecture:** Modular, API-driven, Multi-Agent

---

# 1. Executive Summary

The AI-Powered Agentic Trip Planner is a containerised, cloud-native travel planning application that uses Google's Gemini family of models to research, reason, plan and continuously refine personalised travel itineraries.

The product addresses the fragmented nature of trip planning by bringing destination research, transportation, accommodation, experiences, restaurants, itinerary planning, preparation and packing into a single agentic workflow.

The product is intentionally designed as a **planning and recommendation platform rather than a booking platform**. It can recommend booking options and provide external links, but does not process transactions. Users can also provide existing bookings, which become fixed planning anchors.

The system consists of:

- Angular web application
- Python/FastAPI API layer
- Multi-agent orchestration layer
- Gemini-powered AI agents
- External research/data connectors
- PostgreSQL persistence
- Redis caching
- OpenTelemetry-based observability
- Developer-only agent trace viewer
- Docker containers
- Independent Google Cloud Run services

The architecture is designed so that every major capability can be developed, tested and deployed independently while remaining part of a single monorepository.

---

# 2. Goals

## 2.1 Primary Goals

The technical solution must:

1. Use Gemini/Gemma models as a core AI capability.
2. Implement genuine multi-agent behaviour.
3. Allow agents to communicate and collaborate on a shared planning task.
4. Support autonomous research and decision-making.
5. Support human-in-the-loop checkpoints.
6. Support intelligent incremental replanning.
7. Expose agent workflow traces for development and debugging.
8. Separate frontend and backend through APIs.
9. Run frontend and backend as independent containers.
10. Deploy the solution on Google Cloud.
11. Use Cloud Run for container deployment.
12. Use an open-source database for the prototype.
13. Support independent development and testing of components.
14. Provide a clear path from prototype to scalable production architecture.

---

# 3. Product Scope

The product supports:

- Natural-language trip requests
- Interest extraction
- Destination discovery
- Destination comparison
- Transportation recommendations
- Accommodation recommendations
- Tourist attraction recommendations
- Offbeat/local experiences
- Restaurants and meals
- Multi-city itinerary generation
- Geographic optimisation
- Time-of-day optimisation
- Weather-aware planning
- Packing checklist generation
- Visa and travel-readiness information
- Existing booking anchors
- Traveller profiles
- Plan editing
- Intelligent replanning
- Plan versioning and undo
- Sharing
- Printable/exportable travel guide

---

# 4. Hackathon Compliance

| Hackathon Requirement | Technical Implementation |
|---|---|
| AI model integration | Google Gemini models through Google Cloud / Vertex AI |
| Agentic solution | Multi-agent orchestration |
| Agent interaction | Shared workflow state + agent-to-agent handoffs |
| Agent traceability | OpenTelemetry traces + developer trace UI |
| Cloud deployment | Google Cloud Platform |
| Containerisation | Docker |
| Frontend | Angular container |
| Backend | Python/FastAPI container |
| Frontend/backend separation | REST/SSE APIs |
| Scalable deployment | Cloud Run |
| Database | PostgreSQL |
| Caching | Redis |
| Source control | Git monorepo |
| Independent development | Modular component architecture |
| Independent testing | Unit, integration and contract tests |
| Accessibility | Angular UI designed for WCAG 2.1 AA |
| Language | English |

---

# 5. High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │       User / Browser     │
                         └────────────┬────────────┘
                                      │ HTTPS
                                      ▼
                         ┌─────────────────────────┐
                         │    Angular Frontend     │
                         │      Cloud Run          │
                         └────────────┬────────────┘
                                      │
                           REST API / SSE
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   Python API Gateway    │
                         │      FastAPI            │
                         │      Cloud Run          │
                         └────────────┬────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │       Agent Orchestrator        │
                    │       Python / LangGraph        │
                    └───────────────┬─────────────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
     │ Trip Intent  │      │ Research     │      │ Destination  │
     │ Agent        │      │ Agent        │      │ Agent        │
     └──────────────┘      └──────────────┘      └──────────────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Recommendation   │
                           │ Agent            │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Itinerary        │
                           │ Planning Agent   │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Validation /     │
                           │ Fact Check Agent │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Human Decision   │
                           │ Checkpoint       │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Finalisation /   │
                           │ Replanning Agent │
                           └──────────────────┘

          ┌────────────────────────────────────────────┐
          │                 Data Layer                  │
          │                                            │
          │ PostgreSQL │ Redis │ External APIs │ Web   │
          └────────────────────────────────────────────┘

          ┌────────────────────────────────────────────┐
          │              Observability                 │
          │ OpenTelemetry │ Cloud Logging │ Jaeger     │
          └────────────────────────────────────────────┘
```

---

# 6. Container Architecture

The application is divided into independently deployable containers.

```text
trip-planner/
│
├── frontend/
│   └── angular-app
│
├── backend/
│   ├── api/
│   ├── agents/
│   ├── services/
│   ├── integrations/
│   └── models/
│
├── shared/
│   ├── contracts/
│   └── schemas/
│
├── dev-tools/
│   └── trace-viewer/
│
├── infrastructure/
│   ├── docker/
│   ├── cloud-run/
│   └── terraform/
│
└── docs/
```

## Containers

### Container 1 — Frontend

Technology:

- Angular
- TypeScript
- RxJS
- Angular Material/CDK where appropriate

Responsibilities:

- User interaction
- Trip input
- Itinerary visualisation
- Refinement interface
- Agent progress display
- Trace UI in development mode
- Packing checklist
- Traveller profiles
- Plan version interface

The frontend does not contain business logic belonging to agents.

### Container 2 — Backend API

Technology:

- Python
- FastAPI
- Pydantic
- Uvicorn

Responsibilities:

- Authentication
- API validation
- Trip CRUD
- Traveller profiles
- Plan persistence
- Agent workflow initiation
- Streaming agent results
- Replanning requests
- Feedback/reporting
- Share links

### Container 3 — Agent Runtime

The agent runtime is logically separated from the API layer and can initially run inside the backend container for the hackathon prototype.

It contains:

- Agent definitions
- Agent tools
- Agent state
- Workflow orchestration
- Gemini integration
- Research orchestration
- Validation
- Replanning

For production scale, the agent runtime can be extracted into a separate Cloud Run service without changing the frontend API contract.

### Container 4 — Developer Trace Viewer

Development-only service.

Responsibilities:

- Display agent execution traces
- Show agent sequence
- Show tool calls
- Show latency
- Show model calls
- Show errors
- Show intermediate state
- Show token/cost metadata where available

This service is never exposed publicly.

---

# 7. Agentic Architecture

The product should not be implemented as a single LLM prompt.

Instead, the system uses specialised agents with clearly defined responsibilities.

## 7.1 Agent Topology

```text
                    ┌─────────────────┐
                    │  Trip Manager   │
                    │     Agent       │
                    └────────┬────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
               ▼             ▼             ▼
        Intent Agent    Discovery Agent   Profile Agent
               │             │
               └──────┬──────┘
                      ▼
               Research Manager
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Transport      Attraction     Experience
     Agent          Agent          Agent
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              Recommendation Agent
                      │
                      ▼
               Itinerary Agent
                      │
                      ▼
                Validation Agent
                      │
             ┌────────┴────────┐
             │                 │
          Valid             Invalid
             │                 │
             ▼                 ▼
       Human Checkpoint   Research/Planning
             │              retry loop
             ▼
       Finalisation Agent
```

---

# 8. Agent Responsibilities

## 8.1 Trip Manager Agent

The Trip Manager is the workflow entry point.

Responsibilities:

- Understand user intent
- Create initial workflow state
- Determine which agents are required
- Coordinate agent execution
- Detect missing information
- Determine when human input is required
- Trigger replanning

It does not independently generate the entire itinerary.

## 8.2 Intent Agent

Extracts structured information from natural language.

Example:

```text
"10 days in Japan from Pune, love food and temples,
moderate budget and relaxed pace"
```

becomes:

```json
{
  "destination": "Japan",
  "duration_days": 10,
  "origin": "Pune",
  "interests": [
    "food",
    "temples",
    "culture"
  ],
  "budget": "moderate",
  "pace": "relaxed"
}
```

## 8.3 Traveller Profile Agent

Determines whether the trip is:

- For the user
- For parents
- For a family
- For friends
- For another saved traveller profile

It merges existing profile information with trip-specific preferences.

---

# 9. Research Agents

Research is deliberately distributed across specialised agents.

## 9.1 Destination Research Agent

Finds:

- Destination overview
- Best time to visit
- Seasonality
- Major cities
- Local areas
- Events
- Travel considerations

## 9.2 Attraction Agent

Finds and evaluates:

- Major tourist attractions
- Opening hours
- Entry requirements
- Typical duration
- Location
- Popularity
- Suitability

## 9.3 Experience Agent

Researches:

- Food tours
- Workshops
- Classes
- Performances
- Nature activities
- Local experiences
- Festivals
- Guided tours

Experiences are treated as full itinerary items rather than simple recommendations.

## 9.4 Transport Agent

Researches:

- Flights
- Trains
- Buses
- Local transportation
- Inter-city transport
- Arrival/departure logistics

## 9.5 Food Agent

Researches:

- Restaurants
- Cuisine
- Price range
- Dietary compatibility
- Location
- Meal suitability

## 9.6 Weather Agent

Provides:

- Forecast when available
- Typical climate otherwise
- Rain probability
- Temperature
- Weather-sensitive activity information

This agent also supplies context to the Packing Agent.

## 9.7 Visa & Readiness Agent

Produces:

- Visa guidance
- Entry requirements
- Document checklist
- Travel insurance reminder
- Currency guidance
- Connectivity guidance
- Travel advisories

Visa information is always presented with official-source verification guidance.

---

# 10. Recommendation Agent

The Recommendation Agent combines research outputs and applies user-specific constraints.

Input:

```text
User Preferences
+
Destination Research
+
Attractions
+
Experiences
+
Restaurants
+
Transport
+
Weather
+
Budget
+
Pace
```

Output:

```text
Ranked Recommendation Set
```

Ranking factors include:

1. Interest alignment
2. Experience quality
3. Time efficiency
4. Geographic practicality
5. Uniqueness
6. Cultural significance
7. Time-of-day suitability
8. Seasonality
9. Popularity/reputation

---

# 11. Itinerary Agent

The Itinerary Agent transforms recommendations into an executable plan.

It considers:

- Geographic clustering
- Opening hours
- Travel time
- Meal timing
- Pace
- Rest
- Time of day
- Weather
- Existing bookings
- Locked items
- Arrival/departure times

The output is a structured itinerary rather than free-form text.

Example:

```json
{
  "day": 2,
  "date": "2027-02-10",
  "theme": "Traditional Tokyo",
  "items": [
    {
      "type": "attraction",
      "name": "Senso-ji",
      "start_time": "09:00",
      "duration_minutes": 90
    },
    {
      "type": "experience",
      "name": "Local food walk",
      "start_time": "12:00",
      "duration_minutes": 120
    }
  ]
}
```

---

# 12. Validation Agent

The Validation Agent is a critical safety and quality layer.

It validates:

- Temporal consistency
- Geographic consistency
- Opening-hour conflicts
- Travel-time feasibility
- Duplicate recommendations
- Closed venues
- Booking conflicts
- Missing information
- Unsupported claims
- Invalid itinerary transitions

It also checks that recommendations have sufficient confidence.

---

# 13. Human-in-the-Loop Agent

Not every decision should be autonomous.

The system creates a checkpoint when:

- A full-day excursion is proposed
- A city should be added/removed
- A day trip versus hotel change is being considered
- Two equally suitable options compete
- A major advance-booking experience is proposed

The workflow pauses and returns:

```json
{
  "checkpoint_type": "USER_DECISION",
  "question": "Would you prefer to stay in Kyoto and visit Osaka as a day trip?",
  "options": [
    {
      "id": "day_trip",
      "label": "Day trip",
      "recommended": true
    },
    {
      "id": "stay",
      "label": "Stay 2 nights in Osaka"
    }
  ]
}
```

---

# 14. Replanning Architecture

Replanning must be incremental.

The system must not regenerate the entire trip for every small edit.

Example:

```text
User:
"Remove the museum from Day 3"

        ↓

Change Detector

        ↓

Affected Scope:
Day 3

        ↓

Replanning Agent

        ↓

Preserve:
- Day 1
- Day 2
- Day 4
- Locked items
- Existing bookings

        ↓

Regenerate Day 3

        ↓

Validation

        ↓

Updated Plan
```

---

# 15. Agent Communication Model

Agents communicate through a shared structured workflow state rather than exchanging arbitrary natural-language messages.

```python
class TripPlanningState:
    trip_id: str
    user_profile: TravellerProfile
    trip_constraints: TripConstraints

    research_results: ResearchResults
    recommendations: RecommendationSet

    itinerary: Itinerary
    bookings: list[Booking]

    locked_items: list[str]
    rejected_items: list[str]

    pending_decision: DecisionCheckpoint | None

    validation_results: ValidationResult

    workflow_status: WorkflowStatus
```

Advantages:

- Strong typing
- Easier testing
- Easier debugging
- Deterministic handoffs
- Reduced hallucination
- Easier traceability

---

# 16. Gemini Integration

Gemini is the primary generative reasoning layer.

Recommended model strategy:

| Task | Model |
|---|---|
| Intent extraction | Gemini Flash |
| Classification | Gemini Flash |
| Research synthesis | Gemini Flash |
| Recommendation reasoning | Gemini Flash |
| Itinerary generation | Gemini Flash |
| Complex planning | Gemini Pro-class model |
| Final editorial generation | Gemini Flash/Pro depending on complexity |
| Embeddings | Google embedding model |

Model names should be configured rather than hardcoded.

```text
GEMINI_MODEL_FAST
GEMINI_MODEL_REASONING
GEMINI_EMBEDDING_MODEL
```

This allows the hackathon implementation to switch between available Gemini/Gemma models without changing application code.

---

# 17. Tool Calling

Agents should not be allowed to freely access the internet.

Each agent receives controlled tools.

Example:

```text
Research Agent
    ├── web_search()
    ├── fetch_page()
    ├── get_place()
    ├── get_weather()
    └── get_route()

Transport Agent
    ├── search_transport()
    ├── get_station()
    └── estimate_travel_time()

Validation Agent
    ├── get_place_status()
    ├── get_opening_hours()
    └── validate_route()
```

Every tool should have:

- Typed input
- Typed output
- Timeout
- Retry policy
- Rate limit
- Trace ID
- Error handling

---

# 18. Web Research Safety

External web content must be treated as **untrusted data**.

The system must not allow text returned from a website to override the agent's system instructions.

Example:

```text
Web page
    ↓
HTML extraction
    ↓
Content sanitisation
    ↓
Instruction/injection filtering
    ↓
Structured research result
    ↓
Agent
```

---

# 19. Data Architecture

## 19.1 Primary Database

**PostgreSQL**

Reasons:

- Open source
- Relational consistency
- Strong JSON support
- Excellent Python support
- Suitable for transactional data
- Easy Cloud SQL migration
- Supports structured itinerary data
- Supports versioning

For the prototype:

```text
PostgreSQL
Docker container locally
        ↓
Cloud SQL PostgreSQL
        ↓
Production
```

---

# 20. Database Model

```text
User
 │
 ├── TravellerProfile
 │
 └── Trip
      │
      ├── TripVersion
      │
      ├── Day
      │    └── ItineraryItem
      │
      ├── Booking
      │
      ├── PackingList
      │
      ├── Budget
      │
      ├── ReadinessChecklist
      │
      ├── Recommendation
      │
      ├── Feedback
      │
      └── ShareLink
```

---

# 21. Core Tables

## users

```text
id
email
name
created_at
updated_at
```

## traveller_profiles

```text
id
user_id
name
home_city
nationality
pace
budget
dietary_preferences
interests
group_defaults
created_at
updated_at
```

## trips

```text
id
user_id
profile_id
title
origin
destination
start_date
end_date
status
created_at
updated_at
```

## itinerary_items

```text
id
trip_day_id
type
name
description
latitude
longitude
start_time
end_time
duration
status
locked
visited
confidence
last_checked_at
```

## recommendations

```text
id
trip_id
name
category
classification
reason
confidence
source_count
last_checked_at
metadata
```

## trip_versions

```text
id
trip_id
version_number
state_snapshot
change_reason
created_at
```

---

# 22. Redis

Redis is used for:

- Research caching
- Session/workflow state
- Rate limiting
- Temporary agent state
- Idempotency keys
- Streaming workflow metadata

Example:

```text
research:
destination:japan:2027-02
attraction:sensoji
weather:tokyo:2027-02-10
```

---

# 23. API Architecture

Frontend and backend communicate exclusively through APIs.

```text
Angular
   │
   ├── REST
   │
   └── Server-Sent Events
             │
             ▼
          FastAPI
```

## Core APIs

### Trip

```http
POST /api/v1/trips
GET  /api/v1/trips/{trip_id}
PATCH /api/v1/trips/{trip_id}
DELETE /api/v1/trips/{trip_id}
```

### Planning

```http
POST /api/v1/trips/{trip_id}/plan
POST /api/v1/trips/{trip_id}/replan
POST /api/v1/trips/{trip_id}/decisions
```

### Streaming

```http
GET /api/v1/trips/{trip_id}/workflow/stream
```

Events:

```text
agent_started
research_started
research_completed
recommendations_generated
itinerary_generated
validation_started
checkpoint_required
plan_updated
workflow_completed
workflow_failed
```

### Traveller

```http
GET    /api/v1/profiles
POST   /api/v1/profiles
PATCH  /api/v1/profiles/{id}
DELETE /api/v1/profiles/{id}
```

### Recommendations

```http
POST /api/v1/recommendations/{id}/feedback
POST /api/v1/recommendations/{id}/report
```

---

# 24. API Contract Strategy

All APIs use versioned contracts:

```text
/api/v1/...
```

Pydantic schemas define backend contracts.

Angular models are generated or maintained from the OpenAPI specification.

This prevents frontend/backend drift.

The CI pipeline must validate:

```text
Backend Pydantic
       ↓
OpenAPI
       ↓
API Contract Test
       ↓
Angular API client
```

---

# 25. Progressive Generation

The application should not wait for the entire workflow.

Example:

```text
0 sec
Request accepted

5 sec
Intent extracted

10 sec
Destination understanding

15 sec
Initial outline streamed

25 sec
Research results arriving

45 sec
Recommendations available

60 sec
Itinerary generated

90 sec
Validated final plan
```

The Angular application updates progressively through SSE.

---

# 26. Agent Traceability

Agent observability is a first-class technical requirement.

Every workflow receives:

```text
trace_id
workflow_id
trip_id
user_id
```

Every agent execution creates a span.

Example:

```text
Trip Planning Workflow
│
├── Intent Agent
│   └── Gemini Call
│
├── Research Manager
│   ├── Destination Agent
│   │   └── Web Search
│   ├── Attraction Agent
│   │   ├── Search
│   │   └── Place API
│   └── Weather Agent
│
├── Recommendation Agent
│   └── Gemini Call
│
├── Itinerary Agent
│   └── Gemini Call
│
└── Validation Agent
    ├── Route Validation
    └── Opening Hours Validation
```

---

# 27. Observability Stack

## Application Observability

- OpenTelemetry
- Structured JSON logging
- Google Cloud Logging
- Google Cloud Monitoring

## Development Agent Trace

- OpenTelemetry SDK
- Jaeger
- Developer-only Trace Viewer

Each trace should show:

```text
Agent Name
Start Time
End Time
Duration
Status
Input
Output
Tool Calls
Model
Model Latency
Token Usage
Errors
Parent Agent
Child Agents
```

Sensitive user data must be redacted before being displayed in traces.

---

# 28. Developer Trace UI

The Angular application can expose a development-only route:

```text
/dev/traces/{trace_id}
```

Example:

```text
Trip Planning Workflow
────────────────────────────────────

Trip Manager             ✓ 1.2s
   │
   ├── Intent Agent      ✓ 0.8s
   │
   ├── Research Manager  ✓ 21.3s
   │     ├── Destination ✓ 5.2s
   │     ├── Attraction  ✓ 8.4s
   │     └── Weather     ✓ 2.1s
   │
   ├── Recommendation    ✓ 8.7s
   │
   ├── Itinerary         ✓ 12.4s
   │
   └── Validation        ✓ 4.3s

Total workflow: 48.7s
```

The endpoint and UI are disabled in production.

---

# 29. Security Architecture

Security controls include:

- HTTPS everywhere
- Authentication
- JWT/session-based authorisation
- API rate limiting
- Input validation
- OWASP Top 10 protections
- Secrets stored in Google Secret Manager
- Encryption at rest
- Encryption in transit
- No payment card storage
- PII minimisation
- Trace redaction
- Restricted developer endpoints
- Signed share tokens
- Expirable share links

---

# 30. Privacy

Traveller information should be treated as user-owned data.

Controls include:

- Data export
- Data deletion
- Minimal traveller profiles
- Encrypted booking information
- Revocable share links
- No indexing of shared plans
- Data retention policy

---

# 31. Google Cloud Architecture

```text
                     Google Cloud
                          │
          ┌───────────────┴────────────────┐
          │                                │
          ▼                                ▼
   Cloud Run Frontend               Cloud Run Backend
      Angular                         FastAPI
          │                                │
          │                         Agent Runtime
          │                                │
          │                                ▼
          │                         Gemini / Vertex AI
          │
          └───────────────┬────────────────┘
                          │
                  ┌───────┴────────┐
                  ▼                ▼
              Cloud SQL          Redis
             PostgreSQL        Memorystore
                  │
                  ▼
           Cloud Storage
         Generated Documents
```

---

# 32. Cloud Run Deployment

Both frontend and backend are packaged as independent Docker images.

### Frontend

```text
Dockerfile
    ↓
Angular build
    ↓
Nginx
    ↓
Cloud Run
```

### Backend

```text
Dockerfile
    ↓
Python dependencies
    ↓
FastAPI
    ↓
Uvicorn
    ↓
Cloud Run
```

The frontend and backend therefore have:

- Independent deployment
- Independent scaling
- Independent versioning
- Independent rollback
- Independent health checks

---

# 33. Local Development

The entire system should be runnable with:

```bash
docker compose up
```

Local services:

```text
frontend
backend
postgres
redis
jaeger
```

Example:

```text
localhost:4200
localhost:8000
localhost:5432
localhost:6379
localhost:16686
```

---

# 34. Repository Structure

The project uses a single monorepository.

```text
ai-trip-planner/
│
├── apps/
│   │
│   ├── frontend/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   └── backend/
│       ├── app/
│       │   ├── api/
│       │   ├── agents/
│       │   ├── services/
│       │   ├── integrations/
│       │   ├── repositories/
│       │   ├── models/
│       │   └── core/
│       │
│       ├── tests/
│       └── Dockerfile
│
├── packages/
│   └── contracts/
│
├── infrastructure/
│   ├── docker/
│   ├── cloud-run/
│   └── terraform/
│
├── dev-tools/
│   └── trace-viewer/
│
├── scripts/
│
├── docs/
│
├── docker-compose.yml
├── Makefile
└── README.md
```

---

# 35. Component Ownership

| Component | Responsibility | Independently Testable |
|---|---|---|
| Intent Agent | Parse user request | Yes |
| Profile Agent | Traveller preferences | Yes |
| Destination Agent | Destination research | Yes |
| Attraction Agent | Attraction research | Yes |
| Experience Agent | Experience research | Yes |
| Transport Agent | Transport research | Yes |
| Food Agent | Restaurant research | Yes |
| Weather Agent | Weather research | Yes |
| Recommendation Agent | Ranking | Yes |
| Itinerary Agent | Schedule generation | Yes |
| Validation Agent | Quality validation | Yes |
| Replanning Agent | Incremental modification | Yes |
| Packing Agent | Packing checklist | Yes |
| Readiness Agent | Travel preparation | Yes |
| API | Backend interface | Yes |
| Angular modules | UI features | Yes |

---

# 36. Feature-Based Frontend Structure

```text
frontend/src/app/

├── core/
│   ├── auth/
│   ├── api/
│   ├── interceptors/
│   └── guards/
│
├── features/
│   │
│   ├── trip-input/
│   ├── destination-discovery/
│   ├── itinerary/
│   ├── recommendations/
│   ├── refinement/
│   ├── traveller-profile/
│   ├── bookings/
│   ├── packing/
│   ├── readiness/
│   ├── sharing/
│   └── trace-viewer/
│
└── shared/
    ├── components/
    ├── models/
    └── utilities/
```

Each feature should have:

```text
component
service
model
API integration
unit tests
```

---

# 37. Backend Feature Structure

```text
backend/app/

├── api/
│   └── v1/
│
├── agents/
│   ├── base/
│   ├── intent/
│   ├── research/
│   ├── recommendation/
│   ├── itinerary/
│   ├── validation/
│   └── replanning/
│
├── tools/
│   ├── web_search/
│   ├── maps/
│   ├── places/
│   ├── weather/
│   └── transport/
│
├── workflows/
│   ├── trip_planning.py
│   └── replanning.py
│
├── services/
│   ├── trip_service.py
│   ├── profile_service.py
│   └── recommendation_service.py
│
├── repositories/
│
├── models/
│
└── core/
    ├── config.py
    ├── logging.py
    ├── security.py
    └── tracing.py
```

---

# 38. Development Stages

## Stage 1 — Foundation

Deliver:

- Repository
- Docker
- Angular shell
- FastAPI shell
- PostgreSQL
- Redis
- CI pipeline
- Health endpoints

Commit:

```text
feat/foundation
```

## Stage 2 — Trip Input

Deliver:

- Freeform input
- Intent Agent
- Traveller preferences
- Trip persistence

Commit:

```text
feat/trip-input
```

## Stage 3 — Gemini Integration

Deliver:

- Gemini client
- Prompt management
- Structured outputs
- Model configuration
- Retry/error handling

Commit:

```text
feat/gemini-integration
```

## Stage 4 — Agent Framework

Deliver:

- Agent base class
- Workflow state
- Agent orchestration
- Agent-to-agent handoffs
- Trace instrumentation

Commit:

```text
feat/agent-orchestration
```

## Stage 5 — Research

Deliver:

- Destination Agent
- Attraction Agent
- Experience Agent
- Transport Agent
- Weather Agent

Commit:

```text
feat/research-agents
```

## Stage 6 — Recommendation Engine

Deliver:

- Recommendation Agent
- Ranking
- Tourist/offbeat classification
- Confidence scoring

Commit:

```text
feat/recommendation-engine
```

## Stage 7 — Itinerary

Deliver:

- Itinerary Agent
- Geographic clustering
- Time optimisation
- Meal integration
- Existing booking anchors

Commit:

```text
feat/itinerary-generation
```

## Stage 8 — Human Checkpoints

Deliver:

- Decision checkpoints
- User choice API
- Workflow resume
- Provisional decisions

Commit:

```text
feat/human-checkpoints
```

## Stage 9 — Replanning

Deliver:

- Change detection
- Affected-scope calculation
- Incremental replanning
- Versioning
- Undo

Commit:

```text
feat/intelligent-replanning
```

## Stage 10 — Preparation

Deliver:

- Packing
- Visa/readiness
- Travel advisories
- Apps
- Budget

Commit:

```text
feat/travel-preparation
```

## Stage 11 — Trace Viewer

Deliver:

- OpenTelemetry
- Trace persistence
- Developer trace UI
- Agent timeline
- Tool execution details

Commit:

```text
feat/agent-tracing
```

## Stage 12 — Cloud Deployment

Deliver:

- Docker images
- Cloud Run
- Cloud SQL
- Redis
- Secret Manager
- Monitoring

Commit:

```text
feat/gcp-deployment
```

---

# 39. Git Strategy

All development happens in one repository.

Recommended branches:

```text
main
develop
feature/*
```

Example:

```text
feature/trip-input
feature/gemini-client
feature/research-agents
feature/itinerary-agent
feature/replanning
feature/tracing
feature/cloud-run
```

Every feature must contain:

```text
Implementation
+
Tests
+
API contract changes
+
Documentation
```

---

# 40. Testing Strategy

Testing happens at multiple levels.

## Unit Tests

Test:

- Agents
- Services
- Ranking functions
- Validators
- Parsers
- Data transformations

Example:

```text
test_intent_agent.py
test_recommendation_ranker.py
test_itinerary_validator.py
```

## Integration Tests

Test:

```text
API
 ↓
Agent
 ↓
Database
 ↓
External tool mock
```

External APIs should be mocked.

## Contract Tests

Ensure:

```text
Angular
    ↕
OpenAPI
    ↕
FastAPI
```

remains compatible.

## Agent Evaluation Tests

AI outputs should be evaluated against deterministic criteria.

Example:

```text
Given:
10-day Japan trip

Validate:
✓ Exactly 10 days
✓ No overlapping activities
✓ Travel time accounted for
✓ Locked items preserved
✓ User interests represented
✓ No invalid dates
```

---

# 41. CI/CD

Pipeline:

```text
Git Push
   │
   ▼
Lint
   │
   ▼
Unit Tests
   │
   ▼
Integration Tests
   │
   ▼
Build Docker Images
   │
   ▼
Security Scan
   │
   ▼
Push Image
   │
   ▼
Deploy Cloud Run
   │
   ▼
Smoke Tests
```

Recommended tooling:

- GitHub Actions
- Docker
- pytest
- Angular test runner
- Ruff
- mypy
- ESLint
- Trivy
- Terraform

---

# 42. Configuration Management

No API keys or credentials are committed to Git.

Environment variables:

```text
GCP_PROJECT_ID
GCP_REGION

GEMINI_MODEL_FAST
GEMINI_MODEL_REASONING

DATABASE_URL
REDIS_URL

JWT_SECRET

MAPS_API_KEY
WEATHER_API_KEY
SEARCH_API_KEY

OTEL_ENDPOINT
```

Production secrets are stored in Google Secret Manager.

---

# 43. Error Handling

Agents must fail gracefully.

Example:

```text
Weather API unavailable
        ↓
Weather Agent
        ↓
Retry
        ↓
Fallback to climate information
        ↓
Mark confidence = MODERATE
        ↓
Continue itinerary generation
```

The system must not invent unavailable data.

---

# 44. AI Output Guardrails

All AI agents should use structured outputs.

Example:

```json
{
  "recommendations": [],
  "confidence": "HIGH",
  "missing_information": [],
  "verification_required": []
}
```

The model should never directly write database records.

Instead:

```text
Gemini
 ↓
Structured Output
 ↓
Pydantic Validation
 ↓
Business Rules
 ↓
Database
```

This reduces malformed outputs and makes the system testable.

---

# 45. Confidence Model

Each recommendation receives:

```text
HIGH
MODERATE
LOW
```

### HIGH

Multiple reliable sources or official source.

### MODERATE

Single source or potentially stale source.

### LOW

Conflicting or insufficient information.

LOW-confidence volatile information should not be presented as established fact.

---

# 46. Caching Strategy

Research data should have different TTLs.

| Data | Example TTL |
|---|---:|
| Destination description | 7 days |
| Restaurant existence | 24 hours |
| Opening hours | 12 hours |
| Price | 12 hours |
| Weather | 1 hour |
| Event | 6 hours |
| Transport schedule | 6 hours |

These are implementation defaults and should be configurable.

Volatile information is rechecked during plan generation.

---

# 47. Scalability

Cloud Run allows independent horizontal scaling.

```text
              Cloud Run
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
     Backend   Backend   Backend
     Instance  Instance  Instance
```

The frontend and backend scale independently.

Agent workloads can later be separated:

```text
API Cloud Run
      │
      ▼
Agent Orchestrator Cloud Run
      │
      ├── Research workers
      ├── Planning workers
      └── Validation workers
```

The initial hackathon implementation can keep these logically separated while running within one backend container to minimise infrastructure complexity.

---

# 48. Performance Targets

| Metric | Target |
|---|---:|
| API health response | <500 ms |
| Intent extraction | <5 sec |
| Initial plan outline | ~15 sec |
| Full plan | ~90 sec |
| Replanning | <30 sec target |
| Standard API requests | <2 sec excluding AI workflow |

---

# 49. Availability and Resilience

Target availability:

**99.5%+**

Strategies:

- Cloud Run automatic scaling
- Health checks
- Retries
- Timeouts
- Circuit breakers
- Cached research
- Graceful degradation
- Multiple data providers where possible

---

# 50. Accessibility

Angular UI should target:

**WCAG 2.1 AA**

Requirements include:

- Keyboard navigation
- Screen-reader compatibility
- Accessible form controls
- Semantic HTML
- Colour contrast
- Focus management
- Accessible loading states
- Accessible agent-progress indicators
- Responsive mobile-first UI

---

# 51. Agent Workflow Example

For:

> "Plan 10 days in Japan from Pune. I love food and temples. Moderate budget."

The workflow becomes:

```text
User
 │
 ▼
Intent Agent
 │
 ├── Destination: Japan
 ├── Duration: 10
 ├── Origin: Pune
 ├── Interests: Food, Temples
 └── Budget: Moderate
 │
 ▼
Destination Agent
 │
 ├── Tokyo
 ├── Kyoto
 └── Osaka
 │
 ▼
Research Manager
 │
 ├── Attraction Agent
 ├── Food Agent
 ├── Experience Agent
 ├── Transport Agent
 └── Weather Agent
 │
 ▼
Recommendation Agent
 │
 ▼
Itinerary Agent
 │
 ▼
Validation Agent
 │
 ▼
Decision Checkpoint
 │
 ▼
User selects preferred city/day-trip option
 │
 ▼
Replanning Agent
 │
 ▼
Final Itinerary
```

---

# 52. Trace Example

```text
TRACE: 4f72a8

TripPlanningWorkflow
│
├── IntentAgent
│   ├── Gemini
│   └── StructuredOutputValidator
│
├── DestinationResearchAgent
│   ├── SearchTool
│   ├── WebFetch
│   └── Gemini
│
├── AttractionAgent
│   ├── PlacesTool
│   └── Gemini
│
├── ExperienceAgent
│   ├── SearchTool
│   └── Gemini
│
├── TransportAgent
│   └── TransportTool
│
├── RecommendationAgent
│   └── Gemini
│
├── ItineraryAgent
│   └── Gemini
│
├── ValidationAgent
│   ├── RouteValidator
│   ├── TimeValidator
│   └── ConflictValidator
│
└── HumanCheckpoint
    └── UserDecision
```

This trace is available only in development environments.

---

# 53. Key Design Principles

## Principle 1 — Agents, not one giant prompt

Each agent has one clear responsibility.

## Principle 2 — Structured state, not free-form agent conversations

Agent communication uses typed workflow state.

## Principle 3 — AI proposes; deterministic code validates

Gemini handles reasoning.

Python handles:

- validation
- persistence
- permissions
- calculations
- business rules

## Principle 4 — Research is untrusted

Web content cannot modify agent instructions.

## Principle 5 — Incremental replanning

Only affected parts of the itinerary are regenerated.

## Principle 6 — Human decisions remain explicit

The system asks the user when a decision materially changes the trip.

## Principle 7 — Everything is traceable

Every agent execution is observable.

---

# 54. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| AI hallucination | Structured outputs + validation |
| Incorrect opening hours | Freshness checks + verification |
| Fake hidden gems | Strict classification criteria |
| Web prompt injection | Content sanitisation |
| API failure | Retry + fallback |
| High AI cost | Caching + incremental replanning |
| Long workflow | Parallel agents + progressive streaming |
| Poor destination coverage | Honest limitation handling |
| Data privacy | Encryption + minimisation |
| Agent failure | Workflow checkpoints + retries |
| Frontend/backend drift | OpenAPI contract testing |
| Infrastructure complexity | Start modular, deploy as two primary Cloud Run services |

---

# 55. Prototype Deployment

## Local

```text
Docker Compose
│
├── Angular
├── FastAPI
├── PostgreSQL
├── Redis
└── Jaeger
```

## Google Cloud

```text
                    GCP
                     │
          ┌──────────┴──────────┐
          │                     │
     Cloud Run              Cloud Run
     Frontend                Backend
          │                     │
          │                     ├── Gemini
          │                     ├── APIs
          │                     └── Agent Runtime
          │
          └─────────────┬───────┘
                        │
                 Cloud SQL
                 PostgreSQL
                        │
                   Memorystore
                      Redis
```

---

# 56. Recommended Prototype Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Angular + TypeScript |
| Backend | Python + FastAPI |
| AI | Gemini models |
| Agent orchestration | LangGraph |
| Validation | Pydantic |
| Database | PostgreSQL |
| Cache | Redis |
| API | REST + SSE |
| Containers | Docker |
| Local orchestration | Docker Compose |
| Cloud deployment | Google Cloud Run |
| Database hosting | Cloud SQL |
| Secrets | Secret Manager |
| Logs | Cloud Logging |
| Metrics | Cloud Monitoring |
| Tracing | OpenTelemetry |
| Dev trace UI | Jaeger |
| CI/CD | GitHub Actions |
| Infrastructure | Terraform |
| Testing | Pytest + Angular tests |
| API contract | OpenAPI |

---

# 57. Definition of Done

## Application

- [ ] User can enter a natural-language trip request.
- [ ] Gemini extracts structured trip intent.
- [ ] Multiple agents execute as part of a workflow.
- [ ] Agents use tools/research sources.
- [ ] Agents produce a personalised itinerary.
- [ ] User can make a decision at a human checkpoint.
- [ ] User can modify the itinerary.
- [ ] System performs incremental replanning.
- [ ] Existing bookings can be represented as fixed anchors.
- [ ] Packing/readiness information is generated.

## Architecture

- [ ] Frontend is an independent Angular container.
- [ ] Backend is an independent Python container.
- [ ] Frontend communicates with backend through APIs.
- [ ] PostgreSQL stores application state.
- [ ] Redis provides caching/state support.
- [ ] AI workflow is independently testable.
- [ ] Components are modular.
- [ ] Components have unit tests.

## Agentic

- [ ] At least 5 specialised agents exist.
- [ ] Agents have distinct responsibilities.
- [ ] Agents share structured workflow state.
- [ ] Agents can trigger other agents.
- [ ] Human checkpoints are supported.
- [ ] Agent execution can be traced.

## Google Cloud

- [ ] Docker images build successfully.
- [ ] Frontend deployed to Cloud Run.
- [ ] Backend deployed to Cloud Run.
- [ ] Gemini runs through Google Cloud.
- [ ] Database deployed using Cloud SQL or equivalent GCP service.
- [ ] Secrets are not committed to Git.
- [ ] Logs are visible in Cloud Logging.

## Hackathon

- [ ] Gemini/Gemma integration demonstrable.
- [ ] Agentic workflow demonstrable.
- [ ] GCP deployment demonstrable.
- [ ] Functional end-to-end prototype demonstrable.
- [ ] Technical architecture documented.
- [ ] Agent trace demonstrable to judges.

---

# 58. Future Production Evolution

The hackathon prototype should deliberately avoid unnecessary infrastructure complexity.

The architecture nevertheless allows future evolution:

```text
Prototype

Cloud Run
 └── Backend
      └── Agent Runtime


Production

API Cloud Run
      │
      ▼
Workflow Orchestrator
      │
      ├── Research Workers
      ├── Recommendation Workers
      ├── Planning Workers
      └── Validation Workers
```

Additional future components can include:

- Dedicated vector database
- Event-driven orchestration
- Async task queues
- More specialised agents
- Real-time travel alerts
- Booking integrations
- Collaborative planning
- Offline interactive guide
- Multi-language support

---

# 59. Final Architecture Decision

The proposed solution uses a **modular monorepo + containerised microservice boundary + multi-agent orchestration** architecture.

The initial deployment consists of:

```text
                    ┌──────────────────┐
                    │ Angular Frontend │
                    │   Cloud Run      │
                    └────────┬─────────┘
                             │
                       REST / SSE
                             │
                    ┌────────▼─────────┐
                    │ FastAPI Backend  │
                    │   Cloud Run      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Agent Orchestrator│
                    │    Gemini        │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
       Research        Recommendation      Itinerary
        Agents             Agent             Agent
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                       Validation Agent
                             │
                             ▼
                       Human Checkpoint
                             │
                             ▼
                        Final Plan

          ┌─────────────────────────────────────┐
          │ PostgreSQL │ Redis │ External APIs  │
          └─────────────────────────────────────┘

          ┌─────────────────────────────────────┐
          │ OpenTelemetry │ Cloud Logging │     │
          │ Jaeger (Dev)  │ Cloud Monitoring    │
          └─────────────────────────────────────┘
```

This architecture provides a clear demonstration of the hackathon's required AI, agentic, containerisation and Google Cloud capabilities while keeping the implementation sufficiently modular for parallel development.

The most important architectural principle is:

> **Gemini performs reasoning, agents coordinate specialised work, deterministic Python validates and persists the results, and every agent execution is observable.**

This keeps the prototype genuinely agentic without turning the entire application into an opaque LLM workflow.
