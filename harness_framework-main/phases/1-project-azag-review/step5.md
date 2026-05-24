# Step 5: full-stack-integration-and-final-sweep

## 읽어야 할 파일
- `C:\Project_AZAG\README.md`
- `C:\Project_AZAG\PROJECT_CONTEXT.md`
- `C:\Project_AZAG\docs\project-azag-review-map.md`
- `C:\Project_AZAG\app\**/*`
- `C:\Project_AZAG\frontend\**/*`
- `C:\Project_AZAG\docs\**/*`
- `C:\Project_AZAG\db\**/*`
- `C:\Project_AZAG\alembic\**/*`
- 이전 step에서 생성/수정한 파일

## 작업
`app`, `frontend`, `docs`, `db`, `alembic` 전체를 마지막으로 통합 재검토하고 남은 불일치를 수정한다.

1. Step 0-4의 review map 항목이 해결됐는지 확인한다.
2. backend, frontend, docs, SQL, Alembic 사이에 남은 naming/schema/API 불일치를 수정한다.
3. README 또는 docs에 현재 실행/검증 절차가 실제 구조와 맞는지 확인하고 필요한 부분을 갱신한다.
4. 가능한 테스트와 정적 검증을 실행하고, 실행하지 못한 검증은 이유와 후속 조치를 기록한다.
5. `C:\Project_AZAG\docs\project-azag-review-map.md`에 최종 결과, 수정 요약, 남은 리스크를 남긴다.

## Acceptance Criteria

```powershell
python -m compileall C:\Project_AZAG\app C:\Project_AZAG\alembic
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\frontend'"
powershell -NoProfile -Command "Test-Path 'C:\Project_AZAG\docs\project-azag-review-map.md'"
```

## 검증 절차
1. Acceptance Criteria 명령을 실행한다.
2. 프로젝트에 backend/frontend test 또는 build script가 있으면 가능한 범위에서 실행한다.
3. 실패하면 원인을 수정하고 다시 실행한다.
4. 외부 DB, 네트워크, 미설치 의존성 때문에 실행하지 못한 검증은 skipped로 보고하고 남은 수동 검증 절차를 details에 남긴다.

## 금지사항
- 검증 실패를 문서만 고쳐서 숨기지 마라. 이유: 이 step은 통합 품질 확인이 목적이다.
- 실제 운영 데이터나 비밀값을 fixture, prompt, trace에 넣지 마라. 이유: 보안/개인정보 원칙 위반이다.
- `phases/**/index.json` 상태를 직접 바꾸지 마라. 이유: runner 책임이다.
