# Step 2: db-and-alembic-consistency-review

## 읽어야 할 파일
- `C:\Project_AZAG\docs\project-azag-review-map.md`
- `C:\Project_AZAG\docs\db-design-v2.md`
- `C:\Project_AZAG\docs\table-definition.md`
- `C:\Project_AZAG\db\schema.postgresql.sql`
- `C:\Project_AZAG\db\seed.postgresql.sql`
- `C:\Project_AZAG\db\verify.postgresql.sql`
- `C:\Project_AZAG\db\dashboard-queries.postgresql.sql`
- `C:\Project_AZAG\db\apply-local-teamazag.ps1`
- `C:\Project_AZAG\alembic.ini`
- `C:\Project_AZAG\alembic\env.py`
- `C:\Project_AZAG\alembic\versions\**/*`
- 이전 step에서 생성/수정한 파일

## 작업
DB SQL 산출물과 Alembic migration이 문서의 데이터 계약과 일치하도록 검토하고 수정한다.

1. `schema.postgresql.sql`, seed, verify, dashboard query가 같은 table/column 계약을 쓰는지 확인한다.
2. Alembic env와 versions가 SQL schema 및 `app.models`와 충돌하지 않는지 확인한다.
3. migration 순서, revision id, downgrade 가능성, 누락된 index/constraint/default를 점검한다.
4. SQL과 Alembic 중 한쪽만 수정하지 말고, 필요한 경우 양쪽과 문서를 함께 맞춘다.
5. DB 관련 변경과 남은 위험을 `C:\Project_AZAG\docs\project-azag-review-map.md`에 갱신한다.

## Acceptance Criteria

```powershell
python -m compileall C:\Project_AZAG\alembic
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\db\schema.postgresql.sql'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\db\verify.postgresql.sql'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\alembic\env.py'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. SQL 실행 환경이 있으면 `db\apply-local-teamazag.ps1` 또는 프로젝트 README의 로컬 DB 검증 절차도 실행한다.
3. DB 접속 정보나 로컬 PostgreSQL 부재로 실행할 수 없으면 blocked가 아니라 skipped command로 보고하고, 정적 검토 결과를 details에 남긴다.

## 금지사항
- 운영 DB나 외부 DB에 접속하지 마라. 이유: 이 phase는 로컬 재검토용이다.
- schema와 migration을 서로 다르게 방치하지 마라. 이유: 배포와 로컬 재현성이 깨진다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
