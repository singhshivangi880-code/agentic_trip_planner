# AI-Powered Agentic Trip Planner

An agentic travel planning application built with Angular, Python/FastAPI, LangGraph, Google Gemini, PostgreSQL, and Redis.

## Architecture Baseline
- **Frontend:** Angular (Cloud Run)
- **Backend:** Python / FastAPI (Cloud Run)
- **AI & Orchestration:** Google Gemini, LangGraph
- **Database & Caching:** PostgreSQL, Redis
- **Observability:** OpenTelemetry / Jaeger

## Repository Structure
```
ai-trip-planner/
├── apps/
│   ├── frontend/
│   └── backend/
├── packages/
│   └── contracts/
├── agents/
├── tools/
├── dev-tools/
├── infrastructure/
├── tests/
└── docs/
```

## Quick Start
1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
2. Start local development environment:
   ```bash
   docker compose up
   ```

## Development Rules
See [CONTRIBUTING.md](file:///Users/shivangisingh/AI_Builder_Cup/agentic_trip_planner/CONTRIBUTING.md) for branch strategy, contract-first rules, and directory ownership.
