# DATA MODEL

## 목적
운영 인텔리전스 제품의 모든 추출 결과는 공통 필드를 가져야 한다. 그래야 출처 확인, 사용자 검토, 중복 병합, 인수인계 재사용이 가능하다.

## 공통 원칙
- 모든 item은 `id`와 `source_refs`를 가진다.
- AI 추론 여부는 `inferred`로 표시한다.
- 사용자 검토 상태는 `review_status`로 관리한다.
- 신뢰도는 `confidence`로 표시하되 의사결정은 source evidence와 함께 한다.
- owner나 due date를 모르면 빈 문자열이 아니라 `unassigned`, `unknown` 같은 명시 상태를 쓴다.

## SourceRecord
```json
{
  "record_id": "rec-001",
  "source_type": "meeting_note",
  "title": "Weekly Ops Sync",
  "author": "fixture-user",
  "participants": ["ops-lead", "pm"],
  "created_at": "2026-05-21T09:00:00+09:00",
  "content": "...",
  "source_ref": "fixtures/meeting-001.md",
  "sensitivity": "internal"
}
```

## 공통 Insight 필드
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 항목 고유 id |
| `type` | string | `status`, `risk`, `todo`, `blocked`, `decision`, `knowledge`, `handover` |
| `title` | string | 사람이 읽는 짧은 제목 |
| `summary` | string | 핵심 설명 |
| `source_refs` | array | 근거 record id와 snippet 위치 |
| `confidence` | number | 0.0부터 1.0까지 |
| `inferred` | boolean | AI 추론 여부 |
| `review_status` | string | `proposed`, `confirmed`, `edited`, `dismissed`, `stale` |
| `created_at` | string | 생성 시각 |
| `last_seen_at` | string | 마지막으로 source에서 확인된 시각 |

## Risk
```json
{
  "id": "risk-001",
  "type": "risk",
  "title": "릴리즈 일정 지연 가능성",
  "severity": "high",
  "impact": "고객 공지 일정 지연",
  "owner": "pm",
  "due_date": "2026-05-24",
  "mitigation": "결정권자 승인 필요",
  "source_refs": [{ "record_id": "rec-001", "quote_id": "q1" }],
  "confidence": 0.82,
  "inferred": true,
  "review_status": "proposed"
}
```

## TODO
필수 필드:
- `owner`
- `due_date`
- `priority`
- `status`
- `source_refs`

상태 값:
- `open`
- `in_progress`
- `blocked`
- `done`
- `dismissed`

## Blocked Issue
필수 필드:
- `blocked_reason`
- `required_decision`
- `dependency`
- `owner`
- `next_action`
- `source_refs`

Blocked는 단순 risk가 아니다. 이미 진행을 막고 있는 구체적 장애가 있어야 한다.

## Decision
필수 필드:
- `decision`
- `decider`
- `decided_at`
- `rationale`
- `source_refs`

## Knowledge
필수 필드:
- `topic`
- `content`
- `applicability`
- `last_confirmed_at`
- `source_refs`

## Handover Packet
필수 섹션:
- `current_context`
- `remaining_work`
- `blocked_items`
- `key_decisions`
- `cautions`
- `first_actions`
- `source_refs`

## Review Event
사용자가 AI 결과를 검토할 때 남기는 이벤트다.

```json
{
  "event_id": "rev-001",
  "item_id": "risk-001",
  "action": "edit",
  "actor": "pm",
  "changed_fields": ["owner", "severity"],
  "reason": "담당자가 잘못 추출됨",
  "created_at": "2026-05-21T10:00:00+09:00"
}
```

## 필드 품질 규칙
- `source_refs`가 비어 있으면 `review_status`는 `proposed`를 넘을 수 없다.
- `confidence < 0.6`이면 review queue에 먼저 노출한다.
- `last_seen_at`이 오래된 항목은 stale 후보로 표시한다.
- dismissed 항목은 삭제하지 않고 reason을 보존한다.
