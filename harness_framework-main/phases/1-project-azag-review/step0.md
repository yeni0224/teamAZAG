# Step 0: project-inventory-and-review-map

## 읽어야 할 파일
- `C:\Project_AZAG\README.md`
- `C:\Project_AZAG\PROJECT_CONTEXT.md`
- `C:\Project_AZAG\requirements.txt`
- `C:\Project_AZAG\alembic.ini`
- `C:\Project_AZAG\app\**/*`
- `C:\Project_AZAG\frontend\**/*` if it exists
- `C:\Project_AZAG\docs\**/*`
- `C:\Project_AZAG\db\**/*`
- `C:\Project_AZAG\alembic\**/*`

## 작업
Project AZAG 전체 재검토를 시작하기 위한 inventory와 review map을 만든다.

1. `C:\Project_AZAG`의 `app`, `frontend`, `docs`, `db`, `alembic` 상태를 확인한다.
2. `frontend`가 없으면 실제 프론트엔드가 다른 위치에 있는지 먼저 찾고, 없다는 사실을 review note에 명확히 기록한다.
3. 제품 문서, DB 설계, Alembic migration, FastAPI app, frontend 사이의 주요 계약을 목록화한다.
4. 즉시 수정 가능한 깨진 경로, 오래된 명령, 명백한 문서 불일치를 수정한다.
5. `C:\Project_AZAG\docs\project-azag-review-map.md`를 생성하거나 갱신해 이후 step이 따라갈 점검 목록을 남긴다.

## Acceptance Criteria

```powershell
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\app'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\db'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\alembic'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\project-azag-review-map.md'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 실패하면 누락된 inventory 산출물이나 경로 확인 문제를 수정하고 다시 실행한다.
3. `frontend`가 없어서 생성 여부 판단이 필요하면 review map에 근거를 남기고 다음 step으로 넘긴다.

## 금지사항
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
- 실제 비밀값, 로컬 DB 비밀번호, 운영 데이터를 문서나 로그에 남기지 마라. 이유: 보안/개인정보 원칙 위반이다.
- 전체 리팩터링을 이 step에서 수행하지 마라. 이유: 이 step은 inventory와 review map 작성이 목적이다.
