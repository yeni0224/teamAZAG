# Step 4: frontend-review-and-fixes

## 읽어야 할 파일
- `C:\Project_AZAG\README.md`
- `C:\Project_AZAG\PROJECT_CONTEXT.md`
- `C:\Project_AZAG\docs\project-azag-review-map.md`
- `C:\Project_AZAG\docs\PRD.md`
- `C:\Project_AZAG\docs\teamazag-functions-v3.md`
- `C:\Project_AZAG\app\main.py`
- `C:\Project_AZAG\frontend\**/*` if it exists
- `C:\Project_AZAG\opsradar_v2\**/*` only if it is relevant context for frontend/API behavior
- 이전 step에서 생성/수정한 파일

## 작업
Project AZAG frontend를 재검토하고 backend/API 계약에 맞게 수정한다.

1. `C:\Project_AZAG\frontend`가 있으면 해당 앱의 package, routing, API client, 주요 화면, 상태 처리를 검토한다.
2. `frontend`가 없으면 `C:\Project_AZAG` 안에서 실제 frontend 위치를 찾고, 없다는 것이 확인되면 `C:\Project_AZAG\frontend`에 최소 실행 가능한 frontend scaffold를 만든다.
3. 화면은 PRD의 핵심 사용자 흐름과 `app.main`의 API response shape를 기준으로 맞춘다.
4. 깨진 import, 실행 불가한 script, API endpoint 불일치, 빈 화면 원인을 수정한다.
5. frontend 변경과 남은 위험을 `C:\Project_AZAG\docs\project-azag-review-map.md`에 갱신한다.

## Acceptance Criteria

```powershell
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\frontend'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\project-azag-review-map.md'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. frontend package가 있으면 install이 필요한지 확인하고, 이미 의존성이 준비되어 있으면 build/test 명령을 실행한다.
3. 네트워크나 의존성 설치가 필요해 실행할 수 없으면 blocked로 멈추지 말고 skipped command로 보고하며, 생성/수정한 파일과 남은 실행 조건을 details에 남긴다.

## 금지사항
- 사용자가 요청하지 않은 대형 UI 재설계를 하지 마라. 이유: 이 step은 재검토와 기능 복구가 목적이다.
- backend API 계약을 확인하지 않고 mock 데이터만으로 화면을 맞추지 마라. 이유: 통합 step에서 깨진다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
