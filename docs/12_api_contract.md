# API 및 인터페이스 정의서 (API Contract)

**문서명:** MedAdReview API 명세서  
**버전:** 1.0  
**작성일:** 2026년 1월 7일  
**참조 문서:** PRD v1.0, 데이터 모델 명세서 v1.0  

---

## 1. 개요

### 1.1 API 기본 정보

| 항목 | 값 |
|------|-----|
| Base URL (Production) | `https://api.medadreview.ai` |
| Base URL (Staging) | `https://api-staging.medadreview.ai` |
| API Version | v1 |
| Content-Type | application/json |
| Character Encoding | UTF-8 |

### 1.2 인증

모든 API는 JWT Bearer Token 인증을 사용합니다.

```http
Authorization: Bearer <access_token>
```

---

## 2. 심의 API (/api/v1/review)

### 2.1 심의 요청 생성

**POST /api/v1/review**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| ad_id | string | Y | 광고 고유 ID |
| ad_content | string | Y | 광고 내용 (10~50000자) |
| platform | string | Y | 플랫폼 (naver_blog, instagram, youtube 등) |
| priority | string | N | 우선순위 (urgent, high, normal, low) |
| hospital_name | string | N | 병원명 |

**Request**
```json
{
  "ad_id": "AD-2026-00001",
  "ad_content": "저희 병원은 최첨단 줄기세포 치료로 100% 완치를 보장합니다.",
  "platform": "naver_blog",
  "hospital_name": "OO의원",
  "priority": "normal"
}
```

**Response (202 Accepted)**
```json
{
  "success": true,
  "data": {
    "review_id": "rev_550e8400-e29b-41d4-a716-446655440000",
    "ad_id": "AD-2026-00001",
    "status": "pending",
    "estimated_completion": "2026-01-07T10:05:00Z"
  }
}
```

### 2.2 심의 결과 조회

**GET /api/v1/review/{review_id}**

**Response (200 OK)**
```json
{
  "success": true,
  "data": {
    "review_id": "rev_550e8400...",
    "status": "ai_completed",
    "verdict": "불허",
    "confidence_score": 0.92,
    "violations": [
      {
        "claim": "100% 완치를 보장",
        "violation_code": "V3",
        "article": "제56조 제2항 제3호",
        "reason": "치료 효과 보장은 의학적으로 불가능한 과장 표현",
        "severity": "high",
        "suggested_correction": "치료 효과가 있을 수 있습니다"
      }
    ],
    "reasoning": "본 광고는 의료법 위반 사항이 발견되었습니다...",
    "processing_time_ms": 4523,
    "human_reviewed": false
  }
}
```

### 2.3 심의 목록 조회

**GET /api/v1/review**

Query Parameters: status, priority, platform, page, page_size, sort_by

### 2.4 인간 피드백 제출

**POST /api/v1/review/{review_id}/feedback**

```json
{
  "action": "approve",
  "final_verdict": "불허",
  "feedback": "AI 판단에 동의합니다."
}
```

---

## 3. 법령 API (/api/v1/legal)

### 3.1 법령 검색

**GET /api/v1/legal/search?query={검색어}&doc_type={유형}&limit={개수}**

### 3.2 금지 표현 조회

**GET /api/v1/legal/banned-expressions?category={카테고리}**

---

## 4. 통계 API (/api/v1/stats)

### 4.1 대시보드 통계

**GET /api/v1/stats/dashboard**

```json
{
  "realtime": {
    "processing_count": 23,
    "pending_count": 156,
    "avg_wait_minutes": 3.5
  },
  "today": {
    "total_requests": 1247,
    "verdict_distribution": {
      "허용": 462, "조건부허용": 165, "불허": 418, "보류": 55
    }
  },
  "performance": {
    "legal_recall": 0.962,
    "legal_precision": 0.915,
    "hallucination_rate": 0.008
  }
}
```

---

## 5. WebSocket API (/ws)

### 5.1 심의 진행 상황 구독

```javascript
const ws = new WebSocket('wss://api.medadreview.ai/ws/review/{review_id}');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // { type: "progress", data: { stage: "evaluation", progress_percent: 75 } }
};
```

---

## 6. 에러 코드

| HTTP | Code | 설명 |
|------|------|------|
| 400 | VALIDATION_ERROR | 요청 데이터 검증 실패 |
| 401 | UNAUTHORIZED | 인증 필요 |
| 403 | FORBIDDEN | 권한 없음 |
| 404 | NOT_FOUND | 리소스 없음 |
| 429 | RATE_LIMITED | 요청 한도 초과 |
| 500 | INTERNAL_ERROR | 서버 오류 |

---

## 7. Rate Limiting

| 사용자 유형 | 제한 | 윈도우 |
|------------|------|--------|
| 일반 | 100 req | 1분 |
| 프리미엄 | 500 req | 1분 |
| API Key | 1000 req | 1분 |

---

**문서 끝**
