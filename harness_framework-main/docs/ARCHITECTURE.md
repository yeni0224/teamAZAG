# 아키텍처

## 개요
Codex Harness Framework는 runner 중심 구조다. Codex는 step 작업자이고, runner는 상태 관리자이자 검증자다.

```text
phase index -> prompt compiler -> codex exec -> result parser -> AC runner -> state updater
```

현재 대상 제품은 AI 기반 운영 인텔리전스 시스템이다. 하네스는 이 제품을 phase/step 단위로 구현하기 위한 실행 장치이며, 제품 자체의 ingestion, 분석, 리포트 구조는 별도 step에서 점진적으로 만들어진다.

## 디렉토리 구조
```text
README.md                         # Quickstart와 첫 실행 안내
AGENTS.md                         # Codex 작업 규칙
CLAUDE.md                         # Claude 호환 안내
docs/
  PRODUCT.md                      # 대상 제품 정의
  PRODUCT_UX.md                   # 제품 사용자 여정과 검토 UX
  DATA_MODEL.md                   # SourceRecord와 insight schema
  SECURITY_PRIVACY.md             # 보안/개인정보 원칙
  EVALUATION.md                   # 추출/UX 평가 기준
  PROJECT_BOOTSTRAP.md            # 기존 프로젝트 재개 절차
  DEPLOYMENT.md                   # 배포/공유/이식 기준
  PRD.md                          # 하네스 요구사항
  ARCHITECTURE.md                 # 구조 설명
  ADR.md                          # 설계 결정 기록
  HARNESS.md                      # 하네스 운영 규칙
  HARNESS_UX.md                   # 하네스 사용 경험 개선 기준
  UI_GUIDE.md                     # 시각 디자인 기준
  TROUBLESHOOTING.md              # 실패 복구 가이드
  ROADMAP.md                      # phase 계획
  GLOSSARY.md                     # 용어 정의
.codex/
  config.toml                     # Codex 기본 설정
  hooks.json                      # 안전 hook 설정
schemas/
  step_result.schema.json         # Codex 최종 응답 스키마
scripts/
  codex_execute.py                # Codex runner
  execute.py                      # legacy Claude runner
  check_dangerous_command.py      # 위험 명령 차단 hook
  test_codex_execute.py           # Codex runner 테스트
  test_hooks.py                   # hook 정책과 설정 테스트
phases/
  index.json                      # 전체 phase 목록
  {phase}/
    index.json                    # phase 내부 step 상태
    stepN.md                      # step 지시서
    runs/                         # prompt, trace, result, AC 로그
```

## 하네스 컴포넌트

### Runner
`scripts/codex_execute.py`가 runner다.

역할:
- phase와 step index 읽기
- pending/running step 선택
- prompt 컴파일
- `codex exec` 실행
- 결과 JSON 파싱
- Acceptance Criteria 명령 실행
- step 상태 업데이트
- retry, blocked, error 처리
- git branch/commit/push 처리

향후 UX 개선은 `docs/HARNESS_UX.md`를 따른다.

### Step 파일
`phases/{phase}/stepN.md`는 Codex가 수행할 단일 작업 단위다.

필수 섹션:
- 읽어야 할 파일
- 작업
- Acceptance Criteria
- 검증 절차
- 금지사항

### Result Schema
`schemas/step_result.schema.json`은 Codex 최종 응답 형식을 고정한다.

runner는 이 결과를 읽지만, 최종 성공 여부는 Acceptance Criteria 명령으로 다시 확인한다.

### Hooks
hook은 shell 명령 실행 전 안전장치와 작업 종료 시 검증을 담당한다.

| 설정 파일 | 이벤트 | matcher | 명령 |
|-----------|--------|---------|------|
| `.codex/hooks.json` | `PreToolUse` | `^Bash$` | `python scripts/check_dangerous_command.py` |
| `.claude/settings.json` | `PreToolUse` | `Bash` | `python scripts/check_dangerous_command.py` |
| `.claude/settings.json` | `Stop` | empty | `python -m unittest discover -s scripts -p "test_*.py" -v` |

`scripts/check_dangerous_command.py`는 stdin JSON, `CODEX_TOOL_INPUT`, `CLAUDE_TOOL_INPUT`을 모두 지원한다. Codex runner는 Acceptance Criteria 명령을 실행하기 전에도 같은 위험 명령 정책을 적용하므로, hook이 동작하지 않는 환경에서도 AC 단계에서 한 번 더 차단된다.

## 하네스 데이터 흐름
```text
사용자/계획자
  -> phases/{phase}/stepN.md 작성
  -> runner 실행
  -> runner가 AGENTS.md + docs/*.md + 이전 summary + step 지시를 prompt로 결합
  -> codex exec 실행
  -> runs/에 trace와 result 저장
  -> runner가 AC 명령 안전성 검사 후 실행
  -> index.json 상태 업데이트
  -> 다음 step으로 진행
```

## 상태 모델
| 상태 | 의미 |
|------|------|
| `pending` | 아직 실행 전 |
| `running` | 실행 중이었거나 재개 대상 |
| `completed` | Codex 결과와 AC 검증이 통과 |
| `error` | 최대 재시도 후 실패 |
| `blocked` | 사용자 개입 필요 |

`running`은 중단 복구를 위해 재개 대상에 포함한다.

## 파일 소유권
- Codex 세션: 제품 코드와 step 산출물 수정
- runner: `phases/**/index.json`, timestamp, runs 로그, commit
- 사용자: phase 설계 승인, blocked 해결, 범위 결정

## Git 전략
Git repo 안에서는 runner가 `feat-{phase}` 브랜치를 만들거나 checkout한다.

step 완료 후:
1. 실제 코드 변경을 `feat({phase}): step {num} {name}`로 커밋
2. 하네스 메타데이터와 로그를 `chore({phase}): step {num} output`으로 커밋

Git repo가 아니면 git 단계는 건너뛴다.

`phases/**/runs/`는 prompt와 trace를 포함할 수 있어 기본 `.gitignore` 대상이다. 팀에서 실행 trace를 리뷰해야 한다면 민감정보를 제거한 summary artifact를 별도로 남긴다.

## 배포 구조
이 저장소는 세 가지 방식으로 사용된다.

| 형태 | 설명 |
|------|------|
| Framework repo | 하네스 runner와 문서를 관리하는 기준 저장소 |
| Project-embedded harness | 새 제품 repo 안에 하네스 파일을 복사해 쓰는 형태 |
| Product implementation repo | 하네스를 사용해 실제 앱 코드와 배포 설정까지 포함하는 형태 |

세부 기준은 `docs/DEPLOYMENT.md`를 따른다.

## 대상 제품의 논리 구조
AI 운영 인텔리전스 시스템은 다음 모듈로 나누어 구현한다. 아직 모든 모듈이 코드로 존재한다는 뜻은 아니며, phase/step 계획의 기준 구조다.

```text
sources -> ingestion -> normalization -> extraction -> review workflow -> intelligence model -> report/dashboard
```

### Sources
운영 기록의 원천이다.

- 메일
- 채팅
- 회의록
- 업무 문서
- 티켓/업무 관리 도구

MVP에서는 실제 외부 연동 대신 fixture 파일을 사용한다.

### Ingestion
원천 데이터를 읽어 내부 record로 변환한다. 필드 구조는 `docs/DATA_MODEL.md`의 SourceRecord를 따른다.

### Normalization
메일, 채팅, 회의록처럼 형식이 다른 데이터를 공통 텍스트와 메타데이터 구조로 맞춘다.

### Extraction
AI 또는 deterministic parser가 운영 정보를 추출한다.

출력 분류:
- 운영 상태
- 주요 리스크
- TODO
- Blocked 이슈
- 조직 지식
- 인수인계 정보
- 결정 사항

### Review Workflow
사용자는 AI가 제안한 insight를 검토한다.

- confirm
- edit
- dismiss
- merge
- mark stale
- open source

검토 결과는 `review_status`와 review event로 남긴다.

### Intelligence Model
추출 결과를 연결하고 중복을 줄인다.

- 같은 TODO 병합
- 리스크와 Blocked 이슈 연결
- 담당자/기한/출처 정리
- 원문 근거와 추론 구분
- stale 항목 표시

### Report/Dashboard
사용자가 바로 의사결정할 수 있게 요약한다.

- 현재 상태
- 가장 중요한 리스크
- 막힌 이슈와 필요한 결정
- 담당자별 TODO
- 인수인계 요약
- 원문 출처 링크 또는 record id

제품 화면과 사용자 여정은 `docs/PRODUCT_UX.md`를 따른다.
