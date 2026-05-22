# Step 0: runner-smoke

## 읽어야 할 파일
- `AGENTS.md`
- `docs/HARNESS.md`
- `scripts/codex_execute.py`

## 작업
하네스 실행 구조가 이해 가능한지 확인하기 위한 smoke step이다.

새 기능을 추가하지 말고, 현재 Codex 하네스 파일 구조를 읽은 뒤 최종 JSON 결과만 보고하라.

## Acceptance Criteria

```bash
python scripts/codex_execute.py --help
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 성공하면 `completed`로 보고한다.
3. 실패하면 `error`로 보고하고 구체적인 실패 내용을 적는다.

## 금지사항
- `phases/0-demo/index.json`을 직접 수정하지 마라. 이유: 상태 변경은 runner 책임이다.
- 새 애플리케이션 코드를 만들지 마라. 이유: 이 step은 runner smoke test다.
