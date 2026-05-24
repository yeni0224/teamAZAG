# Project AZAG

TeamAZAG 프로젝트 관리용 DB, API, 프론트 시안, ERD 문서 모음입니다.

## 꼭 받을 브랜치

- 브랜치: `SeongHo`
- 저장소: `https://github.com/yeni0224/teamAZAG.git`
- 처음 받기:

```bash
git clone -b SeongHo https://github.com/yeni0224/teamAZAG.git
```

- 이미 받은 경우:

```bash
git fetch origin
git checkout SeongHo
git pull origin SeongHo
```

- 다른 브랜치 말고 `SeongHo`를 받으면 됩니다.

## 현재 남긴 것

- `app/`: FastAPI 백엔드 초안
- `frontend/`: 단일 HTML 프론트 화면
- `db/`: PostgreSQL 스키마, 시드, 검증 SQL
- `alembic/`: DB 마이그레이션 초안
- `docs/`: PRD, ERD, 테이블 정의서
- `tools/`: ERD 이미지 생성 스크립트
- `requirements.txt`: Python 의존성

## 정리한 것

- `opsradar_v2/`: 이전 백엔드 구조라 삭제
- `harness_framework-main/`: 템플릿/검토용 도구라 삭제
- `PROJECT_CONTEXT.md`: 템플릿 변환 메모라 삭제

## 실행 준비

- Python 3.11 이상 권장
- PostgreSQL 필요
- 기본 DB 주소:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/teamazag
```

- DB 주소를 바꿀 때:

```bash
set DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME
```

## 설치

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## DB 생성

```bash
createdb teamazag
psql -d teamazag -f db/schema.postgresql.sql
psql -d teamazag -f db/seed.postgresql.sql
psql -d teamazag -f db/verify.postgresql.sql
```

## 서버 실행

```bash
uvicorn app.main:app --reload
```

- API 문서: `http://127.0.0.1:8000/docs`
- 프론트 화면: `http://127.0.0.1:8000/front`
- 상태 확인: `http://127.0.0.1:8000/health`

## 주요 API

- `GET /api/dashboard`: 프론트 대시보드 데이터
- `GET /api/analysis/uploads`: 자료 업로드 목록
- `POST /api/analysis/uploads`: 자료 업로드 임시 등록
- `GET /api/todos`: TODO 목록
- `GET /api/issues`: 이슈 목록
- `GET /api/reports/default`: 보고서 초안
- `GET /api/knowledge`: 지식 전달 데이터
- `POST /api/assistant/chat`: AI Assistant 임시 응답
- `GET /projects`: DB 프로젝트 목록
- `GET /projects/{project_id}/dashboard`: 프로젝트 대시보드
- `GET /projects/{project_id}/todos`: 프로젝트 TODO
- `GET /projects/{project_id}/issues`: 프로젝트 이슈
- `GET /projects/{project_id}/documents`: 프로젝트 문서
- `GET /projects/{project_id}/handoff/latest`: 최신 인수인계

## 문서 위치

- `docs/PRD.md`: 제품 요구사항
- `docs/db-design-v2.md`: DB 설계 메모
- `docs/table-definition.md`: 테이블 정의
- `docs/project-azag-erdcloud-white.png`: 전체 ERD 이미지
- `docs/erd-split/`: 영역별 ERD
- `docs/teamazag-functions-v3.md`: 기능 정리

## 작업 기준

- 현재 기준 작업 브랜치는 `SeongHo`입니다.
- 새 작업 전에는 `git pull origin SeongHo`를 먼저 실행합니다.
- 커밋 전에는 `git status`로 변경 파일을 확인합니다.
- DB 관련 변경은 `db/`, `alembic/`, `app/models.py`를 같이 확인합니다.
- 화면 관련 변경은 `frontend/index.html`과 `/api/*` 응답을 같이 확인합니다.
