# PROJECT BOOTSTRAP

## 목적
기존 하네스를 버리고 이 Codex Harness Framework로 프로젝트를 다시 시작할 때의 절차를 정리한다.

목표는 과거 작업을 모두 버리는 것이 아니라, 쓸 만한 기획과 산출물은 문서/fixture로 흡수하고 실행 방식만 Codex 하네스로 재정렬하는 것이다.

## 재개 원칙
- 기존 구현을 무조건 이어붙이지 않는다.
- 먼저 제품 정의, 데이터 모델, 보안 기준, 평가 기준을 고정한다.
- 그 다음 fixture 기반으로 작은 step을 실행한다.
- 실제 connector와 프론트는 뒤쪽 phase로 둔다.

## 첫날 절차
1. 기존 프로젝트에서 재사용할 문서와 아이디어를 모은다.
2. 실제 데이터나 secret은 가져오지 않는다.
3. `docs/PRODUCT.md`에 제품 정의를 확정한다.
4. `docs/DATA_MODEL.md`에 핵심 산출물 구조를 확정한다.
5. `docs/ROADMAP.md`에서 첫 phase를 선택한다.
6. `phases/{phase}/index.json`과 `step0.md`를 만든다.
7. dry-run으로 구조를 확인한다.
8. Codex 실행은 작은 fixture step부터 시작한다.

## 기존 harness에서 가져올 것
가져올 만한 것:
- 좋은 step 분해 방식
- Acceptance Criteria 명령
- 제품 의사결정 기록
- 테스트 fixture
- 실패 로그에서 얻은 교훈

버리거나 다시 써야 할 것:
- Claude 전용 prompt
- status를 에이전트가 직접 바꾸는 방식
- secret이 섞인 trace
- 너무 큰 step
- 검증 명령이 없는 TODO 목록

## 추천 첫 phase
운영 인텔리전스 제품을 재개한다면 첫 phase는 프론트가 아니라 product/data/evaluation 기준을 고정하는 편이 좋다.

```text
1-product-foundation
  step0-product-scope
  step1-user-journeys
  step2-core-data-model
  step3-security-boundaries
  step4-evaluation-fixtures
```

각 step은 문서와 fixture만 다루고, 실제 앱 코드는 아직 만들지 않는다.

## 프론트 시작 조건
프론트를 시작해도 좋은 시점:
- SourceRecord 구조가 정해졌다.
- TODO/Risk/Blocked/Decision item schema가 있다.
- review_status 흐름이 정해졌다.
- fixture input과 expected output이 있다.
- 어떤 화면에서 사용자가 confirm/edit/dismiss/merge 하는지 정해졌다.

이 조건이 없으면 프론트가 "AI 요약 카드 모음"으로 흐를 가능성이 높다.

## 사용자의 역할
이 하네스에서 사용자는 단순 구현자가 아니라 제품 방향과 운영 판단 기준을 정하는 사람이다.

사용자가 정해야 하는 것:
- 어떤 운영 문제를 먼저 풀지
- 어떤 source를 MVP에 포함할지
- 어떤 insight가 실제 행동으로 이어지는지
- AI 결과를 어디까지 자동화하고 어디서 사람 검토를 요구할지
- 프론트를 언제 시작할지

Codex와 runner가 맡는 것:
- step 범위 안의 구현
- 테스트와 검증
- 반복 실행과 실패 기록
- 문서와 코드의 일관성 유지

## 프론트 고민에 대한 기준
프론트를 직접 해보는 것은 좋다. 다만 첫 프론트 phase는 "완성 앱"이 아니라 "검토 가능한 운영 화면 prototype"이어야 한다.

좋은 첫 화면:
- 오늘의 리스크
- 막힌 이슈
- 담당자별 TODO
- confidence 낮은 항목
- 원문 evidence 열기
- confirm/edit/dismiss 버튼

나쁜 첫 화면:
- 큰 hero section
- AI가 다 해준다는 문구
- 출처 없는 summary 카드
- review action 없는 대시보드
