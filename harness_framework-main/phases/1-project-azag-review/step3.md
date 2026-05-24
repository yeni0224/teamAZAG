# Step 3: backend-app-review-and-fixes

## 읽어야 할 파일
- `C:\Project_AZAG\README.md`
- `C:\Project_AZAG\PROJECT_CONTEXT.md`
- `C:\Project_AZAG\requirements.txt`
- `C:\Project_AZAG\docs\project-azag-review-map.md`
- `C:\Project_AZAG\docs\PRD.md`
- `C:\Project_AZAG\docs\db-design-v2.md`
- `C:\Project_AZAG\app\database.py`
- `C:\Project_AZAG\app\main.py`
- `C:\Project_AZAG\app\models.py`
- `C:\Project_AZAG\app\__init__.py`
- `C:\Project_AZAG\db\**/*`
- `C:\Project_AZAG\alembic\**/*`
- 이전 step에서 생성/수정한 파일

## 작업
FastAPI/backend app을 문서와 DB 계약에 맞춰 재검토하고 수정한다.

1. `app.models`가 DB schema/Alembic migration과 일치하는지 확인한다.
2. `app.database`의 engine/session 설정, 환경변수 처리, import 안정성을 점검한다.
3. `app.main`의 route, response shape, error handling, CORS, startup 동작이 PRD 및 frontend 계약과 맞는지 확인한다.
4. 명백한 런타임 오류, 깨진 import, 타입/스키마 불일치를 수정한다.
5. backend 변경과 남은 위험을 `C:\Project_AZAG\docs\project-azag-review-map.md`에 갱신한다.

## Acceptance Criteria

```powershell
python -m compileall C:\Project_AZAG\app
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\app\main.py'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\app\models.py'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 테스트가 존재하면 프로젝트 README 기준으로 backend 테스트도 실행한다.
3. 외부 서비스나 DB 부재로 실행할 수 없는 검증은 skipped command로 보고하고 대체 정적 검토 결과를 details에 남긴다.

## 금지사항
- DB 계약과 문서를 업데이트하지 않은 채 response/model 이름을 임의로 바꾸지 마라. 이유: frontend와 migration step에 영향을 준다.
- 비밀값을 코드에 하드코딩하지 마라. 이유: 보안 원칙 위반이다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
