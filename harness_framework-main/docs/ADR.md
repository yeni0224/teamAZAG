# Architecture Decision Records

## 철학
하네스는 에이전트를 똑똑하게 만드는 마법이 아니라, 에이전트가 실수하기 어려운 작업 환경을 만드는 장치다.

핵심 가치는 세 가지다.

1. 작은 step
2. 실행 가능한 검증
3. 복구 가능한 기록

운영 인텔리전스 제품 작업에서는 여기에 두 가지 원칙을 추가한다.

1. 출처가 있는 요약
2. 민감정보를 남기지 않는 개발 흐름

---

## ADR-001: Codex를 기준 런타임으로 선택

**결정**: 새 runner는 Claude CLI가 아니라 Codex CLI의 `codex exec`를 사용한다.

**이유**:
- 이 프로젝트의 목표가 Codex 기반 하네스이기 때문이다.
- Codex CLI는 비대화형 실행, JSONL 출력, output schema, workspace sandbox를 제공한다.
- Windows 환경에서는 `codex.cmd`로 실행할 수 있다.

**트레이드오프**:
- 기존 `.claude/commands/*`와 완전히 동일한 hook/command 경험을 제공하지 않는다.
- Claude 사용자도 쓸 수는 있지만, 기준 문서는 `AGENTS.md`로 이동한다.

---

## ADR-002: 상태 변경은 runner가 담당

**결정**: Codex step 세션은 `phases/**/index.json` 상태를 직접 변경하지 않는다.

**이유**:
- 에이전트가 성공/실패 판단을 스스로 확정하면 검증 누락이 생길 수 있다.
- timestamp, retry, blocked/error 전이는 deterministic code가 처리하는 편이 안전하다.
- runner가 Acceptance Criteria를 다시 실행하면 결과 신뢰도가 올라간다.

**트레이드오프**:
- Codex 최종 응답만으로는 step이 완료되지 않는다.
- runner 코드가 더 많은 책임을 갖는다.

---

## ADR-003: 결과는 JSON schema로 고정

**결정**: Codex 최종 응답은 `schemas/step_result.schema.json`을 따른다.

**이유**:
- runner가 결과를 안정적으로 파싱할 수 있다.
- summary, commands, details가 다음 step 컨텍스트로 재사용된다.
- error/blocked를 사람이 읽을 수 있는 형식으로 남길 수 있다.

**트레이드오프**:
- 자유 서술형 답변보다 표현이 제한된다.
- schema 변경 시 runner와 테스트를 함께 갱신해야 한다.

---

## ADR-004: Python 표준 라이브러리 우선

**결정**: runner와 테스트는 우선 Python 표준 라이브러리만 사용한다.

**이유**:
- 새 환경에서 바로 실행하기 쉽다.
- Windows 사용자에게 설치 부담을 줄인다.
- 하네스 자체가 프로젝트 의존성 설치에 막히지 않아야 한다.

**트레이드오프**:
- `pytest`, `pydantic`, `rich` 같은 편의 기능은 쓰지 않는다.
- 출력 UI는 단순하게 유지한다.

---

## ADR-005: Legacy Claude 파일은 삭제하지 않음

**결정**: `CLAUDE.md`, `.claude/commands/*`, `scripts/execute.py`는 당장 제거하지 않는다.

**이유**:
- 기존 Claude 기반 워크플로우의 의도와 비교할 수 있다.
- 단계적으로 Codex runner로 옮기는 편이 안전하다.
- 사용자에게 되돌릴 수 있는 기준점이 남는다.

**트레이드오프**:
- 저장소에 Claude와 Codex 용어가 동시에 존재한다.
- 새 문서에서 어떤 파일이 기준인지 명확히 계속 적어야 한다.

---

## ADR-006: 제품 정의는 `docs/PRODUCT.md`로 분리

**결정**: AI 기반 운영 인텔리전스 시스템의 제품 정의는 `docs/PRODUCT.md`에 둔다. `docs/PRD.md`는 하네스 자체의 요구사항을 유지한다.

**이유**:
- 이 저장소에는 하네스 코드와 대상 제품 컨텍스트가 함께 존재한다.
- 두 개념을 섞으면 runner 구현 요구사항과 운영 인텔리전스 제품 요구사항이 충돌한다.
- Codex step은 `docs/*.md`를 함께 읽으므로 제품 컨텍스트를 별도 문서로 둬도 항상 주입된다.

**트레이드오프**:
- 문서가 하나 늘어난다.
- step 작성자는 하네스 작업인지 제품 작업인지 명확히 써야 한다.

---

## ADR-007: MVP 제품 연동은 fixture 우선

**결정**: 운영 인텔리전스 제품의 MVP는 실제 메일/채팅/문서 서비스 연동보다 fixture 기반 ingestion을 먼저 구현한다.

**이유**:
- 외부 인증과 API quota 없이 테스트 가능해야 한다.
- 실제 조직 기록에는 민감정보가 포함될 수 있다.
- 추출 schema, 리포트 구조, 검증 기준을 먼저 안정화해야 한다.

**트레이드오프**:
- 초기 MVP는 실제 업무 도구와 자동 동기화되지 않는다.
- 이후 connector 구현 step이 별도로 필요하다.

---

## ADR-008: UX 문서를 제품 UX와 하네스 UX로 분리

**결정**: 제품 사용자 경험은 `docs/PRODUCT_UX.md`, 하네스 실행 경험은 `docs/HARNESS_UX.md`에 분리해 기록한다.

**이유**:
- 하네스 사용자는 개발자이고, 제품 사용자는 조직 운영 담당자다.
- 두 UX를 한 문서에 섞으면 의사결정 기준이 흐려진다.
- Codex step이 제품 화면을 만들 때와 runner를 고칠 때 서로 다른 UX 기준을 적용해야 한다.

**트레이드오프**:
- 읽어야 할 문서가 늘어난다.
- 대신 step 범위와 성공 기준이 더 명확해진다.

---

## ADR-009: 모든 운영 insight는 source-backed여야 함

**결정**: TODO, Risk, Blocked, Decision, Knowledge, Handover 항목은 원칙적으로 `source_refs`를 가져야 한다.

**이유**:
- 운영 판단은 근거 없는 AI 요약에 의존하면 안 된다.
- 사용자가 원문을 열어 확인할 수 있어야 신뢰가 생긴다.
- source 없는 insight는 hallucination 가능성이 높다.

**트레이드오프**:
- 추출 결과가 줄어들 수 있다.
- source를 연결하는 구현 비용이 늘어난다.

---

## ADR-010: AI 결과는 사용자 검토 상태를 가진다

**결정**: AI가 만든 insight는 `review_status`를 가진다. 기본값은 `proposed`이며 사용자는 confirm, edit, dismiss, merge, mark stale 할 수 있어야 한다.

**이유**:
- 운영 정보는 잘못된 owner나 due date 하나만으로도 혼선을 만든다.
- AI 결과를 바로 확정하면 오류가 조직 지식으로 굳어진다.
- 사용자 피드백은 이후 품질 개선의 핵심 데이터다.

**트레이드오프**:
- UX와 데이터 모델이 복잡해진다.
- 단순 요약 도구보다 구현 범위가 커진다.

---

## ADR-011: runs trace는 기본적으로 commit하지 않음

**결정**: `phases/**/runs/`는 기본적으로 `.gitignore`에 포함한다.

**이유**:
- prompt, trace, stderr, result에는 민감정보가 들어갈 수 있다.
- framework repo를 공개하거나 새 프로젝트에 이식할 때 로그가 가장 큰 보안 리스크다.
- 실패 분석은 로컬에서 가능하고, 공유가 필요한 경우 sanitized summary를 만들 수 있다.

**트레이드오프**:
- runner의 `chore` commit에는 runs artifact가 기본 포함되지 않는다.
- 팀 리뷰에서 원본 trace가 필요하면 별도 보존 정책이 필요하다.

---

## ADR-012: 실제 Codex 실행은 CI 기본 검증에서 제외

**결정**: CI는 runner unittest와 help 명령을 검증하고, `codex exec` 실제 실행은 기본 workflow에서 제외한다.

**이유**:
- Codex 실행은 auth, 네트워크, 비용, 모델 상태에 의존한다.
- PR 검증은 deterministic해야 한다.
- 실제 Codex 실행은 로컬 또는 수동 workflow로 관리하는 편이 안전하다.

**트레이드오프**:
- CI만으로 Codex end-to-end 성공을 보장하지 않는다.
- release 전에는 로컬 smoke test 절차가 필요하다.
