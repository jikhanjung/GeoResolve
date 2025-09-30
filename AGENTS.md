# Repository Guidelines

## Project Structure & Module Organization
- `server/`: FastAPI service (API, resolver engine, DB models).
- `clients/`: Plugins and UIs — `word-addin/`, `qgis-plugin/`, `web/`.
- `data/`: Authority files (ICS timescales, stratigraphic lexicons) and seeds.
- `tests/`: Unit/integration tests with fixtures under `tests/fixtures/`.
- `scripts/`: ETL, data loaders, and maintenance tasks.
- `docs/`: Architecture notes, API schema, ADRs.

## Build, Test, and Development Commands
- Backend dev: `uvicorn server.app:app --reload` — run API locally.
- Install (Python): `pip install -e server[dev]` or `make setup` if provided.
- Tests (Python): `pytest -q` and coverage with `pytest --cov=server`.
- Lint/format: `ruff check server` and `black server`.
- Type check: `mypy server`.
- Frontend/plugins: `npm i && npm run dev` in each client folder; `npm test` for JS/TS tests.

## Coding Style & Naming Conventions
- Python: Black (88 cols), Ruff rules, type hints required on public APIs; modules `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- JS/TS: Prettier + ESLint (Airbnb/TS), `strict` TypeScript; files `kebab-case.tsx/ts`.
- API paths: `/v1/{resource}`; functions `verb_noun` (e.g., `resolve_term`).
- Data files: `data/{source}/{version}/...` with provenance in a sidecar `metadata.json`.

## Testing Guidelines
- Frameworks: `pytest` for backend, Jest/Vitest for clients.
- Layout: `tests/test_*.py` mirrors `server/` packages; fixtures in `tests/fixtures/`.
- Coverage: aim ≥ 85% overall, 100% for resolver core and validators.
- Integration: include sample ICS and lexicon slices for deterministic checks.

## Commit & Pull Request Guidelines
- Commits: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`). Keep small, scoped.
- PRs: clear description, linked issues, screenshots/CLI output for UX changes, and notes on data/migrations.
- API changes: update OpenAPI (`docs/openapi.json`) and bump minor/major per semver.
- Data updates: include provenance in `data/*/metadata.json` and do not commit raw licensed datasets.

## Security & Configuration Tips
- Secrets via `.env` (provide `.env.example`); never commit credentials.
- Use least-privilege DB roles; run Redis/PostgreSQL locally via `docker compose up db redis`.
- Validate inputs in resolvers; prefer allowlists for authority sources.
