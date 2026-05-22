# DEPLOYMENT AND DISTRIBUTION

## 목적
이 문서는 Codex Harness Framework를 GitHub에 공개하거나, 다른 프로젝트에 복사하거나, 팀/개인 작업 환경에 배포하기 전에 확인해야 할 기준을 정리한다.

하네스의 배포는 일반 제품 서버 배포와 다르다. 핵심은 어떤 프로젝트에서도 같은 방식으로 phase/step 실행, 검증 로그, 복구 절차를 재현할 수 있게 만드는 것이다.

## 배포 형태

### 1. Framework repo
이 저장소 자체를 하네스 프레임워크 기준 저장소로 유지한다.

포함:
- `scripts/codex_execute.py`
- `scripts/check_dangerous_command.py`
- `scripts/test_codex_execute.py`
- `scripts/test_hooks.py`
- `schemas/step_result.schema.json`
- `AGENTS.md`
- `docs/HARNESS.md`
- `docs/DEPLOYMENT.md`
- 샘플 `phases/0-demo`

제외:
- 실제 고객/조직 데이터
- 실제 API key
- 제품별 비밀 설정
- 대용량 실행 trace

### 2. Project-embedded harness
실제 제품 프로젝트 안에 하네스를 복사해 쓰는 형태다.

추천 복사 대상:
```text
AGENTS.md
docs/HARNESS.md
docs/TROUBLESHOOTING.md
docs/DEPLOYMENT.md
schemas/step_result.schema.json
scripts/codex_execute.py
scripts/check_dangerous_command.py
scripts/test_codex_execute.py
scripts/test_hooks.py
phases/index.json
.codex/hooks.json
```

제품별로 새로 작성할 문서:
```text
docs/PRODUCT.md
docs/PRODUCT_UX.md
docs/DATA_MODEL.md
docs/SECURITY_PRIVACY.md
docs/EVALUATION.md
docs/ROADMAP.md
```

### 3. Product implementation repo
하네스를 사용해 실제 제품 코드를 만드는 저장소다. 이 경우 `src/`, `package.json`, 앱 README, 배포 설정은 제품 기준으로 추가한다.

하네스 산출물이 실제 Next.js, Python, CLI, 또는 내부 앱 코드와 섞일 수 있지만, runner 책임과 제품 코드 책임은 계속 분리한다.

## Hook 정책
현재 저장소에는 두 종류의 hook 설정이 있다.

| 위치 | 이벤트 | 명령 | 목적 |
|------|--------|------|------|
| `.codex/hooks.json` | `PreToolUse` / `^Bash$` | `python scripts/check_dangerous_command.py` | Codex shell 명령 실행 전 위험 명령 차단 |
| `.claude/settings.json` | `PreToolUse` / `Bash` | `python scripts/check_dangerous_command.py` | Claude shell 명령 실행 전 위험 명령 차단 |
| `.claude/settings.json` | `Stop` | `python -m unittest discover -s scripts -p "test_*.py" -v` | Claude 작업 종료 시 runner/hook 테스트 실행 |

`scripts/check_dangerous_command.py`는 stdin JSON, `CODEX_TOOL_INPUT`, `CLAUDE_TOOL_INPUT`에서 command를 읽는다. hook이 없어도 runner는 Acceptance Criteria 명령 실행 전에 같은 정책을 한 번 더 적용한다.

## Release checklist
GitHub 공개 또는 다른 프로젝트 복사 전에 확인한다.

- `python -m unittest discover -s scripts -p "test_*.py" -v` 통과
- `python scripts\codex_execute.py --help` 실행 가능
- `python scripts\codex_execute.py 0-demo --dry-run` 실행 가능
- `.codex/hooks.json`과 `.claude/settings.json`이 JSON으로 파싱됨
- `scripts/check_dangerous_command.py`가 위험 명령을 차단하고 안전 명령을 허용함
- `codex.cmd doctor`에서 Codex 설치와 auth 상태 확인
- `.gitignore`가 secret, env, cache, 대용량 로그를 제외함
- `phases/**/runs/`에 민감정보가 없는지 확인
- `README.md` Quickstart가 현재 명령과 일치
- `docs/TROUBLESHOOTING.md`에 blocked/error/hook 실패 복구 방법이 있음
- legacy Claude 파일이 Codex 기준 문서와 충돌하지 않음

## GitHub 기준
초기 공개 repo라면 다음 파일이 있어야 한다.

```text
README.md
AGENTS.md
docs/
scripts/
schemas/
phases/0-demo/
.codex/hooks.json
.github/workflows/test.yml
.gitignore
codex-harness.code-workspace
```

추가하면 좋은 파일:
```text
LICENSE
CHANGELOG.md
.githooks/pre-commit
```

## CI 기준
최소 CI 명령:

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\codex_execute.py --help
```

CI에서는 실제 `codex exec`를 기본으로 실행하지 않는다.

이유:
- auth와 네트워크가 필요하다.
- 비용이 발생할 수 있다.
- 비결정적 AI 실행 결과가 PR 검증을 불안정하게 만들 수 있다.

CI에서는 runner와 hook의 deterministic 동작만 검증하고, 실제 Codex 실행은 로컬 또는 명시적 수동 workflow로 둔다.

## Environment policy
하네스 repo 자체는 `.env`를 요구하지 않는다.

제품 프로젝트에서 외부 API를 연결하는 경우:
- `.env.local`은 commit하지 않는다.
- `.env.example`에는 변수 이름만 둔다.
- 실제 key는 runner prompt, trace, result, AC log에 들어가면 안 된다.
- key가 필요하면 step은 `blocked`로 보고한다.

## Artifact policy
`phases/{phase}/runs/`는 디버깅에 유용하지만 민감정보 위험이 있다.

권장 정책:
- framework repo: 데모 runs만 보존하거나 runs를 비운다.
- 실제 제품 repo: runs는 기본적으로 commit하지 않는다.
- 공개 repo: prompt/trace/result에 실제 데이터가 없는지 확인한다.
- private repo: 보존 기간과 접근 권한을 정한다.

필요하면 `.gitignore`에 다음을 둔다.

```gitignore
phases/**/runs/
```

runs를 ignore하면 runner의 metadata commit에는 index 변경만 남는다. 팀에서 trace를 리뷰해야 한다면 sanitized summary만 별도 파일로 남긴다.

## 새 프로젝트에 여는 절차
1. 대상 프로젝트 루트에 하네스 파일을 복사한다.
2. `AGENTS.md`를 제품 기준으로 다시 쓴다.
3. `docs/PRODUCT.md`, `docs/ARCHITECTURE.md`, `docs/ADR.md`를 제품 기준으로 만든다.
4. `phases/index.json`은 빈 phase 목록에서 시작한다.
5. 첫 phase를 `0-baseline` 또는 `0-mvp`로 만든다.
6. step0은 project setup 또는 fixture setup처럼 작게 시작한다.
7. dry-run으로 구조를 확인한다.
8. 실제 Codex 실행 전 Git 상태와 hook 설정을 확인한다.

## Frontend 배포 관련
운영 인텔리전스 제품의 프론트엔드까지 만든다면 배포 기준은 별도 제품 repo에서 정한다.

추천 순서:
1. fixture 기반 report 생성
2. review workflow 데이터 모델
3. dashboard prototype
4. evidence viewer
5. 실제 connector 검토
6. Vercel 또는 사내 배포 환경 선택

프론트를 먼저 만들 수는 있지만, source evidence와 review_status가 없으면 예쁜 요약 화면에서 멈출 가능성이 높다. 먼저 데이터 구조와 fixture 평가를 고정한 뒤 dashboard를 붙이는 편이 안전하다.
