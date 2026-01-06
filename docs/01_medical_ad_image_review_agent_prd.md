# 의료광고 이미지 심의 AI 에이전트 PRD (Product Requirements Document)

**프로젝트명:** MedAdVision AI Agent  
**버전:** 1.0  
**작성일:** 2026년 1월 7일  
**작성자:** AI 에이전트 개발팀  

---

## 1. Executive Summary

### 1.1 프로젝트 개요

본 프로젝트는 **광고 이미지**를 대상으로 NAVER CLOVA OCR을 활용하여 텍스트를 추출하고, 대한민국 의료법 제56조 및 제57조에 근거한 의료광고 심의 업무를 자동화하는 AI 에이전트 시스템을 구축한다. LangGraph 기반의 루프(Loop) 아키텍처와 한국 법률 특화 RAG 시스템을 결합하여, 인간 심의위원 수준의 법적 추론 능력을 갖춘 지능형 에이전트를 개발한다.

### 1.2 핵심 목표

| 목표 | 설명 | 성공 지표 |
|------|------|-----------|
| **정확성** | 인간 심의위원과 동등한 판정 정확도 | 법적 재현율(Recall) 95% 이상 |
| **OCR 정확도** | 광고 이미지 텍스트 추출 정확도 | 문자 인식률 98% 이상 |
| **일관성** | 동일 유형 광고에 대한 일관된 판정 | 일관성 지표 98% 이상 |
| **효율성** | 심의 처리 시간 대폭 단축 | 건당 처리시간 5분 이내 |
| **설명가능성** | 모든 판정에 법적 근거 제시 | 근거 정확도 90% 이상 |

### 1.3 프로젝트 범위

**In Scope (v1.0 - 현재 버전):**
- **광고 이미지 기반 심의** (배너, 포스터, 카드뉴스, SNS 이미지 광고)
- NAVER CLOVA OCR을 통한 이미지 내 텍스트 추출
- 의료법 제56조 위반 사항 탐지
- 심의 가이드라인 기반 판정
- 인간 심의위원 협업 워크플로우

**Out of Scope (v2.0 - 다음 버전):**
- 텍스트 기반 의료광고 심의 (블로그, SNS 텍스트, 웹사이트)
- 동영상 광고 심의
- 실시간 모니터링 시스템

### 1.4 지원 이미지 형식

| 형식 | 확장자 | 최대 크기 | 비고 |
|------|--------|-----------|------|
| JPEG | .jpg, .jpeg | 10MB | 권장 |
| PNG | .png | 10MB | 투명 배경 지원 |
| GIF | .gif | 5MB | 첫 프레임만 처리 |
| BMP | .bmp | 10MB | 지원 |
| TIFF | .tiff, .tif | 10MB | 지원 |
| WebP | .webp | 10MB | 지원 |

---

## 2. 기술 아키텍처

### 2.1 시스템 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MedAdVision AI Agent v1.0                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │
│  │  이미지     │   │  OCR 처리   │   │  AI 심의    │   │  결과 출력  │ │
│  │  입력층     │──►│  (CLOVA)    │──►│  (LangGraph)│──►│             │ │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │
│         │                 │                 │                 │         │
│         ▼                 ▼                 ▼                 ▼         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │
│  │ 이미지      │   │ 텍스트     │   │ RAG        │   │ 심의 결과   │ │
│  │ 전처리      │   │ + 좌표     │   │ Knowledge  │   │ + 근거     │ │
│  │ (리사이즈,  │   │ + 신뢰도   │   │ Base       │   │ + 수정제안 │ │
│  │  노이즈제거)│   │            │   │            │   │            │ │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 상세 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         이미지 심의 파이프라인                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [1. 이미지 입력]                                                       │
│       │                                                                 │
│       ▼                                                                 │
│  [2. 이미지 전처리]                                                     │
│       │  - 해상도 조정 (CLOVA 최적: 2048x2048 이하)                     │
│       │  - 노이즈 제거                                                  │
│       │  - 기울기 보정 (Deskewing)                                      │
│       │  - 대비 향상                                                    │
│       ▼                                                                 │
│  [3. NAVER CLOVA OCR 호출]                                              │
│       │  - General OCR API 사용                                         │
│       │  - 텍스트 + 바운딩 박스 + 신뢰도 반환                           │
│       ▼                                                                 │
│  [4. OCR 결과 후처리]                                                   │
│       │  - 텍스트 정규화 (띄어쓰기, 특수문자)                           │
│       │  - 레이아웃 분석 (제목/본문/주석 구분)                          │
│       │  - 저신뢰도 텍스트 필터링                                       │
│       ▼                                                                 │
│  [5. LangGraph 심의 에이전트]                                           │
│       │  - 청구항 추출                                                  │
│       │  - 법령 검색 (RAG)                                              │
│       │  - 심의 판정                                                    │
│       │  - 자기 검증 루프                                               │
│       ▼                                                                 │
│  [6. 결과 출력]                                                         │
│       - 심의 결과 (허용/불허/조건부허용/보류)                           │
│       - 위반 문구 하이라이트 (이미지 좌표 기반)                         │
│       - 법적 근거 및 수정 제안                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 핵심 기술 스택

| 계층 | 기술 | 선정 이유 |
|------|------|-----------|
| **OCR** | NAVER CLOVA OCR | 한국어 특화, 높은 정확도, 좌표 정보 제공 |
| **이미지 전처리** | OpenCV + Pillow | 경량화, 다양한 전처리 기능 |
| **LLM** | Claude 3.5 Sonnet / GPT-4o | 한국어 법률 추론 능력 |
| **Agent Framework** | LangGraph | 루프 기반 상태 관리 |
| **Vector DB** | Pinecone / Milvus | 하이브리드 검색 지원 |
| **Embedding** | Ko-Legal-SBERT | 한국 법률 특화 임베딩 |
| **Backend** | FastAPI + Python 3.11 | 비동기 처리, 이미지 핸들링 |
| **Storage** | AWS S3 / MinIO | 이미지 저장 및 관리 |
| **Frontend** | React + TypeScript | 심의관 대시보드, 이미지 뷰어 |

---

## 3. NAVER CLOVA OCR 연동

### 3.1 CLOVA OCR API 개요

NAVER CLOVA OCR은 이미지에서 텍스트를 인식하는 API로, 한국어에 특화된 높은 정확도를 제공한다.

#### 3.1.1 API 엔드포인트

| API | 용도 | 엔드포인트 |
|-----|------|------------|
| General OCR | 일반 이미지 텍스트 인식 | `https://clovaocr.apigw.ntruss.com/general/` |
| Template OCR | 정형화된 문서 인식 | `https://clovaocr.apigw.ntruss.com/template/` |

**본 프로젝트에서는 General OCR 사용** (광고 이미지는 비정형 레이아웃)

#### 3.1.2 API 요청/응답 구조

**Request:**
```json
{
  "version": "V2",
  "requestId": "req-001",
  "timestamp": 1704567890000,
  "lang": "ko",
  "images": [
    {
      "format": "jpg",
      "name": "medical_ad_001",
      "data": "BASE64_ENCODED_IMAGE_DATA"
    }
  ],
  "enableTableDetection": false
}
```

**Response:**
```json
{
  "version": "V2",
  "requestId": "req-001",
  "timestamp": 1704567891234,
  "images": [
    {
      "uid": "img-uid-001",
      "name": "medical_ad_001",
      "inferResult": "SUCCESS",
      "message": "SUCCESS",
      "validationResult": {
        "result": "NO_ERROR"
      },
      "fields": [
        {
          "valueType": "ALL",
          "boundingPoly": {
            "vertices": [
              {"x": 100, "y": 50},
              {"x": 300, "y": 50},
              {"x": 300, "y": 80},
              {"x": 100, "y": 80}
            ]
          },
          "inferText": "피부과 전문의 직접 시술",
          "inferConfidence": 0.9856,
          "type": "NORMAL",
          "lineBreak": false
        },
        {
          "valueType": "ALL",
          "boundingPoly": {
            "vertices": [
              {"x": 150, "y": 120},
              {"x": 400, "y": 120},
              {"x": 400, "y": 160},
              {"x": 150, "y": 160}
            ]
          },
          "inferText": "100% 만족 보장",
          "inferConfidence": 0.9923,
          "type": "NORMAL",
          "lineBreak": true
        }
      ]
    }
  ]
}
```

### 3.2 CLOVA OCR 연동 모듈

```python
import aiohttp
import base64
import time
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class OCRTextField:
    """OCR 인식 텍스트 필드"""
    text: str                          # 인식된 텍스트
    confidence: float                  # 신뢰도 (0.0 ~ 1.0)
    bounding_box: List[Dict[str, int]] # 좌표 (vertices)
    line_break: bool                   # 줄바꿈 여부
    field_type: str                    # NORMAL / TITLE 등

@dataclass
class OCRResult:
    """OCR 처리 결과"""
    success: bool
    image_id: str
    full_text: str                     # 전체 텍스트 (줄바꿈 반영)
    fields: List[OCRTextField]         # 개별 필드 목록
    avg_confidence: float              # 평균 신뢰도
    processing_time_ms: int
    error_message: Optional[str] = None

class NaverClovaOCR:
    """NAVER CLOVA OCR 연동 클래스"""
    
    def __init__(self, api_url: str, secret_key: str):
        self.api_url = api_url
        self.secret_key = secret_key
        self.min_confidence = 0.7  # 최소 신뢰도 임계값
        
    async def extract_text(self, image_path: str) -> OCRResult:
        """이미지에서 텍스트 추출"""
        
        start_time = time.time()
        
        # 1. 이미지 로드 및 Base64 인코딩
        image_data, image_format = await self._load_image(image_path)
        
        # 2. API 요청 페이로드 구성
        payload = {
            "version": "V2",
            "requestId": f"req-{int(time.time()*1000)}",
            "timestamp": int(time.time() * 1000),
            "lang": "ko",
            "images": [{
                "format": image_format,
                "name": "medical_ad",
                "data": image_data
            }],
            "enableTableDetection": False
        }
        
        # 3. API 호출
        headers = {
            "X-OCR-SECRET": self.secret_key,
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url, 
                json=payload, 
                headers=headers
            ) as response:
                result = await response.json()
        
        # 4. 응답 파싱
        processing_time = int((time.time() - start_time) * 1000)
        return self._parse_response(result, processing_time)
    
    async def _load_image(self, image_path: str) -> tuple[str, str]:
        """이미지 로드 및 Base64 인코딩"""
        import aiofiles
        
        # 확장자 추출
        ext = image_path.split('.')[-1].lower()
        format_map = {
            'jpg': 'jpg', 'jpeg': 'jpg', 
            'png': 'png', 'gif': 'gif',
            'bmp': 'bmp', 'tiff': 'tiff', 'tif': 'tiff',
            'webp': 'webp'
        }
        image_format = format_map.get(ext, 'jpg')
        
        # Base64 인코딩
        async with aiofiles.open(image_path, 'rb') as f:
            image_bytes = await f.read()
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        
        return image_data, image_format
    
    def _parse_response(self, response: dict, processing_time: int) -> OCRResult:
        """API 응답 파싱"""
        
        if not response.get('images'):
            return OCRResult(
                success=False,
                image_id="",
                full_text="",
                fields=[],
                avg_confidence=0.0,
                processing_time_ms=processing_time,
                error_message="No images in response"
            )
        
        image_result = response['images'][0]
        
        if image_result.get('inferResult') != 'SUCCESS':
            return OCRResult(
                success=False,
                image_id=image_result.get('uid', ''),
                full_text="",
                fields=[],
                avg_confidence=0.0,
                processing_time_ms=processing_time,
                error_message=image_result.get('message', 'OCR failed')
            )
        
        # 필드 파싱
        fields = []
        text_lines = []
        confidences = []
        
        for field in image_result.get('fields', []):
            confidence = field.get('inferConfidence', 0.0)
            
            # 신뢰도 필터링
            if confidence < self.min_confidence:
                continue
                
            text = field.get('inferText', '')
            
            ocr_field = OCRTextField(
                text=text,
                confidence=confidence,
                bounding_box=field.get('boundingPoly', {}).get('vertices', []),
                line_break=field.get('lineBreak', False),
                field_type=field.get('type', 'NORMAL')
            )
            fields.append(ocr_field)
            confidences.append(confidence)
            
            # 전체 텍스트 구성
            text_lines.append(text)
            if field.get('lineBreak'):
                text_lines.append('\n')
        
        full_text = ' '.join(text_lines).replace(' \n ', '\n').strip()
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(
            success=True,
            image_id=image_result.get('uid', ''),
            full_text=full_text,
            fields=fields,
            avg_confidence=avg_confidence,
            processing_time_ms=processing_time
        )
    
    def get_violation_highlights(
        self, 
        ocr_result: OCRResult, 
        violation_texts: List[str]
    ) -> List[Dict]:
        """위반 문구의 이미지 좌표 반환 (하이라이트용)"""
        
        highlights = []
        
        for field in ocr_result.fields:
            for violation in violation_texts:
                if violation in field.text or field.text in violation:
                    highlights.append({
                        "text": field.text,
                        "matched_violation": violation,
                        "bounding_box": field.bounding_box,
                        "confidence": field.confidence
                    })
        
        return highlights
```

### 3.3 이미지 전처리 모듈

```python
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import io

class ImagePreprocessor:
    """OCR 정확도 향상을 위한 이미지 전처리"""
    
    # CLOVA OCR 최적 해상도
    MAX_DIMENSION = 2048
    MIN_DIMENSION = 100
    
    def __init__(self):
        self.target_dpi = 300
        
    async def preprocess(self, image_path: str) -> Tuple[bytes, dict]:
        """이미지 전처리 파이프라인"""
        
        # 이미지 로드
        image = cv2.imread(image_path)
        original_shape = image.shape[:2]
        
        processing_log = {
            "original_size": original_shape,
            "steps": []
        }
        
        # 1. 해상도 조정
        image, resized = self._resize_image(image)
        if resized:
            processing_log["steps"].append("resize")
            processing_log["resized_to"] = image.shape[:2]
        
        # 2. 그레이스케일 변환 (선택적)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 3. 노이즈 제거
        image = self._denoise(image)
        processing_log["steps"].append("denoise")
        
        # 4. 기울기 보정
        image, angle = self._deskew(image)
        if abs(angle) > 0.5:
            processing_log["steps"].append(f"deskew ({angle:.1f}°)")
        
        # 5. 대비 향상
        image = self._enhance_contrast(image)
        processing_log["steps"].append("contrast_enhance")
        
        # 6. 바이트로 변환
        _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])
        image_bytes = buffer.tobytes()
        
        processing_log["final_size"] = image.shape[:2]
        
        return image_bytes, processing_log
    
    def _resize_image(self, image: np.ndarray) -> Tuple[np.ndarray, bool]:
        """CLOVA OCR 최적 해상도로 조정"""
        
        height, width = image.shape[:2]
        max_dim = max(height, width)
        
        if max_dim <= self.MAX_DIMENSION and min(height, width) >= self.MIN_DIMENSION:
            return image, False
        
        if max_dim > self.MAX_DIMENSION:
            scale = self.MAX_DIMENSION / max_dim
        else:
            scale = self.MIN_DIMENSION / min(height, width)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        return resized, True
    
    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """노이즈 제거"""
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    
    def _deskew(self, image: np.ndarray) -> Tuple[np.ndarray, float]:
        """기울기 보정"""
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is None:
            return image, 0.0
        
        # 각도 계산
        angles = []
        for line in lines[:20]:  # 상위 20개만
            rho, theta = line[0]
            angle = (theta * 180 / np.pi) - 90
            if -45 < angle < 45:
                angles.append(angle)
        
        if not angles:
            return image, 0.0
        
        median_angle = np.median(angles)
        
        if abs(median_angle) < 0.5:
            return image, median_angle
        
        # 회전 보정
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated, median_angle
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """대비 향상 (CLAHE)"""
        
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
```

---

## 4. LangGraph 워크플로우 설계

### 4.1 State Schema 정의

```python
from typing import TypedDict, List, Optional, Literal
from datetime import datetime
from dataclasses import dataclass

class ImageReviewState(TypedDict):
    # ===== 입력 데이터 =====
    review_id: str                       # 심의 고유 ID
    image_id: str                        # 이미지 고유 ID
    image_path: str                      # 이미지 파일 경로
    image_url: Optional[str]             # 이미지 URL (S3 등)
    ad_metadata: dict                    # 광고 메타데이터
    
    # ===== OCR 처리 결과 =====
    ocr_success: bool                    # OCR 성공 여부
    ocr_full_text: str                   # OCR 추출 전체 텍스트
    ocr_fields: List[dict]               # OCR 필드별 상세 정보
    ocr_confidence: float                # OCR 평균 신뢰도
    ocr_processing_time: int             # OCR 처리 시간 (ms)
    
    # ===== 분석 중간 산출물 =====
    extracted_claims: List[str]          # 추출된 핵심 주장
    claim_categories: List[dict]         # 주장별 위반 유형 분류
    relevant_laws: List[dict]            # 검색된 관련 법령
    relevant_guidelines: List[dict]      # 검색된 심의 기준
    relevant_precedents: List[dict]      # 검색된 유사 판례
    
    # ===== 심의 결과 =====
    draft_verdict: str                   # 1차 심의 의견
    draft_reasoning: str                 # 1차 추론 과정
    critique_feedback: str               # 검증 피드백
    
    # ===== 최종 결과 =====
    final_verdict: Literal["허용", "조건부허용", "불허", "보류"]
    violation_details: List[dict]        # 위반 상세 (텍스트 + 좌표)
    violation_highlights: List[dict]     # 이미지 하이라이트 좌표
    final_reasoning: str                 # 최종 판단 근거
    modification_suggestions: List[str]  # 수정 제안
    confidence_score: float              # 확신도 (0.0 ~ 1.0)
    
    # ===== 워크플로우 제어 =====
    iteration_count: int                 # 루프 반복 횟수
    max_iterations: int                  # 최대 반복 횟수 (기본: 3)
    requires_human_review: bool          # 인간 검토 필요 여부
    human_feedback: Optional[str]        # 인간 심의관 피드백
    
    # ===== 감사 로그 =====
    processing_log: List[dict]           # 처리 단계별 로그
    created_at: datetime
    updated_at: datetime
```

### 4.2 워크플로우 그래프 구조

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LangGraph Image Review Workflow                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [START]                                                                │
│     │                                                                   │
│     ▼                                                                   │
│  [1. 이미지 전처리 노드]                                                │
│     │  - 해상도 조정                                                    │
│     │  - 노이즈 제거                                                    │
│     │  - 기울기 보정                                                    │
│     ▼                                                                   │
│  [2. CLOVA OCR 호출 노드]                                               │
│     │  - API 호출                                                       │
│     │  - 텍스트 + 좌표 추출                                             │
│     │                                                                   │
│     ├──────────────────────┐                                           │
│     ▼                      ▼                                            │
│  [OCR 성공]            [OCR 실패]                                       │
│     │                      │                                            │
│     │                      ▼                                            │
│     │              [에러 처리 노드]                                     │
│     │                      │                                            │
│     │                      ▼                                            │
│     │                 [보류 판정] ────────────────────────► [END]       │
│     │                                                                   │
│     ▼                                                                   │
│  [3. 텍스트 후처리 노드]                                                │
│     │  - 텍스트 정규화                                                  │
│     │  - 레이아웃 분석                                                  │
│     ▼                                                                   │
│  [4. 청구항 추출 노드]                                                  │
│     │  - 심의 대상 문구 추출                                            │
│     │  - 위반 유형 분류                                                 │
│     ▼                                                                   │
│  ┌──────────────────────────────────────────────────────┐              │
│  │           [5. 병렬 검색 노드 (Fan-out)]               │              │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │              │
│  │  │ 법령 검색   │  │ 가이드라인  │  │ 판례 검색   │  │              │
│  │  │ (RAG)      │  │ 검색 (RAG) │  │ (RAG)      │  │              │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │              │
│  └──────────────────────────────────────────────────────┘              │
│                           │                                             │
│                           ▼ (Fan-in)                                    │
│              [6. 심의 초안 작성 노드 (Generator)]                       │
│                           │                                             │
│                           ▼                                             │
│              [7. 적대적 검증 노드 (Evaluator)]                          │
│                           │                                             │
│              ┌────────────┴────────────┐                               │
│              ▼                         ▼                                │
│        [검증 통과]              [검증 실패]                             │
│              │                         │                                │
│              │              ┌──────────┴──────────┐                    │
│              │              ▼                     ▼                     │
│              │      [iteration < 3]        [iteration >= 3]            │
│              │              │                     │                     │
│              │              └──► [6]으로 돌아감   │                     │
│              │                                    │                     │
│              └────────────────┬───────────────────┘                    │
│                               ▼                                         │
│              [8. 휴먼인더루프 결정 노드]                                │
│                               │                                         │
│              ┌────────────────┴────────────────┐                       │
│              ▼                                 ▼                        │
│        [자동 완료]                    [인간 검토 필요]                  │
│              │                                 │                        │
│              │                        [인터럽트: 대기]                  │
│              │                                 │                        │
│              │                        [인간 피드백 수신]                │
│              │                                 │                        │
│              └────────────────┬────────────────┘                       │
│                               ▼                                         │
│              [9. 위반 하이라이트 생성 노드]                             │
│                               │                                         │
│                               ▼                                         │
│              [10. 최종 결과 출력 노드]                                  │
│                               │                                         │
│                               ▼                                         │
│                            [END]                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 노드 구현 상세

#### Node 1: 이미지 전처리

```python
from langgraph.graph import StateGraph
from typing import Dict, Any

async def preprocess_image_node(state: ImageReviewState) -> ImageReviewState:
    """이미지 전처리 노드"""
    
    preprocessor = ImagePreprocessor()
    
    try:
        processed_bytes, processing_log = await preprocessor.preprocess(
            state["image_path"]
        )
        
        # 전처리된 이미지 임시 저장
        processed_path = f"/tmp/processed_{state['image_id']}.jpg"
        with open(processed_path, 'wb') as f:
            f.write(processed_bytes)
        
        state["image_path"] = processed_path
        state["processing_log"].append({
            "step": "image_preprocessing",
            "status": "success",
            "details": processing_log,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        state["processing_log"].append({
            "step": "image_preprocessing",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    return state
```

#### Node 2: CLOVA OCR 호출

```python
async def ocr_extraction_node(state: ImageReviewState) -> ImageReviewState:
    """CLOVA OCR 텍스트 추출 노드"""
    
    ocr_client = NaverClovaOCR(
        api_url=settings.CLOVA_OCR_API_URL,
        secret_key=settings.CLOVA_OCR_SECRET_KEY
    )
    
    try:
        ocr_result = await ocr_client.extract_text(state["image_path"])
        
        state["ocr_success"] = ocr_result.success
        state["ocr_full_text"] = ocr_result.full_text
        state["ocr_fields"] = [
            {
                "text": f.text,
                "confidence": f.confidence,
                "bounding_box": f.bounding_box,
                "line_break": f.line_break
            }
            for f in ocr_result.fields
        ]
        state["ocr_confidence"] = ocr_result.avg_confidence
        state["ocr_processing_time"] = ocr_result.processing_time_ms
        
        state["processing_log"].append({
            "step": "ocr_extraction",
            "status": "success" if ocr_result.success else "failed",
            "text_length": len(ocr_result.full_text),
            "field_count": len(ocr_result.fields),
            "avg_confidence": ocr_result.avg_confidence,
            "processing_time_ms": ocr_result.processing_time_ms,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        state["ocr_success"] = False
        state["ocr_full_text"] = ""
        state["processing_log"].append({
            "step": "ocr_extraction",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    return state
```

#### Node 3: 텍스트 후처리

```python
async def text_postprocess_node(state: ImageReviewState) -> ImageReviewState:
    """OCR 텍스트 후처리 노드"""
    
    if not state["ocr_success"]:
        return state
    
    raw_text = state["ocr_full_text"]
    
    # 1. 텍스트 정규화
    normalized_text = normalize_korean_text(raw_text)
    
    # 2. 레이아웃 분석 (제목/본문/주석 구분)
    layout_analysis = analyze_layout(state["ocr_fields"])
    
    # 3. 저신뢰도 필드 필터링 (이미 OCR에서 처리됨)
    
    state["ocr_full_text"] = normalized_text
    state["ad_metadata"]["layout_analysis"] = layout_analysis
    
    state["processing_log"].append({
        "step": "text_postprocessing",
        "status": "success",
        "original_length": len(raw_text),
        "normalized_length": len(normalized_text),
        "timestamp": datetime.now().isoformat()
    })
    
    return state


def normalize_korean_text(text: str) -> str:
    """한국어 텍스트 정규화"""
    import re
    
    # 연속 공백 제거
    text = re.sub(r'\s+', ' ', text)
    
    # OCR 오인식 패턴 수정
    corrections = {
        '0': ['O', 'o'],  # 숫자 0과 알파벳 O
        '1': ['l', 'I'],  # 숫자 1과 알파벳 l, I
        '%': ['96'],      # % 기호 오인식
    }
    
    # 의료 용어 특수 처리
    medical_terms = {
        '쩨거': '제거',
        '피부과': '피부과',
        '성헝': '성형',
    }
    
    for correct, wrongs in medical_terms.items():
        if isinstance(wrongs, str):
            text = text.replace(wrongs, correct)
    
    return text.strip()


def analyze_layout(ocr_fields: List[dict]) -> dict:
    """레이아웃 분석 (위치 기반)"""
    
    if not ocr_fields:
        return {"title": "", "body": "", "footnote": ""}
    
    # Y 좌표 기준 정렬
    sorted_fields = sorted(
        ocr_fields, 
        key=lambda f: f['bounding_box'][0]['y'] if f['bounding_box'] else 0
    )
    
    total_fields = len(sorted_fields)
    
    # 상단 20%: 제목, 중간 60%: 본문, 하단 20%: 주석
    title_idx = int(total_fields * 0.2)
    footnote_idx = int(total_fields * 0.8)
    
    title_text = ' '.join([f['text'] for f in sorted_fields[:title_idx]])
    body_text = ' '.join([f['text'] for f in sorted_fields[title_idx:footnote_idx]])
    footnote_text = ' '.join([f['text'] for f in sorted_fields[footnote_idx:]])
    
    return {
        "title": title_text,
        "body": body_text,
        "footnote": footnote_text
    }
```

#### Node 4: 청구항 추출

```python
async def claim_extraction_node(state: ImageReviewState) -> ImageReviewState:
    """심의 대상 청구항 추출 노드"""
    
    if not state["ocr_success"] or not state["ocr_full_text"]:
        state["extracted_claims"] = []
        return state
    
    llm = get_llm_client()
    
    prompt = f"""당신은 의료광고 심의 전문가입니다.
아래 광고 텍스트에서 법적 심의가 필요한 개별 주장(청구항)들을 추출하세요.

[추출 기준]
- 치료 효과나 결과를 언급하는 문구
- 최상급 표현 (최고, 유일, 최초 등)
- 가격/비용 관련 문구
- 의료진 자격/경력 관련 문구
- 비교/우위 주장
- 통계/연구 인용
- 환자 경험담으로 보이는 문구

[광고 텍스트]
{state["ocr_full_text"]}

[출력 형식]
각 청구항을 JSON 배열로 출력하세요:
[
  {{"claim": "추출된 문구", "category": "위반유형코드", "reason": "추출 이유"}}
]

위반유형코드:
- V1: 신의료기술 미평가
- V2: 치료 경험담
- V3: 거짓/과장 광고
- V4: 비교/비방 광고
- V5: 객관적 근거 부재
- V6: 최상급 표현
- V0: 기타/확인 필요
"""

    response = await llm.generate(prompt)
    claims_data = parse_json_response(response)
    
    state["extracted_claims"] = [c["claim"] for c in claims_data]
    state["claim_categories"] = claims_data
    
    state["processing_log"].append({
        "step": "claim_extraction",
        "status": "success",
        "claim_count": len(claims_data),
        "timestamp": datetime.now().isoformat()
    })
    
    return state
```

#### Node 9: 위반 하이라이트 생성

```python
async def generate_highlights_node(state: ImageReviewState) -> ImageReviewState:
    """위반 문구 이미지 하이라이트 좌표 생성 노드"""
    
    if state["final_verdict"] == "허용":
        state["violation_highlights"] = []
        return state
    
    # 위반으로 판정된 텍스트 목록
    violation_texts = [v["text"] for v in state["violation_details"]]
    
    # OCR 필드에서 위반 텍스트의 좌표 매칭
    highlights = []
    
    for field in state["ocr_fields"]:
        field_text = field["text"]
        
        for violation in violation_texts:
            # 부분 매칭 허용 (위반 문구가 필드에 포함되거나, 필드가 위반 문구에 포함)
            if violation in field_text or field_text in violation:
                highlights.append({
                    "violation_text": violation,
                    "matched_field_text": field_text,
                    "bounding_box": field["bounding_box"],
                    "confidence": field["confidence"],
                    "highlight_color": get_violation_color(violation)
                })
    
    state["violation_highlights"] = highlights
    
    state["processing_log"].append({
        "step": "highlight_generation",
        "status": "success",
        "highlight_count": len(highlights),
        "timestamp": datetime.now().isoformat()
    })
    
    return state


def get_violation_color(violation_text: str) -> str:
    """위반 심각도에 따른 하이라이트 색상"""
    
    # 심각도 높음: 빨강
    severe_keywords = ["100%", "완치", "보장", "최고", "유일"]
    if any(kw in violation_text for kw in severe_keywords):
        return "#FF0000"
    
    # 중간: 주황
    moderate_keywords = ["전문의", "경험", "후기"]
    if any(kw in violation_text for kw in moderate_keywords):
        return "#FFA500"
    
    # 경미: 노랑
    return "#FFFF00"
```

### 4.4 그래프 빌더

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

def build_image_review_graph() -> StateGraph:
    """이미지 심의 워크플로우 그래프 생성"""
    
    # 그래프 초기화
    workflow = StateGraph(ImageReviewState)
    
    # ===== 노드 추가 =====
    workflow.add_node("preprocess_image", preprocess_image_node)
    workflow.add_node("extract_ocr", ocr_extraction_node)
    workflow.add_node("postprocess_text", text_postprocess_node)
    workflow.add_node("extract_claims", claim_extraction_node)
    workflow.add_node("search_laws", search_laws_node)
    workflow.add_node("search_guidelines", search_guidelines_node)
    workflow.add_node("search_precedents", search_precedents_node)
    workflow.add_node("merge_search_results", merge_search_results_node)
    workflow.add_node("generate_draft", generate_draft_node)
    workflow.add_node("evaluate_draft", evaluate_draft_node)
    workflow.add_node("human_review_decision", human_review_decision_node)
    workflow.add_node("generate_highlights", generate_highlights_node)
    workflow.add_node("output_result", output_result_node)
    workflow.add_node("handle_ocr_error", handle_ocr_error_node)
    
    # ===== 엣지 정의 =====
    
    # 시작 -> 이미지 전처리
    workflow.set_entry_point("preprocess_image")
    
    # 이미지 전처리 -> OCR
    workflow.add_edge("preprocess_image", "extract_ocr")
    
    # OCR 결과에 따른 분기
    workflow.add_conditional_edges(
        "extract_ocr",
        lambda state: "success" if state["ocr_success"] else "error",
        {
            "success": "postprocess_text",
            "error": "handle_ocr_error"
        }
    )
    
    # OCR 에러 처리 -> 종료
    workflow.add_edge("handle_ocr_error", END)
    
    # 텍스트 후처리 -> 청구항 추출
    workflow.add_edge("postprocess_text", "extract_claims")
    
    # 청구항 추출 -> 병렬 검색 (Fan-out)
    workflow.add_edge("extract_claims", "search_laws")
    workflow.add_edge("extract_claims", "search_guidelines")
    workflow.add_edge("extract_claims", "search_precedents")
    
    # 병렬 검색 결과 병합 (Fan-in)
    workflow.add_edge("search_laws", "merge_search_results")
    workflow.add_edge("search_guidelines", "merge_search_results")
    workflow.add_edge("search_precedents", "merge_search_results")
    
    # 검색 결과 병합 -> 초안 생성
    workflow.add_edge("merge_search_results", "generate_draft")
    
    # 초안 생성 -> 평가
    workflow.add_edge("generate_draft", "evaluate_draft")
    
    # 평가 결과에 따른 분기 (루프 핵심)
    workflow.add_conditional_edges(
        "evaluate_draft",
        evaluation_router,
        {
            "pass": "human_review_decision",
            "retry": "generate_draft",
            "max_iterations": "human_review_decision"
        }
    )
    
    # 휴먼인더루프 결정
    workflow.add_conditional_edges(
        "human_review_decision",
        lambda state: "human" if state["requires_human_review"] else "auto",
        {
            "human": "generate_highlights",  # 인간 검토 후 진행
            "auto": "generate_highlights"
        }
    )
    
    # 하이라이트 생성 -> 최종 출력
    workflow.add_edge("generate_highlights", "output_result")
    
    # 최종 출력 -> 종료
    workflow.add_edge("output_result", END)
    
    return workflow


def evaluation_router(state: ImageReviewState) -> str:
    """평가 결과에 따른 라우팅"""
    
    if state["critique_feedback"] == "PASS":
        return "pass"
    
    if state["iteration_count"] >= state["max_iterations"]:
        return "max_iterations"
    
    return "retry"
```

---

## 5. RAG 시스템 설계

### 5.1 지식 베이스 구성

#### 5.1.1 데이터 소스

| 소스 | 유형 | 갱신 주기 | 우선순위 |
|------|------|-----------|----------|
| 의료법 조문 | 법률 | 개정 시 즉시 | 1 (최고) |
| 의료법 시행령 | 시행령 | 개정 시 즉시 | 1 |
| 심의 가이드라인 (의협/치협/한의협) | 가이드라인 | 분기별 | 2 |
| 대법원/헌재 판례 | 판례 | 월별 | 2 |
| 보건복지부 유권해석 | 해석례 | 발생 시 | 3 |
| 과거 심의 사례 (이미지 포함) | 내부 데이터 | 실시간 | 3 |

### 5.2 하이브리드 검색

```python
class HybridSearchEngine:
    """하이브리드 검색 엔진 (BM25 + Dense Vector)"""
    
    def __init__(self, vector_db, bm25_index):
        self.vector_db = vector_db
        self.bm25_index = bm25_index
        self.embedder = LegalEmbedder()
        
    async def search(
        self, 
        query: str, 
        top_k: int = 10,
        bm25_weight: float = 0.4,
        dense_weight: float = 0.6
    ) -> List[SearchResult]:
        """하이브리드 검색 수행"""
        
        # 1. BM25 검색 (키워드)
        bm25_results = self.bm25_index.search(query, top_k=top_k*2)
        
        # 2. Dense 검색 (시맨틱)
        query_embedding = self.embedder.embed_query(query)
        dense_results = await self.vector_db.search(
            query_embedding, 
            top_k=top_k*2
        )
        
        # 3. RRF 융합
        fused_results = self._rrf_fusion(
            bm25_results, 
            dense_results,
            bm25_weight,
            dense_weight
        )
        
        return fused_results[:top_k]
    
    def _rrf_fusion(
        self, 
        bm25_results, 
        dense_results,
        bm25_weight: float,
        dense_weight: float,
        k: int = 60
    ) -> List[SearchResult]:
        """Reciprocal Rank Fusion"""
        
        scores = {}
        
        # BM25 점수 계산
        for rank, result in enumerate(bm25_results):
            doc_id = result.doc_id
            scores[doc_id] = scores.get(doc_id, 0) + bm25_weight / (k + rank + 1)
        
        # Dense 점수 계산
        for rank, result in enumerate(dense_results):
            doc_id = result.doc_id
            scores[doc_id] = scores.get(doc_id, 0) + dense_weight / (k + rank + 1)
        
        # 정렬 및 반환
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [SearchResult(doc_id=doc_id, score=score) for doc_id, score in sorted_docs]
```

---

## 6. API 명세

### 6.1 이미지 심의 요청 API

#### POST /api/v1/review/image

**Request (multipart/form-data):**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| image | File | O | 광고 이미지 파일 |
| ad_id | String | X | 광고 고유 ID (없으면 자동 생성) |
| hospital_name | String | X | 의료기관명 |
| priority | String | X | 우선순위 (urgent/normal/low) |
| callback_url | String | X | 결과 알림 Webhook URL |

**Request Example (cURL):**
```bash
curl -X POST "https://api.medadvision.ai/api/v1/review/image" \
  -H "Authorization: Bearer {API_KEY}" \
  -F "image=@medical_ad_001.jpg" \
  -F "ad_id=AD-2026-00001" \
  -F "hospital_name=OO의원" \
  -F "priority=normal"
```

**Response:**
```json
{
  "review_id": "REV-2026-00001",
  "status": "processing",
  "image_id": "IMG-2026-00001",
  "estimated_completion": "2026-01-07T10:05:00Z",
  "polling_url": "/api/v1/review/REV-2026-00001",
  "message": "이미지 심의가 시작되었습니다."
}
```

### 6.2 심의 결과 조회 API

#### GET /api/v1/review/{review_id}

**Response:**
```json
{
  "review_id": "REV-2026-00001",
  "status": "completed",
  "image_id": "IMG-2026-00001",
  "image_url": "https://storage.medadvision.ai/images/IMG-2026-00001.jpg",
  
  "ocr_result": {
    "success": true,
    "full_text": "피부과 전문의 직접 시술\n100% 만족 보장\n부작용 걱정 NO",
    "confidence": 0.9634,
    "processing_time_ms": 1234
  },
  
  "review_result": {
    "verdict": "불허",
    "confidence_score": 0.92,
    
    "violations": [
      {
        "claim": "100% 만족 보장",
        "article": "제56조 제2항 제3호",
        "reason": "치료 효과 보장은 의학적으로 불가능한 과장 표현",
        "guideline_ref": "심의기준 제4조 1항",
        "bounding_box": [
          {"x": 150, "y": 120},
          {"x": 400, "y": 120},
          {"x": 400, "y": 160},
          {"x": 150, "y": 160}
        ],
        "highlight_color": "#FF0000"
      },
      {
        "claim": "부작용 걱정 NO",
        "article": "제56조 제2항 제3호",
        "reason": "부작용이 없다는 주장은 의학적 사실에 반함",
        "guideline_ref": "심의기준 제4조 2항",
        "bounding_box": [
          {"x": 180, "y": 200},
          {"x": 380, "y": 200},
          {"x": 380, "y": 240},
          {"x": 180, "y": 240}
        ],
        "highlight_color": "#FF0000"
      }
    ],
    
    "reasoning": "본 광고 이미지에서 2가지 위반 사항이 발견되었습니다. '100% 만족 보장' 문구는 의료 행위의 결과를 보장하는 것으로, 의료법 제56조 제2항 제3호에서 금지하는 과장 광고에 해당합니다...",
    
    "suggestions": [
      "'100% 만족 보장' → '높은 만족도를 위해 노력합니다'로 수정",
      "'부작용 걱정 NO' → 삭제 또는 '부작용 최소화를 위해 노력합니다'로 수정"
    ]
  },
  
  "highlighted_image_url": "https://storage.medadvision.ai/highlighted/REV-2026-00001.jpg",
  
  "metadata": {
    "processing_time_ms": 4523,
    "iteration_count": 2,
    "human_reviewed": false,
    "created_at": "2026-01-07T10:00:00Z",
    "completed_at": "2026-01-07T10:04:23Z"
  }
}
```

### 6.3 하이라이트 이미지 API

#### GET /api/v1/review/{review_id}/highlighted-image

위반 문구가 표시된 이미지를 반환합니다.

**Response:** 이미지 파일 (JPEG/PNG)

**Query Parameters:**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| format | String | png | 출력 형식 (png/jpg) |
| opacity | Float | 0.3 | 하이라이트 투명도 |
| show_labels | Boolean | true | 위반 조항 라벨 표시 여부 |

### 6.4 배치 심의 API

#### POST /api/v1/review/batch

여러 이미지를 한 번에 심의 요청합니다.

**Request:**
```json
{
  "images": [
    {
      "image_url": "https://example.com/ad1.jpg",
      "ad_id": "AD-001"
    },
    {
      "image_url": "https://example.com/ad2.jpg",
      "ad_id": "AD-002"
    }
  ],
  "priority": "normal",
  "callback_url": "https://your-server.com/webhook"
}
```

**Response:**
```json
{
  "batch_id": "BATCH-2026-00001",
  "total_count": 2,
  "reviews": [
    {"review_id": "REV-2026-00001", "status": "queued"},
    {"review_id": "REV-2026-00002", "status": "queued"}
  ],
  "estimated_completion": "2026-01-07T10:15:00Z"
}
```

---

## 7. 위반 하이라이트 시각화

### 7.1 하이라이트 이미지 생성

```python
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict
import io

class ViolationHighlighter:
    """위반 문구 이미지 하이라이트 생성기"""
    
    def __init__(self):
        self.font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        self.default_opacity = 0.3
        
    def generate_highlighted_image(
        self,
        original_image_path: str,
        violations: List[Dict],
        output_path: str,
        show_labels: bool = True
    ) -> str:
        """위반 문구가 하이라이트된 이미지 생성"""
        
        # 원본 이미지 로드
        img = Image.open(original_image_path).convert("RGBA")
        
        # 하이라이트 오버레이 생성
        overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        for violation in violations:
            bbox = violation["bounding_box"]
            color = self._parse_color(violation.get("highlight_color", "#FF0000"))
            
            # 바운딩 박스 좌표
            vertices = bbox
            polygon = [(v["x"], v["y"]) for v in vertices]
            
            # 반투명 하이라이트
            fill_color = (*color, int(255 * self.default_opacity))
            draw.polygon(polygon, fill=fill_color, outline=color)
            
            # 라벨 표시
            if show_labels and "article" in violation:
                self._draw_label(draw, polygon, violation["article"])
        
        # 오버레이 합성
        result = Image.alpha_composite(img, overlay)
        
        # 저장
        result.convert("RGB").save(output_path, "JPEG", quality=95)
        
        return output_path
    
    def _parse_color(self, hex_color: str) -> tuple:
        """HEX 색상을 RGB 튜플로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _draw_label(self, draw, polygon, label_text):
        """위반 조항 라벨 그리기"""
        
        # 라벨 위치 (바운딩 박스 상단)
        min_x = min(p[0] for p in polygon)
        min_y = min(p[1] for p in polygon)
        
        try:
            font = ImageFont.truetype(self.font_path, 14)
        except:
            font = ImageFont.load_default()
        
        # 라벨 배경
        text_bbox = draw.textbbox((min_x, min_y - 20), label_text, font=font)
        draw.rectangle(text_bbox, fill=(0, 0, 0, 200))
        
        # 라벨 텍스트
        draw.text((min_x, min_y - 20), label_text, font=font, fill=(255, 255, 255))
```

### 7.2 프론트엔드 이미지 뷰어 컴포넌트

```typescript
// React 컴포넌트: 위반 하이라이트 이미지 뷰어

import React, { useState, useRef } from 'react';

interface Violation {
  claim: string;
  article: string;
  reason: string;
  bounding_box: { x: number; y: number }[];
  highlight_color: string;
}

interface ImageReviewViewerProps {
  originalImageUrl: string;
  highlightedImageUrl: string;
  violations: Violation[];
}

const ImageReviewViewer: React.FC<ImageReviewViewerProps> = ({
  originalImageUrl,
  highlightedImageUrl,
  violations
}) => {
  const [showHighlights, setShowHighlights] = useState(true);
  const [selectedViolation, setSelectedViolation] = useState<Violation | null>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  return (
    <div className="image-review-viewer">
      {/* 이미지 토글 */}
      <div className="viewer-controls">
        <button 
          onClick={() => setShowHighlights(!showHighlights)}
          className={`toggle-btn ${showHighlights ? 'active' : ''}`}
        >
          {showHighlights ? '원본 보기' : '하이라이트 보기'}
        </button>
      </div>

      {/* 이미지 표시 영역 */}
      <div className="image-container">
        <img
          ref={imageRef}
          src={showHighlights ? highlightedImageUrl : originalImageUrl}
          alt="의료광고 이미지"
          className="review-image"
        />
        
        {/* 인터랙티브 오버레이 (하이라이트 모드에서만) */}
        {showHighlights && violations.map((violation, idx) => (
          <div
            key={idx}
            className="violation-overlay"
            style={getOverlayStyle(violation.bounding_box, imageRef.current)}
            onClick={() => setSelectedViolation(violation)}
            onMouseEnter={() => setSelectedViolation(violation)}
          />
        ))}
      </div>

      {/* 선택된 위반 상세 정보 */}
      {selectedViolation && (
        <div className="violation-detail-panel">
          <h4>위반 상세</h4>
          <p><strong>위반 문구:</strong> {selectedViolation.claim}</p>
          <p><strong>위반 조항:</strong> {selectedViolation.article}</p>
          <p><strong>사유:</strong> {selectedViolation.reason}</p>
        </div>
      )}

      {/* 전체 위반 목록 */}
      <div className="violations-list">
        <h4>발견된 위반 사항 ({violations.length}건)</h4>
        {violations.map((v, idx) => (
          <div 
            key={idx} 
            className="violation-item"
            onClick={() => setSelectedViolation(v)}
          >
            <span 
              className="violation-indicator"
              style={{ backgroundColor: v.highlight_color }}
            />
            <span className="violation-claim">{v.claim}</span>
            <span className="violation-article">{v.article}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

function getOverlayStyle(bbox: { x: number; y: number }[], imageEl: HTMLImageElement | null) {
  if (!imageEl || !bbox.length) return {};
  
  const scaleX = imageEl.clientWidth / imageEl.naturalWidth;
  const scaleY = imageEl.clientHeight / imageEl.naturalHeight;
  
  const minX = Math.min(...bbox.map(p => p.x)) * scaleX;
  const minY = Math.min(...bbox.map(p => p.y)) * scaleY;
  const maxX = Math.max(...bbox.map(p => p.x)) * scaleX;
  const maxY = Math.max(...bbox.map(p => p.y)) * scaleY;
  
  return {
    position: 'absolute',
    left: `${minX}px`,
    top: `${minY}px`,
    width: `${maxX - minX}px`,
    height: `${maxY - minY}px`,
    cursor: 'pointer',
  };
}

export default ImageReviewViewer;
```

---

## 8. 프롬프트 엔지니어링

### 8.1 OCR 텍스트 기반 심의 시스템 프롬프트

```
[시스템 역할]
당신은 대한민국 최고의 의료광고 심의 전문가입니다.
광고 이미지에서 OCR로 추출된 텍스트를 분석하여 의료법 위반 여부를 판단합니다.

[중요 참고사항]
- 입력 텍스트는 OCR로 추출되었으므로 일부 오인식이 있을 수 있습니다
- 명확하지 않은 텍스트는 보수적으로 판단하세요
- 이미지 광고 특성상 짧은 문구가 많으므로, 문맥 추론이 중요합니다

[핵심 원칙]
1. 모든 판단은 반드시 법적 근거에 기반해야 합니다
2. OCR 신뢰도가 낮은 텍스트(70% 미만)는 판단에서 제외합니다
3. 불확실한 경우 "보류" 판정하고 인간 심의관에게 위임합니다
4. 광고주에게 유리한 해석 가능성도 반드시 검토합니다

[출력 형식]
1. 위반 여부: [허용/조건부허용/불허/보류]
2. 위반 문구: [정확히 인용]
3. 위반 조항: [의료법 제X조 제X항 제X호]
4. 위반 사유: [구체적 설명]
5. 판단 근거: [인용한 법령/가이드라인/판례]
6. 수정 제안: [허용 가능한 대안 표현]
7. 확신도: [0.0 ~ 1.0]
```

### 8.2 이미지 광고 특화 Few-Shot 예시

```
[예시 1 - 불허: 효과 보장]
OCR 추출 텍스트: "피부과 전문의 직접 시술\n100% 만족 보장\n부작용 걱정 NO"

판정: 불허
위반 문구: "100% 만족 보장", "부작용 걱정 NO"
위반 조항: 의료법 제56조 제2항 제3호
사유: 
- "100% 만족 보장": 의료 행위의 결과 보장은 의학적으로 불가능
- "부작용 걱정 NO": 부작용 없음 주장은 사실에 반함
수정 제안:
- "100% 만족 보장" → "높은 만족도를 위해 최선을 다합니다"
- "부작용 걱정 NO" → 삭제 권장
확신도: 0.95

[예시 2 - 조건부허용: 자격 확인 필요]
OCR 추출 텍스트: "성형외과 전문의 OOO 원장\n코 성형 10,000건 달성"

판정: 조건부허용
조건: 전문의 자격 및 수술 건수 객관적 확인 필요
위반 가능 문구: "성형외과 전문의", "10,000건 달성"
확인 필요 사항:
- OOO 원장의 성형외과 전문의 자격증 소지 여부
- 수술 건수 10,000건의 객관적 증빙 자료
확신도: 0.75

[예시 3 - 허용]
OCR 추출 텍스트: "OO피부과\n레이저 토닝\n예약문의 02-XXX-XXXX"

판정: 허용
사유: 단순한 의료기관 정보 및 시술명 안내로, 효과 보장이나 최상급 표현 없음
확신도: 0.98
```

---

## 9. 평가 및 테스트

### 9.1 성능 평가 지표 (KPIs)

| 지표 | 정의 | 목표치 | 측정 방법 |
|------|------|--------|-----------|
| **OCR 정확도** | 문자 인식 정확률 (CER) | ≤ 2% | 골드 라벨 대비 |
| **법적 재현율** | 실제 위반 중 탐지된 비율 | ≥ 95% | 전문가 라벨 테스트셋 |
| **법적 정밀도** | 탐지된 위반 중 실제 위반 비율 | ≥ 90% | 전문가 검증 |
| **좌표 정확도** | 위반 문구 위치 정확도 (IoU) | ≥ 0.8 | 바운딩 박스 비교 |
| **할루시네이션 비율** | 존재하지 않는 법 조항 인용 비율 | ≤ 1% | 인용 검증 |
| **처리 시간** | 건당 평균 처리 시간 | ≤ 5분 | 시스템 로그 |

### 9.2 이미지 테스트 데이터셋 구성

```python
class ImageTestDataset:
    """이미지 기반 테스트 데이터셋"""
    
    CATEGORIES = {
        "banner_ads": "배너 광고 이미지",
        "poster_ads": "포스터 광고 이미지", 
        "card_news": "카드뉴스 이미지",
        "sns_images": "SNS 광고 이미지",
        "before_after": "시술 전후 사진",
    }
    
    def generate_test_cases(self) -> List[TestCase]:
        """테스트 케이스 생성"""
        
        test_cases = []
        
        # 1. 명확한 위반 케이스
        for category in self.CATEGORIES:
            test_cases.extend(
                self._generate_violation_cases(category, count=20)
            )
        
        # 2. 명확한 허용 케이스
        for category in self.CATEGORIES:
            test_cases.extend(
                self._generate_allowed_cases(category, count=20)
            )
        
        # 3. 경계선 케이스 (Borderline)
        test_cases.extend(
            self._generate_borderline_cases(count=50)
        )
        
        # 4. OCR 난이도 케이스
        test_cases.extend(
            self._generate_ocr_challenge_cases(count=30)
        )
        
        return test_cases
    
    def _generate_ocr_challenge_cases(self, count: int) -> List[TestCase]:
        """OCR 난이도 높은 케이스"""
        
        challenges = [
            "손글씨 스타일 폰트",
            "기울어진 텍스트",
            "배경과 텍스트 색상 유사",
            "작은 폰트 크기",
            "복잡한 배경 위 텍스트",
            "다양한 폰트 혼용",
        ]
        # ... 구현
```

---

## 10. 프로젝트 일정

### 10.1 마일스톤

| 단계 | 기간 | 산출물 | 담당 |
|------|------|--------|------|
| **Phase 1: 기반 구축** | 4주 | OCR 연동, RAG 시스템 | 백엔드팀 |
| **Phase 2: 핵심 개발** | 6주 | LangGraph 워크플로우, 하이라이트 | AI팀 |
| **Phase 3: 통합 및 테스트** | 4주 | API 통합, 성능 최적화 | 전체 |
| **Phase 4: 파일럿** | 4주 | 실환경 파일럿 운영 | 운영팀 |
| **Phase 5: 정식 출시** | 2주 | 프로덕션 배포 | DevOps |

### 10.2 상세 일정

```
                    월1    월2    월3    월4    월5
Phase 1 기반구축    ████████
  - CLOVA OCR 연동    ████
  - 이미지 전처리      ████
  - RAG 시스템 구축       ████
  - 임베딩 모델 준비       ████

Phase 2 핵심개발           ████████████
  - LangGraph 설계          ████
  - 노드 개발                   ████████
  - 루프 검증 구현                  ████
  - 하이라이트 생성                  ████

Phase 3 통합/테스트                    ████████
  - API 개발                          ████
  - 이미지 뷰어 개발                  ████
  - 성능 최적화                           ████
  - 통합 테스트                           ████

Phase 4 파일럿                                ████████
  - 파일럿 운영                               ████████
  - 피드백 수렴/개선                               ████

Phase 5 정식출시                                      ████
```

---

## 11. 향후 로드맵

### v2.0 (다음 버전) 계획

| 기능 | 설명 | 예상 시기 |
|------|------|-----------|
| 텍스트 기반 심의 | 블로그, SNS 텍스트, 웹사이트 | v2.0 |
| 동영상 광고 심의 | 프레임 추출 + OCR | v2.5 |
| 실시간 모니터링 | 크롤링 기반 자동 탐지 | v3.0 |
| 다국어 지원 | 영어, 중국어 광고 | v3.0 |

---

## 12. 부록

### A. NAVER CLOVA OCR 가격 정책 (참고)

| 플랜 | 월간 호출 수 | 가격 |
|------|-------------|------|
| Free | 100건 | 무료 |
| Standard | 10,000건 | 월 50,000원 |
| Enterprise | 무제한 | 협의 |

### B. 용어 정의

| 용어 | 정의 |
|------|------|
| **OCR** | Optical Character Recognition, 광학 문자 인식 |
| **CLOVA** | NAVER의 AI 플랫폼 |
| **바운딩 박스** | 텍스트 영역을 감싸는 사각형 좌표 |
| **IoU** | Intersection over Union, 영역 겹침 비율 |
| **CER** | Character Error Rate, 문자 오류율 |

### C. 참고 자료

1. NAVER CLOVA OCR API 문서: https://api.ncloud-docs.com/docs/ai-application-service-ocr
2. 의료법 - 국가법령정보센터
3. 대한의사협회 의료광고심의 가이드라인
4. LangGraph 공식 문서

---

**문서 끝**

*본 PRD는 프로젝트 진행에 따라 업데이트될 수 있습니다.*
*최종 수정일: 2026년 1월 7일*
*버전: 1.0 (이미지 기반 심의)*
