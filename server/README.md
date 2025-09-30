# GeoResolve Server (Django)

## Quickstart
- Python version: 3.11 (recommended). 3.13 호환은 아직 보장되지 않습니다.
- Create env: `python -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r server/requirements.txt`
- Run dev: `python server/manage.py migrate && python server/manage.py runserver`

## Endpoints
- `GET /healthz/` — liveness
- `GET /api/v1/ping/` — resolver service ping
- `GET /api/v1/resolve/?q=permian` — demo resolve

## Auth & Docs
- JWT: `POST /api/token/` (username/password) → access/refresh, `POST /api/token/refresh/`
- OpenAPI JSON: `GET /api/schema/`
- Swagger UI: `GET /api/docs/`

## Settings
- Default dev settings: `config.settings.dev` (SQLite)
- Override DB with `DATABASE_URL` (PostgreSQL)

## Docker Compose
- Start: `docker compose up --build`
- Services: Postgres(:5432), Redis(:6379), API(:8000), Web(:3000), Celery worker, Celery beat

## Admin bootstrap
- Create superuser from env (dev):
  - `ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=admin123 python server/manage.py create_default_admin`

## Load seed authority data
- CSVs live under `data/ics/2023/terms.csv` and `data/ics/2023/synonyms.csv`.
- Load locally: `python server/manage.py load_authority data/ics/2023 --slug ics-2023 --name ICS --version 2023`
- Compose (API container): `docker compose exec api python server/manage.py load_authority data/ics/2023`
- Celery Beat runs a daily sync task; override path with `AUTHORITY_SEED_PATH`.

## Python 3.13 사용 시 권장
- 아직 일부 의존성이 3.13 빌드/배포가 불완전할 수 있습니다.
- 옵션 A: Docker/Compose로 실행 (호스트 Python 버전 무관)
- 옵션 B: `pyenv`로 3.11 설치 후 사용
  - `pyenv install 3.11.9 && pyenv local 3.11.9`
  - 이후 Quickstart 절차 동일
