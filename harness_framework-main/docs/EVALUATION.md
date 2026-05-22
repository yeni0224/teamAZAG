# EVALUATION

## 목적
운영 인텔리전스 제품은 AI가 그럴듯한 요약을 만드는 것만으로 성공할 수 없다. 사용자가 실제 운영 판단에 쓸 수 있을 만큼 정확하고, 출처가 있고, 수정 가능해야 한다.

## 평가 단위
- SourceRecord normalization
- TODO extraction
- Risk extraction
- Blocked issue detection
- Decision extraction
- Knowledge extraction
- Handover packet quality
- Source attribution
- Review workflow usability

## 핵심 지표
| 지표 | 의미 |
|------|------|
| precision | 추출한 항목 중 실제로 맞는 비율 |
| recall | 원문에 있는 항목 중 놓치지 않은 비율 |
| source attribution accuracy | 항목의 근거 source가 맞는 비율 |
| hallucination rate | 근거 없는 항목 비율 |
| owner accuracy | 담당자 추출 정확도 |
| due date accuracy | 기한 추출 정확도 |
| severity agreement | 사람이 판단한 severity와 일치하는 정도 |
| handover usefulness | 신규 담당자가 다음 행동을 정할 수 있는 정도 |

## MVP 통과 기준
MVP에서는 정량 기준을 엄격히 자동화하기보다 fixture 기반 regression을 우선한다.

- 모든 추출 항목에 `source_refs`가 있다.
- source 없는 주요 insight는 실패로 본다.
- TODO fixture에서 owner/due/action을 추출한다.
- Blocked fixture에서 blocked_reason과 required_decision을 구분한다.
- Handover packet에 first_actions가 있다.
- dismissed/edited review event가 다음 report에 반영된다.

## Fixture 설계
좋은 fixture는 쉬운 케이스만 담지 않는다.

포함해야 할 케이스:
- 명시적 TODO
- 암시적 TODO
- 담당자 없는 TODO
- 기한 없는 TODO
- risk지만 blocked는 아닌 항목
- 실제 blocked 항목
- 결정 사항
- 번복된 결정
- 오래되어 stale이 된 정보
- 중복 표현된 같은 업무
- 민감정보 마스킹 케이스

## 사람이 평가할 질문
리포트를 읽은 사용자는 다음 질문에 답할 수 있어야 한다.

- 지금 가장 중요한 위험은 무엇인가?
- 이 위험의 근거는 어디인가?
- 오늘 누가 무엇을 해야 하는가?
- 무엇이 막혔고 어떤 결정이 필요한가?
- 새 담당자가 첫날 해야 할 행동은 무엇인가?

## 실패 유형
| 실패 | 설명 |
|------|------|
| missing source | 근거 없는 항목 생성 |
| wrong owner | 담당자 오추출 |
| wrong due | 기한 오추출 |
| risk inflation | 사소한 내용을 과도한 risk로 판단 |
| blocked confusion | risk와 blocked를 혼동 |
| stale carryover | 오래된 정보를 현재 상태처럼 표시 |
| privacy leak | fixture나 log에 민감정보 노출 |

## 평가 산출물
각 phase는 가능하면 다음 파일을 남긴다.

- fixture input
- expected output
- actual output
- diff or evaluation summary
- known limitations
