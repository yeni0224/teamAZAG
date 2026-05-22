# PRODUCT UX: AI 운영 인텔리전스

## UX 목표
사용자가 흩어진 운영 기록을 다시 읽지 않아도 현재 상황, 위험, 막힌 일, 다음 행동, 인수인계 맥락을 빠르게 판단하게 만든다.

좋은 UX의 기준은 예쁜 대시보드가 아니라 다음 질문에 1분 안에 답하는 것이다.

- 지금 조직 운영은 정상인가?
- 가장 위험한 이슈는 무엇인가?
- 무엇이 막혔고 누가 풀어야 하는가?
- 오늘 처리해야 할 TODO는 무엇인가?
- 어떤 결정이 내려졌고 근거는 어디인가?
- 새 담당자는 무엇부터 보면 되는가?

## 사용자 페르소나
| 사용자 | 목표 | 실패하면 생기는 문제 |
|------|------|------|
| 조직장/팀장 | 운영 상태와 주요 리스크를 빠르게 판단 | 리스크를 늦게 발견하고 의사결정이 지연된다 |
| PM/PO | TODO, Blocked, 의존성을 정리 | 업무 누락, 중복 지시, 일정 지연이 생긴다 |
| 실무자 | AI가 뽑은 항목을 검토하고 수정 | 잘못된 담당자/기한이 확산된다 |
| 신규 담당자 | 맥락과 남은 일을 빠르게 이해 | 인수인계 공백과 반복 질문이 늘어난다 |
| 관리자/보안 담당자 | 데이터 접근과 삭제 가능성을 확인 | 민감정보 노출과 감사 실패 위험이 생긴다 |

## 핵심 사용자 여정
### 1. 팀장의 아침 운영 점검
1. Overview에서 운영 상태와 전일 대비 변화를 본다.
2. Critical risk와 Blocked issue를 확인한다.
3. source evidence를 열어 AI 판단 근거를 확인한다.
4. 필요한 결정을 남기거나 담당자에게 액션을 넘긴다.

성공 기준:
- 1분 안에 top 3 risk를 파악한다.
- 각 risk에 source와 decision needed가 있다.
- 오래된 정보와 최신 정보가 구분된다.

### 2. PM의 TODO/Blocked 정리
1. TODO board에서 owner, due date, source 기준으로 정렬한다.
2. 중복 TODO를 merge한다.
3. 잘못된 owner나 due date를 수정한다.
4. Blocked issue의 required decision을 정리한다.

성공 기준:
- 모든 TODO에 owner 또는 `unassigned` 상태가 있다.
- Blocked issue는 막힌 이유와 다음 액션이 분리되어 있다.
- 수정 내역은 audit trail로 남는다.

### 3. 실무자의 AI 결과 검토
1. Review queue에서 새로 추출된 항목을 본다.
2. 항목별로 confirm, edit, dismiss, merge 중 하나를 선택한다.
3. 틀린 추론은 feedback reason을 남긴다.
4. confirmed 항목만 리포트의 주요 영역에 반영된다.

성공 기준:
- AI 결과를 맹목적으로 확정하지 않는다.
- source-backed fact와 inferred insight가 구분된다.
- 사용자의 수정이 다음 리포트에 반영된다.

### 4. 신규 담당자의 인수인계
1. Handover packet을 연다.
2. 현재 맥락, 남은 작업, 막힌 이슈, 핵심 결정, 주의사항을 읽는다.
3. source evidence로 필요한 원문만 확인한다.
4. 첫날 해야 할 TODO를 확인한다.

성공 기준:
- 인수인계 문서 하나로 첫 행동을 정할 수 있다.
- 관련 source와 담당자 맵이 함께 제공된다.
- stale 정보가 표시된다.

## 핵심 화면
| 화면 | 목적 | 반드시 보여줄 정보 |
|------|------|------|
| Overview | 운영 상태 요약 | health, trend, top risks, blocked count, stale alerts |
| Risks | 위험 관리 | severity, impact, owner, due, source, confidence |
| Blocked | 막힌 이슈 해소 | blocker, required decision, dependency, next action |
| TODO | 실행 항목 관리 | item, owner, due, priority, status, source |
| Knowledge | 조직 지식 축적 | rule, decision, FAQ, source, last confirmed |
| Handover | 인수인계 | context, remaining work, cautions, links, first actions |
| Evidence | 원문 근거 확인 | snippet, source metadata, timestamp, participants |
| Review Queue | AI 결과 검토 | proposed item, confidence, source, review actions |

## AI 결과 검토 액션
| 액션 | 의미 | 결과 |
|------|------|------|
| confirm | AI 추출이 맞다 | `review_status=confirmed` |
| edit | 일부 필드를 수정한다 | 변경 전후가 audit log에 남는다 |
| dismiss | 운영 항목으로 쓰지 않는다 | reason과 함께 숨김 처리된다 |
| merge | 중복 항목을 합친다 | source_refs가 합쳐진다 |
| mark stale | 오래된 정보로 표시한다 | 리포트 우선순위가 낮아진다 |
| open source | 근거 원문을 확인한다 | 판단 근거를 검토한다 |

## 신뢰 UX 원칙
- confidence는 색상만으로 표현하지 않는다. 숫자, 라벨, 근거를 함께 보여준다.
- AI가 추론한 문장은 `inferred`로 표시한다.
- 원문에 명시된 사실은 `source-backed`로 표시한다.
- 출처가 없는 항목은 주요 의사결정 영역에 노출하지 않는다.
- confirmed 되지 않은 항목은 review queue에 먼저 둔다.

## 빈 상태와 실패 상태
| 상태 | 사용자에게 보여줄 메시지 |
|------|------|
| 데이터 없음 | 아직 수집된 운영 기록이 없습니다. fixture 또는 source connector를 추가하세요. |
| 출처 없음 | 이 항목은 근거 source가 없어 검토가 필요합니다. |
| 낮은 confidence | AI가 불확실하게 판단했습니다. 원문을 확인하세요. |
| stale | 최근 source에서 다시 언급되지 않았습니다. 현재 유효한지 확인하세요. |
| blocked | 사용자 결정이나 외부 의존성이 필요합니다. |

## MVP UX 범위
- fixture 기반 Overview report
- TODO/Risk/Blocked/Handover 항목 목록
- source id와 confidence 표시
- review_status 필드 표시
- confirm/edit/dismiss/merge는 데이터 모델과 mock action 수준까지 정의

## MVP 이후
- 역할 기반 보기
- Slack/Notion/Jira deep link
- 알림과 digest
- 사용자 feedback 기반 추출 품질 개선
- 팀별 권한과 데이터 범위 필터
