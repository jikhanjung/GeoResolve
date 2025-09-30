# GeoResolve 기술 스택

## 개요
지질 용어 표준화·검증 서비스 특성상 실시간 제안, 데이터 동기화(권위 파일), 온프렘 배포가 중요합니다. 이에 따라 서버는 안정적인 Django LTS와 Postgres 중심, 클라이언트는 웹/플러그인 병행 구조로 설계합니다.

## 서버(Backend)
- 프레임워크: Python 3.11, Django 4.2 LTS, Django REST Framework(DRF)
- API 규격: drf-spectacular(OpenAPI), 버전 경로 ` /api/v1/... `
- 데이터베이스: PostgreSQL 15+ (`pg_trgm`, `unaccent`, 선택: `pgvector`)
- 캐시/큐: Redis, Celery + Celery Beat(정기 동기화/ETL), 모니터링 Flower
- 검색/매칭: rapidfuzz(문자열 유사도) + 규칙 검증, Postgres GIN + trigram 인덱스
- 인증/권한: `djangorestframework-simplejwt`(JWT), 필요 시 `django-guardian`(객체 권한)
- 실시간(옵션): Django Channels(WebSocket) — 대용량은 폴백(서버 이벤트/폴링) 고려
- 설정/보안: `settings/{base,dev,prod}.py`, `.env` 관리(`django-environ`), CORS/CSRF 정책 명시
- 로깅/관측: Sentry, Prometheus exporter, 구조화 로깅(structlog)
- 배포: Docker 이미지, Gunicorn + Nginx(리버스 프록시), 마이그레이션 `python manage.py migrate`

예시 명령
- 개발 서버: `python manage.py runserver`
- 마이그레이션: `python manage.py makemigrations && python manage.py migrate`
- 워커: `celery -A config.celery_app worker -l info` / 스케줄러: `celery -A config.celery_app beat -l info`

## 클라이언트(Frontend & Plugins)
- 웹 앱: Next.js(React + TypeScript), 상태/데이터 `TanStack Query`, UI(Chakra UI 또는 MUI)
- API 연동: OpenAPI 기반 SDK 자동생성(`openapi-typescript`/`openapi-generator`), 요청은 `fetch` 래퍼 또는 `axios`
- 국제화: `react-i18next`(한/영 우선), 접근성 지침 준수(WAI-ARIA)
- Word/Overleaf Add-in: Office.js + React(Vite), 배포는 Add-in manifest(XML)로 사이드로드/스토어 배포
- QGIS 플러그인: PyQGIS + Qt(PyQt5/6), API 호출로 용어 표준화/검증, 플러그인 빌더/리포지터리 배포
- 테스트: Jest/Vitest(Unit), Playwright(E2E, 웹), ESLint + Prettier(스타일)

## 데이터/ETL
- 소스: ICS 연도별 시대표, 지역 Stratigraphic Lexicon, 지질도/시추 메타데이터
- 파이프라인: Django management command + Celery task(증분 동기화), pandas/polars 활용
- 저장: 정규화된 테이블 + 검색 보조 인덱스(trigram/vector), 원천 데이터 라이선스 존중(원본 미커밋)
 - 로더: `python server/manage.py load_authority data/ics/2023` (Celery Beat로 일일 동기화)

## 로컬 개발/운영
- Docker Compose: `web(api)`, `worker`, `beat`, `db(postgres)`, `redis`, (선택)`meilisearch`
- 실행: `docker compose up -d` | 환경: `.env`(예: `POSTGRES_DB`, `REDIS_URL`)
- 브랜치/버전: SemVer, API는 `v1` 유지(파괴적 변경 시 `v2`), 마이그레이션은 하위호환 우선

## 디렉터리 권장 구조(개요)
- `server/`(Django 프로젝트: `config/`, `apps/{resolver,authority,accounts,audit}`, `manage.py`)
- `clients/web/`(Next.js), `clients/word-addin/`, `clients/qgis-plugin/`
- `data/`(권위 파일, 시드), `scripts/`(ETL/유틸), `docs/`(문서), `tests/`
