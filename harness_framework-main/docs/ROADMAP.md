# ROADMAP

## 목적
이 로드맵은 하네스 자체 개선과 AI 운영 인텔리전스 제품 개발을 분리해서 진행하기 위한 기준이다.

## 원칙
- 먼저 하네스 UX와 안전성을 안정화한다.
- 그 다음 제품 UX와 데이터 모델을 고정한다.
- 실제 외부 연동은 fixture 기반 extraction과 evaluation이 안정된 뒤 진행한다.

## Phase 0: Harness Baseline
상태: 일부 완료

목표:
- Codex runner 기본 실행
- dry-run
- result schema
- AC 실행
- docs guardrail 주입

남은 작업:
- 전체 테스트 기준 정리
- doctor/status UX
- git dirty 안전장치
- prompt stdin 전달
- 배포/이식 체크리스트 정리
- sanitized artifact 정책 확정

## Phase 0.5: Distribution Readiness
목표:
- 새 프로젝트에 하네스를 심는 절차 확정
- GitHub 공개/공유 기준 확정
- CI 최소 검증 명령 확정
- runs/log artifact 정책 확정

추천 step:
- `step0-bootstrap-guide`
- `step1-deployment-checklist`
- `step2-ci-workflow`
- `step3-artifact-policy`

## Phase 1: Product UX Foundation
목표:
- 사용자 여정 확정
- 핵심 화면 정의
- review workflow 정의
- insight item schema 확정

추천 step:
- `step0-user-journeys`
- `step1-core-screens`
- `step2-review-actions`
- `step3-empty-error-states`

Acceptance Criteria 예시:
```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

## Phase 2: Data Fixtures
목표:
- 샘플 운영 기록 fixture 작성
- SourceRecord normalization 구현
- 민감정보 마스킹 fixture 포함

추천 step:
- `step0-fixture-format`
- `step1-sample-records`
- `step2-normalizer`
- `step3-fixture-tests`

## Phase 3: Extraction Schema
목표:
- TODO/Risk/Blocked/Decision/Knowledge/Handover 추출 구조 구현
- source_refs와 confidence 포함
- deterministic baseline parser 또는 mock extractor 구현

추천 step:
- `step0-insight-schema`
- `step1-todo-extractor`
- `step2-risk-blocked-extractor`
- `step3-decision-knowledge-extractor`
- `step4-handover-generator`

## Phase 4: Report Generation
목표:
- Overview report 생성
- 담당자별 TODO
- 리스크/Blocked 우선순위
- Handover packet 출력

추천 step:
- `step0-report-model`
- `step1-overview-renderer`
- `step2-handover-renderer`
- `step3-review-status-filtering`

## Phase 5: Dashboard Prototype
목표:
- UX 문서 기준의 화면 prototype
- Evidence viewer
- Review queue mock action

추천 step:
- `step0-dashboard-shell`
- `step1-overview-screen`
- `step2-review-queue`
- `step3-evidence-viewer`

## Phase 6: Evaluation
목표:
- fixture 기반 평가
- expected vs actual 비교
- hallucination/source attribution 검사

추천 step:
- `step0-evaluation-fixtures`
- `step1-evaluator`
- `step2-regression-report`

## Phase 7: Connectors
목표:
- 실제 외부 연동 검토
- 권한 모델 적용
- sync 범위 제한

조건:
- 보안/개인정보 정책이 먼저 확정되어야 한다.
- 실제 credential은 하네스 로그에 남기지 않아야 한다.
