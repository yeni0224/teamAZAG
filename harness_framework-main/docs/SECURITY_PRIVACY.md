# SECURITY AND PRIVACY

## 목적
운영 인텔리전스 시스템은 조직의 실제 운영 기록을 다룬다. 따라서 기능 구현보다 먼저 데이터 최소화, 출처 추적, 접근 통제, 삭제 가능성을 전제로 설계해야 한다.

## 데이터 분류
| 등급 | 예시 | 처리 원칙 |
|------|------|------|
| public | 공개 문서 | 제한 없음 |
| internal | 내부 회의록, 업무 문서 | 기본 처리 대상 |
| confidential | 고객명, 계약, 재무, 인사 정보 | 마스킹 또는 제한 처리 |
| secret | API key, password, token | 저장 금지, 로그 출력 금지 |

## 개발 원칙
- MVP는 실제 조직 데이터 대신 fixture만 사용한다.
- trace, prompt, result, AC log에 secret이 남지 않아야 한다.
- 원문 전체 저장보다 필요한 snippet과 source reference를 우선한다.
- 사용자가 삭제해야 하는 데이터는 record id 기준으로 추적 가능해야 한다.
- source-backed insight와 inferred insight를 분리한다.

## 마스킹 기준
| 데이터 | 처리 |
|------|------|
| API key/token/password | 저장 금지, 발견 시 즉시 blocked |
| 개인 전화번호/이메일 | fixture에서는 가명 처리 |
| 고객명 | fixture에서는 `customer-a`처럼 대체 |
| 인사/평가 정보 | MVP 입력에서 제외 |
| 계약/금액 정보 | confidential로 표시하고 요약 제한 |

## 접근 권한 원칙
MVP에서는 실제 권한 시스템을 구현하지 않더라도 모델에 다음 개념을 둔다.

- 사용자 역할: `admin`, `manager`, `member`, `viewer`
- source 접근 범위: 팀, 프로젝트, 문서 단위
- insight 접근은 원문 source 접근 권한을 넘을 수 없다.
- 인수인계 packet은 포함된 source 중 가장 높은 민감도 등급을 상속한다.

## 로그와 보존
- `phases/**/runs/`에는 개발 실행 로그가 남는다.
- 실제 운영 데이터는 runs 로그에 포함하지 않는다.
- fixture에는 민감정보를 넣지 않는다.
- 로그 보존 기간은 제품 운영 단계에서 별도 정책으로 정한다.

## 삭제 요구
삭제 가능한 단위:
- source record
- insight item
- review event
- generated report

삭제 시 고려사항:
- insight가 여러 source를 참조하면 삭제된 source_ref만 제거한다.
- source가 모두 삭제된 insight는 review queue로 되돌리거나 숨긴다.
- audit log는 개인정보 없는 최소 이벤트만 남긴다.

## 보안 UX
사용자에게 보안 상태를 숨기지 않는다.

- 민감도 라벨을 표시한다.
- source 접근 불가 항목은 이유를 보여준다.
- 마스킹된 값은 복원 가능한 것처럼 보이지 않게 한다.
- export 전 민감정보 포함 여부를 경고한다.

## Blocked 조건
다음 상황은 구현 step에서 `blocked`로 보고한다.

- 실제 API key가 필요하다.
- 실제 조직 데이터 접근이 필요하다.
- 민감정보 처리 정책 없이 저장 구조를 결정해야 한다.
- 외부 서비스 권한 범위가 불명확하다.
