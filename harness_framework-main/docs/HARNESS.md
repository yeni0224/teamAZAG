# Codex Harness 운영 가이드

## 핵심 요약
phase는 하나의 목표이고, step은 Codex가 한 번에 처리할 수 있는 작은 작업 단위다. runner는 step을 순서대로 실행하고, 검증하고, 기록한다.

하네스 작업과 AI 운영 인텔리전스 제품 작업은 같은 방식으로 실행한다. 차이는 step의 목표 파일과 Acceptance Criteria다.

처음 사용하는 경우에는 `README.md`를 먼저 읽고, 실패 상황은 `docs/TROUBLESHOOTING.md`를 따른다. 하네스 자체의 UX 개선 방향은 `docs/HARNESS_UX.md`에 정리되어 있다.

기존 harness에서 이 구조로 프로젝트를 다시 시작하는 경우에는 `docs/PROJECT_BOOTSTRAP.md`를 먼저 따른다. GitHub 공유나 새 프로젝트 이식 기준은 `docs/DEPLOYMENT.md`를 따른다.

## 기본 워크플로우
1. `README.md`, `docs/PRODUCT.md`, `docs/PRODUCT_UX.md`, `docs/DATA_MODEL.md`, `docs/ARCHITECTURE.md`, `docs/ADR.md`를 읽고 작업 목표를 정한다.
2. phase 이름을 정한다. 예: `0-mvp`, `1-product-ux-foundation`, `2-data-fixtures`
3. `phases/index.json`에 phase 항목을 추가한다.
4. `phases/{phase}/index.json`에 step 목록을 작성한다.
5. 각 step마다 `phases/{phase}/stepN.md`를 작성한다.
6. 가능하면 dry-run으로 phase 구조를 확인한다.
7. `python scripts/codex_execute.py {phase}`를 실행한다.
8. blocked/error가 나면 `docs/TROUBLESHOOTING.md`를 보고 원인을 해결한 뒤 재실행한다.

## Quickstart
```powershell
codex.cmd doctor
python scripts\codex_execute.py --help
python scripts\codex_execute.py 0-demo --dry-run
python -m unittest discover -s scripts -p "test_*.py" -v
```

## Phase index
`phases/index.json`은 전체 phase 목록이다.

```json
{
  "phases": [
    {
      "dir": "0-demo",
      "status": "pending"
    }
  ]
}
```

상태는 `pending`, `completed`, `error`, `blocked` 중 하나다. timestamp는 runner가 기록한다.

## Step index
`phases/{phase}/index.json`은 해당 phase의 step 목록이다.

```json
{
  "project": "Codex Harness Demo",
  "phase": "demo",
  "steps": [
    { "step": 0, "name": "runner-smoke", "status": "pending" }
  ]
}
```

규칙:
- `step`은 0부터 시작한다.
- `name`은 kebab-case를 사용한다.
- 생성 시 `status`는 `pending`으로 둔다.
- `created_at`, `started_at`, `completed_at`, `failed_at`, `blocked_at`은 runner가 기록한다.
- `summary`, `error_message`, `blocked_reason`은 runner가 Codex 결과를 바탕으로 기록한다.

## Step 파일 템플릿
````markdown
# Step N: step-name

## 읽어야 할 파일
- `AGENTS.md`
- `README.md`
- `docs/PRODUCT.md`
- `docs/PRODUCT_UX.md`
- `docs/DATA_MODEL.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/EVALUATION.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR.md`
- 이전 step에서 생성/수정한 파일

## 작업
이 step에서 수행할 작업만 구체적으로 적는다.

제품 step이라면 사용자 여정, 데이터 모델, source evidence, review_status를 함께 고려한다.

## Acceptance Criteria

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 실패하면 원인을 수정하고 다시 실행한다.
3. 사용자 개입이 필요하면 blocked로 보고한다.

## 금지사항
- 이 step 범위 밖의 리팩터링을 하지 마라. 이유: 다음 step의 범위를 침범한다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
- 실제 조직 데이터나 비밀값을 fixture, prompt, trace에 넣지 마라. 이유: 보안/개인정보 원칙 위반이다.
````

## 제품 step 작성 기준
AI 운영 인텔리전스 제품을 구현하는 step은 다음 중 하나의 작은 축에 집중한다.

- 사용자 여정
- fixture 데이터 구조
- record normalization
- TODO 추출
- 리스크 추출
- Blocked 이슈 추출
- 결정 사항 추출
- review workflow
- 인수인계 리포트 생성
- 대시보드 UI
- 개인정보 마스킹
- 평가 fixture

한 step에서 ingestion, AI 추출, UI, 권한 처리를 동시에 만들지 않는다. 범위가 커지면 실패 원인과 검증 기준이 흐려진다.

## Step 설계 원칙
- 하나의 step은 하나의 레이어나 하나의 모듈만 다룬다.
- step 파일은 독립 세션에서도 이해 가능해야 한다.
- 이전 대화를 참조하지 말고 필요한 맥락을 파일에 적는다.
- Acceptance Criteria는 실행 가능한 명령이어야 한다.
- 금지사항은 "무엇을 하지 말라 + 이유" 형태로 쓴다.
- 제품 step에서는 산출물에 원문 출처나 fixture id가 남도록 요구한다.
- 제품 step에서는 사용자에게 다음 행동이 보이는지 확인한다.

## 실행 명령
```powershell
python scripts\codex_execute.py 0-demo
```

dry-run:

```powershell
python scripts\codex_execute.py 0-demo --dry-run
```

모델 지정:

```powershell
python scripts\codex_execute.py 0-demo --model gpt-5.5
```

push까지:

```powershell
python scripts\codex_execute.py 0-demo --push
```

## Runner가 자동 처리하는 것
- `feat-{phase}` 브랜치 생성 또는 checkout
- `AGENTS.md`, `CLAUDE.md`, `docs/*.md` 가드레일 주입
- 완료된 step summary를 다음 step prompt에 누적
- Codex prompt, JSONL trace, 최종 result 저장
- Acceptance Criteria 명령 실행 전 위험 명령 차단
- Acceptance Criteria 실행
- 실패 시 최대 3회 retry
- `running` 상태 step 재개
- top-level phase 상태 업데이트
- 코드 변경과 메타데이터 변경 분리 커밋

주의: `phases/**/runs/`는 기본 `.gitignore` 대상이다. runner는 로컬 로그를 만들지만, 공개 repo에 trace를 남기려면 먼저 민감정보를 검토하고 sanitized summary로 옮긴다.

## Hook 설정
현재 hook은 다음 역할을 한다.

| 위치 | 이벤트 | 명령 |
|------|--------|------|
| `.codex/hooks.json` | `PreToolUse` | `python scripts/check_dangerous_command.py` |
| `.claude/settings.json` | `PreToolUse` | `python scripts/check_dangerous_command.py` |
| `.claude/settings.json` | `Stop` | `python -m unittest discover -s scripts -p "test_*.py" -v` |

hook 정책을 수정하면 다음 명령으로 설정과 차단 동작을 함께 검증한다.

```powershell
python -m unittest scripts.test_hooks -v
python -m unittest discover -s scripts -p "test_*.py" -v
```

## 복구 방법
상세한 문제 해결은 `docs/TROUBLESHOOTING.md`를 따른다.

### error
1. `phases/{phase}/index.json`에서 실패 step을 찾는다.
2. `error_message`와 runs 로그를 확인한다.
3. 원인을 해결한다.
4. `status`를 `pending`으로 바꾼다.
5. `error_message`를 삭제한다.
6. runner를 다시 실행한다.

### blocked
1. `blocked_reason`에 적힌 사용자 개입 사항을 해결한다.
2. `status`를 `pending`으로 바꾼다.
3. `blocked_reason`을 삭제한다.
4. runner를 다시 실행한다.

상태 수정은 runner가 정상 복구하지 못한 경우의 수동 복구 절차다. 일반 step 세션에서는 상태를 직접 바꾸지 않는다.

## 로그 위치
각 실행의 산출물은 `phases/{phase}/runs/`에 남는다.

```text
step0-attempt1-prompt.md
step0-attempt1.jsonl
step0-attempt1-result.json
step0-attempt1-ac.json
step0-attempt1-stderr.txt
```

이 로그는 실패 원인 분석과 다음 prompt 개선에 사용한다. 실제 운영 데이터나 비밀값이 로그에 남지 않도록 fixture와 마스킹을 우선한다.

기본 정책에서는 `runs/`를 commit하지 않는다. trace 공유가 필요한 경우 `docs/DEPLOYMENT.md`의 Artifact policy를 따른다.
