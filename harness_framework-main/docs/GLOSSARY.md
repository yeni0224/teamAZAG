# GLOSSARY

## 목적
운영 인텔리전스 시스템에서 쓰는 용어를 명확히 정의한다. 용어가 흐리면 AI 추출 기준과 UX가 흔들린다.

## 용어
| 용어 | 정의 | 구분 기준 |
|------|------|------|
| 운영 상태 | 현재 업무/조직 운영의 건강도와 변화 요약 | 여러 source를 종합한 현재 상태 |
| TODO | 누군가 실행해야 하는 구체적 작업 | action, owner 또는 owner 후보, 기한 또는 우선순위가 있음 |
| Risk | 앞으로 문제가 될 가능성이 있는 위험 | 아직 막히지는 않았지만 영향이 예상됨 |
| Blocked 이슈 | 이미 진행을 막고 있는 문제 | required decision 또는 dependency가 있음 |
| Decision | 명시적으로 내려진 결정 | decider, decided_at, rationale이 있으면 좋음 |
| 조직 지식 | 반복적으로 재사용 가능한 규칙, 노하우, 맥락 | 단일 TODO가 아니라 미래 업무에 재사용됨 |
| 인수인계 정보 | 새 담당자가 이어받기 위한 요약 | 현재 맥락, 남은 일, 주의사항, source가 포함됨 |
| SourceRecord | 메일, 채팅, 회의록, 문서에서 정규화된 원문 단위 | 모든 insight의 근거 |
| SourceRef | insight가 참조하는 원문 위치 | record id, snippet, quote id |
| Confidence | AI가 추출 결과를 신뢰하는 정도 | source 검토를 대체하지 않음 |
| Inferred | 원문에 직접 없고 AI가 추론한 정보 | UI에서 명시 표시 필요 |
| Review Status | 사용자가 AI 결과를 검토한 상태 | proposed, confirmed, edited, dismissed, stale |
| Handover Packet | 인수인계를 위한 묶음 리포트 | first actions가 있어야 함 |
| Stale | 최신 source에서 다시 확인되지 않은 정보 | 현재 유효성 검토 필요 |

## Risk와 Blocked 차이
Risk:
- 문제가 될 가능성이 있다.
- 아직 업무를 직접 멈추지는 않았다.
- 예: “승인이 늦어지면 릴리즈가 지연될 수 있음”

Blocked:
- 이미 진행이 멈췄다.
- 필요한 결정이나 외부 의존성이 있다.
- 예: “보안 승인 없이는 배포할 수 없음”

## TODO와 Decision 차이
TODO:
- 앞으로 해야 할 행동이다.
- 예: “PM이 금요일까지 고객 공지 초안을 작성한다.”

Decision:
- 이미 결정된 사항이다.
- 예: “릴리즈 범위에서 관리자 기능은 제외하기로 결정했다.”

## 조직 지식과 인수인계 차이
조직 지식:
- 여러 번 재사용 가능한 지식이다.
- 예: “장애 공지는 30분 내 1차 공유한다.”

인수인계:
- 특정 시점의 담당자 전환을 돕는 패키지다.
- 예: “현재 배포는 QA 승인 대기 중이고, 다음 행동은 보안 리뷰 요청이다.”
