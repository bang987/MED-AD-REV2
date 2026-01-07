# MedAdVision 구현 To-Do List

**문서명:** 구현 체크리스트
**버전:** 1.1
**작성일:** 2026년 1월 7일
**참조 문서:** PRD v1.0, 데이터 모델 명세서 v1.0, API 정의서 v1.0, 기술 스택 가이드 v1.0, UI/UX 디자인 시스템 v1.1

---

## 전체 진행 현황

| Phase | 항목 | 상태 | 진행률 |
|-------|------|------|--------|
| 1 | 프로젝트 초기 설정 | **완료** | 100% |
| 2 | 데이터베이스 구축 | 대기 | 0% |
| 3 | 백엔드 기본 구조 | 대기 | 0% |
| 4 | 인증/권한 시스템 | 대기 | 0% |
| 5 | CLOVA OCR 연동 | 대기 | 0% |
| 6 | 이미지 전처리 모듈 | 대기 | 0% |
| 7 | RAG 시스템 구축 | 대기 | 0% |
| 8 | LangGraph 에이전트 | 대기 | 0% |
| 9 | REST API 개발 | 대기 | 0% |
| 10 | WebSocket 실시간 기능 | 대기 | 0% |
| 11 | 프론트엔드 개발 | 대기 | 0% |
| 12 | 테스트 | 대기 | 0% |
| 13 | 배포 및 인프라 | 대기 | 0% |

---

## Phase 1: 프로젝트 초기 설정

### 1.1 백엔드 프로젝트 초기화
- [x] Poetry 프로젝트 생성 (`poetry init`)
- [x] Python 3.11+ 버전 설정
- [x] 기본 의존성 설치
  - [x] fastapi
  - [x] uvicorn[standard]
  - [x] pydantic
  - [x] pydantic-settings
  - [x] sqlalchemy[asyncio]
  - [x] asyncpg
  - [x] redis
  - [x] aioredis
  - [x] python-dotenv
  - [x] python-multipart
  - [x] python-jose[cryptography]
  - [x] passlib[bcrypt]
  - [x] httpx
- [x] AI/ML 의존성 설치
  - [x] langchain
  - [x] langchain-core
  - [x] langchain-anthropic
  - [x] langchain-openai
  - [x] langgraph
  - [x] pinecone-client
  - [x] sentence-transformers
- [x] 이미지 처리 의존성 설치
  - [x] opencv-python-headless
  - [x] pillow
  - [x] aiohttp
  - [x] aiofiles
- [x] 개발 도구 설치
  - [x] pytest
  - [x] pytest-asyncio
  - [x] pytest-cov
  - [x] black
  - [x] ruff
  - [x] mypy
  - [x] pre-commit

### 1.2 디렉토리 구조 생성
```
medadreview-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── review.py
│   │       ├── legal.py
│   │       ├── users.py
│   │       ├── stats.py
│   │       └── notifications.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── middleware.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── review.py
│   │   ├── legal.py
│   │   ├── notification.py
│   │   └── enums.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── request/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── review.py
│   │   │   └── feedback.py
│   │   └── response/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── review.py
│   │       └── common.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── review_service.py
│   │   ├── legal_service.py
│   │   ├── user_service.py
│   │   ├── notification_service.py
│   │   └── stats_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repo.py
│   │   ├── review_repo.py
│   │   └── legal_repo.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── graph.py
│   │   ├── nodes/
│   │   │   ├── __init__.py
│   │   │   ├── preprocess_image.py
│   │   │   ├── extract_ocr.py
│   │   │   ├── postprocess_text.py
│   │   │   ├── claim_extraction.py
│   │   │   ├── violation_classification.py
│   │   │   ├── search_laws.py
│   │   │   ├── search_guidelines.py
│   │   │   ├── search_precedents.py
│   │   │   ├── merge_search_results.py
│   │   │   ├── generate_draft.py
│   │   │   ├── evaluate_draft.py
│   │   │   ├── human_review_decision.py
│   │   │   ├── generate_highlights.py
│   │   │   ├── output_result.py
│   │   │   └── handle_ocr_error.py
│   │   └── prompts/
│   │       ├── __init__.py
│   │       ├── system.py
│   │       ├── claim_extraction.py
│   │       ├── violation_classification.py
│   │       ├── draft_generation.py
│   │       └── evaluation.py
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── clova_client.py
│   │   ├── preprocessor.py
│   │   ├── postprocessor.py
│   │   └── models.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embedder.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── vector_store.py
│   ├── storage/
│   │   ├── __init__.py
│   │   └── s3_client.py
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── seed_data.py
│   ├── index_documents.py
│   └── migrate.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── .env.example
├── pyproject.toml
├── pytest.ini
└── README.md
```
- [x] 위 디렉토리 구조 전체 생성
- [x] 모든 `__init__.py` 파일 생성

### 1.3 설정 파일 구성
- [x] `.env.example` 환경 변수 템플릿 작성
- [x] `app/config/settings.py` Pydantic Settings 구현
- [x] `app/config/logging.py` 로깅 설정 (structlog)
- [x] `pyproject.toml` Poetry 설정 완성
- [x] `.gitignore` 작성
- [x] `pytest.ini` 테스트 설정
- [ ] `pre-commit` 설정 (.pre-commit-config.yaml) *(Phase 2에서 진행)*

### 1.4 프론트엔드 프로젝트 초기화
- [x] Next.js 16 프로젝트 생성 (App Router)
- [x] TypeScript 5.x 설정
- [x] Tailwind CSS 4.x 설정
- [x] 의존성 설치
  - [x] @tanstack/react-query
  - [x] zustand
  - [x] axios
  - [x] zod
  - [x] react-hook-form
  - [x] @hookform/resolvers
  - [x] date-fns
  - [x] lucide-react (아이콘)
  - [x] recharts (차트)
  - [x] react-dropzone
- [x] 디렉토리 구조 생성
  ```
  src/
  ├── app/                    # Next.js App Router
  │   ├── (auth)/            # 인증 관련 라우트
  │   ├── (dashboard)/       # 대시보드 라우트
  │   └── api/               # API Routes (BFF)
  ├── components/
  │   ├── ui/                # 공통 UI 컴포넌트
  │   ├── layout/            # 레이아웃 컴포넌트
  │   ├── review/            # 심의 관련 컴포넌트
  │   └── dashboard/         # 대시보드 컴포넌트
  ├── hooks/                  # 커스텀 훅
  ├── stores/                 # Zustand 스토어
  ├── services/               # API 서비스
  ├── types/                  # TypeScript 타입
  └── lib/                    # 유틸리티
  ```
- [x] ESLint + Prettier 설정
- [x] 경로 별칭 설정 (@/)
- [x] 디자인 시스템 컬러 설정
  - [x] Primary: 에메랄드 (`emerald-500` #10B981)
  - [x] 배경: 밝은 회색 (`gray-50` #F9FAFB)

---

## Phase 2: 데이터베이스 구축

### 2.1 PostgreSQL 설정
- [ ] Docker로 PostgreSQL 16 컨테이너 구성
- [ ] 개발용 데이터베이스 생성 (medadreview_dev)
- [ ] 테스트용 데이터베이스 생성 (medadreview_test)
- [ ] 비동기 연결 풀 설정 (asyncpg)
- [ ] 한글 검색용 pg_trgm 확장 활성화

### 2.2 SQLAlchemy 모델 정의
- [ ] `app/models/base.py` - Base 클래스, 공통 Mixin
- [ ] `app/models/enums.py` - 열거형 정의
  - [ ] ReviewStatus
  - [ ] VerdictType
  - [ ] ViolationCode
  - [ ] Platform
  - [ ] UserRole
  - [ ] Priority
  - [ ] Severity
- [ ] `app/models/organization.py` - 의료기관/광고주 모델
- [ ] `app/models/user.py` - 사용자 모델
- [ ] `app/models/review.py` - 심의 관련 모델
  - [ ] ReviewRequest
  - [ ] ReviewResult
  - [ ] Violation
  - [ ] ReviewLog
- [ ] `app/models/legal.py` - 법령 관련 모델
  - [ ] LegalDocument
  - [ ] BannedExpression
- [ ] `app/models/notification.py` - 알림 모델

### 2.3 Alembic 마이그레이션 설정
- [ ] Alembic 초기화 (`alembic init alembic`)
- [ ] `alembic/env.py` 비동기 설정 수정
- [ ] 초기 마이그레이션 생성 (`alembic revision --autogenerate`)
- [ ] 마이그레이션 적용 (`alembic upgrade head`)
- [ ] 롤백 테스트 (`alembic downgrade -1`)

### 2.4 데이터베이스 제약조건 및 인덱스
- [ ] 외래 키 제약조건 확인
- [ ] 유니크 제약조건 설정
- [ ] 비즈니스 규칙 CHECK 제약조건
- [ ] 인덱스 생성
  - [ ] 상태별 조회 인덱스
  - [ ] 날짜별 조회 인덱스
  - [ ] 복합 인덱스 (status + priority + created_at)
  - [ ] 전문 검색 인덱스 (GIN)

### 2.5 Redis 설정
- [ ] Docker로 Redis 7 컨테이너 구성
- [ ] aioredis 연결 클라이언트 구현
- [ ] 캐시 키 네이밍 규칙 정의
- [ ] TTL 정책 구현
  - [ ] 세션: 8시간
  - [ ] 심의 상태: 24시간
  - [ ] 검색 캐시: 30분
  - [ ] 통계 캐시: 5분

### 2.6 초기 데이터 시드
- [ ] `scripts/seed_data.py` 작성
- [ ] 기본 관리자 계정 생성
- [ ] 금지 표현 목록 데이터 삽입 (100+ 항목)
- [ ] 의료법 제56조 관련 조문 삽입
- [ ] 심의 가이드라인 기초 데이터 삽입

---

## Phase 3: 백엔드 기본 구조

### 3.1 FastAPI 앱 설정
- [ ] `app/main.py` 앱 진입점 구현
  - [ ] FastAPI 인스턴스 생성
  - [ ] lifespan 이벤트 핸들러 (startup/shutdown)
  - [ ] 미들웨어 등록
  - [ ] 예외 핸들러 등록
  - [ ] 라우터 통합
- [ ] CORS 미들웨어 설정
- [ ] GZip 미들웨어 설정
- [ ] 요청 ID 미들웨어
- [ ] `/health` 헬스체크 엔드포인트
- [ ] `/docs` OpenAPI 문서 설정

### 3.2 의존성 주입 시스템
- [ ] `app/api/deps.py` 의존성 모듈
  - [ ] `get_db()` - 데이터베이스 세션
  - [ ] `get_redis()` - Redis 클라이언트
  - [ ] `get_current_user()` - 현재 인증 사용자
  - [ ] `get_current_active_user()` - 활성 사용자
  - [ ] `require_roles()` - 역할 기반 권한 체크
  - [ ] `get_pagination()` - 페이지네이션 파라미터

### 3.3 커스텀 예외 시스템
- [ ] `app/core/exceptions.py`
  - [ ] MedAdReviewException (기본 예외)
  - [ ] ValidationError (검증 실패)
  - [ ] NotFoundError (리소스 없음)
  - [ ] DuplicateError (중복)
  - [ ] ProcessingError (처리 실패)
  - [ ] AuthenticationError (인증 실패)
  - [ ] AuthorizationError (권한 없음)
  - [ ] RateLimitError (요청 제한 초과)
  - [ ] ExternalServiceError (외부 서비스 오류)
- [ ] 예외 핸들러 등록 (JSON 응답 변환)

### 3.4 미들웨어 구현
- [ ] `app/core/middleware.py`
  - [ ] RequestLoggingMiddleware (요청/응답 로깅)
  - [ ] ProcessTimeMiddleware (처리 시간 측정)
  - [ ] RequestIDMiddleware (요청 ID 추적)

### 3.5 공통 유틸리티
- [ ] `app/utils/helpers.py`
  - [ ] generate_uuid()
  - [ ] hash_content() - SHA-256 해싱
  - [ ] format_datetime()
  - [ ] parse_json_response()
- [ ] `app/utils/validators.py`
  - [ ] validate_image_format()
  - [ ] validate_file_size()
  - [ ] sanitize_filename()

### 3.6 Repository 패턴 구현
- [ ] `app/repositories/base.py` - BaseRepository 추상 클래스
- [ ] `app/repositories/user_repo.py` - UserRepository
- [ ] `app/repositories/review_repo.py` - ReviewRepository
- [ ] `app/repositories/legal_repo.py` - LegalRepository

---

## Phase 4: 인증/권한 시스템

### 4.1 보안 모듈 구현
- [ ] `app/core/security.py`
  - [ ] 비밀번호 해싱 (bcrypt)
  - [ ] 비밀번호 검증
  - [ ] JWT 액세스 토큰 생성
  - [ ] JWT 리프레시 토큰 생성
  - [ ] JWT 토큰 검증 및 디코딩
  - [ ] 토큰 블랙리스트 (Redis)

### 4.2 인증 스키마
- [ ] `app/schemas/request/auth.py`
  - [ ] LoginRequest
  - [ ] RefreshTokenRequest
  - [ ] PasswordChangeRequest
- [ ] `app/schemas/response/auth.py`
  - [ ] TokenResponse
  - [ ] UserResponse

### 4.3 인증 API 엔드포인트
- [ ] `app/api/v1/auth.py`
  - [ ] `POST /api/v1/auth/login` - 로그인
  - [ ] `POST /api/v1/auth/logout` - 로그아웃
  - [ ] `POST /api/v1/auth/refresh` - 토큰 갱신
  - [ ] `GET /api/v1/auth/me` - 현재 사용자 정보
  - [ ] `PUT /api/v1/auth/password` - 비밀번호 변경

### 4.4 역할 기반 접근 제어 (RBAC)
- [ ] 역할 정의
  - [ ] super_admin: 전체 시스템 관리
  - [ ] reviewer_lead: 심의위원장
  - [ ] reviewer: 심의위원
  - [ ] submitter: 광고 제출자
  - [ ] viewer: 조회 전용
- [ ] 역할별 권한 매트릭스 정의
- [ ] `require_roles()` 데코레이터 구현
- [ ] 엔드포인트별 권한 적용

### 4.5 사용자 관리 API
- [ ] `app/api/v1/users.py`
  - [ ] `GET /api/v1/users` - 사용자 목록 (admin)
  - [ ] `POST /api/v1/users` - 사용자 생성 (admin)
  - [ ] `GET /api/v1/users/{user_id}` - 사용자 상세
  - [ ] `PUT /api/v1/users/{user_id}` - 사용자 수정
  - [ ] `DELETE /api/v1/users/{user_id}` - 사용자 비활성화

---

## Phase 5: CLOVA OCR 연동

### 5.1 OCR 데이터 모델
- [ ] `app/ocr/models.py`
  - [ ] OCRTextField (텍스트 필드 정보)
    - [ ] text: str
    - [ ] confidence: float
    - [ ] bounding_box: List[Dict]
    - [ ] line_break: bool
    - [ ] field_type: str
  - [ ] OCRResult (OCR 결과)
    - [ ] success: bool
    - [ ] image_id: str
    - [ ] full_text: str
    - [ ] fields: List[OCRTextField]
    - [ ] avg_confidence: float
    - [ ] processing_time_ms: int
    - [ ] error_message: Optional[str]

### 5.2 CLOVA OCR 클라이언트
- [ ] `app/ocr/clova_client.py`
  - [ ] NaverClovaOCR 클래스
    - [ ] `__init__()` - API URL, Secret Key 설정
    - [ ] `async extract_text()` - 이미지에서 텍스트 추출
    - [ ] `_load_image()` - 이미지 로드 및 Base64 인코딩
    - [ ] `_build_request_payload()` - API 요청 페이로드 구성
    - [ ] `_parse_response()` - API 응답 파싱
    - [ ] `_handle_error()` - 에러 처리
    - [ ] `get_violation_highlights()` - 위반 문구 좌표 반환
  - [ ] 재시도 로직 (최대 3회)
  - [ ] 타임아웃 설정 (30초)
  - [ ] 비동기 HTTP 클라이언트 (aiohttp)

### 5.3 OCR 결과 후처리
- [ ] `app/ocr/postprocessor.py`
  - [ ] OCRPostprocessor 클래스
    - [ ] `normalize_text()` - 텍스트 정규화
      - [ ] 연속 공백 제거
      - [ ] 특수문자 정리
      - [ ] OCR 오인식 패턴 수정
    - [ ] `analyze_layout()` - 레이아웃 분석
      - [ ] Y 좌표 기반 영역 분류
      - [ ] 제목/본문/주석 구분
    - [ ] `filter_low_confidence()` - 저신뢰도 필터링
    - [ ] `merge_fields()` - 인접 필드 병합

### 5.4 테스트
- [ ] `tests/unit/test_clova_client.py`
  - [ ] Mock 응답 테스트
  - [ ] 에러 핸들링 테스트
  - [ ] 타임아웃 테스트
- [ ] `tests/integration/test_ocr_integration.py`
  - [ ] 실제 API 연동 테스트 (샘플 이미지)
  - [ ] 다양한 이미지 포맷 테스트

---

## Phase 6: 이미지 전처리 모듈

### 6.1 이미지 전처리 파이프라인
- [ ] `app/ocr/preprocessor.py`
  - [ ] ImagePreprocessor 클래스
    - [ ] `async preprocess()` - 전처리 파이프라인 실행
    - [ ] `_load_image()` - 이미지 로드
    - [ ] `_resize_image()` - 해상도 조정 (최대 2048px)
    - [ ] `_denoise()` - 노이즈 제거 (fastNlMeansDenoisingColored)
    - [ ] `_deskew()` - 기울기 보정 (Hough Transform)
    - [ ] `_enhance_contrast()` - 대비 향상 (CLAHE)
    - [ ] `_to_bytes()` - 바이트 변환

### 6.2 이미지 유효성 검사
- [ ] `app/utils/validators.py` 확장
  - [ ] `validate_image_format()` - 포맷 검증
    - [ ] 지원: jpg, jpeg, png, gif, bmp, tiff, webp
  - [ ] `validate_image_size()` - 크기 검증 (최대 10MB)
  - [ ] `validate_image_dimensions()` - 해상도 검증
  - [ ] `check_image_corruption()` - 손상 여부 검사

### 6.3 이미지 저장소 (S3/MinIO)
- [ ] `app/storage/s3_client.py`
  - [ ] S3StorageClient 클래스
    - [ ] `__init__()` - boto3 클라이언트 설정
    - [ ] `async upload_image()` - 이미지 업로드
    - [ ] `async download_image()` - 이미지 다운로드
    - [ ] `generate_presigned_url()` - 서명된 URL 생성
    - [ ] `delete_image()` - 이미지 삭제
  - [ ] 버킷 구조
    - [ ] `originals/` - 원본 이미지
    - [ ] `processed/` - 전처리된 이미지
    - [ ] `highlighted/` - 하이라이트 이미지

### 6.4 테스트
- [ ] `tests/unit/test_preprocessor.py`
  - [ ] 리사이즈 테스트
  - [ ] 노이즈 제거 테스트
  - [ ] 기울기 보정 테스트
- [ ] 다양한 이미지 테스트
  - [ ] 저해상도 이미지
  - [ ] 고해상도 이미지
  - [ ] 기울어진 이미지
  - [ ] 노이즈가 많은 이미지

---

## Phase 7: RAG 시스템 구축

### 7.1 Pinecone 벡터 DB 설정
- [ ] Pinecone 계정 및 인덱스 생성
  - [ ] 인덱스명: medadreview-legal-kb
  - [ ] Dimension: 768 (SBERT)
  - [ ] Metric: cosine
- [ ] 네임스페이스 구조 설정
  - [ ] `laws` - 법률 조항
  - [ ] `guidelines` - 심의 가이드라인
  - [ ] `precedents` - 판례
  - [ ] `expressions` - 금지/허용 표현

### 7.2 벡터 저장소 클라이언트
- [ ] `app/rag/vector_store.py`
  - [ ] PineconeVectorStore 클래스
    - [ ] `__init__()` - Pinecone 클라이언트 초기화
    - [ ] `async upsert()` - 벡터 삽입/업데이트
    - [ ] `async search()` - 벡터 검색
    - [ ] `async delete()` - 벡터 삭제
    - [ ] `_build_metadata()` - 메타데이터 구성

### 7.3 임베딩 모듈
- [ ] `app/rag/embedder.py`
  - [ ] LegalEmbedder 클래스
    - [ ] `__init__()` - 모델 로드 (sentence-transformers)
    - [ ] `embed_query()` - 쿼리 임베딩
    - [ ] `embed_documents()` - 문서 임베딩 (배치)
    - [ ] `_preprocess_text()` - 텍스트 전처리
  - [ ] 모델 선택
    - [ ] 옵션 1: `jhgan/ko-sroberta-multitask`
    - [ ] 옵션 2: OpenAI `text-embedding-3-small`

### 7.4 검색 모듈
- [ ] `app/rag/retriever.py`
  - [ ] HybridRetriever 클래스
    - [ ] `__init__()` - 벡터 DB, BM25 인덱스 설정
    - [ ] `async search()` - 하이브리드 검색
    - [ ] `_dense_search()` - Dense 벡터 검색
    - [ ] `_sparse_search()` - BM25 스파스 검색
    - [ ] `_rrf_fusion()` - RRF 순위 융합
  - [ ] 검색 파라미터
    - [ ] top_k: 10
    - [ ] bm25_weight: 0.4
    - [ ] dense_weight: 0.6

### 7.5 리랭킹 모듈
- [ ] `app/rag/reranker.py`
  - [ ] CrossEncoderReranker 클래스
    - [ ] `__init__()` - Cross-Encoder 모델 로드
    - [ ] `rerank()` - 검색 결과 리랭킹
    - [ ] `_score_pair()` - 쿼리-문서 쌍 점수 계산
  - [ ] 모델: `cross-encoder/ms-marco-MiniLM-L-6-v2`

### 7.6 법령 데이터 인덱싱
- [ ] `scripts/index_documents.py`
  - [ ] 의료법 제56조 조문 인덱싱
  - [ ] 의료법 시행령 관련 조문 인덱싱
  - [ ] 심의 가이드라인 인덱싱
  - [ ] 금지 표현 패턴 인덱싱
  - [ ] 판례 데이터 인덱싱 (가용 시)
- [ ] 인덱싱 검증
  - [ ] 중복 체크
  - [ ] 메타데이터 정확성 검증

### 7.7 테스트
- [ ] `tests/unit/test_embedder.py`
- [ ] `tests/unit/test_retriever.py`
- [ ] `tests/integration/test_rag_pipeline.py`
  - [ ] 검색 정확도 테스트
  - [ ] 응답 시간 테스트

---

## Phase 8: LangGraph 에이전트 개발

### 8.1 상태 정의
- [ ] `app/agent/state.py`
  - [ ] ImageReviewState (TypedDict)
    - [ ] 입력 데이터 필드
      - [ ] review_id, image_id, image_path, image_url, ad_metadata
    - [ ] OCR 처리 결과 필드
      - [ ] ocr_success, ocr_full_text, ocr_fields, ocr_confidence, ocr_processing_time
    - [ ] 분석 중간 산출물 필드
      - [ ] extracted_claims, claim_categories
      - [ ] relevant_laws, relevant_guidelines, relevant_precedents
    - [ ] 심의 결과 필드
      - [ ] draft_verdict, draft_reasoning, critique_feedback
      - [ ] final_verdict, violation_details, violation_highlights
      - [ ] final_reasoning, modification_suggestions, confidence_score
    - [ ] 워크플로우 제어 필드
      - [ ] iteration_count, max_iterations
      - [ ] requires_human_review, human_feedback
    - [ ] 감사 로그 필드
      - [ ] processing_log, created_at, updated_at

### 8.2 프롬프트 템플릿
- [ ] `app/agent/prompts/system.py`
  - [ ] 시스템 역할 정의
  - [ ] 핵심 원칙 명시
  - [ ] 출력 형식 지정
- [ ] `app/agent/prompts/claim_extraction.py`
  - [ ] 청구항 추출 프롬프트
  - [ ] 추출 기준 정의
  - [ ] Few-shot 예시 포함
- [ ] `app/agent/prompts/violation_classification.py`
  - [ ] 위반 유형 분류 프롬프트
  - [ ] V1~V6 분류 기준
- [ ] `app/agent/prompts/draft_generation.py`
  - [ ] CoT (Chain of Thought) 프롬프트
  - [ ] 단계별 추론 유도
- [ ] `app/agent/prompts/evaluation.py`
  - [ ] 적대적 검증 프롬프트
  - [ ] 검증 체크리스트

### 8.3 노드 구현
- [ ] `app/agent/nodes/preprocess_image.py`
  - [ ] 이미지 전처리 노드
  - [ ] 전처리 로그 기록
- [ ] `app/agent/nodes/extract_ocr.py`
  - [ ] CLOVA OCR 호출 노드
  - [ ] 결과 상태 저장
- [ ] `app/agent/nodes/postprocess_text.py`
  - [ ] 텍스트 후처리 노드
  - [ ] 레이아웃 분석
- [ ] `app/agent/nodes/claim_extraction.py`
  - [ ] 청구항 추출 노드
  - [ ] LLM 호출 및 파싱
- [ ] `app/agent/nodes/violation_classification.py`
  - [ ] 위반 유형 분류 노드
  - [ ] 카테고리별 분류
- [ ] `app/agent/nodes/search_laws.py`
  - [ ] 법령 검색 노드 (RAG)
- [ ] `app/agent/nodes/search_guidelines.py`
  - [ ] 가이드라인 검색 노드 (RAG)
- [ ] `app/agent/nodes/search_precedents.py`
  - [ ] 판례 검색 노드 (RAG)
- [ ] `app/agent/nodes/merge_search_results.py`
  - [ ] 검색 결과 병합 노드 (Fan-in)
- [ ] `app/agent/nodes/generate_draft.py`
  - [ ] 초안 생성 노드 (Generator)
  - [ ] CoT 추론 적용
- [ ] `app/agent/nodes/evaluate_draft.py`
  - [ ] 적대적 검증 노드 (Evaluator)
  - [ ] 검증 점수 계산
- [ ] `app/agent/nodes/human_review_decision.py`
  - [ ] HITL 결정 노드
  - [ ] 확신도 기반 판단
- [ ] `app/agent/nodes/generate_highlights.py`
  - [ ] 위반 문구 하이라이트 좌표 생성
  - [ ] 바운딩 박스 매칭
- [ ] `app/agent/nodes/output_result.py`
  - [ ] 최종 결과 정리 노드
- [ ] `app/agent/nodes/handle_ocr_error.py`
  - [ ] OCR 실패 처리 노드
  - [ ] 보류 판정 생성

### 8.4 그래프 구성
- [ ] `app/agent/graph.py`
  - [ ] StateGraph 초기화
  - [ ] 노드 등록 (add_node)
  - [ ] 진입점 설정 (set_entry_point)
  - [ ] 순차 엣지 정의 (add_edge)
  - [ ] 조건부 엣지 정의 (add_conditional_edges)
    - [ ] OCR 성공/실패 분기
    - [ ] 평가 통과/재시도 분기
    - [ ] HITL 필요/자동완료 분기
  - [ ] 체크포인터 설정 (SqliteSaver/MemorySaver)
  - [ ] 인터럽트 포인트 설정 (HITL)
  - [ ] 그래프 컴파일

### 8.5 라우팅 함수
- [ ] `ocr_result_router()` - OCR 성공/실패 판단
- [ ] `evaluation_router()` - 평가 통과/재시도/최대반복 판단
- [ ] `human_review_router()` - HITL 필요 여부 판단

### 8.6 테스트
- [ ] `tests/unit/agent/` - 노드별 단위 테스트
  - [ ] test_claim_extraction.py
  - [ ] test_violation_classification.py
  - [ ] test_generate_draft.py
  - [ ] test_evaluate_draft.py
- [ ] `tests/integration/test_agent_workflow.py`
  - [ ] 전체 워크플로우 테스트
  - [ ] 루프 반복 테스트
  - [ ] HITL 인터럽트 테스트

---

## Phase 9: REST API 개발

### 9.1 Pydantic 스키마 정의
- [ ] `app/schemas/base.py`
  - [ ] BaseResponse
  - [ ] PaginationParams
  - [ ] PaginatedResponse
  - [ ] ErrorResponse
- [ ] `app/schemas/request/review.py`
  - [ ] ReviewImageRequest (multipart)
  - [ ] ReviewBatchRequest
  - [ ] HumanFeedbackRequest
- [ ] `app/schemas/response/review.py`
  - [ ] ReviewCreateResponse
  - [ ] ReviewDetailResponse
  - [ ] ReviewListResponse
  - [ ] ViolationDetail
  - [ ] HighlightInfo

### 9.2 심의 API
- [ ] `app/api/v1/review.py`
  - [ ] `POST /api/v1/review/image` - 이미지 심의 요청
    - [ ] 이미지 파일 수신 (multipart/form-data)
    - [ ] 유효성 검사
    - [ ] 백그라운드 태스크 시작
    - [ ] review_id 즉시 반환
  - [ ] `GET /api/v1/review/{review_id}` - 심의 결과 조회
    - [ ] 상태별 응답 (pending/processing/completed)
    - [ ] 위반 상세 포함
  - [ ] `GET /api/v1/review` - 심의 목록 조회
    - [ ] 필터: status, priority, platform, verdict
    - [ ] 정렬: created_at, priority
    - [ ] 페이지네이션
  - [ ] `POST /api/v1/review/{review_id}/feedback` - 인간 피드백 제출
    - [ ] 액션: approve, reject, modify
    - [ ] 최종 판정 확정
  - [ ] `GET /api/v1/review/{review_id}/highlighted-image` - 하이라이트 이미지
    - [ ] 이미지 파일 반환
    - [ ] 옵션: format, opacity, show_labels
  - [ ] `POST /api/v1/review/batch` - 배치 심의 요청

### 9.3 법령 API
- [ ] `app/api/v1/legal.py`
  - [ ] `GET /api/v1/legal/search` - 법령 검색
    - [ ] 쿼리 파라미터: query, doc_type, limit
    - [ ] 하이브리드 검색 적용
  - [ ] `GET /api/v1/legal/documents/{doc_id}` - 법령 문서 상세
  - [ ] `GET /api/v1/legal/banned-expressions` - 금지 표현 목록
    - [ ] 카테고리별 필터

### 9.4 통계 API
- [ ] `app/api/v1/stats.py`
  - [ ] `GET /api/v1/stats/dashboard` - 대시보드 통계
    - [ ] 실시간 처리 현황
    - [ ] 판정 분포
    - [ ] 성능 지표
  - [ ] `GET /api/v1/stats/daily` - 일별 통계
  - [ ] `GET /api/v1/stats/performance` - AI 성능 지표
    - [ ] 재현율, 정밀도, 할루시네이션 비율

### 9.5 알림 API
- [ ] `app/api/v1/notifications.py`
  - [ ] `GET /api/v1/notifications` - 알림 목록
  - [ ] `PUT /api/v1/notifications/{id}/read` - 읽음 처리
  - [ ] `PUT /api/v1/notifications/read-all` - 전체 읽음

### 9.6 서비스 레이어 구현
- [ ] `app/services/review_service.py`
  - [ ] create_review()
  - [ ] get_review()
  - [ ] get_reviews()
  - [ ] process_review() - 에이전트 실행
  - [ ] submit_feedback()
  - [ ] generate_highlighted_image()
- [ ] `app/services/legal_service.py`
- [ ] `app/services/stats_service.py`
- [ ] `app/services/notification_service.py`

### 9.7 API 테스트
- [ ] `tests/integration/test_review_api.py`
- [ ] `tests/integration/test_legal_api.py`
- [ ] `tests/integration/test_stats_api.py`

---

## Phase 10: WebSocket 실시간 기능

### 10.1 WebSocket 서버 구현
- [ ] `app/api/websocket.py`
  - [ ] WebSocket 엔드포인트 (`/ws/review/{review_id}`)
  - [ ] ConnectionManager 클래스
    - [ ] 연결 관리 (connect, disconnect)
    - [ ] 메시지 브로드캐스트
    - [ ] 개별 메시지 전송
  - [ ] 인증 처리 (쿼리 파라미터 토큰)

### 10.2 실시간 업데이트 메시지
- [ ] 메시지 타입 정의
  - [ ] `progress` - 진행 상황 업데이트
    - [ ] stage: 현재 단계
    - [ ] progress_percent: 진행률
    - [ ] message: 상태 메시지
  - [ ] `completed` - 처리 완료
    - [ ] verdict: 판정 결과
    - [ ] review_id: 심의 ID
  - [ ] `error` - 에러 발생
    - [ ] error_code: 에러 코드
    - [ ] message: 에러 메시지

### 10.3 에이전트-WebSocket 연동
- [ ] 노드 실행 시 진행 상황 발행
- [ ] Redis Pub/Sub 활용
- [ ] 연결 복구 로직

### 10.4 테스트
- [ ] WebSocket 연결 테스트
- [ ] 메시지 수신 테스트
- [ ] 연결 해제 처리 테스트

---

## Phase 11: 프론트엔드 개발

> **기술 스택:** Next.js 16 (App Router) + TypeScript 5.x + Tailwind CSS 4.x
> **디자인 시스템:** Primary 에메랄드(#10B981), 배경 밝은 회색(#F9FAFB)

### 11.1 공통 UI 컴포넌트
- [ ] `components/ui/Button.tsx`
  - [ ] variants: primary(emerald), secondary, danger, ghost, outline
  - [ ] Primary 스타일: `bg-emerald-500 hover:bg-emerald-600 text-white`
  - [ ] sizes: sm, md, lg
  - [ ] loading 상태
- [ ] `components/ui/Badge.tsx`
  - [ ] 판정 배지 (허용/조건부허용/불허/보류)
    - [ ] 허용: `bg-green-100 text-green-700`
    - [ ] 조건부허용: `bg-amber-100 text-amber-700`
    - [ ] 불허: `bg-red-100 text-red-700`
    - [ ] 보류: `bg-gray-100 text-gray-600`
  - [ ] 심각도 배지 (critical/high/medium/low)
  - [ ] 상태 배지 (pending/processing/completed)
- [ ] `components/ui/Card.tsx` - 흰색 배경 (`bg-white`)
- [ ] `components/ui/Table.tsx`
  - [ ] 정렬 기능
  - [ ] 선택 기능
- [ ] `components/ui/Modal.tsx`
- [ ] `components/ui/Input.tsx`
  - [ ] 포커스 스타일: `focus:ring-emerald-500`
- [ ] `components/ui/Select.tsx`
- [ ] `components/ui/Textarea.tsx`
- [ ] `components/ui/Pagination.tsx`
- [ ] `components/ui/Loading.tsx` (Spinner, Skeleton)
- [ ] `components/ui/Toast.tsx` (알림)
- [ ] `components/ui/Tabs.tsx`
- [ ] `components/ui/Progress.tsx`

### 11.2 레이아웃 컴포넌트
- [ ] `components/layout/Header.tsx`
  - [ ] 로고
  - [ ] 검색바
  - [ ] 알림 아이콘
  - [ ] 사용자 메뉴
- [ ] `components/layout/Sidebar.tsx`
  - [ ] 네비게이션 메뉴
  - [ ] 긴급 항목 배지
  - [ ] 접힘/펼침 기능
  - [ ] 배경: `bg-gray-100`
- [ ] `components/layout/Footer.tsx`
- [ ] `components/layout/DashboardLayout.tsx`
  - [ ] Header + Sidebar + Main 조합
  - [ ] 페이지 배경: `bg-gray-50`

### 11.3 심의 관련 컴포넌트
- [ ] `components/review/ReviewCard.tsx`
  - [ ] 심의 요약 카드
  - [ ] 판정 배지
  - [ ] 확신도 표시
- [ ] `components/review/ReviewList.tsx`
  - [ ] 카드/테이블 뷰 전환
  - [ ] 필터 컨트롤
- [ ] `components/review/ReviewDetail.tsx`
  - [ ] 광고 원문 표시
  - [ ] AI 판정 결과
  - [ ] 위반 사항 목록
- [ ] `components/review/ViolationCard.tsx`
  - [ ] 위반 문구
  - [ ] 위반 조항
  - [ ] 심각도 배지
  - [ ] 수정 제안
- [ ] `components/review/FeedbackForm.tsx`
  - [ ] 액션 선택 (승인/기각/수정)
  - [ ] 피드백 입력
  - [ ] 제출 버튼
- [ ] `components/review/ImageViewer.tsx`
  - [ ] 원본/하이라이트 토글
  - [ ] 줌 인/아웃
  - [ ] 위반 영역 인터랙션
- [ ] `components/review/ImageUploader.tsx`
  - [ ] 드래그 앤 드롭
  - [ ] 파일 선택
  - [ ] 미리보기
  - [ ] 업로드 진행률
- [ ] `components/review/ProgressTracker.tsx`
  - [ ] 단계별 진행 표시
  - [ ] 현재 단계 하이라이트

### 11.4 대시보드 컴포넌트
- [ ] `components/dashboard/StatsCard.tsx`
  - [ ] 숫자 강조
  - [ ] 증감 표시
  - [ ] 아이콘
- [ ] `components/dashboard/RealtimeIndicator.tsx`
  - [ ] 실시간 처리 현황
  - [ ] 대기 건수
- [ ] `components/dashboard/VerdictDistributionChart.tsx`
  - [ ] 파이 차트
  - [ ] 범례
- [ ] `components/dashboard/TrendChart.tsx`
  - [ ] 라인 차트
  - [ ] 기간 선택
- [ ] `components/dashboard/PendingReviewList.tsx`
  - [ ] 인간 검토 대기 목록
  - [ ] 긴급 표시

### 11.5 페이지 구현
- [ ] `app/(auth)/login/page.tsx` - 로그인
- [ ] `app/(auth)/logout/page.tsx` - 로그아웃 처리
- [ ] `app/(dashboard)/page.tsx` - 대시보드 메인
- [ ] `app/(dashboard)/reviews/page.tsx` - 심의 목록
- [ ] `app/(dashboard)/reviews/new/page.tsx` - 새 심의 요청
- [ ] `app/(dashboard)/reviews/[id]/page.tsx` - 심의 상세
- [ ] `app/(dashboard)/legal/page.tsx` - 법령 검색
- [ ] `app/(dashboard)/legal/[id]/page.tsx` - 법령 상세
- [ ] `app/(dashboard)/users/page.tsx` - 사용자 관리 (admin)
- [ ] `app/(dashboard)/settings/page.tsx` - 설정
- [ ] `app/(dashboard)/notifications/page.tsx` - 알림 목록

### 11.6 상태 관리
- [ ] `stores/authStore.ts` - 인증 상태
  - [ ] user, token, isAuthenticated
  - [ ] login(), logout(), refreshToken()
- [ ] `stores/reviewStore.ts` - 심의 상태
  - [ ] currentReview, reviewList
  - [ ] filters, pagination
- [ ] `stores/uiStore.ts` - UI 상태
  - [ ] sidebarOpen, theme
  - [ ] toast notifications

### 11.7 API 서비스
- [ ] `services/api.ts` - Axios 인스턴스
  - [ ] 인터셉터 (토큰 첨부, 에러 처리)
  - [ ] 기본 URL 설정
- [ ] `services/authService.ts`
- [ ] `services/reviewService.ts`
- [ ] `services/legalService.ts`
- [ ] `services/statsService.ts`

### 11.8 커스텀 훅
- [ ] `hooks/useAuth.ts`
- [ ] `hooks/useReview.ts`
- [ ] `hooks/useReviewList.ts`
- [ ] `hooks/useWebSocket.ts`
- [ ] `hooks/useStats.ts`
- [ ] `hooks/useDebounce.ts`

### 11.9 타입 정의
- [ ] `types/review.ts`
- [ ] `types/user.ts`
- [ ] `types/legal.ts`
- [ ] `types/api.ts`
- [ ] `types/common.ts`

---

## Phase 12: 테스트

### 12.1 백엔드 단위 테스트
- [ ] `tests/unit/test_ocr_client.py`
- [ ] `tests/unit/test_preprocessor.py`
- [ ] `tests/unit/test_postprocessor.py`
- [ ] `tests/unit/test_embedder.py`
- [ ] `tests/unit/test_retriever.py`
- [ ] `tests/unit/test_reranker.py`
- [ ] `tests/unit/agent/test_claim_extraction.py`
- [ ] `tests/unit/agent/test_violation_classification.py`
- [ ] `tests/unit/agent/test_generate_draft.py`
- [ ] `tests/unit/agent/test_evaluate_draft.py`
- [ ] `tests/unit/agent/test_highlights.py`
- [ ] `tests/unit/test_security.py`
- [ ] `tests/unit/test_validators.py`

### 12.2 백엔드 통합 테스트
- [ ] `tests/integration/test_ocr_integration.py`
- [ ] `tests/integration/test_rag_pipeline.py`
- [ ] `tests/integration/test_agent_workflow.py`
- [ ] `tests/integration/test_review_api.py`
- [ ] `tests/integration/test_auth_api.py`
- [ ] `tests/integration/test_legal_api.py`
- [ ] `tests/integration/test_websocket.py`

### 12.3 E2E 테스트
- [ ] `tests/e2e/test_full_review_flow.py`
  - [ ] 이미지 업로드 → OCR → 판정 → 결과 조회
- [ ] `tests/e2e/test_hitl_flow.py`
  - [ ] 인간 검토 필요 케이스 → 피드백 제출 → 최종 확정
- [ ] `tests/e2e/test_batch_review.py`
- [ ] `tests/e2e/test_error_recovery.py`

### 12.4 프론트엔드 테스트
- [ ] Jest 설정
- [ ] 컴포넌트 단위 테스트
  - [ ] Button, Badge, Card 등
- [ ] 페이지 통합 테스트
- [ ] Cypress E2E 테스트
  - [ ] 로그인 플로우
  - [ ] 심의 요청 플로우
  - [ ] 결과 조회 플로우

### 12.5 성능 테스트
- [ ] Locust 부하 테스트 설정
- [ ] API 응답 시간 측정
- [ ] OCR 처리 시간 측정
- [ ] RAG 검색 응답 시간 측정
- [ ] 전체 파이프라인 처리 시간 측정
- [ ] 동시 요청 처리 테스트

### 12.6 테스트 커버리지
- [ ] 백엔드 커버리지 목표: 80%
- [ ] 프론트엔드 커버리지 목표: 70%
- [ ] 커버리지 리포트 생성

---

## Phase 13: 배포 및 인프라

### 13.1 Docker 설정
- [ ] `docker/Dockerfile` (백엔드 프로덕션)
- [ ] `docker/Dockerfile.dev` (백엔드 개발)
- [ ] `docker/Dockerfile.frontend` (프론트엔드)
- [ ] `docker-compose.yml` (로컬 개발)
  - [ ] PostgreSQL
  - [ ] Redis
  - [ ] Backend
  - [ ] Frontend
  - [ ] MinIO (S3 호환)
- [ ] `docker-compose.prod.yml` (프로덕션)
- [ ] `.dockerignore` 작성

### 13.2 Kubernetes 설정
- [ ] `k8s/namespace.yaml`
- [ ] `k8s/configmap.yaml`
- [ ] `k8s/secret.yaml`
- [ ] `k8s/deployment-api.yaml`
- [ ] `k8s/deployment-worker.yaml` (Celery worker)
- [ ] `k8s/deployment-frontend.yaml`
- [ ] `k8s/service-api.yaml`
- [ ] `k8s/service-frontend.yaml`
- [ ] `k8s/ingress.yaml`
- [ ] `k8s/hpa.yaml` (Horizontal Pod Autoscaler)
- [ ] `k8s/pdb.yaml` (Pod Disruption Budget)

### 13.3 CI/CD 파이프라인
- [ ] `.github/workflows/ci.yml`
  - [ ] 코드 린팅 (black, ruff)
  - [ ] 타입 체크 (mypy)
  - [ ] 단위 테스트
  - [ ] 통합 테스트
  - [ ] 커버리지 리포트
- [ ] `.github/workflows/cd.yml`
  - [ ] Docker 이미지 빌드
  - [ ] 이미지 푸시 (ECR/GCR)
  - [ ] 스테이징 배포
  - [ ] 프로덕션 배포 (수동 승인)
- [ ] ArgoCD 설정 (GitOps)

### 13.4 모니터링 및 로깅
- [ ] Prometheus 메트릭 설정
  - [ ] API 요청 수/응답 시간
  - [ ] 에러율
  - [ ] 활성 연결 수
- [ ] Grafana 대시보드 구성
  - [ ] 시스템 개요 대시보드
  - [ ] API 성능 대시보드
  - [ ] 에이전트 성능 대시보드
- [ ] 알림 규칙 설정 (Alertmanager)
- [ ] Sentry 에러 트래킹 연동
- [ ] 로그 수집 (Loki/ELK)

### 13.5 보안
- [ ] API 키/시크릿 관리 (AWS Secrets Manager)
- [ ] 네트워크 정책 설정
- [ ] SSL/TLS 인증서 (Let's Encrypt/ACM)
- [ ] 보안 스캔 (Trivy)
- [ ] OWASP 취약점 점검
- [ ] Rate Limiting 설정

### 13.6 백업 및 복구
- [ ] PostgreSQL 자동 백업 설정
- [ ] Redis 스냅샷 설정
- [ ] S3 버전 관리 활성화
- [ ] 재해 복구 계획 문서화

### 13.7 문서화
- [ ] README.md 완성
- [ ] API 문서 (OpenAPI/Swagger)
- [ ] 아키텍처 문서
- [ ] 운영 가이드
- [ ] 트러블슈팅 가이드

---

## 완료 기준 (Definition of Done)

### 각 Phase 완료 시 확인 사항
- [ ] 모든 체크리스트 항목 완료
- [ ] 관련 단위 테스트 통과
- [ ] 코드 리뷰 완료
- [ ] 문서 업데이트
- [ ] 스테이징 환경 배포 및 검증

### 전체 프로젝트 완료 기준
- [ ] 모든 Phase 완료
- [ ] 테스트 커버리지 목표 달성
- [ ] 성능 목표 달성
  - [ ] 건당 처리시간 5분 이내
  - [ ] API 응답시간 200ms 이내
- [ ] 정확도 목표 달성
  - [ ] 법적 재현율 95% 이상
  - [ ] 정밀도 90% 이상
- [ ] 프로덕션 배포 완료
- [ ] 운영 문서 완성

---

## 부록: 의존성 관계도

```
Phase 1 (초기 설정)
    │
    ▼
Phase 2 (데이터베이스) ──────────────────────────┐
    │                                            │
    ▼                                            │
Phase 3 (백엔드 기본) ◄──────────────────────────┤
    │                                            │
    ├────────────┐                               │
    ▼            ▼                               │
Phase 4      Phase 5 (OCR) ◄─── Phase 6 (전처리)│
(인증)           │                               │
    │            │                               │
    │            ▼                               │
    │       Phase 7 (RAG) ◄──────────────────────┘
    │            │
    │            ▼
    └──────► Phase 8 (에이전트)
                 │
                 ▼
            Phase 9 (REST API)
                 │
                 ├────────────┐
                 ▼            ▼
            Phase 10      Phase 11
            (WebSocket)   (프론트엔드)
                 │            │
                 └─────┬──────┘
                       ▼
                  Phase 12 (테스트)
                       │
                       ▼
                  Phase 13 (배포)
```

---

**문서 끝**
