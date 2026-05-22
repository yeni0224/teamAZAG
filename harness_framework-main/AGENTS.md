# Codex Harness Framework

이 저장소는 큰 개발 작업을 작은 step으로 나누고, 각 step을 Codex CLI로 실행하는 하네스 프레임워크다.

현재 이 하네스의 주요 대상 제품은 **AI 기반 운영 인텔리전스 시스템**이다. 이 제품은 조직 내 흩어진 운영 기록(메일, 채팅, 회의록, 업무 문서 등)을 AI가 분석해 운영 상태, 주요 리스크, TODO, Blocked 이슈, 조직 지식, 인수인계 정보를 자동으로 구조화한다.

Claude 기반 아이디어를 참고할 수는 있지만, 이 프로젝트의 기준 런타임은 Codex다. Codex 작업자는 `AGENTS.md`, `docs/*.md`, `phases/{phase}/stepN.md`를 읽고 현재 step 범위 안에서만 움직인다.

## 반드시 읽을 문서
- `README.md`: 첫 실행, Quickstart, 현재 주의사항
- `docs/PRODUCT.md`: 현재 대상 제품인 AI 운영 인텔리전스 시스템의 정의와 범위
- `docs/PRODUCT_UX.md`: 사용자 여정, 핵심 화면, AI 결과 검토 흐름
- `docs/DATA_MODEL.md`: SourceRecord와 insight item 구조
- `docs/SECURITY_PRIVACY.md`: 민감정보, 마스킹, 권한, 삭제 원칙
- `docs/EVALUATION.md`: 추출 품질과 UX 품질 평가 기준
- `docs/PROJECT_BOOTSTRAP.md`: 기존 harness에서 이 하네스로 재개하는 절차
- `docs/DEPLOYMENT.md`: GitHub 공유, 새 프로젝트 이식, CI, artifact 정책
- `docs/PRD.md`: 왜 이 하네스를 만드는지와 제품 개발에 어떻게 쓰는지
- `docs/ARCHITECTURE.md`: runner, phase, step, trace의 구조와 대상 제품의 큰 구조
- `docs/ADR.md`: 중요한 설계 결정과 트레이드오프
- `docs/HARNESS.md`: 실제 step 작성과 실행 규칙
- `docs/HARNESS_UX.md`: 하네스 CLI/로그/복구 UX 개선 기준
- `docs/UI_GUIDE.md`: 하네스와 운영 인텔리전스 UI의 시각 기준
- `docs/TROUBLESHOOTING.md`: 실패 상황별 복구 방법
- `docs/ROADMAP.md`: 하네스와 제품 개발 phase 순서
- `docs/GLOSSARY.md`: 운영 인텔리전스 용어 정의

## 역할 분리
| 책임 | 담당 |
|------|------|
| 코드 읽기와 수정 | Codex step 세션 |
| 최종 step 결과 보고 | Codex step 세션 |
| `index.json` 상태 변경 | runner |
| timestamp 기록 | runner |
| Acceptance Criteria 실행 | runner |
| retry 판정 | runner |
| git branch/commit/push | runner |

Codex 세션은 `phases/**/index.json`의 상태를 직접 바꾸지 않는다. 상태 변경은 `scripts/codex_execute.py`가 한다.

## 작업 원칙
- step 파일에 적힌 범위를 넘지 않는다.
- 기존 사용자 변경사항을 되돌리지 않는다.
- 필요한 파일을 먼저 읽고, 기존 구조를 따른다.
- 새 기능이나 동작 변경에는 테스트를 함께 추가한다.
- 운영 데이터, 인증 정보, 개인 정보, 고객 정보는 샘플/fixture로만 다루고 실제 비밀값을 출력하지 않는다.
- Acceptance Criteria 명령을 실행하거나, 실행하지 못한 이유를 명확히 남긴다.
- 외부 인증, API key, 수동 설정이 필요하면 `blocked`로 보고한다.

## Hook 기준
이 저장소의 hook은 shell 명령 안전성과 기본 검증을 담당한다.

| 위치 | 이벤트 | 목적 |
|------|--------|------|
| `.codex/hooks.json` | `PreToolUse` / `^Bash$` | Codex shell 명령 실행 전 위험 명령 차단 |
| `.claude/settings.json` | `PreToolUse` / `Bash` | Claude shell 명령 실행 전 위험 명령 차단 |
| `.claude/settings.json` | `Stop` | 작업 종료 시 runner/hook 테스트 실행 |

위험 명령 정책은 `scripts/check_dangerous_command.py`에 있다. `scripts/codex_execute.py`도 Acceptance Criteria 명령을 실행하기 전에 같은 정책으로 한 번 더 검사한다.

hook 또는 runner 안전 정책을 바꾸면 `scripts/test_hooks.py`와 `scripts/test_codex_execute.py`를 함께 갱신하고, 다음 명령을 통과시킨다.

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

## UX 우선 원칙
- 사용자에게 다음 행동이 보이지 않는 결과는 실패로 본다.
- AI 결과는 confirm, edit, dismiss, merge 같은 검토 흐름을 가져야 한다.
- 모든 운영 insight는 source evidence와 review status를 가져야 한다.
- 낮은 confidence, stale, inferred 항목은 UI에서 명확히 표시한다.
- 하네스 에러는 원인, 영향, 다음 명령을 함께 알려야 한다.

## 제품 작업 기준
AI 운영 인텔리전스 시스템을 구현하는 step에서는 다음 산출물을 우선 구조화한다.

- 운영 상태: 현재 진행 상황, 건강도, 최근 변화
- 주요 리스크: 일정, 품질, 의존성, 담당자 부재, 의사결정 지연
- TODO: 담당자, 기한, 출처, 우선순위가 있는 실행 항목
- Blocked 이슈: 막힌 이유, 필요한 의사결정, 외부 의존성
- 조직 지식: 반복되는 운영 규칙, 결정, 노하우, 문맥
- 인수인계 정보: 새 담당자가 이어받기 위한 요약, 링크, 남은 작업

## 결과 보고
Codex step 세션의 최종 응답은 `schemas/step_result.schema.json`을 따른다.

```json
{
  "status": "completed",
  "summary": "무엇을 만들었고 어떤 파일이 핵심인지 한 줄로 요약",
  "commands": [
    { "command": "python -m unittest discover -s scripts -p \"test_*.py\" -v", "status": "passed", "notes": "통과" }
  ],
  "details": "다음 step에 넘길 맥락"
}
```

## 안전 규칙
- `git reset --hard`, 강제 push, 대량 삭제, 비밀값 출력 같은 위험 작업은 사용자가 명시하지 않으면 하지 않는다.
- 네트워크 설치나 외부 서비스 접근이 필요하면 먼저 blocked 사유로 보고한다.
- 하네스 메타데이터 변경과 실제 제품 코드 변경은 runner가 분리 커밋하도록 설계한다.
- 실제 조직 기록을 처리하는 기능은 최소 수집, 마스킹, 출처 추적, 삭제 가능성을 기본 전제로 설계한다.
- `phases/**/runs/`는 prompt와 trace를 포함할 수 있으므로 공개/공유 전 민감정보를 확인한다.

## 배포/재사용 원칙
- 이 저장소는 framework repo이고, 실제 제품 repo에는 필요한 하네스 파일만 이식한다.
- 제품 repo의 `AGENTS.md`는 반드시 제품 특화 규칙으로 다시 쓴다.
- 실제 Codex 실행은 CI 기본 검증으로 돌리지 않는다. CI에서는 runner 테스트와 help 명령까지만 검증한다.
- 프론트 구현은 fixture, data model, review workflow가 정해진 뒤 시작한다.

## Windows 주의사항
Windows PowerShell에서는 `codex` shim이 실행 정책에 막힐 수 있다. runner는 기본적으로 `codex.cmd`를 우선 사용한다.
