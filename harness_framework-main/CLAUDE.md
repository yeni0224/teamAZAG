# Claude 호환 안내

이 프로젝트의 주 실행 환경은 Codex다. Claude Code에서 이 저장소를 열 경우에도 기준 문서는 `AGENTS.md`이며, 아래 규칙을 따른다.

현재 대상 제품은 **AI 기반 운영 인텔리전스 시스템**이다. 제품 정의는 `docs/PRODUCT.md`를 기준으로 하고, 사용자 경험 기준은 `docs/PRODUCT_UX.md`와 `docs/HARNESS_UX.md`를 따른다.

## 기준 문서
- Codex/Cursor/Claude 공통 작업 규칙: `AGENTS.md`
- 첫 실행 안내: `README.md`
- 제품 정의: `docs/PRODUCT.md`
- 제품 UX: `docs/PRODUCT_UX.md`
- 데이터 모델: `docs/DATA_MODEL.md`
- 보안/개인정보: `docs/SECURITY_PRIVACY.md`
- 평가 기준: `docs/EVALUATION.md`
- 하네스 설계와 운영: `docs/HARNESS.md`
- 하네스 UX: `docs/HARNESS_UX.md`
- 문제 해결: `docs/TROUBLESHOOTING.md`
- 아키텍처: `docs/ARCHITECTURE.md`
- 결정 기록: `docs/ADR.md`

## Claude 사용 시 규칙
- 기존 `.claude/commands/*`는 참고용 legacy command로 유지한다.
- 새 실행기는 `scripts/codex_execute.py`다.
- 새 phase/step 설계는 `docs/HARNESS.md`의 Codex 기준을 따른다.
- `phases/**/index.json` 상태 변경은 runner 책임이다. Claude 세션에서 직접 완료 처리하지 않는다.
- 운영 인텔리전스 제품 기능을 다룰 때는 `docs/PRODUCT.md`, `docs/PRODUCT_UX.md`, `docs/DATA_MODEL.md`, `docs/SECURITY_PRIVACY.md`의 기준을 따른다.

## 마이그레이션 방향
기존 Claude 기반 구조의 좋은 점은 유지한다.

- 문서 가드레일을 매 step에 주입한다.
- 완료된 step summary를 다음 step에 넘긴다.
- 실패하면 에러를 다음 시도에 피드백한다.
- 코드 변경과 메타데이터 변경을 분리한다.

다만 실행 런타임과 책임 분리는 Codex 기준으로 바꾼다.
