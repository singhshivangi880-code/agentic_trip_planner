# AI-Powered Agentic Trip Planner
# Detailed Stepwise Engineering Task Plan

**Purpose:** Break the technical design into small, independently executable work packages so multiple developers/coding agents can work in parallel on separate laptops and commit to one Git repository with minimal merge conflicts.

**Architecture baseline:** Angular frontend, Python/FastAPI backend, Gemini-based multi-agent workflow, LangGraph orchestration, PostgreSQL, Redis, REST + SSE, Docker, Docker Compose, OpenTelemetry/Jaeger for development tracing, and Google Cloud Run deployment.

---

# 0. How This Plan Should Be Used

## 0.1 Core development model

The project is a **single monorepo**, but each major work package owns a clearly separated directory.

The preferred workflow is:

```text
Developer / Coding Agent
        │
        ▼
Create feature branch
        │
        ▼
Work only inside assigned ownership boundary
        │
        ▼
Run local tests
        │
        ▼
Run integration contract checks
        │
        ▼
Commit
        │
        ▼
Pull Request
        │
        ▼
Merge to main/develop
```

The objective is that two developers should be able to work simultaneously without modifying the same files.

---

# 1. Global Repository Ownership Rules

Before development begins, establish these rules.

## 1.1 Directory ownership

```text
/apps/frontend/       → Frontend developer
/apps/backend/        → Backend/API developer
/apps/agents/         → Agent developer
/packages/contracts/  → Contract/schema owner
/infrastructure/      → DevOps/cloud developer
/dev-tools/           → Observability developer
/tests/               → Test/integration owner
/docs/                → Documentation owner
```

Do not allow two developers to modify the same feature directory simultaneously.

---

## 1.2 Shared files are protected

The following files should have one designated owner because they are merge-conflict hotspots:

```text
docker-compose.yml
README.md
package.json
pnpm-lock.yaml / package-lock.json
pyproject.toml
requirements.txt
Makefile
.github/workflows/*
terraform/*
OpenAPI generated files
shared environment templates
```

Changes to these files should be made through a dedicated infrastructure/integration branch.

---

## 1.3 Contract-first rule

Before frontend and backend implementation starts, agree on:

- API endpoint names
- Request schema
- Response schema
- Error schema
- SSE event schema
- Trip ID format
- Agent workflow ID format

The contract is stored under:

```text
/packages/contracts/
```

Frontend and backend should consume the contract rather than independently inventing models.

---

# 2. Final Repository Structure

The repository should converge toward:

```text
ai-trip-planner/
│
├── apps/
│   ├── frontend/
│   │   ├── src/
│   │   │   └── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   │
│   └── backend/
│       ├── app/
│       │   ├── api/
│       │   ├── core/
│       │   ├── models/
│       │   ├── repositories/
│       │   ├── services/
│       │   └── main.py
│       ├── tests/
│       └── Dockerfile
│
├── packages/
│   └── contracts/
│       ├── api/
│       ├── events/
│       └── workflow/
│
├── agents/
│   ├── common/
│   ├── intent/
│   ├── profile/
│   ├── research/
│   ├── recommendation/
│   ├── itinerary/
│   ├── validation/
│   ├── replanning/
│   ├── preparation/
│   └── workflow/
│
├── tools/
│   ├── search/
│   ├── places/
│   ├── maps/
│   ├── weather/
│   └── transport/
│
├── dev-tools/
│   └── trace-viewer/
│
├── infrastructure/
│   ├── docker/
│   ├── cloud-run/
│   ├── terraform/
│   └── scripts/
│
├── tests/
│   ├── contract/
│   ├── integration/
│   ├── e2e/
│   └── evaluation/
│
├── docs/
│
├── docker-compose.yml
├── Makefile
└── README.md
```

---

# 3. Stage 0 — Repository Bootstrap

**Owner:** Developer A  
**Branch:** `feature/bootstrap`  
**Main ownership:** Repository root only

## Task 0.1 — Create Git repository

- Create repository.
- Create `main`.
- Create `develop` if the team wants a development branch.
- Add branch protection.
- Add pull request template.
- Add issue template.
- Add CODEOWNERS.

### Output

```text
.git/
.github/
CODEOWNERS
README.md
.gitignore
```

---

## Task 0.2 — Create directory skeleton

Create all top-level directories.

Do not implement business logic.

### Acceptance criteria

```bash
tree -L 2
```

shows the agreed repository structure.

---

## Task 0.3 — Create root README

README should contain:

- Project description
- Architecture diagram
- Local startup command
- Branch strategy
- Directory ownership
- Required environment variables
- Development rules

---

## Task 0.4 — Create `.env.example`

Include placeholders only:

```text
GCP_PROJECT_ID=
GCP_REGION=

GEMINI_MODEL_FAST=
GEMINI_MODEL_REASONING=
GEMINI_EMBEDDING_MODEL=

DATABASE_URL=
REDIS_URL=

OTEL_ENDPOINT=

MAPS_API_KEY=
WEATHER_API_KEY=
SEARCH_API_KEY=
```

No secrets.

---

## Task 0.5 — Create contribution rules

Add:

```text
CONTRIBUTING.md
```

Document:

- Branch naming
- Commit naming
- PR naming
- Directory ownership
- Testing requirement
- Contract-first requirement
- No direct commits to main
- No secrets in Git

---

## Connectivity Check C0

Every developer should be able to:

```bash
git clone <repo>
cd ai-trip-planner
```

and see the complete skeleton.

### Commit

```text
chore: bootstrap monorepo structure
```

---

# 4. Stage 1 — Local Development Infrastructure

**Owner:** Developer B  
**Branch:** `feature/local-infrastructure`  
**Ownership:** `docker-compose.yml`, Docker infrastructure files only

## Task 1.1 — PostgreSQL container

Configure PostgreSQL.

Create:

```text
postgres
```

with:

- database
- username
- password
- persistent volume
- health check

---

## Task 1.2 — Redis container

Configure Redis.

Requirements:

- Persistent development configuration where appropriate
- Health check
- Exposed local port

---

## Task 1.3 — Jaeger container

Configure Jaeger for development tracing.

Expose:

```text
16686
```

---

## Task 1.4 — Create Docker network

All containers must communicate using service names.

Example:

```text
backend → postgres:5432
backend → redis:6379
backend → jaeger:4317
```

Do not hardcode container IPs.

---

## Task 1.5 — Create Docker Compose

Compose should start:

```text
frontend
backend
postgres
redis
jaeger
```

At this stage frontend/backend can be placeholder containers.

---

## Task 1.6 — Health checks

Create:

```text
PostgreSQL health check
Redis health check
Jaeger health check
```

---

## Acceptance Criteria

```bash
docker compose up
```

starts the infrastructure without errors.

---

## Connectivity Check C1

Verify:

```text
Backend container
   ├── PostgreSQL ✓
   ├── Redis ✓
   └── Jaeger ✓
```

This check must be completed before backend development begins.

### Commit

```text
chore: add local docker infrastructure
```

---

# 5. Stage 2 — Backend Skeleton

**Owner:** Developer C  
**Branch:** `feature/backend-foundation`  
**Ownership:** `/apps/backend/`

## Task 2.1 — Create Python project

Use:

```text
Python
FastAPI
Uvicorn
Pydantic
SQLAlchemy
Alembic
pytest
```

---

## Task 2.2 — Create backend package structure

```text
app/
├── api/
├── core/
├── models/
├── repositories/
├── services/
└── main.py
```

---

## Task 2.3 — Create FastAPI application

Create:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Task 2.4 — Configuration layer

Create typed configuration.

Example:

```python
class Settings:
    database_url: str
    redis_url: str
    gemini_model_fast: str
```

---

## Task 2.5 — Logging

Create structured JSON logging.

Every request should contain:

```text
request_id
timestamp
method
path
status_code
duration_ms
```

---

## Task 2.6 — Exception handling

Create common API errors:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "request_id": "..."
  }
}
```

---

## Task 2.7 — Backend Dockerfile

Create production-style Dockerfile.

Requirements:

- Small base image
- Non-root user
- Health endpoint
- Environment-driven configuration

---

## Task 2.8 — Backend unit tests

Tests:

```text
test_health.py
test_config.py
test_error_handler.py
```

---

## Connectivity Check C2

Run backend container and verify:

```text
GET /health → 200
```

Then connect backend to:

```text
PostgreSQL
Redis
```

without implementing trip logic.

### Commit

```text
feat: create fastapi backend foundation
```

---

# 6. Stage 3 — Frontend Skeleton

**Owner:** Developer D  
**Branch:** `feature/frontend-foundation`  
**Ownership:** `/apps/frontend/`

## Task 3.1 — Create Angular application

Create:

```text
Angular + TypeScript
```

---

## Task 3.2 — Configure application structure

```text
core/
shared/
features/
```

---

## Task 3.3 — Create routing

Routes:

```text
/
 /trip/new
 /trip/:tripId
 /trip/:tripId/itinerary
 /trip/:tripId/preparation
```

---

## Task 3.4 — Create API service abstraction

Create:

```text
ApiClient
TripApiService
```

Do not hardcode endpoint logic inside components.

---

## Task 3.5 — Create global error handling

Handle:

```text
400
401
403
404
409
422
500
503
```

---

## Task 3.6 — Create loading state

Create reusable:

```text
LoadingSpinner
LoadingOverlay
EmptyState
ErrorState
```

---

## Task 3.7 — Create Angular Dockerfile

Use:

```text
Angular build
        ↓
Nginx
        ↓
Runtime
```

---

## Task 3.8 — Frontend tests

Create:

```text
app.spec.ts
api-service.spec.ts
routing.spec.ts
```

---

## Connectivity Check C3

Angular must call:

```http
GET /health
```

from the backend.

Expected:

```text
Angular → FastAPI → 200
```

No business API is required yet.

### Commit

```text
feat: create angular frontend foundation
```

---

# 7. Stage 4 — API Contract Package

**Owner:** Developer E  
**Branch:** `feature/api-contracts`  
**Ownership:** `/packages/contracts/`

This is one of the most important stages for preventing merge conflicts.

## Task 4.1 — Define Trip request

```json
{
  "origin": "Pune",
  "destination": "Japan",
  "start_date": "2027-02-08",
  "end_date": "2027-02-18",
  "preferences": {
    "budget": "moderate",
    "pace": "relaxed",
    "interests": ["food", "temples"]
  }
}
```

---

## Task 4.2 — Define Trip response

Include:

```text
trip_id
status
destination
dates
preferences
workflow_status
```

---

## Task 4.3 — Define itinerary schema

Define:

```text
Trip
TripDay
ItineraryItem
Booking
Recommendation
```

---

## Task 4.4 — Define workflow event schema

Events:

```text
workflow_started
agent_started
agent_completed
agent_failed
research_started
research_completed
checkpoint_required
plan_updated
workflow_completed
workflow_failed
```

---

## Task 4.5 — Define agent state schema

Create shared state definitions:

```text
TripPlanningState
AgentResult
AgentError
DecisionCheckpoint
ValidationResult
```

---

## Task 4.6 — Define error contract

All APIs use the same error format.

---

## Task 4.7 — Generate OpenAPI

FastAPI should eventually expose:

```text
/openapi.json
```

Contract tests compare implementation against agreed schemas.

---

## Connectivity Check C4

Backend and frontend must consume the same sample JSON fixtures.

Create:

```text
packages/contracts/fixtures/
```

Example:

```text
trip.json
itinerary.json
workflow-events.json
```

### Commit

```text
feat: define shared api and workflow contracts
```

---

# 8. Stage 5 — Database Foundation

**Owner:** Developer F  
**Branch:** `feature/database-foundation`  
**Ownership:** `/apps/backend/app/models/`, `/repositories/`, migrations

## Task 5.1 — Configure SQLAlchemy

Create database session factory.

---

## Task 5.2 — Configure Alembic

Create migration system.

---

## Task 5.3 — Create User model

Fields:

```text
id
email
name
created_at
updated_at
```

---

## Task 5.4 — Create TravellerProfile model

Fields:

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
```

---

## Task 5.5 — Create Trip model

Fields:

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
```

---

## Task 5.6 — Create TripVersion model

Fields:

```text
id
trip_id
version_number
state_snapshot
change_reason
created_at
```

---

## Task 5.7 — Create itinerary models

Create:

```text
TripDay
ItineraryItem
```

---

## Task 5.8 — Create Recommendation model

Create:

```text
Recommendation
```

---

## Task 5.9 — Create Booking model

Bookings must support:

```text
locked = true
```

because existing bookings become planning anchors.

---

## Task 5.10 — Create migrations

Create initial migration.

---

## Task 5.11 — Repository tests

Test CRUD for each model.

---

## Connectivity Check C5

Run:

```text
Backend
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

Create a test trip, read it back, update it, delete it.

### Commit

```text
feat: add postgres domain models and repositories
```

---

# 9. Stage 6 — Redis Foundation

**Owner:** Developer G  
**Branch:** `feature/redis-foundation`  
**Ownership:** Redis service code only

## Task 6.1 — Redis client

Create typed Redis client.

---

## Task 6.2 — Cache abstraction

Create:

```python
cache.get()
cache.set()
cache.delete()
```

---

## Task 6.3 — TTL support

Allow:

```text
set(key, value, ttl)
```

---

## Task 6.4 — Workflow temporary state

Support temporary workflow metadata.

---

## Task 6.5 — Idempotency

Create idempotency key support for workflow requests.

---

## Task 6.6 — Tests

Use mocked Redis for unit tests.

---

## Connectivity Check C6

```text
Backend → Redis → set/get/delete
```

### Commit

```text
feat: add redis cache foundation
```

---

# 10. Stage 7 — Gemini Client

**Owner:** Developer H  
**Branch:** `feature/gemini-client`  
**Ownership:** `/agents/common/gemini/`

## Task 7.1 — Create Gemini configuration

Environment-driven model configuration.

---

## Task 7.2 — Create Gemini client wrapper

The rest of the application must not call the Gemini SDK directly.

Create:

```text
GeminiClient
```

---

## Task 7.3 — Structured output support

Support:

```text
prompt
schema
model
temperature/config
```

and return validated structured output.

---

## Task 7.4 — Retry policy

Handle transient failures.

---

## Task 7.5 — Timeout policy

Configure model call timeout.

---

## Task 7.6 — Error mapping

Map provider errors to application errors.

---

## Task 7.7 — Model abstraction

Allow:

```text
GEMINI_MODEL_FAST
GEMINI_MODEL_REASONING
```

to be changed without code changes.

---

## Task 7.8 — Gemini tests

Do not make real model calls in normal unit tests.

Use:

```text
MockGeminiClient
```

---

## Connectivity Check C7

Create one small test workflow:

```text
Input
 ↓
Gemini
 ↓
Structured JSON
 ↓
Pydantic validation
```

### Commit

```text
feat: add gemini client abstraction
```

---

# 11. Stage 8 — Agent Framework Foundation

**Owner:** Developer I  
**Branch:** `feature/agent-framework`  
**Ownership:** `/agents/common/`, `/agents/workflow/`

The technical design requires specialised agents, structured shared state and observable execution.

## Task 8.1 — Agent base interface

Define:

```python
class BaseAgent:
    name: str

    async def execute(
        self,
        state: TripPlanningState
    ) -> AgentResult:
        ...
```

---

## Task 8.2 — Agent result

Define:

```text
status
output
errors
confidence
metadata
```

---

## Task 8.3 — Workflow state

Create the shared state object.

It should contain:

```text
trip
profile
constraints
research
recommendations
itinerary
bookings
locked_items
rejected_items
pending_decision
validation_results
workflow_status
```

---

## Task 8.4 — LangGraph workflow skeleton

Create:

```text
START
 ↓
Trip Manager
 ↓
END
```

Do not add all agents yet.

---

## Task 8.5 — Agent handoff mechanism

Support:

```text
Agent A
 ↓
updated state
 ↓
Agent B
```

---

## Task 8.6 — Failure state

Workflow should support:

```text
RUNNING
WAITING_FOR_USER
COMPLETED
FAILED
CANCELLED
```

---

## Task 8.7 — Retry state

Support agent-level retry count.

---

## Connectivity Check C8

Implement:

```text
DummyAgentA
    ↓
DummyAgentB
    ↓
workflow completed
```

Both agents must see the same state.

### Commit

```text
feat: add multi-agent workflow foundation
```

---

# 12. Stage 9 — Trip API

**Owner:** Developer C  
**Branch:** `feature/trip-api`  
**Ownership:** `/apps/backend/app/api/trips/`

## Task 9.1 — POST trip

Implement:

```http
POST /api/v1/trips
```

---

## Task 9.2 — GET trip

```http
GET /api/v1/trips/{trip_id}
```

---

## Task 9.3 — PATCH trip

```http
PATCH /api/v1/trips/{trip_id}
```

---

## Task 9.4 — Trip validation

Validate:

- Date order
- Required destination
- Valid preferences
- Duration
- Origin

---

## Task 9.5 — Trip repository integration

Connect API to repository layer.

---

## Task 9.6 — API tests

Create:

```text
POST success
POST invalid
GET success
GET not found
PATCH success
```

---

## Connectivity Check C9

```text
Angular
 ↓
POST /trips
 ↓
FastAPI
 ↓
Repository
 ↓
PostgreSQL
```

### Commit

```text
feat: add trip management api
```

---

# 13. Stage 10 — Angular Trip Input

**Owner:** Developer D  
**Branch:** `feature/trip-input-ui`  
**Ownership:** `/apps/frontend/src/app/features/trip-input/`

## Task 10.1 — Trip input page

Fields:

```text
Origin
Destination
Start date
End date
Budget
Pace
Interests
```

---

## Task 10.2 — Form validation

Validate:

- Required fields
- Date range
- At least one destination
- Supported preference values

---

## Task 10.3 — Connect TripApiService

Call:

```http
POST /api/v1/trips
```

---

## Task 10.4 — Navigate to trip page

After creation:

```text
/trip/{tripId}
```

---

## Task 10.5 — Loading/error states

Implement:

```text
Submitting
Success
Validation error
Server error
```

---

## Connectivity Check C10

Complete vertical slice:

```text
Angular Trip Form
        ↓
POST /trips
        ↓
PostgreSQL
        ↓
Trip ID
        ↓
Angular Trip Page
```

### Commit

```text
feat: add trip creation ui
```

---

# 14. Stage 11 — Intent Agent

**Owner:** Developer J  
**Branch:** `feature/intent-agent`  
**Ownership:** `/agents/intent/`

## Task 11.1 — Intent schema

Create structured output:

```text
destination
duration
origin
budget
pace
interests
constraints
traveller_type
missing_information
```

---

## Task 11.2 — Intent prompt

Create system prompt separately from code.

---

## Task 11.3 — Gemini invocation

Use only:

```text
GeminiClient
```

---

## Task 11.4 — Structured validation

Use Pydantic.

---

## Task 11.5 — Missing information handling

Return:

```text
missing_information[]
```

rather than inventing values.

---

## Task 11.6 — Unit tests

Use mocked Gemini responses.

Test:

```text
simple request
complex request
missing date
missing destination
ambiguous request
```

---

## Connectivity Check C11

```text
Trip input
 ↓
Intent Agent
 ↓
TripPlanningState
```

### Commit

```text
feat: add trip intent agent
```

---

# 15. Stage 12 — Traveller Profile Agent

**Owner:** Developer K  
**Branch:** `feature/profile-agent`  
**Ownership:** `/agents/profile/`

## Task 12.1 — Profile retrieval

Read traveller profile.

---

## Task 12.2 — Trip-specific preference merging

Merge:

```text
saved profile
+
current trip preferences
```

---

## Task 12.3 — Conflict resolution

Current trip preferences override defaults.

Example:

```text
Profile: vegetarian
Trip: no dietary restriction
```

The agent should preserve the explicitly supplied trip value according to the agreed business rule.

---

## Task 12.4 — Output schema

```text
EffectiveTravellerPreferences
```

---

## Task 12.5 — Tests

Test:

```text
profile only
trip only
both
conflicting values
missing profile
```

---

## Connectivity Check C12

```text
Profile API
 ↓
Profile Agent
 ↓
TripPlanningState.user_profile
```

### Commit

```text
feat: add traveller profile agent
```

---

# 16. Stage 13 — Research Tool Interfaces

**Owner:** Developer L  
**Branch:** `feature/research-tools`  
**Ownership:** `/tools/`

The tools should be built independently of agents.

## Task 13.1 — Search interface

Define:

```python
search(query, location=None)
```

---

## Task 13.2 — Page fetch interface

Define:

```python
fetch(url)
```

---

## Task 13.3 — Places interface

Define:

```python
get_place(place_id)
get_opening_hours(place_id)
```

---

## Task 13.4 — Maps interface

Define:

```python
get_route(origin, destination)
get_distance_matrix(locations)
```

---

## Task 13.5 — Weather interface

Define:

```python
get_weather(location, date)
get_forecast(location)
```

---

## Task 13.6 — Transport interface

Define:

```python
search_transport(origin, destination, date)
```

---

## Task 13.7 — Tool error standardisation

Every tool returns:

```text
success
data
source
retrieved_at
confidence
error
```

---

## Task 13.8 — Tool mocks

Create deterministic fake providers.

---

## Connectivity Check C13

Every tool must pass:

```text
mock request
 ↓
tool
 ↓
typed response
```

No agent dependency yet.

### Commit

```text
feat: add research tool interfaces
```

---

# 17. Stage 14 — Destination Research Agent

**Owner:** Developer M  
**Branch:** `feature/destination-agent`  
**Ownership:** `/agents/research/destination/`

## Task 14.1 — Destination schema

Create:

```text
DestinationOverview
CityCandidate
Seasonality
TravelConsideration
```

---

## Task 14.2 — Research workflow

```text
Destination Agent
 ↓
Search Tool
 ↓
Page Fetch
 ↓
Gemini synthesis
```

---

## Task 14.3 — Source capture

Store:

```text
source_url
source_name
retrieved_at
```

---

## Task 14.4 — Prompt injection protection

External content must be treated as untrusted.

---

## Task 14.5 — Cache research

Use Redis.

---

## Task 14.6 — Tests

Test using mocked search results.

---

## Connectivity Check C14

```text
Destination Agent
 ↓
Mock Search Tool
 ↓
Gemini Mock
 ↓
DestinationResearchResult
```

### Commit

```text
feat: add destination research agent
```

---

# 18. Stage 15 — Attraction Agent

**Owner:** Developer N  
**Branch:** `feature/attraction-agent`  
**Ownership:** `/agents/research/attractions/`

## Tasks

1. Define attraction schema.
2. Integrate Places tool.
3. Add opening-hours retrieval.
4. Add attraction categorisation.
5. Add duration estimation.
6. Add location information.
7. Add source metadata.
8. Add confidence.
9. Add Redis caching.
10. Add unit tests.
11. Add integration tests with mocked Places API.

### Connectivity Check

```text
Attraction Agent
 ↓
Places Tool
 ↓
Attraction Result
```

### Commit

```text
feat: add attraction research agent
```

---

# 19. Stage 16 — Experience Agent

**Owner:** Developer O  
**Branch:** `feature/experience-agent`  
**Ownership:** `/agents/research/experiences/`

## Tasks

1. Define experience schema.
2. Define experience categories.
3. Research local experiences.
4. Research workshops.
5. Research food experiences.
6. Research cultural experiences.
7. Add source metadata.
8. Add confidence.
9. Add tourist/offbeat classification.
10. Add caching.
11. Add tests.

### Connectivity Check

```text
Experience Agent
 ↓
Search Tool
 ↓
Experience Result
```

### Commit

```text
feat: add experience research agent
```

---

# 20. Stage 17 — Food Agent

**Owner:** Developer P  
**Branch:** `feature/food-agent`  
**Ownership:** `/agents/research/food/`

## Tasks

1. Define restaurant schema.
2. Define dietary preference filtering.
3. Search restaurants.
4. Capture cuisine.
5. Capture price category.
6. Capture location.
7. Capture opening information.
8. Add source metadata.
9. Add confidence.
10. Add caching.
11. Add tests.

### Connectivity Check

```text
Food Agent
 ↓
Search / Places Tool
 ↓
Food Recommendation Result
```

### Commit

```text
feat: add food research agent
```

---

# 21. Stage 18 — Transport Agent

**Owner:** Developer Q  
**Branch:** `feature/transport-agent`  
**Ownership:** `/agents/research/transport/`

## Tasks

1. Define transport option schema.
2. Search inter-city transport.
3. Search local transport.
4. Estimate duration.
5. Capture departure/arrival.
6. Capture booking information.
7. Mark stale data.
8. Add confidence.
9. Add tests.

### Connectivity Check

```text
Transport Agent
 ↓
Transport Tool
 ↓
TransportOption[]
```

### Commit

```text
feat: add transport research agent
```

---

# 22. Stage 19 — Weather Agent

**Owner:** Developer R  
**Branch:** `feature/weather-agent`  
**Ownership:** `/agents/research/weather/`

## Tasks

1. Define weather schema.
2. Forecast retrieval.
3. Typical climate fallback.
4. Temperature handling.
5. Rain handling.
6. Weather-sensitive activity flag.
7. Cache by location/date.
8. Confidence handling.
9. Tests.

### Connectivity Check

```text
Weather Agent
 ↓
Weather Tool
 ↓
WeatherResult
```

### Commit

```text
feat: add weather research agent
```

---

# 23. Stage 20 — Research Manager

**Owner:** Developer I  
**Branch:** `feature/research-orchestration`  
**Ownership:** `/agents/workflow/research/`

This stage connects the independent research agents.

## Task 20.1 — Parallel execution

Run:

```text
Destination
Attraction
Experience
Food
Transport
Weather
```

in parallel where dependencies allow.

---

## Task 20.2 — Collect results

Merge results into:

```text
ResearchResults
```

---

## Task 20.3 — Handle partial failure

Example:

```text
Food Agent ✓
Weather Agent ✓
Transport Agent ✗
```

The workflow continues with an explicit missing-data marker.

---

## Task 20.4 — Research completion event

Emit:

```text
research_completed
```

---

## Task 20.5 — Tests

Test:

```text
all succeed
one fails
multiple fail
timeout
empty result
```

---

## Connectivity Check C20

```text
Trip
 ↓
Intent
 ↓
Research Manager
 ├── Destination
 ├── Attraction
 ├── Experience
 ├── Food
 ├── Transport
 └── Weather
 ↓
ResearchResults
```

### Commit

```text
feat: orchestrate parallel research agents
```

---

# 24. Stage 21 — Recommendation Agent

**Owner:** Developer S  
**Branch:** `feature/recommendation-agent`  
**Ownership:** `/agents/recommendation/`

## Task 21.1 — Recommendation schema

Include:

```text
name
category
reason
score components
confidence
sources
```

---

## Task 21.2 — Preference matching

Compare:

```text
user interests
destination research
```

---

## Task 21.3 — Geographic practicality

Use route/distance information.

---

## Task 21.4 — Time-of-day suitability

Example:

```text
Temple → morning
Food market → lunch
Night experience → evening
```

---

## Task 21.5 — Tourist/offbeat classification

Do not invent classification.

Use explicit criteria.

---

## Task 21.6 — Recommendation ranking

Create deterministic ranking function around model-provided signals.

---

## Task 21.7 — Tests

Create deterministic test fixtures.

### Connectivity Check C21

```text
ResearchResults
+
TravellerProfile
+
TripConstraints
 ↓
Recommendation Agent
 ↓
RecommendationSet
```

### Commit

```text
feat: add recommendation agent
```

---

# 25. Stage 22 — Itinerary Agent

**Owner:** Developer T  
**Branch:** `feature/itinerary-agent`  
**Ownership:** `/agents/itinerary/`

## Task 22.1 — Itinerary schema

Define:

```text
Itinerary
TripDay
ItineraryItem
```

---

## Task 22.2 — Day grouping

Group activities geographically.

---

## Task 22.3 — Time scheduling

Schedule:

```text
start
duration
end
```

---

## Task 22.4 — Travel-time insertion

Insert travel between locations.

---

## Task 22.5 — Meal placement

Reserve appropriate meal windows.

---

## Task 22.6 — Booking anchors

Locked bookings cannot be moved.

---

## Task 22.7 — Pace calculation

Prevent unrealistic schedules.

---

## Task 22.8 — Gemini generation

Gemini proposes the schedule.

Python validates it.

---

## Task 22.9 — Tests

Test:

```text
no overlap
locked booking
travel time
opening hours
rest time
multi-city
```

### Connectivity Check C22

```text
Recommendations
+
Transport
+
Bookings
+
Weather
+
Constraints
 ↓
Itinerary Agent
 ↓
Itinerary
```

### Commit

```text
feat: add itinerary planning agent
```

---

# 26. Stage 23 — Deterministic Validation Engine

**Owner:** Developer U  
**Branch:** `feature/itinerary-validation`  
**Ownership:** `/agents/validation/validators/`

This should be independent of Gemini.

## Task 23.1 — Time validator

Check:

```text
start < end
no overlap
```

---

## Task 23.2 — Opening-hours validator

Check activity against known availability.

---

## Task 23.3 — Route validator

Check travel time.

---

## Task 23.4 — Booking conflict validator

Locked bookings must not be violated.

---

## Task 23.5 — Duplicate validator

Detect duplicate activities.

---

## Task 23.6 — Date validator

Ensure all items fit trip dates.

---

## Task 23.7 — Validation result

Return:

```text
valid
errors[]
warnings[]
```

---

## Task 23.8 — Tests

At least one test for every rule.

### Connectivity Check C23

Feed intentionally invalid itinerary fixtures and confirm deterministic failures.

### Commit

```text
feat: add deterministic itinerary validators
```

---

# 27. Stage 24 — Validation Agent

**Owner:** Developer U  
**Branch:** `feature/validation-agent`  
**Ownership:** `/agents/validation/agent/`

## Tasks

1. Consume itinerary.
2. Invoke deterministic validators.
3. Aggregate failures.
4. Ask Gemini for semantic validation only where needed.
5. Produce final validation result.
6. Trigger retry/replanning if invalid.
7. Emit validation events.
8. Add tests.

### Connectivity Check

```text
Itinerary Agent
 ↓
Validation Agent
 ├── Time Validator
 ├── Route Validator
 ├── Opening Hours Validator
 └── Conflict Validator
 ↓
ValidationResult
```

### Commit

```text
feat: add itinerary validation agent
```

---

# 28. Stage 25 — Human Checkpoint

**Owner:** Developer V  
**Branch:** `feature/human-checkpoints`  
**Ownership:** `/agents/workflow/checkpoints/` + backend checkpoint API

## Task 25.1 — Decision schema

```text
DecisionCheckpoint
```

Fields:

```text
id
question
context
options
default_option
created_at
expires_at
```

---

## Task 25.2 — Pause workflow

Workflow status becomes:

```text
WAITING_FOR_USER
```

---

## Task 25.3 — Resume workflow

User decision resumes the workflow.

---

## Task 25.4 — Decision API

```http
POST /api/v1/trips/{trip_id}/decisions
```

---

## Task 25.5 — Persist decision

Store decision with workflow state.

---

## Task 25.6 — Tests

Test:

```text
pause
persist
resume
invalid option
duplicate decision
expired checkpoint
```

### Connectivity Check C25

```text
Workflow
 ↓
Checkpoint
 ↓
API
 ↓
User decision
 ↓
Workflow resume
```

### Commit

```text
feat: add human decision checkpoints
```

---

# 29. Stage 26 — Angular Agent Progress UI

**Owner:** Developer D  
**Branch:** `feature/workflow-progress-ui`  
**Ownership:** `/apps/frontend/src/app/features/workflow/`

## Task 26.1 — Workflow status component

Display:

```text
Understanding trip
Researching destinations
Finding experiences
Building itinerary
Validating itinerary
```

---

## Task 26.2 — Agent event listener

Consume SSE.

---

## Task 26.3 — Event-to-UI mapping

Map:

```text
agent_started → spinner
agent_completed → check
agent_failed → error
checkpoint_required → decision card
```

---

## Task 26.4 — Reconnect logic

If SSE disconnects:

```text
reconnect
resume current state
```

---

## Task 26.5 — Tests

Test event streams.

### Connectivity Check C26

```text
Backend emits SSE
 ↓
Angular receives event
 ↓
UI updates
```

### Commit

```text
feat: add agent workflow progress ui
```

---

# 30. Stage 27 — SSE Backend

**Owner:** Developer C  
**Branch:** `feature/workflow-sse`  
**Ownership:** `/apps/backend/app/api/workflow/`

## Task 27.1 — SSE endpoint

```http
GET /api/v1/trips/{trip_id}/workflow/stream
```

---

## Task 27.2 — Event serialization

Convert workflow events to SSE.

---

## Task 27.3 — Heartbeat

Prevent connection timeout.

---

## Task 27.4 — Reconnection

Client should be able to reconnect.

---

## Task 27.5 — Last-known event

Support resuming from workflow state.

### Connectivity Check C27

Run complete:

```text
Agent
 ↓
Event
 ↓
SSE
 ↓
Angular
```

### Commit

```text
feat: add workflow sse streaming
```

---

# 31. Stage 28 — Intelligent Replanning Engine

**Owner:** Developer W  
**Branch:** `feature/replanning-engine`  
**Ownership:** `/agents/replanning/`

The architecture explicitly requires incremental replanning rather than regenerating the whole trip.

## Task 28.1 — Change detector

Detect:

```text
item removed
item added
time changed
date changed
booking added
booking removed
preference changed
```

---

## Task 28.2 — Impact analyser

Determine:

```text
affected days
affected cities
affected itinerary items
```

---

## Task 28.3 — Preserve unaffected state

Unaffected days must remain unchanged.

---

## Task 28.4 — Preserve locked items

Locked bookings must remain fixed.

---

## Task 28.5 — Replanning prompt

Only send relevant context to Gemini.

---

## Task 28.6 — Revalidate

Every replanned result goes through the same validators.

---

## Task 28.7 — Version creation

Create:

```text
TripVersion N+1
```

---

## Task 28.8 — Undo

Restore previous version.

---

## Task 28.9 — Tests

Test:

```text
remove attraction
add attraction
change date
change booking
change preference
```

### Connectivity Check C28

```text
Existing Itinerary
 ↓
Change Detector
 ↓
Impact Analysis
 ↓
Replanning Agent
 ↓
Validation
 ↓
New TripVersion
```

### Commit

```text
feat: add incremental itinerary replanning
```

---

# 32. Stage 29 — Angular Itinerary UI

**Owner:** Developer X  
**Branch:** `feature/itinerary-ui`  
**Ownership:** `/apps/frontend/src/app/features/itinerary/`

## Task 29.1 — Day-by-day layout

Display:

```text
Day 1
Day 2
Day 3
...
```

---

## Task 29.2 — Itinerary item card

Display:

```text
name
type
time
duration
location
description
confidence
```

---

## Task 29.3 — Map integration placeholder

Create interface for map view.

---

## Task 29.4 — Locked item visual state

Clearly identify bookings/locked activities.

---

## Task 29.5 — Edit interaction

Allow:

```text
remove
move
replace
lock
unlock
```

---

## Task 29.6 — Version/undo UI

Display:

```text
Current version
Previous version
Undo
```

---

## Task 29.7 — Accessibility

Implement:

- keyboard navigation
- semantic headings
- accessible buttons
- focus management

### Connectivity Check C29

```text
GET trip
 ↓
Angular itinerary
 ↓
edit action
 ↓
PATCH/replan API
 ↓
updated itinerary
```

### Commit

```text
feat: add itinerary experience
```

---

# 33. Stage 30 — Packing Agent

**Owner:** Developer Y  
**Branch:** `feature/packing-agent`  
**Ownership:** `/agents/preparation/packing/`

## Tasks

1. Define packing schema.
2. Consume weather.
3. Consume destination.
4. Consume itinerary activities.
5. Generate clothing.
6. Generate activity-specific items.
7. Generate electronics.
8. Generate document reminders.
9. Add confidence/assumptions.
10. Add tests.

### Connectivity Check

```text
Weather + Destination + Itinerary
 ↓
Packing Agent
 ↓
PackingList
```

### Commit

```text
feat: add packing agent
```

---

# 34. Stage 31 — Visa & Travel Readiness Agent

**Owner:** Developer Z  
**Branch:** `feature/readiness-agent`  
**Ownership:** `/agents/preparation/readiness/`

## Tasks

1. Define readiness schema.
2. Identify visa information requirement.
3. Identify document requirements.
4. Add insurance reminder.
5. Add connectivity checklist.
6. Add currency checklist.
7. Add travel advisory source.
8. Capture official source links.
9. Mark volatile information.
10. Add tests.

### Important rule

The agent must not present volatile visa/entry information as permanently valid.

### Connectivity Check

```text
Traveller Profile
+
Destination
+
Travel Date
 ↓
Readiness Agent
 ↓
ReadinessChecklist
```

### Commit

```text
feat: add travel readiness agent
```

---

# 35. Stage 32 — Sharing

**Owner:** Developer AA  
**Branch:** `feature/trip-sharing`  
**Ownership:** Sharing backend + sharing frontend feature directories

## Task 32.1 — Share model

Fields:

```text
share_id
trip_id
token
expires_at
created_at
```

---

## Task 32.2 — Generate share link

---

## Task 32.3 — Read-only shared itinerary API

---

## Task 32.4 — Share page

---

## Task 32.5 — Revoke link

---

## Task 32.6 — Security

No private user profile data should leak.

### Connectivity Check

```text
Owner
 ↓
Create share
 ↓
Share URL
 ↓
Unauthenticated viewer
 ↓
Read-only itinerary
```

### Commit

```text
feat: add trip sharing
```

---

# 36. Stage 33 — Agent Observability

**Owner:** Developer AB  
**Branch:** `feature/agent-tracing`  
**Ownership:** `/dev-tools/`, `/agents/common/tracing/`

The technical design requires every agent execution to be observable and a developer-only trace viewer.

## Task 33.1 — OpenTelemetry setup

Instrument:

```text
workflow
agent
tool
Gemini call
database
external API
```

---

## Task 33.2 — Trace context propagation

Every workflow must carry:

```text
trace_id
workflow_id
trip_id
```

---

## Task 33.3 — Agent spans

Every agent creates a span.

---

## Task 33.4 — Tool spans

Every tool call creates a child span.

---

## Task 33.5 — Gemini spans

Capture:

```text
model
latency
status
token metadata where available
```

Do not store raw secrets.

---

## Task 33.6 — Redaction

Redact:

```text
email
phone
booking numbers
payment information
authentication tokens
```

---

## Task 33.7 — Jaeger integration

Send traces to local Jaeger.

---

## Task 33.8 — Trace viewer

Create:

```text
/dev/traces/{trace_id}
```

---

## Task 33.9 — Timeline

Display:

```text
Agent
Start
End
Duration
Status
Parent
```

---

## Task 33.10 — Tool call details

Display tool calls under agents.

---

## Task 33.11 — Error details

Display errors and failed spans.

---

## Task 33.12 — Production protection

Disable or protect trace UI in production.

### Connectivity Check C33

Run:

```text
Trip Workflow
 ↓
Intent Agent
 ↓
Gemini
 ↓
Research Tool
 ↓
Trace
 ↓
Jaeger
 ↓
Trace Viewer
```

### Commit

```text
feat: add agent workflow tracing
```

---

# 37. Stage 34 — Security Foundation

**Owner:** Developer AC  
**Branch:** `feature/security`  
**Ownership:** `/apps/backend/app/core/security/`, authentication feature directories

## Task 34.1 — Authentication abstraction

Do not tightly couple business logic to one authentication provider.

---

## Task 34.2 — Authorisation

Define:

```text
user owns trip
user can modify own trip
shared viewer can only read
developer trace access is restricted
```

---

## Task 34.3 — Rate limiting

Apply limits to:

```text
trip creation
AI workflows
research endpoints
share creation
```

---

## Task 34.4 — Input validation

All external inputs validated by Pydantic/business rules.

---

## Task 34.5 — Secret management

Local:

```text
.env
```

Production:

```text
Google Secret Manager
```

---

## Task 34.6 — Security tests

Test:

```text
unauthorised trip access
cross-user trip access
invalid tokens
rate limits
```

### Commit

```text
feat: add application security controls
```

---

# 38. Stage 35 — AI Guardrails

**Owner:** Developer AD  
**Branch:** `feature/ai-guardrails`  
**Ownership:** `/agents/common/guardrails/`

## Task 35.1 — Structured output validation

Every Gemini response must pass schema validation.

---

## Task 35.2 — Prompt injection filtering

Sanitise external content.

---

## Task 35.3 — Source attribution

Research outputs must retain source metadata.

---

## Task 35.4 — Hallucination checks

Require:

```text
source
confidence
verification_required
```

where appropriate.

---

## Task 35.5 — Unsupported claim handling

Agents must be able to return:

```text
UNKNOWN
NOT_VERIFIED
```

instead of inventing data.

---

## Task 35.6 — Guardrail tests

Create adversarial fixtures:

```text
malicious web content
invalid model JSON
missing sources
conflicting sources
prompt injection
```

### Commit

```text
feat: add ai output guardrails
```

---

# 39. Stage 36 — Agent Evaluation Suite

**Owner:** Developer AE  
**Branch:** `feature/agent-evaluation`  
**Ownership:** `/tests/evaluation/`

## Task 36.1 — Intent evaluation

Metrics:

```text
field accuracy
missing-field detection
invalid-value rate
```

---

## Task 36.2 — Recommendation evaluation

Check:

```text
interest alignment
duplicate rate
source presence
confidence quality
```

---

## Task 36.3 — Itinerary evaluation

Check:

```text
date correctness
time correctness
travel feasibility
booking preservation
activity diversity
```

---

## Task 36.4 — Replanning evaluation

Check:

```text
requested change applied
unaffected days preserved
locked items preserved
new plan validated
```

---

## Task 36.5 — Regression fixtures

Store known scenarios:

```text
fixtures/
├── japan-food-temples/
├── family-trip/
├── budget-trip/
├── multi-city/
└── replanning/
```

### Commit

```text
test: add agent evaluation suite
```

---

# 40. Stage 37 — End-to-End Workflow

**Owner:** Developer AF  
**Branch:** `feature/e2e-workflow`  
**Ownership:** `/tests/e2e/`

## Task 37.1 — Create test trip

Use deterministic fixture.

---

## Task 37.2 — Run full workflow

```text
Trip Manager
 ↓
Intent
 ↓
Profile
 ↓
Research
 ↓
Recommendation
 ↓
Itinerary
 ↓
Validation
```

---

## Task 37.3 — Human checkpoint

Force a checkpoint.

---

## Task 37.4 — Resume

Submit test decision.

---

## Task 37.5 — Replan

Change one activity.

---

## Task 37.6 — Verify unaffected days

Compare versions.

---

## Task 37.7 — Verify trace

Ensure trace exists.

---

## Task 37.8 — Verify database

Check:

```text
trip
version
itinerary
decision
trace metadata
```

### Commit

```text
test: add end to end agent workflow
```

---

# 41. Stage 38 — Docker Integration

**Owner:** Developer B  
**Branch:** `feature/docker-finalisation`  
**Ownership:** Docker files and Compose only

## Task 38.1 — Final backend image

Ensure:

```text
docker build backend
```

works.

---

## Task 38.2 — Final frontend image

Ensure:

```text
docker build frontend
```

works.

---

## Task 38.3 — Production-like Compose

Start:

```text
frontend
backend
postgres
redis
jaeger
```

---

## Task 38.4 — Environment isolation

Ensure secrets are injected through environment variables.

---

## Task 38.5 — Startup dependency checks

Backend waits for database readiness.

---

## Task 38.6 — Smoke test script

Create:

```bash
./scripts/smoke-test.sh
```

### Connectivity Check C38

One command:

```bash
docker compose up --build
```

must bring up the complete prototype.

### Commit

```text
chore: finalise containerised local stack
```

---

# 42. Stage 39 — Cloud Infrastructure

**Owner:** Developer AG  
**Branch:** `feature/gcp-infrastructure`  
**Ownership:** `/infrastructure/terraform/`

## Task 39.1 — GCP project configuration

Define:

```text
project
region
services
```

---

## Task 39.2 — Enable required APIs

Enable only required services.

---

## Task 39.3 — Cloud Run frontend

Define service.

---

## Task 39.4 — Cloud Run backend

Define service.

---

## Task 39.5 — Cloud SQL

Create PostgreSQL instance.

---

## Task 39.6 — Redis

Create production Redis solution appropriate to prototype budget.

---

## Task 39.7 — Secret Manager

Create secrets.

---

## Task 39.8 — Service accounts

Use least privilege.

---

## Task 39.9 — IAM

Backend receives only required permissions.

### Commit

```text
feat: add gcp infrastructure
```

---

# 43. Stage 40 — Cloud Deployment

**Owner:** Developer AH  
**Branch:** `feature/gcp-deployment`

## Task 40.1 — Build frontend image

---

## Task 40.2 — Build backend image

---

## Task 40.3 — Push images

Use a Google Cloud container registry/artifact repository.

---

## Task 40.4 — Deploy frontend

---

## Task 40.5 — Deploy backend

---

## Task 40.6 — Configure frontend backend URL

---

## Task 40.7 — Configure secrets

---

## Task 40.8 — Configure health checks

---

## Task 40.9 — Configure logs

---

## Task 40.10 — Configure metrics

### Connectivity Check C40

```text
Browser
 ↓
Cloud Run Frontend
 ↓
Cloud Run Backend
 ↓
Cloud SQL
 ↓
Redis
 ↓
Gemini
```

### Commit

```text
feat: deploy application to cloud run
```

---

# 44. Stage 41 — CI Pipeline

**Owner:** Developer AI  
**Branch:** `feature/ci-pipeline`  
**Ownership:** `.github/workflows/`

## Task 41.1 — Lint frontend

---

## Task 41.2 — Lint backend

---

## Task 41.3 — Type checks

---

## Task 41.4 — Backend unit tests

---

## Task 41.5 — Frontend unit tests

---

## Task 41.6 — Contract tests

---

## Task 41.7 — Build Docker images

---

## Task 41.8 — Security scan

---

## Task 41.9 — E2E tests

---

## Task 41.10 — Deployment workflow

Deploy only after required checks pass.

### Commit

```text
ci: add validation and deployment pipeline
```

---

# 45. Stage 42 — Observability & Monitoring

**Owner:** Developer AB  
**Branch:** `feature/cloud-observability`

## Task 42.1 — Cloud Logging

Verify structured logs.

---

## Task 42.2 — Cloud Monitoring

Create:

```text
request latency
error rate
Cloud Run instance count
```

---

## Task 42.3 — AI metrics

Track:

```text
workflow duration
agent duration
Gemini latency
workflow failure rate
```

---

## Task 42.4 — Alerts

Create alerts for:

```text
high 5xx
high latency
workflow failure spike
```

### Commit

```text
feat: add cloud observability
```

---

# 46. Stage 43 — Accessibility and UI Quality

**Owner:** Frontend developer  
**Branch:** `feature/accessibility`

## Task 43.1 — Keyboard navigation

---

## Task 43.2 — Screen reader labels

---

## Task 43.3 — Focus management

---

## Task 43.4 — Colour contrast

---

## Task 43.5 — Responsive layouts

---

## Task 43.6 — Loading states

---

## Task 43.7 — Error states

---

## Task 43.8 — Empty states

---

## Task 43.9 — Accessibility test

Run automated accessibility checks and manual keyboard testing.

### Commit

```text
feat: improve accessibility and responsive ui
```

---

# 47. Stage 44 — Final Hackathon Demo Flow

**Owner:** Demo/integration owner  
**Branch:** `feature/demo-hardening`

The demo should demonstrate the entire agentic capability.

## Demo Step 1

Create trip:

```text
10 days in Japan
from Pune
food + temples
moderate budget
relaxed pace
```

---

## Demo Step 2

Show live agent progress:

```text
Intent
Research
Recommendations
Itinerary
Validation
```

---

## Demo Step 3

Show generated itinerary.

---

## Demo Step 4

Show recommendation sources/confidence.

---

## Demo Step 5

Trigger human checkpoint.

---

## Demo Step 6

User chooses option.

---

## Demo Step 7

Workflow resumes.

---

## Demo Step 8

Remove one activity.

---

## Demo Step 9

Show incremental replanning.

---

## Demo Step 10

Show that unaffected days remain unchanged.

---

## Demo Step 11

Open developer trace viewer.

Show:

```text
Trip Manager
 ↓
Intent Agent
 ↓
Research Agents
 ↓
Recommendation
 ↓
Itinerary
 ↓
Validation
```

---

## Demo Step 12

Show Docker/GCP deployment.

---

# 48. Merge Strategy

The team should not merge branches randomly.

Use this dependency order:

```text
Bootstrap
   │
   ├── Local Infrastructure
   ├── Backend Foundation
   ├── Frontend Foundation
   └── Contracts
           │
           ├── Database
           ├── Redis
           ├── Gemini Client
           └── Agent Framework
                    │
                    ├── Intent
                    ├── Profile
                    ├── Research Tools
                    │       ├── Destination
                    │       ├── Attractions
                    │       ├── Experiences
                    │       ├── Food
                    │       ├── Transport
                    │       └── Weather
                    │
                    ├── Recommendation
                    ├── Itinerary
                    └── Validation
                              │
                              ├── Checkpoint
                              ├── Replanning
                              └── Preparation
                                      │
                                      ├── Frontend
                                      ├── Tracing
                                      ├── Security
                                      └── Cloud
```

---

# 49. Merge Gates

A feature cannot merge until:

## Gate 1 — Build

```text
Build passes
```

## Gate 2 — Unit tests

```text
Unit tests pass
```

## Gate 3 — Contract

```text
Shared contracts unchanged or intentionally versioned
```

## Gate 4 — Ownership

```text
No unexpected files outside assigned ownership
```

## Gate 5 — Integration

The developer provides a short connectivity test.

Example:

```text
Agent → Tool → Result
```

## Gate 6 — Documentation

README or component documentation updated if the interface changed.

---

# 50. How to Avoid Merge Conflicts

## Rule 1

Do not modify another team's directories unless explicitly coordinated.

## Rule 2

Do not create shared helper functions in random locations.

All shared utilities go under:

```text
agents/common/
apps/backend/app/core/
frontend/shared/
packages/contracts/
```

## Rule 3

Do not modify database models for another feature without coordination.

## Rule 4

Do not manually edit generated OpenAPI clients.

## Rule 5

Do not commit generated files unless the repository strategy explicitly requires them.

## Rule 6

Keep commits small.

Bad:

```text
feat: implement whole application
```

Good:

```text
feat: add itinerary schema
feat: add itinerary validator
feat: add itinerary agent
```

## Rule 7

Rebase before opening a PR.

```bash
git fetch origin
git rebase origin/main
```

## Rule 8

One feature branch should have one clear purpose.

---

# 51. Coding Agent Instructions

Every coding agent should receive the following context:

```text
You are working in the AI Trip Planner monorepo.

Rules:
1. Only modify files inside your assigned ownership boundary.
2. Do not refactor unrelated code.
3. Do not rename shared files without approval.
4. Use existing contracts instead of creating duplicate schemas.
5. Add unit tests for every new behaviour.
6. Do not call Gemini directly outside GeminiClient.
7. Do not call databases directly from agents.
8. Agents must use typed workflow state.
9. AI output must be validated before persistence.
10. Do not add secrets to the repository.
11. Run tests before committing.
12. Provide a connectivity test for your component.
13. Keep public interfaces backward compatible.
14. If a contract must change, modify packages/contracts first and clearly document the change.
15. Do not modify another feature's implementation to make your task easier.
```

---

# 52. Standard Task Definition Template

Every task should be issued to a coding agent using this format:

```text
TASK ID:
TASK NAME:

OWNER:
BRANCH:

OBJECTIVE:

OWNED FILES/DIRECTORIES:

DO NOT MODIFY:

INPUT CONTRACT:

OUTPUT CONTRACT:

IMPLEMENTATION STEPS:

UNIT TESTS:

INTEGRATION TEST:

ACCEPTANCE CRITERIA:

CONNECTIVITY CHECK:

EXPECTED COMMIT:

DEPENDENCIES:
```

---

# 53. Example Coding-Agent Task

```text
TASK ID:
AGENT-INTENT-001

TASK NAME:
Implement Intent Agent

OWNER:
Agent Developer

BRANCH:
feature/intent-agent

OWNED FILES:
/agents/intent/**

DO NOT MODIFY:
/agents/research/**
/apps/frontend/**
/infrastructure/**
/packages/contracts/**

OBJECTIVE:
Convert natural-language trip input into structured TripIntent.

INPUT:
TripPlanningState with raw_user_request.

OUTPUT:
TripIntent.

IMPLEMENTATION:
1. Create IntentAgent.
2. Create system prompt.
3. Call GeminiClient.
4. Parse structured response.
5. Validate with Pydantic.
6. Populate workflow state.
7. Return AgentResult.

TESTS:
1. Normal request.
2. Missing destination.
3. Missing dates.
4. Ambiguous request.
5. Invalid Gemini response.
6. Gemini timeout.

CONNECTIVITY:
Mock GeminiClient → IntentAgent → TripIntent.

COMMIT:
feat: add trip intent agent
```

---

# 54. Final Component Dependency Matrix

| Component | Depends On | Must Not Depend On |
|---|---|---|
| Angular Core | Contracts | Agent implementation |
| Trip Input UI | Trip API | Database |
| FastAPI API | Services, contracts | Angular |
| Repository | Database | Gemini |
| Gemini Client | Gemini SDK | Agent-specific code |
| Base Agent | Contracts, Gemini abstraction | Frontend |
| Intent Agent | Base Agent, Gemini | Database |
| Research Tools | External APIs | Angular |
| Research Agents | Tools, Gemini | Frontend |
| Recommendation Agent | Research state | Angular |
| Itinerary Agent | Recommendations, transport, bookings | Angular |
| Validators | Pure domain models | Gemini |
| Validation Agent | Validators | Angular |
| Replanning Agent | Itinerary + validators | Frontend |
| SSE | Workflow events | Angular implementation |
| Trace Layer | Agent/tool workflow | Business logic |
| Trace Viewer | Trace API | Agent implementation |
| Cloud Infrastructure | Container images | Application internals |

---

# 55. Parallel Development Plan

Once Stages 0–8 are complete, development can proceed in parallel.

```text
                     Shared Foundation
                            │
              ┌─────────────┼──────────────┐
              │             │              │
              ▼             ▼              ▼
         Frontend       Research        Platform
              │             │              │
              │       ┌─────┼─────┐        │
              │       ▼     ▼     ▼        │
              │      Dest  Attr  Exp       │
              │       │     │     │        │
              │       └─────┼─────┘        │
              │             ▼              │
              │       Recommendation       │
              │             │              │
              │        Itinerary           │
              │             │              │
              │        Validation          │
              │             │              │
              └─────────────┼──────────────┘
                            ▼
                       Integration
                            │
                 ┌──────────┼───────────┐
                 ▼          ▼           ▼
             Replanning  Tracing     Security
                 │          │           │
                 └──────────┼───────────┘
                            ▼
                       GCP Deployment
```

---

# 56. Critical Connectivity Checkpoints

These are the points where separate workstreams must be integrated.

## C0 — Repository

```text
Everyone can clone repository
```

## C1 — Infrastructure

```text
Backend ↔ PostgreSQL
Backend ↔ Redis
Backend ↔ Jaeger
```

## C2 — Backend

```text
FastAPI → health
```

## C3 — Frontend

```text
Angular → FastAPI
```

## C4 — Contracts

```text
Angular ↔ shared contracts ↔ FastAPI
```

## C5 — Persistence

```text
API ↔ PostgreSQL
```

## C6 — Cache

```text
Backend ↔ Redis
```

## C7 — AI

```text
GeminiClient → Gemini → structured output
```

## C8 — Agents

```text
Agent A → State → Agent B
```

## C9 — Trip Vertical Slice

```text
Angular → API → DB
```

## C20 — Research

```text
Workflow → Research Manager → Research Agents
```

## C21 — Recommendations

```text
Research → Recommendation
```

## C22 — Itinerary

```text
Recommendations → Itinerary
```

## C23 — Validation

```text
Itinerary → Validators
```

## C25 — Human Loop

```text
Workflow → UI → Decision → Workflow
```

## C27 — Streaming

```text
Workflow → SSE → Angular
```

## C28 — Replanning

```text
Existing Plan → Change → Replan → Validate
```

## C33 — Trace

```text
Workflow → OpenTelemetry → Jaeger → Trace UI
```

## C38 — Container

```text
Docker Compose → Full local stack
```

## C40 — Cloud

```text
Browser → Cloud Run Frontend → Cloud Run Backend → GCP services
```

## C44 — Final

```text
User → Full agentic workflow → Final itinerary
```

---

# 57. Recommended Team Assignment

For a large parallel team:

```text
Person 1  → Repository / contracts
Person 2  → Local infrastructure
Person 3  → Backend foundation
Person 4  → Angular foundation
Person 5  → Database
Person 6  → Redis
Person 7  → Gemini client
Person 8  → Agent framework
Person 9  → Intent agent
Person 10 → Profile agent
Person 11 → Research tools
Person 12 → Destination agent
Person 13 → Attraction agent
Person 14 → Experience agent
Person 15 → Food agent
Person 16 → Transport agent
Person 17 → Weather agent
Person 18 → Research orchestration
Person 19 → Recommendation agent
Person 20 → Itinerary agent
Person 21 → Validation
Person 22 → Human checkpoints
Person 23 → Replanning
Person 24 → Frontend itinerary
Person 25 → Preparation agents
Person 26 → Traceability
Person 27 → Security
Person 28 → Evaluation
Person 29 → GCP
Person 30 → CI/CD
```

For a smaller team, multiple work packages can be assigned to one person, but the **directory ownership boundaries should remain the same**.

---

# 58. Minimum Viable Hackathon Path

If time becomes constrained, implement these stages first:

```text
1. Bootstrap
2. Docker infrastructure
3. Backend foundation
4. Frontend foundation
5. Contracts
6. Database
7. Gemini client
8. Agent framework
9. Intent Agent
10. Research Manager
11. Destination Agent
12. Attraction Agent
13. Experience Agent
14. Recommendation Agent
15. Itinerary Agent
16. Validation
17. SSE
18. Human checkpoint
19. Replanning
20. Trace viewer
21. Cloud Run
22. End-to-end testing
```

The following can then be added if time permits:

```text
Food Agent
Transport Agent
Weather Agent
Packing Agent
Readiness Agent
Sharing
Advanced security
Advanced monitoring
```

---

# 59. Final Definition of Done

The prototype is considered technically complete when:

## Frontend

- [ ] Angular application runs in Docker.
- [ ] User can create a trip.
- [ ] User sees agent progress.
- [ ] User sees itinerary.
- [ ] User can make a workflow decision.
- [ ] User can modify the itinerary.
- [ ] User sees replanning results.
- [ ] User can view preparation information.
- [ ] UI is accessible.

## Backend

- [ ] FastAPI runs in Docker.
- [ ] REST APIs work.
- [ ] SSE works.
- [ ] PostgreSQL persistence works.
- [ ] Redis works.
- [ ] API contracts are tested.
- [ ] Error handling is standardised.

## AI

- [ ] Gemini is integrated.
- [ ] Structured outputs are used.
- [ ] Multiple specialised agents exist.
- [ ] Agents communicate through typed state.
- [ ] Agent workflow is orchestrated.
- [ ] Research tools are integrated.
- [ ] AI output is validated.

## Agentic

- [ ] Intent Agent
- [ ] Profile Agent
- [ ] Destination Agent
- [ ] Attraction Agent
- [ ] Experience Agent
- [ ] Food Agent
- [ ] Transport Agent
- [ ] Weather Agent
- [ ] Recommendation Agent
- [ ] Itinerary Agent
- [ ] Validation Agent
- [ ] Replanning Agent
- [ ] Preparation agents

## Observability

- [ ] Every agent creates trace spans.
- [ ] Tool calls are visible.
- [ ] Gemini calls are traceable.
- [ ] Trace IDs propagate through workflow.
- [ ] Developer trace UI works.
- [ ] Production trace UI is protected/disabled.

## Cloud

- [ ] Frontend container deploys to Cloud Run.
- [ ] Backend container deploys to Cloud Run.
- [ ] Database works on GCP.
- [ ] Redis works.
- [ ] Gemini works.
- [ ] Secrets are protected.
- [ ] Logs are available.
- [ ] Health checks work.

## Engineering

- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] Contract tests pass.
- [ ] Agent evaluation tests pass.
- [ ] E2E workflow passes.
- [ ] Docker Compose works.
- [ ] CI passes.
- [ ] No secrets in Git.
- [ ] No unresolved merge conflicts.
- [ ] Documentation is updated.

---

# 60. Final Engineering Principle

The project should be developed as a set of **independent vertical capabilities connected by explicit contracts**.

The intended development model is:

```text
                   CONTRACTS
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    FRONTEND        BACKEND           AGENTS
       │               │                │
       │               │        ┌───────┼────────┐
       │               │        ▼       ▼        ▼
       │               │      RESEARCH RECO   ITINERARY
       │               │        │       │        │
       │               │        └───────┼────────┘
       │               │                ▼
       │               │           VALIDATION
       │               │                │
       └───────────────┼────────────────┘
                       ▼
                  INTEGRATION
                       │
                       ▼
                 OBSERVABILITY
                       │
                       ▼
                   CLOUD RUN
```

The key rule is:

> **A developer should be able to complete, test and commit their component without needing to modify another team's implementation.**

When integration is required, it should happen through:

```text
1. Shared contract
2. Typed interface
3. Mock implementation
4. Connectivity test
5. Integration test
```

rather than by directly coupling implementation details.

This approach preserves independent development, minimises merge conflicts, allows coding agents to work safely in parallel, and still produces one coherent agentic application.
