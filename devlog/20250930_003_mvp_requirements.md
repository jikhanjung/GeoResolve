# 2025-09-30 Dev Log — MVP 요구사항 정리

## 목적/범위
- 지질 용어 표준화·검증의 최소가치 제공: 검색(후보 제안) + 검증(경고 리포트) + 기본 운영.
- 온프렘/클라우드 공통 배포 가능(Compose 기준), DB는 PostgreSQL 사용.

## 기능 요구사항(FR)
- Resolve
  - `GET /api/v1/resolve/?q=...` 단건 해석(기본 결과)
  - `GET /api/v1/resolve/candidates?q=&type=&limit=` 후보 N개 점수순 반환(트라이그램/부분일치 포함)
- Validate
  - `POST /api/v1/validate` 문서/리스트 입력 → 경고/제안 리포트(JSON)
  - 규칙: 연대-용어 불일치, 위계(Group/Formation/Member) 위반, 금칙/권장
- 데이터 관리
  - Authority 모델(CRUD, Admin UI), 시드 로더(`load_authority`), Celery Beat 일일 동기화
- 인증/권한
  - JWT 로그인(`/api/token`), 기본 보호(비공개 API), 공개 엔드포인트는 `AllowAny`
- 문서화
  - OpenAPI 100% 스키마, Swagger UI(`/api/docs`), 예제 포함

## 데이터 요구사항
- 모델: `AuthoritySource`, `Term(type, lang, meta, age_range)`, `Synonym`
- 위계/연대: Group/Formation/Member, Period/Epoch/Age, 최소 연대범위 필드(ka/Ma)
- 인덱스: Postgres GIN + `pg_trgm`(name/synonym), 대소문자/악센트 정규화 전략
- 샘플: ICS 소규모 세트 제공, `data/*/metadata.json`(버전/출처/라이선스/체크섬)

## 비기능 요구사항(NFR)
- 성능: 후보 API p95 < 200ms(단일 노드, 50k 용어 기준, 캐시 미사용)
- 정확도: 샘플 셋 기준 Top-1 ≥ 85%, Top-3 ≥ 95%(휴리스틱)
- 가용성: dev 환경 단일 인스턴스, 헬스체크 `/healthz`
- 보안: 레이트리밋(익명 resolve), CORS 최소 허용, 비밀정보는 `.env`
- 로깅/관측: 구조화 로그(레벨/요청ID), 에러 수집(Sentry)

## API 계약
- 버전 경로: `/api/v1/*` 고정, 파괴적 변경 시 `v2`
- 스키마: drf-spectacular 생성 → CI에서 스냅샷 검증, SDK 생성(선택)

## 배포/운영
- Docker Compose: `db`, `redis`, `api(gunicorn)`, `worker`, `beat`, `web`
- 마이그레이션/시드: 부트시 자동 또는 명령 실행 가이드 제공
- 환경변수: `DATABASE_URL`, `CELERY_*`, `AUTHORITY_SEED_PATH`, `DJANGO_*`

## 테스트/수용 기준
- 테스트: 유닛/통합(로더/해석/검증), 커버리지 ≥ 80%
- 수동 UAT 체크리스트: 해석/후보/검증/관리자/문서 페이지 동작
- 완료 정의: OpenAPI 최신, 시드 로딩 성공, 후보 랭킹 품질 기준 충족

## 범위 외(이번 MVP)
- 실시간 WebSocket 제안, 대규모 임베딩 검색, 플러그인 상점 배포(Word/QGIS) 전체 기능
