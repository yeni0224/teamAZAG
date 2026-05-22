# TROUBLESHOOTING

## 빠른 진단 순서
1. Codex 자체 상태를 확인한다.

```powershell
codex.cmd doctor
```

2. runner 도움말을 확인한다.

```powershell
python scripts\codex_execute.py --help
```

3. dry-run으로 phase 구조를 확인한다.

```powershell
python scripts\codex_execute.py 0-demo --dry-run
```

4. runner 단위 테스트를 실행한다.

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

## Codex auth 실패
증상:
- `codex doctor`에서 auth fail
- 실제 `codex exec`가 인증 오류로 실패

해결:
```powershell
codex.cmd login
codex.cmd doctor
```

API key 방식이 필요한 경우에는 팀 보안 정책을 먼저 확인한다. 키를 문서나 로그에 쓰지 않는다.

## 네트워크 실패
증상:
- WebSocket 또는 provider endpoint reachability 실패
- VPN, proxy, firewall 오류

해결:
- 회사 VPN 또는 방화벽 정책을 확인한다.
- `codex doctor`의 Connectivity 섹션을 확인한다.
- 네트워크가 막혀 있으면 step 결과는 `blocked`로 남긴다.

## phase 없음
증상:
```text
phases/{phase} not found
```

확인:
- `phases/index.json`에 phase가 있는지 확인한다.
- `phases/{phase}/index.json`이 있는지 확인한다.
- `phases/{phase}/stepN.md` 파일이 있는지 확인한다.

## Acceptance Criteria 실패
확인할 파일:
```text
phases/{phase}/runs/stepN-attemptM-ac.json
phases/{phase}/runs/stepN-attemptM-stderr.txt
```

해결:
- 실패한 command를 직접 실행한다.
- 테스트가 잘못된 것인지 코드가 잘못된 것인지 분리한다.
- 수정 후 runner를 다시 실행한다.

`stderr_tail`에 `Blocked dangerous command`가 있으면 AC 명령이 위험 명령 정책에 걸린 것이다. step 파일의 Acceptance Criteria를 안전한 검증 명령으로 바꾸거나, 실제로 필요한 파괴적 작업이라면 사용자 승인 절차가 있는 별도 수동 작업으로 분리한다.

## Hook 실패
확인할 파일:
```text
.codex/hooks.json
.claude/settings.json
scripts/check_dangerous_command.py
scripts/test_hooks.py
```

검증:
```powershell
python -m json.tool .codex\hooks.json
python -m json.tool .claude\settings.json
python -m unittest scripts.test_hooks -v
```

증상과 대응:
- 안전한 명령이 차단된다: `scripts/test_hooks.py`에 재현 케이스를 추가한 뒤 pattern을 좁힌다.
- 위험한 명령이 통과한다: 재현 케이스를 추가한 뒤 `scripts/check_dangerous_command.py`의 pattern을 보강한다.
- hook 파일 JSON 파싱이 실패한다: trailing comma, quote escaping, command 문자열을 확인한다.

## result JSON 파싱 실패
증상:
- Codex가 schema에 맞는 최종 JSON을 쓰지 못했다.

해결:
- `stepN-attemptM-result.json`을 확인한다.
- `stepN-attemptM-prompt.md`에서 최종 응답 지시가 들어갔는지 확인한다.
- 필요하면 step 파일의 결과 요구사항을 더 구체화한다.

## blocked 발생
증상:
- `blocked_reason`이 index에 기록됨

해결:
1. `blocked_reason`을 읽고 사용자 개입 사항을 해결한다.
2. `phases/{phase}/index.json`에서 해당 step의 `status`를 `pending`으로 바꾼다.
3. `blocked_reason`을 삭제한다.
4. runner를 다시 실행한다.

## error 발생
해결:
1. `error_message`와 runs 로그를 확인한다.
2. 원인을 수정한다.
3. 해당 step의 `status`를 `pending`으로 바꾼다.
4. `error_message`를 삭제한다.
5. runner를 다시 실행한다.

## 전체 테스트 discovery 실패
현재 `scripts/test_execute.py`는 legacy Claude runner 테스트이며 `pytest`가 필요하다. `pytest`가 없으면 기본 `unittest discover` 검증에서 skipped로 표시된다.

기본 검증 명령:
```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

전체 테스트 discovery를 목표로 하려면 legacy 테스트를 `unittest`로 변환하거나 별도 optional test로 분리한다.

## 실제 데이터가 로그에 남은 경우
1. 즉시 작업을 중단한다.
2. 어떤 파일에 남았는지 확인한다.
3. 사용자에게 알리고 삭제/마스킹 방침을 확인한다.
4. 해당 데이터를 fixture로 대체한다.

`git reset --hard` 같은 파괴적 명령으로 처리하지 않는다.
