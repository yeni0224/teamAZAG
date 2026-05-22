이 프로젝트는 Codex Harness Framework다. Claude Code에서 이 command를 실행하더라도 기준 문서는 `AGENTS.md`와 `docs/HARNESS.md`다.

---

## 워크플로우

### A. 탐색
먼저 아래 문서를 읽어라.

- `AGENTS.md`
- `README.md`
- `docs/PRD.md`
- `docs/PRODUCT.md`
- `docs/PRODUCT_UX.md`
- `docs/DATA_MODEL.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/EVALUATION.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR.md`
- `docs/HARNESS.md`
- `docs/HARNESS_UX.md`
- `docs/TROUBLESHOOTING.md`
- `docs/ROADMAP.md`
- `docs/GLOSSARY.md`

이 프로젝트의 기준 실행기는 `scripts/codex_execute.py`다. 기존 `scripts/execute.py`는 Claude 기반 legacy runner다.

### B. 논의
구현을 위해 더 정해야 할 내용이 있으면 사용자에게 짧고 구체적으로 질문한다.

### C. Step 설계
사용자가 구현 계획 작성을 지시하면 phase와 step 초안을 만든다.

step 설계 원칙:

1. 하나의 step은 하나의 레이어나 모듈만 다룬다.
2. step 파일은 독립 실행 가능해야 한다.
3. 이전 대화에 의존하지 말고 필요한 맥락을 파일에 적는다.
4. Acceptance Criteria는 실행 가능한 명령으로 적는다.
5. 금지사항은 "X를 하지 마라. 이유: Y" 형식으로 적는다.
6. 제품 step은 사용자 여정, source evidence, review_status를 고려한다.
7. step name은 kebab-case를 쓴다.

### D. 파일 생성
사용자가 승인하면 아래 파일을 만든다.

- `phases/index.json`
- `phases/{phase}/index.json`
- `phases/{phase}/stepN.md`

`phases/**/index.json`의 timestamp와 상태 변경은 runner가 담당한다. step 파일을 만들 때는 초기 상태를 `pending`으로 둔다.

### E. 실행
Codex runner 실행:

```bash
python scripts/codex_execute.py {phase}
```

dry-run:

```bash
python scripts/codex_execute.py {phase} --dry-run
```

Claude legacy runner 실행은 필요한 경우에만 사용한다.

```bash
python scripts/execute.py {phase}
```

### F. 복구
`error` 또는 `blocked`가 발생하면 `docs/TROUBLESHOOTING.md`와 `docs/HARNESS.md`의 복구 방법을 따른다.
