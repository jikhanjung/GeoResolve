# 2025-09-30 Dev Log — Django 스택 스캐폴딩 및 Compose 구성

## 개요
GeoResolve 초기 셋업을 완료했습니다. Django+DRF 기반 서버, Next.js 클라이언트, 권위 데이터(Authority) 모델/로더, JWT 인증, API 문서, Docker Compose 개발 환경까지 일괄 구성했습니다.

## 주요 변경
- 문서
  - `AGENTS.md`: 기여 가이드
  - `docs/TECH_STACK.md`: Django 중심 기술스택 정리
- 서버(backend)
  - Django 프로젝트 스캐폴딩(`server/`), 설정 분리(`base/dev/prod`), Celery 설정
  - DRF 전환, 기본 권한 `IsAuthenticated`(공개 엔드포인트는 `AllowAny`)
  - JWT(`POST /api/token/`, `.../refresh/`), OpenAPI/Swagger(`/api/schema`, `/api/docs`)
  - Resolver API: `GET /api/v1/ping/`, `GET /api/v1/resolve/?q=`
  - Authority 앱: `AuthoritySource/Term/Synonym` 모델, 마이그레이션, Admin 등록
  - 시드 로더: `manage.py load_authority data/ics/2023` (CSV 로딩)
  - Celery Beat 일일 동기화 태스크(`AUTHORITY_SEED_PATH` 경로 사용)
  - 테스트: `pytest` 설정 및 기본 테스트 추가
  - 기타: `server/requirements.txt` 정리(`sentry-sdk` 이름 수정), `.python-version=3.11`
- 클라이언트(frontend)
  - `clients/web/` Next.js(App Router) 스캐폴딩, API 샘플 호출 포함
- 운영
  - `docker-compose.yml`: `db`, `redis`, `api`, `web`, `worker`, `beat`
  - 각 서비스 Dockerfile 추가 및 코드 볼륨 마운트로 핫리로드

## 실행/검증
- Compose: `docker compose up --build`
- 시드 로딩: `docker compose exec api python server/manage.py load_authority data/ics/2023`
- 문서: http://localhost:8000/api/docs/
- 웹: http://localhost:3000

## 다음 제안 작업
- 후보 랭킹 엔드포인트(`/api/v1/resolve/candidates`) 및 트라이그램/Fuzzy 매칭
- 연대 범위/위계 모델링 및 검증 규칙 추가
