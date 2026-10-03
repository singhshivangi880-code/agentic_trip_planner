# Contribution & Development Guidelines

## Directory Ownership
- `/apps/frontend/` → Frontend development
- `/apps/backend/` → Backend/API development
- `/agents/` → Agent development & LangGraph orchestrator
- `/packages/contracts/` → Contract & schema definitions
- `/tools/` → Search, maps, weather, transport tools
- `/infrastructure/` → Docker, Terraform & Cloud Run configs
- `/dev-tools/` → Observability & trace viewer

## Development Rules
1. **Contract First:** Agree on API and SSE schemas in `/packages/contracts/` before implementing features.
2. **Directory Isolation:** Modify only files inside your assigned directory scope.
3. **No Secrets:** Never commit `.env` or secret keys to Git.
4. **Testing:** Run local unit and contract tests before submitting PRs.
