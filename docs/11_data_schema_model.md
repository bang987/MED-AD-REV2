# 데이터 모델 명세서 (Data Schema & Model)

**문서명:** MedAdReview 데이터 모델 명세서  
**버전:** 1.0  
**작성일:** 2026년 1월 7일  
**참조 문서:** PRD v1.0  

---

## 1. 개요

### 1.1 문서 목적

본 문서는 MedAdReview AI Agent 시스템의 전체 데이터 모델을 정의합니다. 관계형 데이터베이스(PostgreSQL), 벡터 데이터베이스(Pinecone), 캐시 저장소(Redis), 그리고 애플리케이션 레벨의 데이터 구조를 포함합니다.

### 1.2 데이터 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────────┐
│                        데이터 레이어 아키텍처                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ PostgreSQL  │  │  Pinecone   │  │    Redis    │  │    S3     │ │
│  │   (RDBMS)   │  │ (VectorDB)  │  │   (Cache)   │  │  (Files)  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                │                │       │
│         └────────────────┴────────────────┴────────────────┘       │
│                                 │                                   │
│                         ┌──────▼──────┐                            │
│                         │   ORM/DAL   │                            │
│                         │ (SQLAlchemy)│                            │
│                         └──────┬──────┘                            │
│                                │                                    │
│                         ┌──────▼──────┐                            │
│                         │ Application │                            │
│                         │   Layer     │                            │
│                         └─────────────┘                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. PostgreSQL 스키마

### 2.1 ERD (Entity Relationship Diagram)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  organizations  │       │     users       │       │   review_       │
│─────────────────│       │─────────────────│       │   requests      │
│ id (PK)         │◄──┐   │ id (PK)         │◄──┐   │─────────────────│
│ name            │   │   │ org_id (FK)     │   │   │ id (PK)         │
│ type            │   │   │ email           │   │   │ ad_id (UK)      │
│ license_number  │   │   │ name            │   │   │ org_id (FK)     │
│ created_at      │   │   │ role            │   │   │ submitted_by(FK)│
└─────────────────┘   │   │ created_at      │   │   │ ad_content      │
                      │   └─────────────────┘   │   │ platform        │
                      │                         │   │ status          │
                      └─────────────────────────┼───│ priority        │
                                                │   │ created_at      │
                                                │   └────────┬────────┘
                                                │            │
                                                │            │ 1:1
                                                │            ▼
┌─────────────────┐       ┌─────────────────┐   │   ┌─────────────────┐
│ legal_documents │       │  review_logs    │   │   │ review_results  │
│─────────────────│       │─────────────────│   │   │─────────────────│
│ id (PK)         │       │ id (PK)         │   │   │ id (PK)         │
│ doc_type        │       │ request_id (FK) │───┼──►│ request_id (FK) │
│ title           │       │ stage           │   │   │ verdict         │
│ content         │       │ input_data      │   │   │ confidence      │
│ article         │       │ output_data     │   │   │ violations      │
│ effective_date  │       │ llm_model       │   │   │ reasoning       │
│ is_active       │       │ tokens_used     │   │   │ suggestions     │
│ embedding_id    │       │ latency_ms      │   │   │ human_reviewed  │
└─────────────────┘       │ created_at      │   │   │ reviewed_by(FK) │
                          └─────────────────┘   │   │ finalized_at    │
                                                │   └─────────────────┘
                          ┌─────────────────┐   │
                          │ banned_         │   │   ┌─────────────────┐
                          │ expressions     │   │   │   violations    │
                          │─────────────────│   │   │─────────────────│
                          │ id (PK)         │   │   │ id (PK)         │
                          │ expression      │   │   │ result_id (FK)  │
                          │ category        │   └──►│ claim           │
                          │ verdict         │       │ article         │
                          │ exception       │       │ reason          │
                          │ reference       │       │ guideline_ref   │
                          │ is_active       │       │ severity        │
                          └─────────────────┘       └─────────────────┘
```

### 2.2 테이블 상세 정의

#### 2.2.1 organizations (의료기관/광고주)

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 기본 정보
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('hospital', 'clinic', 'pharmacy', 'agency')),
    license_number VARCHAR(50) UNIQUE,
    business_registration_number VARCHAR(20),
    
    -- 연락처
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    
    -- 상태
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'inactive')),
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    
    -- 인덱스용 검색 컬럼
    search_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('korean', coalesce(name, '') || ' ' || coalesce(address, ''))
    ) STORED
);

-- 인덱스
CREATE INDEX idx_organizations_type ON organizations(type);
CREATE INDEX idx_organizations_status ON organizations(status);
CREATE INDEX idx_organizations_search ON organizations USING GIN(search_vector);
```

#### 2.2.2 users (사용자)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 소속
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    
    -- 인증 정보
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- 프로필
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    
    -- 권한
    role VARCHAR(30) NOT NULL CHECK (role IN (
        'super_admin',      -- 시스템 관리자
        'reviewer',         -- 심의위원
        'reviewer_lead',    -- 심의위원장
        'submitter',        -- 광고 제출자 (의료기관)
        'viewer'            -- 조회 전용
    )),
    permissions JSONB DEFAULT '[]'::JSONB,
    
    -- 상태
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'locked')),
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_users_org ON users(organization_id);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_email ON users(email);
```

#### 2.2.3 review_requests (심의 요청)

```sql
CREATE TABLE review_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 광고 식별
    ad_id VARCHAR(50) UNIQUE NOT NULL,  -- 외부 광고 ID (예: AD-2026-00001)
    
    -- 관계
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    submitted_by UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- 광고 내용
    ad_content TEXT NOT NULL,
    ad_content_hash VARCHAR(64) NOT NULL,  -- SHA-256 해시 (중복 검사용)
    
    -- 광고 메타데이터
    platform VARCHAR(50) NOT NULL CHECK (platform IN (
        'naver_blog', 'instagram', 'youtube', 'facebook',
        'website', 'kakaotalk', 'tiktok', 'other'
    )),
    ad_type VARCHAR(30) DEFAULT 'text' CHECK (ad_type IN ('text', 'image', 'video', 'mixed')),
    ad_url TEXT,
    hospital_name VARCHAR(200),
    target_audience VARCHAR(100),
    
    -- 처리 상태
    status VARCHAR(30) DEFAULT 'pending' CHECK (status IN (
        'pending',           -- 대기 중
        'processing',        -- AI 처리 중
        'ai_completed',      -- AI 심의 완료
        'human_review',      -- 인간 검토 중
        'approved',          -- 최종 승인
        'rejected',          -- 최종 거부
        'revision_requested' -- 수정 요청
    )),
    
    -- 우선순위
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('urgent', 'high', 'normal', 'low')),
    
    -- 처리 정보
    assigned_reviewer_id UUID REFERENCES users(id),
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 제약조건
    CONSTRAINT valid_processing_time CHECK (
        processing_completed_at IS NULL OR 
        processing_completed_at >= processing_started_at
    )
);

-- 인덱스
CREATE INDEX idx_review_requests_org ON review_requests(organization_id);
CREATE INDEX idx_review_requests_status ON review_requests(status);
CREATE INDEX idx_review_requests_priority ON review_requests(priority);
CREATE INDEX idx_review_requests_platform ON review_requests(platform);
CREATE INDEX idx_review_requests_created ON review_requests(created_at DESC);
CREATE INDEX idx_review_requests_hash ON review_requests(ad_content_hash);

-- 복합 인덱스 (대시보드 쿼리 최적화)
CREATE INDEX idx_review_requests_status_priority ON review_requests(status, priority, created_at DESC);
```

#### 2.2.4 review_results (심의 결과)

```sql
CREATE TABLE review_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 관계
    request_id UUID UNIQUE NOT NULL REFERENCES review_requests(id) ON DELETE CASCADE,
    
    -- AI 판정 결과
    verdict VARCHAR(20) NOT NULL CHECK (verdict IN ('허용', '조건부허용', '불허', '보류')),
    confidence_score DECIMAL(4,3) CHECK (confidence_score BETWEEN 0 AND 1),
    
    -- 분석 내용 (JSONB)
    extracted_claims JSONB DEFAULT '[]'::JSONB,
    /*
    예시:
    [
        {"claim": "100% 완치 보장", "category": "V3", "severity": "high"},
        {"claim": "국내 유일", "category": "V6", "severity": "medium"}
    ]
    */
    
    -- 위반 정보 (정규화된 별도 테이블 참조)
    violation_count INT DEFAULT 0,
    
    -- 추론 과정
    reasoning TEXT,
    reasoning_steps JSONB DEFAULT '[]'::JSONB,
    /*
    예시:
    [
        {"step": 1, "action": "claim_extraction", "result": "..."},
        {"step": 2, "action": "law_retrieval", "result": "..."}
    ]
    */
    
    -- 수정 제안
    suggestions JSONB DEFAULT '[]'::JSONB,
    /*
    예시:
    [
        {"original": "100% 완치", "suggested": "치료 효과가 있을 수 있습니다", "reason": "..."}
    ]
    */
    
    -- 참조된 법령
    cited_laws JSONB DEFAULT '[]'::JSONB,
    cited_guidelines JSONB DEFAULT '[]'::JSONB,
    cited_precedents JSONB DEFAULT '[]'::JSONB,
    
    -- 처리 메타데이터
    iteration_count INT DEFAULT 1,
    processing_time_ms INT,
    llm_model VARCHAR(50),
    total_tokens_used INT,
    
    -- 인간 검토
    human_reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by UUID REFERENCES users(id),
    human_verdict VARCHAR(20) CHECK (human_verdict IN ('허용', '조건부허용', '불허', '보류')),
    human_feedback TEXT,
    human_modifications JSONB,
    
    -- 최종 확정
    final_verdict VARCHAR(20) CHECK (final_verdict IN ('허용', '조건부허용', '불허', '보류')),
    finalized_by UUID REFERENCES users(id),
    finalized_at TIMESTAMP WITH TIME ZONE,
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_review_results_verdict ON review_results(verdict);
CREATE INDEX idx_review_results_final_verdict ON review_results(final_verdict);
CREATE INDEX idx_review_results_human_reviewed ON review_results(human_reviewed);
CREATE INDEX idx_review_results_confidence ON review_results(confidence_score);
```

#### 2.2.5 violations (위반 상세)

```sql
CREATE TABLE violations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 관계
    result_id UUID NOT NULL REFERENCES review_results(id) ON DELETE CASCADE,
    
    -- 위반 내용
    claim TEXT NOT NULL,                    -- 위반 문구
    claim_index INT,                        -- 원본 광고에서의 위치
    
    -- 분류
    violation_code VARCHAR(10) NOT NULL,    -- V1, V2, V3, ...
    violation_type VARCHAR(100) NOT NULL,   -- 신의료기술 미평가, 치료 경험담, ...
    
    -- 법적 근거
    article VARCHAR(50) NOT NULL,           -- 제56조 제2항 제1호
    article_content TEXT,                   -- 해당 조항 전문
    guideline_ref VARCHAR(100),             -- 심의기준 제X조
    
    -- 상세 정보
    reason TEXT NOT NULL,                   -- 위반 판단 사유
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    
    -- 수정 제안
    suggested_correction TEXT,
    
    -- 검증 정보
    verification_status VARCHAR(20) DEFAULT 'ai_detected' CHECK (verification_status IN (
        'ai_detected',       -- AI가 탐지
        'human_confirmed',   -- 인간이 확인
        'human_rejected',    -- 인간이 기각
        'appealed'           -- 이의 제기됨
    )),
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_violations_result ON violations(result_id);
CREATE INDEX idx_violations_code ON violations(violation_code);
CREATE INDEX idx_violations_severity ON violations(severity);
```

#### 2.2.6 review_logs (심의 로그)

```sql
CREATE TABLE review_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 관계
    request_id UUID NOT NULL REFERENCES review_requests(id) ON DELETE CASCADE,
    
    -- 로그 내용
    stage VARCHAR(50) NOT NULL CHECK (stage IN (
        'claim_extraction',
        'violation_classification',
        'law_retrieval',
        'guideline_retrieval',
        'precedent_retrieval',
        'draft_generation',
        'evaluation',
        'human_review',
        'finalization'
    )),
    
    -- 데이터 (대용량이므로 압축 고려)
    input_data JSONB,
    output_data JSONB,
    
    -- 실행 정보
    llm_model VARCHAR(50),
    prompt_template VARCHAR(100),
    tokens_input INT,
    tokens_output INT,
    latency_ms INT,
    
    -- 에러 정보
    error_occurred BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    error_stack TEXT,
    
    -- 메타데이터
    iteration INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_review_logs_request ON review_logs(request_id);
CREATE INDEX idx_review_logs_stage ON review_logs(stage);
CREATE INDEX idx_review_logs_created ON review_logs(created_at);

-- 파티셔닝 (월별)
-- CREATE TABLE review_logs_2026_01 PARTITION OF review_logs
--     FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

#### 2.2.7 legal_documents (법령 문서)

```sql
CREATE TABLE legal_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 문서 유형
    doc_type VARCHAR(30) NOT NULL CHECK (doc_type IN (
        'law',           -- 법률
        'decree',        -- 시행령
        'regulation',    -- 시행규칙
        'guideline',     -- 심의 가이드라인
        'precedent',     -- 판례
        'interpretation' -- 유권해석
    )),
    
    -- 문서 정보
    title VARCHAR(300) NOT NULL,
    content TEXT NOT NULL,
    content_summary TEXT,
    
    -- 법령 구조
    law_name VARCHAR(100),           -- 의료법
    article VARCHAR(20),             -- 56
    paragraph VARCHAR(10),           -- 2
    item VARCHAR(10),                -- 1
    sub_item VARCHAR(10),            -- 가
    
    -- 계층 관계 (자기 참조)
    parent_id UUID REFERENCES legal_documents(id),
    hierarchy_level INT DEFAULT 0,   -- 0: 조, 1: 항, 2: 호, 3: 목
    hierarchy_path VARCHAR(100),     -- 56.2.1.가
    
    -- 효력 정보
    effective_date DATE NOT NULL,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 소스 정보
    source_url TEXT,
    source_name VARCHAR(100),        -- 국가법령정보센터, 대한의사협회 등
    
    -- 벡터 DB 연동
    embedding_id VARCHAR(100),       -- Pinecone vector ID
    embedding_updated_at TIMESTAMP WITH TIME ZONE,
    
    -- 검색
    search_vector TSVECTOR,
    
    -- 메타데이터
    keywords JSONB DEFAULT '[]'::JSONB,
    related_docs JSONB DEFAULT '[]'::JSONB,  -- 관련 문서 ID 목록
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_legal_docs_type ON legal_documents(doc_type);
CREATE INDEX idx_legal_docs_law_name ON legal_documents(law_name);
CREATE INDEX idx_legal_docs_article ON legal_documents(article, paragraph, item);
CREATE INDEX idx_legal_docs_active ON legal_documents(is_active);
CREATE INDEX idx_legal_docs_effective ON legal_documents(effective_date);
CREATE INDEX idx_legal_docs_search ON legal_documents USING GIN(search_vector);
CREATE INDEX idx_legal_docs_parent ON legal_documents(parent_id);
```

#### 2.2.8 banned_expressions (금지 표현)

```sql
CREATE TABLE banned_expressions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 표현 정보
    expression VARCHAR(200) NOT NULL,
    expression_pattern VARCHAR(500),     -- 정규표현식 패턴
    
    -- 분류
    category VARCHAR(50) NOT NULL CHECK (category IN (
        '최상급',
        '효능과장',
        '자격표시',
        '가격유인',
        '비교표현',
        '보장표현',
        '기타'
    )),
    
    -- 판정
    verdict VARCHAR(20) NOT NULL CHECK (verdict IN ('불허', '조건부허용', '주의')),
    
    -- 예외 및 조건
    exception_condition TEXT,
    required_evidence TEXT,              -- 허용에 필요한 증빙
    
    -- 법적 근거
    reference VARCHAR(100) NOT NULL,     -- 심의기준 제X조, 의료법 제56조 등
    
    -- 활성화
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 메타데이터
    examples JSONB DEFAULT '[]'::JSONB,  -- 실제 적용 예시
    notes TEXT,
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- 인덱스
CREATE INDEX idx_banned_expr_category ON banned_expressions(category);
CREATE INDEX idx_banned_expr_verdict ON banned_expressions(verdict);
CREATE INDEX idx_banned_expr_active ON banned_expressions(is_active);
CREATE INDEX idx_banned_expr_text ON banned_expressions USING GIN(to_tsvector('korean', expression));
```

#### 2.2.9 notifications (알림)

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 수신자
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 내용
    type VARCHAR(50) NOT NULL CHECK (type IN (
        'review_completed',
        'human_review_required',
        'verdict_finalized',
        'revision_requested',
        'system_alert'
    )),
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    
    -- 관련 리소스
    resource_type VARCHAR(50),           -- review_request, review_result
    resource_id UUID,
    
    -- 상태
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    
    -- 메타데이터
    metadata JSONB DEFAULT '{}'::JSONB,
    
    -- 감사 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_notifications_created ON notifications(created_at DESC);
```

### 2.3 뷰 (Views)

#### 2.3.1 심의 현황 대시보드 뷰

```sql
CREATE OR REPLACE VIEW v_review_dashboard AS
SELECT 
    rr.id,
    rr.ad_id,
    rr.hospital_name,
    rr.platform,
    rr.status,
    rr.priority,
    rr.created_at,
    rr.processing_started_at,
    rr.processing_completed_at,
    EXTRACT(EPOCH FROM (
        COALESCE(rr.processing_completed_at, NOW()) - rr.created_at
    )) / 60 AS waiting_minutes,
    res.verdict AS ai_verdict,
    res.confidence_score,
    res.final_verdict,
    res.human_reviewed,
    res.violation_count,
    u.name AS reviewer_name,
    o.name AS org_name
FROM review_requests rr
LEFT JOIN review_results res ON rr.id = res.request_id
LEFT JOIN users u ON rr.assigned_reviewer_id = u.id
LEFT JOIN organizations o ON rr.organization_id = o.id;
```

#### 2.3.2 일별 통계 뷰

```sql
CREATE OR REPLACE VIEW v_daily_statistics AS
SELECT 
    DATE(created_at) AS review_date,
    COUNT(*) AS total_requests,
    COUNT(*) FILTER (WHERE status = 'approved') AS approved_count,
    COUNT(*) FILTER (WHERE status = 'rejected') AS rejected_count,
    COUNT(*) FILTER (WHERE status = 'human_review') AS human_review_count,
    AVG(EXTRACT(EPOCH FROM (processing_completed_at - processing_started_at))) AS avg_processing_seconds,
    COUNT(DISTINCT organization_id) AS unique_orgs
FROM review_requests
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY review_date DESC;
```

---

## 3. Pinecone (Vector DB) 스키마

### 3.1 인덱스 구성

```yaml
# pinecone-index-config.yaml

index_name: "medadreview-legal-kb"
environment: "us-east-1"
dimension: 768  # Ko-Legal-SBERT 출력 차원
metric: "cosine"
pods: 1
replicas: 1
pod_type: "p1.x1"

metadata_config:
  indexed:
    - doc_type      # law, guideline, precedent
    - law_name      # 의료법, 심의기준 등
    - article       # 조 번호
    - is_active     # 현행 여부
    - effective_date # 시행일
    - category      # 위반 유형 카테고리
```

### 3.2 벡터 레코드 구조

```json
{
  "id": "legal_doc_medical_law_56_2_1",
  "values": [0.123, -0.456, 0.789, ...],  // 768 dimensions
  "metadata": {
    "doc_type": "law",
    "law_name": "의료법",
    "full_reference": "의료법 제56조 제2항 제1호",
    "article": "56",
    "paragraph": "2",
    "item": "1",
    "title": "신의료기술 미평가 광고 금지",
    "content": "「신의료기술평가에 관한 규칙」에 따른 신의료기술평가의 결과 안전성·유효성이 확인되지 아니한 의료기술에 관한 광고",
    "parent_content": "의료법인·의료기관 또는 의료인은 다음 각 호의 어느 하나에 해당하는 의료광고를 하지 못한다.",
    "hierarchy_path": "56.2.1",
    "effective_date": "2024-01-01",
    "is_active": true,
    "keywords": ["신의료기술", "안전성", "유효성", "평가"],
    "violation_code": "V1",
    "postgres_id": "uuid-string-here",
    "source": "국가법령정보센터",
    "last_updated": "2026-01-01"
  }
}
```

### 3.3 네임스페이스 구조

```
medadreview-legal-kb/
├── laws/           # 법률 조항
├── guidelines/     # 심의 가이드라인
├── precedents/     # 판례
├── interpretations/# 유권해석
└── expressions/    # 금지/허용 표현 패턴
```

---

## 4. Redis 스키마

### 4.1 캐시 키 구조

```
# 키 네이밍 컨벤션: {domain}:{entity}:{identifier}:{attribute}

# 세션 캐시
session:{user_id}                        -> JSON (user session data)
session:{user_id}:permissions            -> SET (permission names)

# 심의 상태 캐시
review:{request_id}:status              -> STRING (current status)
review:{request_id}:state               -> JSON (LangGraph state)
review:{request_id}:progress            -> HASH (processing progress)

# 검색 결과 캐시
search:law:{query_hash}                  -> JSON (search results)
search:guideline:{query_hash}            -> JSON (search results)

# 통계 캐시
stats:daily:{date}                       -> HASH (daily statistics)
stats:realtime                           -> HASH (real-time metrics)

# Rate Limiting
ratelimit:{user_id}:{endpoint}           -> STRING (request count)
ratelimit:api:{api_key}                  -> STRING (request count)

# 금지 표현 캐시
banned:expressions                       -> SET (all banned expressions)
banned:patterns                          -> JSON (regex patterns)
```

### 4.2 데이터 구조 예시

```python
# 심의 진행 상태 (Hash)
review:{request_id}:progress = {
    "stage": "evaluation",
    "progress_percent": 75,
    "iteration": 2,
    "started_at": "2026-01-07T10:00:00Z",
    "estimated_completion": "2026-01-07T10:05:00Z"
}

# 실시간 통계 (Hash)
stats:realtime = {
    "processing_count": "23",
    "pending_count": "156",
    "avg_wait_minutes": "3.5",
    "today_total": "1247",
    "today_approved": "524",
    "today_rejected": "478"
}

# 세션 데이터 (JSON String)
session:{user_id} = {
    "user_id": "uuid",
    "email": "reviewer@example.com",
    "role": "reviewer",
    "organization_id": "uuid",
    "permissions": ["review:read", "review:write"],
    "expires_at": "2026-01-07T18:00:00Z"
}
```

### 4.3 TTL 정책

| 키 패턴 | TTL | 설명 |
|---------|-----|------|
| `session:*` | 8시간 | 사용자 세션 |
| `review:*:status` | 24시간 | 심의 상태 캐시 |
| `review:*:state` | 1시간 | LangGraph 상태 |
| `search:*` | 30분 | 검색 결과 캐시 |
| `stats:daily:*` | 7일 | 일별 통계 |
| `stats:realtime` | 영구 | 실시간 통계 (갱신) |
| `banned:*` | 1시간 | 금지 표현 캐시 |
| `ratelimit:*` | 1분 | Rate limit 카운터 |

---

## 5. Application Layer 데이터 모델

### 5.1 Pydantic 모델 정의

#### 5.1.1 요청/응답 모델

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime
from uuid import UUID

# ============ 공통 ============

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int

# ============ 심의 요청 ============

class ReviewRequestCreate(BaseModel):
    """심의 요청 생성"""
    ad_id: str = Field(..., max_length=50, description="광고 고유 ID")
    ad_content: str = Field(..., min_length=10, max_length=50000, description="광고 내용")
    platform: Literal[
        'naver_blog', 'instagram', 'youtube', 'facebook',
        'website', 'kakaotalk', 'tiktok', 'other'
    ]
    ad_url: Optional[str] = None
    hospital_name: Optional[str] = Field(None, max_length=200)
    priority: Literal['urgent', 'high', 'normal', 'low'] = 'normal'
    metadata: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "ad_id": "AD-2026-00001",
                "ad_content": "저희 병원은 최첨단 줄기세포 치료로 100% 완치를 보장합니다.",
                "platform": "naver_blog",
                "hospital_name": "OO의원",
                "priority": "normal"
            }
        }

class ReviewRequestResponse(BaseModel):
    """심의 요청 응답"""
    id: UUID
    ad_id: str
    status: str
    priority: str
    created_at: datetime
    estimated_completion: Optional[datetime] = None

# ============ 심의 결과 ============

class ViolationDetail(BaseModel):
    """위반 상세 정보"""
    claim: str
    violation_code: str
    violation_type: str
    article: str
    reason: str
    severity: Literal['critical', 'high', 'medium', 'low']
    suggested_correction: Optional[str] = None

class ReviewResultResponse(BaseModel):
    """심의 결과 응답"""
    review_id: UUID
    request_id: UUID
    status: str
    verdict: Literal['허용', '조건부허용', '불허', '보류']
    confidence_score: float
    violations: List[ViolationDetail]
    reasoning: str
    suggestions: List[dict]
    
    # 처리 정보
    iteration_count: int
    processing_time_ms: int
    human_reviewed: bool
    
    # 최종 결과 (인간 검토 후)
    final_verdict: Optional[str] = None
    finalized_at: Optional[datetime] = None
    
    created_at: datetime
    updated_at: datetime

# ============ 인간 피드백 ============

class HumanFeedbackRequest(BaseModel):
    """인간 심의관 피드백"""
    action: Literal['approve', 'reject', 'modify']
    feedback: Optional[str] = Field(None, max_length=2000)
    modifications: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "action": "approve",
                "feedback": "AI 판단에 동의함. 최종 불허 처리."
            }
        }
```

#### 5.1.2 LangGraph State 모델

```python
from typing import TypedDict, List, Optional, Literal, Annotated
from datetime import datetime
from operator import add

class ClaimInfo(TypedDict):
    """추출된 주장 정보"""
    claim: str
    index: int
    category: Optional[str]
    severity: Optional[str]

class RetrievedDocument(TypedDict):
    """검색된 법령 문서"""
    id: str
    doc_type: str
    title: str
    content: str
    relevance_score: float
    metadata: dict

class ProcessingLog(TypedDict):
    """처리 로그"""
    stage: str
    timestamp: str
    duration_ms: int
    success: bool
    message: Optional[str]

class ReviewState(TypedDict):
    """LangGraph 심의 상태"""
    
    # === 입력 데이터 ===
    request_id: str
    ad_id: str
    ad_content: str
    ad_platform: str
    ad_metadata: dict
    
    # === 분석 중간 산출물 ===
    extracted_claims: Annotated[List[ClaimInfo], add]
    claim_categories: List[dict]
    
    # === 검색 결과 ===
    relevant_laws: List[RetrievedDocument]
    relevant_guidelines: List[RetrievedDocument]
    relevant_precedents: List[RetrievedDocument]
    
    # === 심의 초안 ===
    draft_verdict: Optional[str]
    draft_reasoning: Optional[str]
    draft_violations: List[dict]
    
    # === 검증 결과 ===
    evaluation_passed: bool
    critique_feedback: Optional[str]
    critique_scores: dict
    
    # === 최종 결과 ===
    final_verdict: Optional[Literal["허용", "조건부허용", "불허", "보류"]]
    final_reasoning: Optional[str]
    violation_articles: List[str]
    confidence_score: float
    suggestions: List[dict]
    
    # === 워크플로우 제어 ===
    iteration_count: int
    max_iterations: int
    requires_human_review: bool
    human_feedback: Optional[str]
    
    # === 메타데이터 ===
    processing_logs: Annotated[List[ProcessingLog], add]
    errors: List[str]
    created_at: str
    updated_at: str
```

### 5.2 열거형 (Enums)

```python
from enum import Enum

class ReviewStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    AI_COMPLETED = "ai_completed"
    HUMAN_REVIEW = "human_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_REQUESTED = "revision_requested"

class VerdictType(str, Enum):
    ALLOWED = "허용"
    CONDITIONAL = "조건부허용"
    DENIED = "불허"
    PENDING = "보류"

class ViolationCode(str, Enum):
    V1 = "V1"  # 신의료기술 미평가
    V2 = "V2"  # 치료 경험담
    V3 = "V3"  # 거짓/과장 광고
    V4 = "V4"  # 비교/비방 광고
    V5 = "V5"  # 객관적 근거 부재
    V6 = "V6"  # 최상급 표현

class Platform(str, Enum):
    NAVER_BLOG = "naver_blog"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    WEBSITE = "website"
    KAKAOTALK = "kakaotalk"
    TIKTOK = "tiktok"
    OTHER = "other"

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    REVIEWER = "reviewer"
    REVIEWER_LEAD = "reviewer_lead"
    SUBMITTER = "submitter"
    VIEWER = "viewer"

class Priority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

---

## 6. 데이터 무결성 및 제약조건

### 6.1 비즈니스 규칙

```sql
-- 1. 심의 결과는 반드시 심의 요청과 1:1 매핑
ALTER TABLE review_results 
ADD CONSTRAINT unique_request_result UNIQUE (request_id);

-- 2. 최종 판정은 인간 검토 후에만 가능
ALTER TABLE review_results
ADD CONSTRAINT human_review_before_final CHECK (
    final_verdict IS NULL OR human_reviewed = TRUE
);

-- 3. 확신도는 0~1 사이
ALTER TABLE review_results
ADD CONSTRAINT valid_confidence CHECK (
    confidence_score IS NULL OR 
    (confidence_score >= 0 AND confidence_score <= 1)
);

-- 4. 위반 건수는 음수 불가
ALTER TABLE review_results
ADD CONSTRAINT non_negative_violations CHECK (violation_count >= 0);

-- 5. 법령 문서의 효력 기간 유효성
ALTER TABLE legal_documents
ADD CONSTRAINT valid_effective_period CHECK (
    expiry_date IS NULL OR expiry_date > effective_date
);
```

### 6.2 트리거

```sql
-- 1. 심의 결과 생성 시 위반 건수 자동 계산
CREATE OR REPLACE FUNCTION update_violation_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE review_results
    SET violation_count = (
        SELECT COUNT(*) FROM violations WHERE result_id = NEW.result_id
    )
    WHERE id = NEW.result_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_violation_count
AFTER INSERT OR DELETE ON violations
FOR EACH ROW EXECUTE FUNCTION update_violation_count();

-- 2. 레코드 수정 시 updated_at 자동 갱신
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_review_requests_timestamp
BEFORE UPDATE ON review_requests
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_review_results_timestamp
BEFORE UPDATE ON review_results
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

---

## 7. 마이그레이션 전략

### 7.1 Alembic 마이그레이션

```python
# alembic/versions/001_initial_schema.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

def upgrade():
    # organizations 테이블 생성
    op.create_table(
        'organizations',
        sa.Column('id', UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        # ... 나머지 컬럼
    )
    
    # 인덱스 생성
    op.create_index('idx_organizations_type', 'organizations', ['type'])
    
    # ... 나머지 테이블

def downgrade():
    op.drop_table('organizations')
```

### 7.2 데이터 시드 (Seed Data)

```python
# scripts/seed_data.py

INITIAL_BANNED_EXPRESSIONS = [
    {
        "expression": "최고",
        "category": "최상급",
        "verdict": "불허",
        "exception_condition": "객관적 수상/인증 근거 시 예외",
        "reference": "심의기준 제3조"
    },
    {
        "expression": "100% 완치",
        "category": "보장표현",
        "verdict": "불허",
        "exception_condition": None,
        "reference": "의료법 제56조 제2항 제3호"
    },
    # ... 더 많은 금지 표현
]

INITIAL_LEGAL_DOCUMENTS = [
    {
        "doc_type": "law",
        "title": "의료법 제56조 제2항 제1호",
        "law_name": "의료법",
        "article": "56",
        "paragraph": "2",
        "item": "1",
        "content": "「신의료기술평가에 관한 규칙」에 따른...",
        "effective_date": "2024-01-01",
        "is_active": True
    },
    # ... 더 많은 법령
]
```

---

## 8. 부록

### A. 데이터 사전 (Data Dictionary)

| 테이블 | 컬럼 | 타입 | 설명 | 예시 |
|--------|------|------|------|------|
| review_requests | ad_id | VARCHAR(50) | 외부 광고 ID | AD-2026-00001 |
| review_requests | ad_content | TEXT | 광고 전문 | "저희 병원은..." |
| review_requests | platform | VARCHAR(50) | 게시 플랫폼 | naver_blog |
| review_results | verdict | VARCHAR(20) | AI 판정 결과 | 불허 |
| review_results | confidence_score | DECIMAL(4,3) | 확신도 | 0.925 |
| violations | violation_code | VARCHAR(10) | 위반 코드 | V3 |
| violations | severity | VARCHAR(20) | 심각도 | high |

### B. 성능 최적화 권장사항

1. **파티셔닝**: `review_logs` 테이블은 월별 파티셔닝 적용
2. **인덱스**: 자주 조회되는 복합 조건에 대한 복합 인덱스 생성
3. **아카이빙**: 6개월 이상된 로그 데이터는 별도 아카이브 테이블로 이동
4. **Connection Pooling**: PgBouncer 사용 권장 (max 100 connections)

---

**문서 끝**
