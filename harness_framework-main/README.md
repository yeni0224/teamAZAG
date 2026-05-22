# Codex Harness Framework

Codex Harness Framework는 큰 개발 작업을 phase와 step으로 쪼개 Codex CLI로 실행하고, 결과와 검증 로그를 남기는 작업 실행 프레임워크다.

현재 이 하네스의 우선 대상 제품은 **AI 기반 운영 인텔리전스 시스템**이다. 이 제품은 조직 내 흩어진 운영 기록(메일, 채팅, 회의록, 업무 문서 등)을 분석해 운영 상태, 리스크, TODO, Blocked 이슈, 조직 지식, 인수인계 정보를 구조화한다.

## 5분 Quickstart
1. 환경 상태를 확인한다.

```powershell
codex.cmd doctor
python scripts\codex_execute.py --help
```

2. 하네스 dry-run을 실행한다.

```powershell
python scripts\codex_execute.py 0-demo --dry-run
```

3. 실제 Codex 실행 전 조건을 확인한다.

- `codex.cmd doctor`에서 auth가 통과해야 한다.
- 네트워크가 OpenAI/ChatGPT endpoint에 접근 가능해야 한다.
- Git repo가 아니어도 실행은 가능하지만 commit/push 단계는 건너뛴다.
- 실제 조직 데이터는 넣지 말고 fixture를 사용한다.

4. 실제 실행은 다음 명령으로 시작한다.

```powershell
python scripts\codex_execute.py 0-demo
```

## 문서 읽는 순서
1. `docs/PRODUCT.md`: 무엇을 만들지
2. `docs/PRODUCT_UX.md`: 누가 어떤 흐름으로 제품을 쓰는지
3. `docs/DATA_MODEL.md`: 운영 인텔리전스 산출물의 구조
4. `docs/PROJECT_BOOTSTRAP.md`: 기존 harness를 버리고 이 하네스로 재개하는 절차
5. `docs/HARNESS.md`: phase와 step을 어떻게 만들고 실행하는지
6. `docs/DEPLOYMENT.md`: GitHub 공유, 새 프로젝트 이식, 배포/CI 기준
7. `docs/TROUBLESHOOTING.md`: 막혔을 때 어떻게 복구하는지
8. `docs/ROADMAP.md`: 다음 phase 순서

## 핵심 명령
```powershell
python scripts\codex_execute.py 0-demo --dry-run
python scripts\codex_execute.py 0-demo
python -m unittest discover -s scripts -p "test_*.py" -v
python -m unittest scripts.test_hooks -v
```

## 현재 알려진 주의사항
- `scripts/test_execute.py`는 legacy Claude runner 테스트이며 `pytest`가 필요하다. `pytest`가 없으면 `unittest discover`에서 skipped로 표시된다.
- phase 생성과 복구는 아직 수동 JSON 편집이 필요하다. UX 개선 대상은 `docs/HARNESS_UX.md`에 정리되어 있다.
- `phases/**/runs/`는 prompt/trace를 포함할 수 있어 기본적으로 `.gitignore`에 포함했다. 공유가 필요한 로그는 민감정보 검토 후 별도 summary로 남긴다.

## Hook 요약
| 위치 | 이벤트 | 역할 |
|------|--------|------|
| `.codex/hooks.json` | `PreToolUse` / `^Bash$` | 위험 shell 명령 차단 |
| `.claude/settings.json` | `PreToolUse` / `Bash` | 위험 shell 명령 차단 |
| `.claude/settings.json` | `Stop` | 전체 runner/hook 테스트 실행 |

hook 정책은 `scripts/check_dangerous_command.py`에 있고, runner도 Acceptance Criteria 실행 전에 같은 정책을 적용한다.

## 제품 UX 원칙
운영 인텔리전스 제품은 AI가 요약을 보여주는 도구가 아니라, 사용자가 운영 판단을 빠르게 검토하고 다음 행동으로 이어가게 하는 도구다.

- 모든 insight는 출처를 가져야 한다.
- AI 추론과 원문 사실은 구분되어야 한다.
- 사용자는 추출 결과를 confirm, dismiss, edit, merge 할 수 있어야 한다.
- TODO, Risk, Blocked는 owner, due date, severity, source를 보여줘야 한다.
- 인수인계는 새 담당자가 오늘 바로 행동할 수 있는 형태여야 한다.

## 문제 해결 바로가기
- Codex 인증 실패: `docs/TROUBLESHOOTING.md`의 `Codex auth 실패` 참고
- phase 없음: `phases/index.json`과 `phases/{phase}/index.json` 확인
- Acceptance Criteria 실패: `phases/{phase}/runs/*-ac.json` 확인
- blocked 발생: `blocked_reason`을 해결한 뒤 수동 복구 절차 실행

## 배포/재사용 바로가기
- 새 프로젝트에 하네스 심기: `docs/PROJECT_BOOTSTRAP.md`
- GitHub 공개/공유 체크리스트: `docs/DEPLOYMENT.md`
- 프론트 시작 기준: `docs/PROJECT_BOOTSTRAP.md`의 `프론트 시작 조건`
