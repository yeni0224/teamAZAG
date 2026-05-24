# Step 1: docs-product-and-data-contract-review

## 읽어야 할 파일
- `C:\Project_AZAG\README.md`
- `C:\Project_AZAG\PROJECT_CONTEXT.md`
- `C:\Project_AZAG\docs\project-azag-review-map.md`
- `C:\Project_AZAG\docs\PRD.md`
- `C:\Project_AZAG\docs\db-design-v2.md`
- `C:\Project_AZAG\docs\table-definition.md`
- `C:\Project_AZAG\docs\teamazag-functions-v3.md`
- `C:\Project_AZAG\docs\team-memory-erd.mmd`
- `C:\Project_AZAG\docs\erd-split\**/*`
- 이전 step에서 생성/수정한 파일

## 작업
문서와 제품/데이터 계약을 재검토하고, 이후 코드 수정이 따라야 할 단일 기준을 만든다.

1. PRD, 기능 문서, DB 설계 문서, table definition, ERD 사이의 불일치를 찾는다.
2. table 이름, column 이름, enum/status 값, 관계, nullable/default 정책을 정리한다.
3. `app`, `db`, `alembic`, `frontend`가 따라야 할 API/data contract를 문서에 명확히 남긴다.
4. 오래된 내용, 중복 설명, 모순된 스키마 설명을 수정한다.
5. 수정 내역과 남은 위험을 `C:\Project_AZAG\docs\project-azag-review-map.md`에 갱신한다.

## Acceptance Criteria

```powershell
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\PRD.md'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\db-design-v2.md'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\table-definition.md'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\project-azag-review-map.md'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 문서 간 충돌이 남아 있으면 근거 파일을 다시 읽고 하나의 기준으로 수정한다.
3. 코드 수정이 필요한 사항은 review map에 다음 step 작업으로 연결한다.

## 금지사항
- 문서 기준 없이 `db`, `alembic`, `app`, `frontend`를 먼저 크게 바꾸지 마라. 이유: 계약이 흔들리면 이후 step 검증이 어려워진다.
- 실제 조직 데이터 예시를 추가하지 마라. 이유: 보안/개인정보 원칙 위반이다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
