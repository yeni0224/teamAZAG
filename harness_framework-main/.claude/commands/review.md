이 프로젝트의 변경 사항을 리뷰하라.

먼저 다음 문서를 읽어라.

- `AGENTS.md`
- `README.md`
- `docs/PRODUCT.md`
- `docs/PRODUCT_UX.md`
- `docs/DATA_MODEL.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/EVALUATION.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR.md`
- `docs/HARNESS.md`
- `docs/HARNESS_UX.md`
- `docs/TROUBLESHOOTING.md`

그 다음 변경된 파일을 확인하고 아래 기준으로 검토하라.

## 체크리스트

1. **Codex 기준 준수**: 새 작업이 `AGENTS.md`와 `docs/HARNESS.md`를 따르는가?
2. **UX 기준 준수**: 제품 작업이 `docs/PRODUCT_UX.md`, 하네스 작업이 `docs/HARNESS_UX.md`를 따르는가?
3. **데이터 모델 준수**: insight가 source_refs, confidence, review_status를 고려하는가?
4. **보안 기준 준수**: 실제 비밀값이나 조직 데이터가 로그/fixture에 남지 않는가?
5. **책임 분리**: Codex step 세션과 runner의 책임이 섞이지 않았는가?
6. **상태 관리**: `phases/**/index.json` 상태 변경을 runner가 담당하도록 되어 있는가?
7. **검증 가능성**: Acceptance Criteria가 실제 실행 가능한 명령인가?
8. **테스트**: runner 또는 문서 규칙 변경에 맞는 테스트가 있는가?
9. **호환성**: 기존 Claude legacy 파일을 불필요하게 깨뜨리지 않았는가?

## 출력 형식

| 항목 | 결과 | 비고 |
|------|------|------|
| Codex 기준 준수 | OK/FAIL | 상세 |
| UX 기준 준수 | OK/FAIL | 상세 |
| 데이터 모델 준수 | OK/FAIL | 상세 |
| 보안 기준 준수 | OK/FAIL | 상세 |
| 책임 분리 | OK/FAIL | 상세 |
| 상태 관리 | OK/FAIL | 상세 |
| 검증 가능성 | OK/FAIL | 상세 |
| 테스트 | OK/FAIL | 상세 |
| 호환성 | OK/FAIL | 상세 |

위반 사항이 있으면 파일 경로와 수정 방향을 구체적으로 제시하라.
