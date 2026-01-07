# MedAdReview Backend

Medical Advertisement Review AI Agent Backend

## Tech Stack

- **Framework**: FastAPI
- **Python**: 3.11+
- **Database**: PostgreSQL 16 + SQLAlchemy 2.x
- **Cache**: Redis 7
- **AI/Agent**: LangGraph + LangChain + Claude
- **Vector DB**: Pinecone
- **OCR**: NAVER CLOVA OCR

## Setup

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL 16
- Redis 7

### Installation

```bash
# Install dependencies
poetry install

# Copy environment file
cp .env.example .env

# Edit .env with your settings
```

### Running

```bash
# Development
poetry run uvicorn app.main:app --reload --port 8000

# Production
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config/              # Configuration
│   ├── api/v1/              # API endpoints
│   ├── core/                # Core modules (security, exceptions)
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── repositories/        # Data access
│   ├── agent/               # LangGraph agent
│   ├── ocr/                 # CLOVA OCR integration
│   ├── rag/                 # RAG system
│   └── utils/               # Utilities
├── tests/                   # Test files
├── scripts/                 # Utility scripts
├── alembic/                 # Database migrations
└── docker/                  # Docker files
```
