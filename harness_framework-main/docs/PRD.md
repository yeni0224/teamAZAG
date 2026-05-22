# PRD: Codex Harness Framework

## 목표
큰 개발 작업을 Codex가 안정적으로 수행할 수 있도록, 작업을 작은 step으로 나누고 실행, 검증, 재시도, 기록을 자동화하는 하네스를 만든다.

현재 이 하네스의 우선 적용 대상은 `docs/PRODUCT.md`에 정의된 AI 기반 운영 인텔리전스 시스템이다. 즉, 이 저장소는 “운영 인텔리전스 제품을 한 번에 만들기”가 아니라, 제품 개발을 작은 Codex step으로 쪼개 안정적으로 실행하기 위한 작업 프레임워크다.

## 문제
LLM 코딩 에이전트는 긴 작업에서 맥락을 잃거나, 검증을 생략하거나, 실패 상태를 애매하게 남기기 쉽다. 사용자는 매번 프롬프트를 다시 구성하고, 어떤 step이 어디까지 끝났는지 수동으로 추적해야 한다.

운영 인텔리전스 시스템처럼 ingestion, 추출, 요약, UI, 보안 기준이 얽힌 제품은 작업 범위가 쉽게 커진다. 따라서 phase/step 단위로 범위를 제한하고, 각 step의 검증 결과를 남기는 하네스가 필요하다.

## 사용자
- Codex로 여러 단계의 구현 작업을 안정적으로 실행하려는 개발자
- PRD, 아키텍처 문서, step 계획을 기반으로 에이전트 작업을 관리하려는 팀
- AI 운영 인텔리전스 제품을 작은 단위로 설계, 구현, 검증하려는 사용자
- Claude 기반 하네스 아이디어를 Codex 중심 워크플로우로 옮기려는 사용자

## UX 요구사항
- 첫 사용자는 `README.md`만 읽고 dry-run까지 실행할 수 있어야 한다.
- 실패 메시지는 원인, 영향, 다음 행동을 알려야 한다.
- phase/step 상태는 사용자가 JSON을 직접 열지 않아도 이해할 수 있어야 한다.
- 운영 인텔리전스 제품의 AI 결과는 검토, 수정, dismiss, merge 가능해야 한다.
- 모든 insight는 source evidence, confidence, review_status를 가져야 한다.

## 핵심 기능
1. phase/step 기반 작업 계획 관리
2. `AGENTS.md`와 `docs/*.md`를 step prompt에 자동 주입
3. Codex CLI 비대화형 실행(`codex exec`)
4. 구조화된 step 결과 JSON 저장
5. Acceptance Criteria 명령 실행과 결과 기록
6. 실패 시 최대 3회 retry
7. blocked/error/completed 상태와 timestamp 기록
8. git branch/commit/push 자동화

## MVP 범위
- Python 표준 라이브러리 기반 runner
- `phases/index.json`과 `phases/{phase}/index.json` 상태 관리
- `schemas/step_result.schema.json` 기반 결과 보고
- Windows에서 `codex.cmd` 우선 사용
- 테스트 가능한 dry-run 모드
- 기존 Claude 문서와 병렬 공존
- 제품 개발 step에서 UX, 데이터 모델, 보안, 평가 문서를 공통 컨텍스트로 주입

## MVP 제외 사항
- 하네스 웹 대시보드
- 복잡한 멀티 에이전트 스케줄러
- 원격 실행 서버
- 외부 DB 저장
- Codex 인증 자동 설정
- 임의 프로젝트 템플릿 생성기
- 운영 인텔리전스 제품의 실제 외부 서비스 연동

## 성공 기준
- 새 phase를 만들고 `python scripts/codex_execute.py {phase}`로 실행할 수 있다.
- runner가 step prompt, Codex trace, 최종 JSON, AC 결과를 보존한다.
- 실패 step은 error/blocked 상태로 명확히 남는다.
- dry-run과 단위 테스트가 외부 의존성 없이 통과한다.
- 제품 구현 step은 운영 상태, 리스크, TODO, Blocked, 지식, 인수인계라는 공통 분류를 유지한다.
- 제품 UX step은 사용자 여정과 review workflow를 깨뜨리지 않는다.

## 비기능 요구사항
- 저장소가 Git repo가 아니어도 git 단계만 건너뛰고 실행 가능해야 한다.
- Windows PowerShell 환경에서 동작해야 한다.
- 하네스 메타데이터는 사람이 읽고 수정할 수 있는 JSON/Markdown이어야 한다.
- 실행 실패는 조용히 삼키지 않고 다음 시도에 쓸 수 있는 형태로 남겨야 한다.
- 실제 운영 데이터나 비밀값이 문서, trace, 로그에 그대로 남지 않도록 step에서 fixture와 마스킹을 우선한다.
