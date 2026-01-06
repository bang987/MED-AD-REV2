# 기술 스택 및 컨벤션 가이드 (Tech Stack & Rule Book)

**문서명:** MedAdReview 기술 스택 및 개발 컨벤션  
**버전:** 1.0  
**작성일:** 2026년 1월 7일  
**참조 문서:** PRD v1.0, 데이터 모델 명세서 v1.0, API 정의서 v1.0  

---

## 1. 기술 스택 개요

### 1.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              프로덕션 환경                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Client Layer                                 │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │   │
│  │  │  Web App      │  │  Mobile App   │  │  External API │           │   │
│  │  │  (React)      │  │  (React Native)│  │  Consumers   │           │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    API Gateway (Kong / AWS API Gateway)              │   │
│  │              - Rate Limiting, Auth, Load Balancing                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Application Layer                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  FastAPI    │  │  LangGraph  │  │  Celery     │  │ WebSocket │  │   │
│  │  │  Backend    │  │  Agent      │  │  Workers    │  │  Server   │  │   │
│  │  │  (Python)   │  │  (Python)   │  │  (Python)   │  │           │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          Data Layer                                  │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │   │
│  │  │PostgreSQL │  │ Pinecone  │  │   Redis   │  │    S3     │       │   │
│  │  │  (RDB)    │  │ (Vector)  │  │  (Cache)  │  │  (Files)  │       │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         External Services                            │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │   │
│  │  │  Claude API   │  │  OpenAI API   │  │  법령 API     │           │   │
│  │  │  (Anthropic)  │  │  (Fallback)   │  │  (국가법령)   │           │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 기술 스택 상세

| 계층 | 기술 | 버전 | 선정 이유 |
|------|------|------|-----------|
| **Frontend** | React | 18.x | 컴포넌트 기반 UI, 대규모 생태계 |
| | TypeScript | 5.x | 타입 안정성, 개발 생산성 |
| | TailwindCSS | 3.x | 유틸리티 기반 스타일링 |
| | Zustand | 4.x | 경량 상태 관리 |
| | React Query | 5.x | 서버 상태 관리, 캐싱 |
| **Backend** | FastAPI | 0.109+ | 비동기 처리, 자동 문서화 |
| | Python | 3.11+ | AI/ML 생태계, 타입 힌팅 |
| | Pydantic | 2.x | 데이터 검증 |
| | SQLAlchemy | 2.x | ORM, 비동기 지원 |
| **AI/Agent** | LangGraph | 0.1+ | 상태 기반 에이전트, 루프 지원 |
| | LangChain | 0.1+ | RAG 파이프라인 |
| | Ko-Legal-SBERT | - | 한국 법률 특화 임베딩 |
| **Database** | PostgreSQL | 16.x | JSONB, 전문 검색 |
| | Pinecone | - | 벡터 검색, 하이브리드 검색 |
| | Redis | 7.x | 캐싱, 세션, 큐 |
| **Infra** | Docker | 24.x | 컨테이너화 |
| | Kubernetes | 1.29+ | 오케스트레이션 |
| | AWS / GCP | - | 클라우드 인프라 |
| **CI/CD** | GitHub Actions | - | CI/CD 파이프라인 |
| | ArgoCD | - | GitOps 배포 |
| **Monitoring** | Prometheus | - | 메트릭 수집 |
| | Grafana | - | 대시보드, 알림 |
| | Sentry | - | 에러 트래킹 |

---

## 2. 프로젝트 구조

### 2.1 백엔드 디렉토리 구조

```
medadreview-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 앱 진입점
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # 환경 설정
│   │   └── logging.py             # 로깅 설정
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # 의존성 주입
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # API 라우터 통합
│   │       ├── auth.py            # 인증 API
│   │       ├── review.py          # 심의 API
│   │       ├── legal.py           # 법령 API
│   │       └── stats.py           # 통계 API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, 암호화
│   │   ├── exceptions.py          # 커스텀 예외
│   │   └── middleware.py          # 미들웨어
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # SQLAlchemy 베이스
│   │   ├── user.py
│   │   ├── review.py
│   │   ├── legal.py
│   │   └── enums.py               # 열거형
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py                # Pydantic 베이스
│   │   ├── request/               # 요청 스키마
│   │   │   ├── review.py
│   │   │   └── auth.py
│   │   └── response/              # 응답 스키마
│   │       ├── review.py
│   │       └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── review_service.py      # 심의 비즈니스 로직
│   │   ├── legal_service.py       # 법령 서비스
│   │   └── user_service.py        # 사용자 서비스
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                # Repository 베이스
│   │   ├── review_repo.py
│   │   └── user_repo.py
│   ├── agent/                     # LangGraph 에이전트
│   │   ├── __init__.py
│   │   ├── state.py               # 상태 정의
│   │   ├── nodes/                 # 노드 구현
│   │   │   ├── __init__.py
│   │   │   ├── claim_extraction.py
│   │   │   ├── violation_classification.py
│   │   │   ├── retrieval.py
│   │   │   ├── generator.py
│   │   │   └── evaluator.py
│   │   ├── graph.py               # 그래프 구성
│   │   └── prompts/               # 프롬프트 템플릿
│   │       ├── system.py
│   │       ├── claim_extraction.py
│   │       └── evaluation.py
│   ├── rag/                       # RAG 시스템
│   │   ├── __init__.py
│   │   ├── embedder.py            # 임베딩
│   │   ├── retriever.py           # 검색기
│   │   ├── reranker.py            # 리랭커
│   │   └── vector_store.py        # 벡터 저장소
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest 설정
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── seed_data.py               # 초기 데이터
│   ├── migrate.py                 # DB 마이그레이션
│   └── index_documents.py         # 벡터 인덱싱
├── alembic/                       # DB 마이그레이션
│   ├── versions/
│   └── env.py
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── .env.example
├── pyproject.toml                 # Poetry 설정
├── pytest.ini
└── README.md
```

### 2.2 프론트엔드 디렉토리 구조

```
medadreview-frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx             # 루트 레이아웃
│   │   ├── page.tsx               # 홈페이지
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── logout/
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # 대시보드
│   │   │   ├── reviews/
│   │   │   │   ├── page.tsx       # 심의 목록
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx   # 심의 상세
│   │   │   ├── legal/
│   │   │   └── settings/
│   │   └── api/                   # API 라우트 (BFF)
│   ├── components/
│   │   ├── ui/                    # 공통 UI 컴포넌트
│   │   │   ├── Button/
│   │   │   ├── Card/
│   │   │   ├── Table/
│   │   │   ├── Modal/
│   │   │   └── ...
│   │   ├── layout/                # 레이아웃 컴포넌트
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   └── Footer/
│   │   ├── review/                # 심의 관련 컴포넌트
│   │   │   ├── ReviewCard/
│   │   │   ├── ReviewDetail/
│   │   │   ├── ViolationBadge/
│   │   │   └── FeedbackForm/
│   │   └── dashboard/             # 대시보드 컴포넌트
│   │       ├── StatsCard/
│   │       ├── TrendChart/
│   │       └── RealtimeIndicator/
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useReview.ts
│   │   ├── useWebSocket.ts
│   │   └── useStats.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── reviewStore.ts
│   │   └── uiStore.ts
│   ├── services/
│   │   ├── api.ts                 # Axios 인스턴스
│   │   ├── authService.ts
│   │   ├── reviewService.ts
│   │   └── legalService.ts
│   ├── types/
│   │   ├── index.ts
│   │   ├── review.ts
│   │   ├── user.ts
│   │   └── api.ts
│   ├── lib/
│   │   ├── utils.ts
│   │   └── constants.ts
│   └── styles/
│       └── globals.css
├── public/
├── tests/
├── .env.local.example
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

---

## 3. 코딩 컨벤션

### 3.1 Python 백엔드 컨벤션

#### 3.1.1 스타일 가이드

```python
# ✅ Good: PEP 8 준수, 타입 힌트 사용
from typing import Optional, List
from datetime import datetime

class ReviewService:
    """심의 관련 비즈니스 로직을 처리하는 서비스 클래스"""
    
    def __init__(self, repository: ReviewRepository) -> None:
        self._repository = repository
    
    async def create_review(
        self,
        ad_content: str,
        platform: str,
        *,
        priority: str = "normal",
        metadata: Optional[dict] = None,
    ) -> ReviewResult:
        """
        새로운 심의 요청을 생성합니다.
        
        Args:
            ad_content: 광고 내용
            platform: 게시 플랫폼
            priority: 우선순위 (기본값: normal)
            metadata: 추가 메타데이터
            
        Returns:
            ReviewResult: 생성된 심의 결과
            
        Raises:
            ValidationError: 입력값이 유효하지 않은 경우
            DuplicateError: 동일한 광고가 이미 존재하는 경우
        """
        # 구현...


# ❌ Bad: 타입 힌트 없음, 문서화 없음
class ReviewService:
    def __init__(self, repository):
        self.repository = repository
    
    async def create_review(self, ad_content, platform, priority="normal"):
        pass
```

#### 3.1.2 네이밍 규칙

```python
# 클래스: PascalCase
class ReviewService:
    pass

class ReviewResultSchema:
    pass

# 함수/메서드: snake_case
async def create_review_request():
    pass

def calculate_confidence_score():
    pass

# 상수: SCREAMING_SNAKE_CASE
MAX_ITERATIONS = 3
DEFAULT_CONFIDENCE_THRESHOLD = 0.8

# 프라이빗 멤버: _prefix
class Service:
    def __init__(self):
        self._private_attribute = None
    
    def _private_method(self):
        pass

# 환경 변수: SCREAMING_SNAKE_CASE with prefix
MEDADREVIEW_DATABASE_URL = "postgresql://..."
MEDADREVIEW_REDIS_URL = "redis://..."
```

#### 3.1.3 예외 처리

```python
# exceptions.py
from fastapi import HTTPException, status

class MedAdReviewException(Exception):
    """기본 예외 클래스"""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(MedAdReviewException):
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field

class NotFoundError(MedAdReviewException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            f"{resource}를 찾을 수 없습니다: {identifier}",
            "NOT_FOUND"
        )

class ProcessingError(MedAdReviewException):
    def __init__(self, message: str, retry_available: bool = True):
        super().__init__(message, "PROCESSING_ERROR")
        self.retry_available = retry_available


# 사용 예시
async def get_review(review_id: str) -> Review:
    review = await repository.find_by_id(review_id)
    if not review:
        raise NotFoundError("Review", review_id)
    return review
```

#### 3.1.4 Pydantic 모델 작성

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime

class ReviewRequestCreate(BaseModel):
    """심의 요청 생성 스키마"""
    
    ad_id: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="광고 고유 ID",
        examples=["AD-2026-00001"]
    )
    ad_content: str = Field(
        ..., 
        min_length=10, 
        max_length=50000,
        description="광고 내용"
    )
    platform: Literal[
        'naver_blog', 'instagram', 'youtube', 
        'facebook', 'website', 'other'
    ] = Field(..., description="게시 플랫폼")
    priority: Literal['urgent', 'high', 'normal', 'low'] = Field(
        default='normal',
        description="우선순위"
    )
    hospital_name: Optional[str] = Field(
        None, 
        max_length=200,
        description="병원명"
    )
    
    @field_validator('ad_content')
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("광고 내용은 공백만으로 구성될 수 없습니다")
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "ad_id": "AD-2026-00001",
                "ad_content": "저희 병원은 최첨단 치료를 제공합니다.",
                "platform": "naver_blog",
                "priority": "normal",
                "hospital_name": "OO의원"
            }
        }
    }
```

### 3.2 TypeScript 프론트엔드 컨벤션

#### 3.2.1 컴포넌트 작성

```tsx
// ✅ Good: 타입 정의, props 구조 분해, 명확한 반환 타입
import { FC, useState, useCallback } from 'react';
import { Review, Verdict } from '@/types';
import { Button, Badge, Card } from '@/components/ui';
import { formatDate } from '@/lib/utils';

interface ReviewCardProps {
  review: Review;
  onSelect?: (id: string) => void;
  isSelected?: boolean;
  className?: string;
}

export const ReviewCard: FC<ReviewCardProps> = ({
  review,
  onSelect,
  isSelected = false,
  className = '',
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleClick = useCallback(() => {
    onSelect?.(review.id);
  }, [review.id, onSelect]);
  
  const getVerdictColor = (verdict: Verdict): string => {
    const colors: Record<Verdict, string> = {
      '허용': 'bg-green-100 text-green-800',
      '조건부허용': 'bg-yellow-100 text-yellow-800',
      '불허': 'bg-red-100 text-red-800',
      '보류': 'bg-gray-100 text-gray-800',
    };
    return colors[verdict];
  };
  
  return (
    <Card 
      className={`p-4 cursor-pointer ${isSelected ? 'ring-2 ring-blue-500' : ''} ${className}`}
      onClick={handleClick}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-gray-900">{review.ad_id}</h3>
          <p className="text-sm text-gray-500">{review.hospital_name}</p>
        </div>
        <Badge className={getVerdictColor(review.verdict)}>
          {review.verdict}
        </Badge>
      </div>
      
      <p className="mt-2 text-sm text-gray-600 line-clamp-2">
        {review.ad_content}
      </p>
      
      <div className="mt-3 flex items-center text-xs text-gray-400">
        <span>{formatDate(review.created_at)}</span>
        <span className="mx-2">•</span>
        <span>확신도: {(review.confidence_score * 100).toFixed(1)}%</span>
      </div>
    </Card>
  );
};
```

#### 3.2.2 커스텀 훅 작성

```tsx
// hooks/useReview.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { reviewService } from '@/services/reviewService';
import { ReviewRequest, ReviewResult, HumanFeedback } from '@/types';

export const useReview = (reviewId: string) => {
  return useQuery({
    queryKey: ['review', reviewId],
    queryFn: () => reviewService.getReview(reviewId),
    enabled: !!reviewId,
    staleTime: 30 * 1000, // 30초
    refetchInterval: (data) => 
      data?.status === 'processing' ? 3000 : false,
  });
};

export const useReviewList = (params: ReviewListParams) => {
  return useQuery({
    queryKey: ['reviews', params],
    queryFn: () => reviewService.getReviews(params),
    keepPreviousData: true,
  });
};

export const useCreateReview = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (request: ReviewRequest) => 
      reviewService.createReview(request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews'] });
    },
  });
};

export const useSubmitFeedback = (reviewId: string) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (feedback: HumanFeedback) =>
      reviewService.submitFeedback(reviewId, feedback),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['review', reviewId] });
      queryClient.invalidateQueries({ queryKey: ['reviews'] });
    },
  });
};
```

#### 3.2.3 타입 정의

```typescript
// types/review.ts
export type Verdict = '허용' | '조건부허용' | '불허' | '보류';
export type ViolationCode = 'V1' | 'V2' | 'V3' | 'V4' | 'V5' | 'V6';
export type Severity = 'critical' | 'high' | 'medium' | 'low';
export type ReviewStatus = 
  | 'pending' 
  | 'processing' 
  | 'ai_completed' 
  | 'human_review' 
  | 'approved' 
  | 'rejected';

export interface Violation {
  id: string;
  claim: string;
  violationCode: ViolationCode;
  violationType: string;
  article: string;
  reason: string;
  severity: Severity;
  suggestedCorrection?: string;
}

export interface Review {
  id: string;
  adId: string;
  adContent: string;
  platform: string;
  hospitalName?: string;
  status: ReviewStatus;
  verdict?: Verdict;
  confidenceScore?: number;
  violations: Violation[];
  reasoning?: string;
  suggestions: Suggestion[];
  humanReviewed: boolean;
  finalVerdict?: Verdict;
  createdAt: string;
  updatedAt: string;
}

export interface ReviewRequest {
  adId: string;
  adContent: string;
  platform: string;
  priority?: 'urgent' | 'high' | 'normal' | 'low';
  hospitalName?: string;
  metadata?: Record<string, unknown>;
}

export interface HumanFeedback {
  action: 'approve' | 'reject' | 'modify';
  finalVerdict?: Verdict;
  feedback?: string;
  modifications?: {
    addViolations?: Partial<Violation>[];
    removeViolations?: string[];
    updateSeverity?: Record<string, Severity>;
  };
}
```

### 3.3 Git 컨벤션

#### 3.3.1 브랜치 전략

```
main (production)
  └── develop (staging)
        ├── feature/MAR-123-add-violation-detection
        ├── feature/MAR-124-improve-rag-accuracy
        ├── bugfix/MAR-125-fix-confidence-calculation
        ├── hotfix/MAR-126-critical-security-fix
        └── refactor/MAR-127-optimize-retrieval
```

#### 3.3.2 커밋 메시지

```bash
# 형식: <type>(<scope>): <subject>
# 
# type: feat, fix, docs, style, refactor, test, chore
# scope: api, agent, rag, ui, db, infra (선택)
# subject: 명령형, 현재 시제로 작성

# ✅ Good
feat(agent): 적대적 검증 노드 추가
fix(api): 심의 결과 조회 시 null 처리 오류 수정
docs: API 문서에 WebSocket 섹션 추가
refactor(rag): 하이브리드 검색 로직 개선
test(agent): Generator 노드 단위 테스트 추가
chore: 의존성 패키지 업데이트

# ❌ Bad
updated code
fix bug
WIP
asdf
```

#### 3.3.3 PR 템플릿

```markdown
## 📋 변경 사항
<!-- 이 PR에서 변경된 내용을 설명하세요 -->

## 🎯 관련 이슈
<!-- 관련된 Jira/GitHub 이슈 번호 -->
- MAR-123

## 🧪 테스트
<!-- 테스트 방법 또는 테스트 결과 -->
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

## 📸 스크린샷 (UI 변경 시)
<!-- 해당되는 경우 스크린샷 첨부 -->

## ✅ 체크리스트
- [ ] 코드 스타일 가이드 준수
- [ ] 필요한 문서 업데이트
- [ ] 타입 정의 추가/수정
- [ ] 에러 처리 추가
```

---

## 4. LangGraph 에이전트 구현 가이드

### 4.1 State 정의 규칙

```python
# agent/state.py
from typing import TypedDict, List, Optional, Literal, Annotated
from operator import add

class ReviewState(TypedDict):
    """
    LangGraph 상태 정의
    
    규칙:
    1. 모든 필드는 TypedDict로 정의
    2. 누적이 필요한 리스트는 Annotated[List, add] 사용
    3. 선택적 필드는 Optional 사용
    4. 열거형 값은 Literal 사용
    """
    
    # 불변 입력 데이터
    request_id: str
    ad_content: str
    
    # 누적되는 데이터 (reducer 사용)
    extracted_claims: Annotated[List[dict], add]
    processing_logs: Annotated[List[dict], add]
    
    # 단계별 덮어쓰기 데이터
    draft_verdict: Optional[str]
    final_verdict: Optional[Literal["허용", "조건부허용", "불허", "보류"]]
    
    # 제어 변수
    iteration_count: int
    should_continue: bool
```

### 4.2 노드 구현 패턴

```python
# agent/nodes/claim_extraction.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from ..state import ReviewState
from ..prompts.claim_extraction import CLAIM_EXTRACTION_PROMPT

async def extract_claims(state: ReviewState) -> dict:
    """
    노드 구현 규칙:
    1. state를 입력으로 받고 dict를 반환
    2. 반환 dict는 업데이트할 필드만 포함
    3. 에러 발생 시 적절한 로깅 후 기본값 반환
    4. 비동기 함수로 구현
    """
    try:
        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        prompt = ChatPromptTemplate.from_template(CLAIM_EXTRACTION_PROMPT)
        
        chain = prompt | llm
        response = await chain.ainvoke({
            "ad_content": state["ad_content"]
        })
        
        claims = parse_claims(response.content)
        
        return {
            "extracted_claims": claims,
            "processing_logs": [{
                "stage": "claim_extraction",
                "success": True,
                "claims_count": len(claims)
            }]
        }
        
    except Exception as e:
        logger.error(f"Claim extraction failed: {e}")
        return {
            "extracted_claims": [],
            "processing_logs": [{
                "stage": "claim_extraction",
                "success": False,
                "error": str(e)
            }]
        }
```

### 4.3 그래프 구성

```python
# agent/graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import ReviewState
from .nodes import (
    extract_claims,
    classify_violations,
    retrieve_laws,
    generate_draft,
    evaluate_draft,
    decide_human_review,
    finalize_result
)

def create_review_graph():
    """
    그래프 구성 규칙:
    1. 명확한 노드 이름 사용
    2. 조건부 엣지는 별도 함수로 정의
    3. 무한 루프 방지를 위한 max_iterations 체크
    """
    
    workflow = StateGraph(ReviewState)
    
    # 노드 추가
    workflow.add_node("extract_claims", extract_claims)
    workflow.add_node("classify_violations", classify_violations)
    workflow.add_node("retrieve_laws", retrieve_laws)
    workflow.add_node("generate_draft", generate_draft)
    workflow.add_node("evaluate_draft", evaluate_draft)
    workflow.add_node("decide_human_review", decide_human_review)
    workflow.add_node("finalize", finalize_result)
    
    # 엣지 정의
    workflow.set_entry_point("extract_claims")
    
    workflow.add_edge("extract_claims", "classify_violations")
    workflow.add_edge("classify_violations", "retrieve_laws")
    workflow.add_edge("retrieve_laws", "generate_draft")
    workflow.add_edge("generate_draft", "evaluate_draft")
    
    # 조건부 엣지: 평가 통과 여부
    workflow.add_conditional_edges(
        "evaluate_draft",
        should_retry_generation,
        {
            "retry": "generate_draft",
            "proceed": "decide_human_review"
        }
    )
    
    # 조건부 엣지: 인간 검토 필요 여부
    workflow.add_conditional_edges(
        "decide_human_review",
        requires_human_review,
        {
            "human_review": END,  # 인터럽트
            "auto_complete": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    # 체크포인터 추가 (상태 저장)
    memory = MemorySaver()
    
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["decide_human_review"]  # HITL 인터럽트
    )


def should_retry_generation(state: ReviewState) -> str:
    """평가 통과 여부에 따른 라우팅"""
    if state.get("evaluation_passed", False):
        return "proceed"
    
    if state.get("iteration_count", 0) >= 3:
        # 최대 반복 횟수 도달
        return "proceed"
    
    return "retry"


def requires_human_review(state: ReviewState) -> str:
    """인간 검토 필요 여부 판단"""
    confidence = state.get("confidence_score", 0)
    
    if confidence < 0.8:
        return "human_review"
    
    if state.get("verdict") == "보류":
        return "human_review"
    
    return "auto_complete"
```

---

## 5. 테스트 가이드

### 5.1 테스트 구조

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.base import Base
from app.config.settings import settings

@pytest.fixture
async def db_session():
    """테스트용 DB 세션"""
    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def sample_review_request():
    """테스트용 심의 요청 데이터"""
    return {
        "ad_id": "TEST-001",
        "ad_content": "최고의 의료 서비스를 제공합니다.",
        "platform": "naver_blog",
        "priority": "normal"
    }
```

### 5.2 단위 테스트 예시

```python
# tests/unit/test_claim_extraction.py
import pytest
from app.agent.nodes.claim_extraction import extract_claims, parse_claims

class TestClaimExtraction:
    
    @pytest.mark.asyncio
    async def test_extract_claims_success(self, mock_llm):
        """정상적인 주장 추출 테스트"""
        state = {
            "ad_content": "100% 완치를 보장하는 최고의 병원입니다."
        }
        
        result = await extract_claims(state)
        
        assert "extracted_claims" in result
        assert len(result["extracted_claims"]) >= 1
        assert result["processing_logs"][0]["success"] is True
    
    def test_parse_claims_with_valid_response(self):
        """주장 파싱 테스트"""
        response = """
        1. "100% 완치" - 치료 보장 표현
        2. "최고의 병원" - 최상급 표현
        """
        
        claims = parse_claims(response)
        
        assert len(claims) == 2
        assert claims[0]["claim"] == "100% 완치"
    
    @pytest.mark.asyncio
    async def test_extract_claims_empty_content(self):
        """빈 광고 내용 처리 테스트"""
        state = {"ad_content": "   "}
        
        result = await extract_claims(state)
        
        assert result["extracted_claims"] == []
```

### 5.3 통합 테스트 예시

```python
# tests/integration/test_review_workflow.py
import pytest
from app.agent.graph import create_review_graph

class TestReviewWorkflow:
    
    @pytest.mark.asyncio
    async def test_full_review_workflow(self):
        """전체 심의 워크플로우 테스트"""
        graph = create_review_graph()
        
        initial_state = {
            "request_id": "test-001",
            "ad_content": "저희 병원은 100% 완치를 보장합니다.",
            "extracted_claims": [],
            "processing_logs": [],
            "iteration_count": 0
        }
        
        config = {"configurable": {"thread_id": "test-thread"}}
        
        result = await graph.ainvoke(initial_state, config)
        
        assert result["final_verdict"] in ["허용", "조건부허용", "불허", "보류"]
        assert result["confidence_score"] >= 0
        assert len(result["extracted_claims"]) > 0
    
    @pytest.mark.asyncio
    async def test_loop_iteration_limit(self):
        """루프 반복 제한 테스트"""
        graph = create_review_graph()
        
        # 항상 평가 실패하는 상태
        initial_state = {
            "request_id": "test-002",
            "ad_content": "...",
            "iteration_count": 0,
            "evaluation_passed": False
        }
        
        result = await graph.ainvoke(initial_state)
        
        # 최대 3회 반복 후 종료
        assert result["iteration_count"] <= 3
```

---

## 6. 배포 가이드

### 6.1 Docker 설정

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 소스 복사
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6.2 Kubernetes 설정

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medadreview-api
  labels:
    app: medadreview-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: medadreview-api
  template:
    metadata:
      labels:
        app: medadreview-api
    spec:
      containers:
      - name: api
        image: medadreview/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: medadreview-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
```

---

## 7. 환경 변수

```bash
# .env.example

# === Application ===
APP_ENV=development  # development, staging, production
APP_DEBUG=true
APP_SECRET_KEY=your-secret-key-here

# === Database ===
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/medadreview
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# === Redis ===
REDIS_URL=redis://localhost:6379/0

# === Vector DB (Pinecone) ===
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=medadreview-legal-kb

# === LLM ===
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key  # Fallback
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=8000

# === Agent Settings ===
AGENT_MAX_ITERATIONS=3
AGENT_CONFIDENCE_THRESHOLD=0.8
AGENT_AUTO_APPROVE_THRESHOLD=0.95

# === JWT ===
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480

# === External APIs ===
LEGAL_API_BASE_URL=https://www.law.go.kr/api

# === Monitoring ===
SENTRY_DSN=https://xxx@sentry.io/xxx
LOG_LEVEL=INFO
```

---

**문서 끝**
