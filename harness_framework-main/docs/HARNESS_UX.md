# HARNESS UX

## 목적
하네스 UX는 개발자가 Codex step을 안전하게 실행하고, 실패했을 때 다음 행동을 즉시 알 수 있게 만드는 것이다.

좋은 하네스 UX는 다음을 만족한다.

- 처음 실행 명령이 명확하다.
- 실패 메시지가 원인과 다음 행동을 알려준다.
- 현재 phase와 step 상태를 한눈에 보여준다.
- 사용자의 기존 변경사항을 실수로 커밋하지 않는다.
- 로그 위치와 복구 절차가 바로 보인다.

## 현재 UX 문제
| 문제 | 영향 | 개선 방향 |
|------|------|------|
| README 없음 | 첫 사용자가 시작점 파악 어려움 | Quickstart 추가 |
| 수동 JSON 편집 | 실수 가능성 높음 | `new-phase`, `status`, `resume` 명령 추가 |
| raw error 출력 | 다음 행동 불명확 | 친절한 error format 도입 |
| Codex preflight 없음 | 인증/네트워크 실패를 늦게 발견 | `doctor` 명령 추가 |
| git dirty 감지 없음 | 사용자 변경사항 커밋 위험 | 실행 전 dirty check |
| prompt가 argv로 전달됨 | Windows 길이 제한 위험 | stdin 전달 |

## 추천 CLI 명령
### doctor
```powershell
python scripts\codex_execute.py doctor
```

검사:
- Codex 설치
- Codex auth
- 네트워크 reachability
- phase/index schema
- step 파일 존재
- git 상태
- 모델 설정 충돌
- 테스트 명령 실행 가능성

### status
```powershell
python scripts\codex_execute.py status
python scripts\codex_execute.py status 1-product-ux-foundation
```

보여줄 정보:
- phase 목록
- 각 phase 상태
- 현재 pending/running step
- 마지막 실패 원인
- runs 로그 위치

### new-phase
```powershell
python scripts\codex_execute.py new-phase 1-product-ux-foundation
```

생성:
- `phases/{phase}/index.json`
- `phases/{phase}/step0.md`
- `phases/index.json` 항목

### resume
```powershell
python scripts\codex_execute.py resume 1-product-ux-foundation
```

동작:
- error/blocked step을 보여준다.
- 사용자가 해결했는지 확인한다.
- 상태를 pending으로 되돌린다.
- runner를 재실행한다.

## 에러 메시지 형식
모든 에러는 다음 형식이 좋다.

```text
ERROR: phase not found

What happened:
  phases/1-product-ux-foundation directory does not exist.

Why it matters:
  Runner can only execute registered phase directories.

Next steps:
  1. Check phases/index.json
  2. Create phases/1-product-ux-foundation/index.json
  3. Add step0.md
```

## 실행 전 확인 UX
실제 Codex 실행 전 runner는 다음을 요약해야 한다.

```text
Phase: 1-product-ux-foundation
Next step: 0 user-journeys
Codex: codex.cmd
Model: gpt-5.5
Git: not a repository, commit will be skipped
AC: python -m unittest ...
Runs dir: phases/1-product-ux-foundation/runs
```

## 로그 UX
`runs/` 로그는 기계가 읽는 JSON과 사람이 읽는 요약을 둘 다 제공하는 것이 좋다.

- `*-prompt.md`: Codex에 전달한 전체 prompt
- `*.jsonl`: Codex trace
- `*-result.json`: 최종 JSON
- `*-ac.json`: AC 실행 결과
- `*-summary.md`: 사람이 보는 요약

## 우선 구현 순서
1. `README.md` Quickstart
2. `doctor` 명령
3. `status` 명령
4. 친절한 error format
5. dirty git 감지
6. prompt stdin 전달
7. `new-phase`와 `resume`
