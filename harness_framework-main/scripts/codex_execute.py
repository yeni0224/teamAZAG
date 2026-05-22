#!/usr/bin/env python3
"""
Codex Harness Step Executor.

Runs phase steps with `codex exec`, stores trace/result artifacts, verifies
Acceptance Criteria commands, and updates phase metadata from the runner side.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import check_dangerous_command as command_policy


ROOT = Path(__file__).resolve().parent.parent
KST = timezone(timedelta(hours=9))


class HarnessError(RuntimeError):
    """Base error for runner-controlled failures."""


@dataclass(frozen=True)
class CommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str
    elapsed_seconds: float

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def stamp() -> str:
    return datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def default_codex_bin() -> str:
    if os.name == "nt" and shutil.which("codex.cmd"):
        return "codex.cmd"
    return "codex"


def run_command(command: str, cwd: Path, timeout: int = 1800) -> CommandResult:
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return CommandResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        elapsed_seconds=time.monotonic() - started,
    )


def strip_inline_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for idx, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_double:
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:idx].rstrip()
    return line.rstrip()


def extract_acceptance_commands(step_text: str) -> list[str]:
    heading = re.search(r"^##\s+Acceptance Criteria\s*$", step_text, flags=re.MULTILINE | re.IGNORECASE)
    if not heading:
        return []

    rest = step_text[heading.end() :]
    next_heading = re.search(r"^##\s+", rest, flags=re.MULTILINE)
    section = rest[: next_heading.start()] if next_heading else rest
    blocks = re.findall(r"```(?:bash|sh|shell|powershell|ps1)?\s*\n(.*?)```", section, flags=re.DOTALL | re.IGNORECASE)

    commands: list[str] = []
    for block in blocks:
        for raw_line in block.splitlines():
            line = strip_inline_comment(raw_line.strip())
            if line:
                commands.append(line)
    return commands

DEFAULT_CODEX_MODEL = "gpt-5.5"


class CodexStepExecutor:
    MAX_RETRIES = 3
    FEAT_MSG = "feat({phase}): step {num} {name}"
    CHORE_MSG = "chore({phase}): step {num} output"

    def __init__(
        self,
        phase_dir_name: str,
        *,
        root: Path = ROOT,
        codex_bin: str | None = None,
        model: str | None = DEFAULT_CODEX_MODEL,
        auto_push: bool = False,
        dry_run: bool = False,
    ):
        self.root = root
        self.phases_dir = root / "phases"
        self.phase_dir = self.phases_dir / phase_dir_name
        self.phase_dir_name = phase_dir_name
        self.index_file = self.phase_dir / "index.json"
        self.top_index_file = self.phases_dir / "index.json"
        self.schema_file = root / "schemas" / "step_result.schema.json"
        self.runs_dir = self.phase_dir / "runs"
        self.codex_bin = codex_bin or default_codex_bin()
        self.model = model
        self.auto_push = auto_push
        self.dry_run = dry_run
        self.git_enabled = self._is_git_repo()

        if not self.phase_dir.is_dir():
            raise HarnessError(f"{self.phase_dir} not found")
        if not self.index_file.exists():
            raise HarnessError(f"{self.index_file} not found")
        if not self.schema_file.exists():
            raise HarnessError(f"{self.schema_file} not found")

        index = read_json(self.index_file)
        self.project = index.get("project", "project")
        self.phase_name = index.get("phase", phase_dir_name)
        self.total = len(index.get("steps", []))

    def run(self) -> None:
        self._print_header()
        self._check_blockers()
        self._checkout_branch()
        self._ensure_created_at()
        self._execute_all_steps()
        self._finalize()

    def _is_git_repo(self) -> bool:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(self.root),
            capture_output=True,
            text=True,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"

    def _run_git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=str(self.root), capture_output=True, text=True)

    def _checkout_branch(self) -> None:
        if not self.git_enabled or self.dry_run:
            print("  Git: skipped")
            return

        branch = f"feat-{self.phase_name}"
        current = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        if current.returncode != 0:
            raise HarnessError(current.stderr.strip() or "git branch check failed")
        if current.stdout.strip() == branch:
            return

        exists = self._run_git("rev-parse", "--verify", branch)
        result = self._run_git("checkout", branch) if exists.returncode == 0 else self._run_git("checkout", "-b", branch)
        if result.returncode != 0:
            raise HarnessError(result.stderr.strip() or f"failed to checkout {branch}")
        print(f"  Branch: {branch}")

    def _commit_step(self, step_num: int, step_name: str) -> None:
        if not self.git_enabled or self.dry_run:
            return

        output_rel = f"phases/{self.phase_dir_name}/runs"
        index_rel = f"phases/{self.phase_dir_name}/index.json"

        self._run_git("add", "-A")
        self._run_git("reset", "HEAD", "--", output_rel)
        self._run_git("reset", "HEAD", "--", index_rel)

        if self._run_git("diff", "--cached", "--quiet").returncode != 0:
            msg = self.FEAT_MSG.format(phase=self.phase_name, num=step_num, name=step_name)
            result = self._run_git("commit", "-m", msg)
            if result.returncode == 0:
                print(f"  Commit: {msg}")
            else:
                print(f"  WARN: code commit failed: {result.stderr.strip()}")

        self._run_git("add", "-A")
        if self._run_git("diff", "--cached", "--quiet").returncode != 0:
            msg = self.CHORE_MSG.format(phase=self.phase_name, num=step_num)
            result = self._run_git("commit", "-m", msg)
            if result.returncode == 0:
                print(f"  Commit: {msg}")
            else:
                print(f"  WARN: metadata commit failed: {result.stderr.strip()}")

    def _load_guardrails(self) -> str:
        sections: list[str] = []
        agents_md = self.root / "AGENTS.md"
        if agents_md.exists():
            sections.append(f"## AGENTS.md\n\n{agents_md.read_text(encoding='utf-8')}")

        legacy = self.root / "CLAUDE.md"
        if legacy.exists():
            sections.append(f"## Legacy CLAUDE.md\n\n{legacy.read_text(encoding='utf-8')}")

        docs_dir = self.root / "docs"
        if docs_dir.is_dir():
            for doc in sorted(docs_dir.glob("*.md")):
                sections.append(f"## docs/{doc.name}\n\n{doc.read_text(encoding='utf-8')}")
        return "\n\n---\n\n".join(sections)

    @staticmethod
    def _build_step_context(index: dict) -> str:
        lines = []
        for step in index.get("steps", []):
            if step.get("status") == "completed" and step.get("summary"):
                lines.append(f"- Step {step['step']} ({step['name']}): {step['summary']}")
        if not lines:
            return ""
        return "## 이전 Step 산출물\n\n" + "\n".join(lines) + "\n"

    def _build_prompt(self, step: dict, previous_error: str | None = None) -> str:
        step_num = step["step"]
        step_file = self.phase_dir / f"step{step_num}.md"
        if not step_file.exists():
            raise HarnessError(f"{step_file} not found")

        index = read_json(self.index_file)
        retry = ""
        if previous_error:
            retry = f"""
## 이전 시도 실패 정보

아래 실패 원인을 반영해 같은 step을 다시 수행하라.

```text
{previous_error}
```
"""

        return f"""
당신은 {self.project} 프로젝트의 Codex 작업자다.

아래 가드레일과 step 지시를 읽고, 현재 step 범위 안에서만 작업하라.
최종 응답은 반드시 제공된 JSON schema에 맞춰 작성하라.
`phases/**/index.json` 상태 변경은 runner가 담당하므로 직접 수정하지 마라.

---

{self._load_guardrails()}

---

{self._build_step_context(index)}
{retry}

---

{step_file.read_text(encoding='utf-8')}
""".strip()

    def _codex_command(self, prompt: str, result_file: Path) -> list[str]:
        command = [
            self.codex_bin,
            "exec",
            "--sandbox",
            "workspace-write",
            "--ask-for-approval",
            "never",
            "--json",
            "--output-schema",
            str(self.schema_file),
            "--output-last-message",
            str(result_file),
            "-C",
            str(self.root),
        ]
        if self.model:
            command.extend(["--model", self.model])
        if not self.git_enabled:
            command.append("--skip-git-repo-check")
        command.append(prompt)
        return command

    def _invoke_codex(self, step: dict, attempt: int, previous_error: str | None) -> dict:
        step_num = step["step"]
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        trace_file = self.runs_dir / f"step{step_num}-attempt{attempt}.jsonl"
        result_file = self.runs_dir / f"step{step_num}-attempt{attempt}-result.json"
        prompt_file = self.runs_dir / f"step{step_num}-attempt{attempt}-prompt.md"
        prompt = self._build_prompt(step, previous_error)
        prompt_file.write_text(prompt, encoding="utf-8")

        if self.dry_run:
            result = {
                "status": "completed",
                "summary": f"dry-run completed step {step_num}",
                "commands": [],
                "details": "Codex invocation skipped because --dry-run was set.",
            }
            write_json(result_file, result)
            trace_file.write_text("", encoding="utf-8")
            return result

        command = self._codex_command(prompt, result_file)
        completed = subprocess.run(command, cwd=str(self.root), capture_output=True, text=True, timeout=3600)
        trace_file.write_text(completed.stdout, encoding="utf-8")

        if completed.stderr:
            (self.runs_dir / f"step{step_num}-attempt{attempt}-stderr.txt").write_text(
                completed.stderr,
                encoding="utf-8",
            )

        if completed.returncode != 0:
            return {
                "status": "error",
                "summary": f"Codex exited with code {completed.returncode}",
                "commands": [],
                "details": completed.stderr[-4000:] if completed.stderr else completed.stdout[-4000:],
            }

        try:
            return read_json(result_file)
        except Exception as exc:
            return {
                "status": "error",
                "summary": "Codex result file could not be parsed",
                "commands": [],
                "details": str(exc),
            }

    def _run_acceptance_criteria(self, step_num: int) -> tuple[bool, list[dict], str]:
        step_file = self.phase_dir / f"step{step_num}.md"
        commands = extract_acceptance_commands(step_file.read_text(encoding="utf-8"))
        if not commands:
            return True, [], "No Acceptance Criteria commands were declared."

        records = []
        failures = []
        for command in commands:
            blocked_pattern = command_policy.find_dangerous_pattern(command)
            if blocked_pattern:
                record = {
                    "command": command,
                    "status": "failed",
                    "returncode": 2,
                    "elapsed_seconds": 0.0,
                    "stdout_tail": "",
                    "stderr_tail": f"Blocked dangerous command matching {blocked_pattern}",
                }
                records.append(record)
                failures.append(record)
                break

            result = run_command(command, self.root)
            record = {
                "command": command,
                "status": "passed" if result.passed else "failed",
                "returncode": result.returncode,
                "elapsed_seconds": round(result.elapsed_seconds, 3),
                "stdout_tail": result.stdout[-2000:],
                "stderr_tail": result.stderr[-2000:],
            }
            records.append(record)
            if not result.passed:
                failures.append(record)
                break

        if failures:
            return False, records, f"Acceptance Criteria failed: {failures[0]['command']}"
        return True, records, "Acceptance Criteria passed."

    def _set_step_status(self, step_num: int, **updates: object) -> None:
        index = read_json(self.index_file)
        for step in index.get("steps", []):
            if step.get("step") == step_num:
                step.update(updates)
                break
        write_json(self.index_file, index)

    def _update_top_index(self, status: str) -> None:
        if not self.top_index_file.exists():
            return
        top = read_json(self.top_index_file)
        timestamp_key = {
            "completed": "completed_at",
            "error": "failed_at",
            "blocked": "blocked_at",
        }.get(status)
        for phase in top.get("phases", []):
            if phase.get("dir") == self.phase_dir_name:
                phase["status"] = status
                if timestamp_key:
                    phase[timestamp_key] = stamp()
                break
        write_json(self.top_index_file, top)

    def _print_header(self) -> None:
        print(f"\n{'=' * 60}")
        print("  Codex Harness Step Executor")
        print(f"  Phase: {self.phase_name} | Steps: {self.total}")
        print(f"  Codex: {self.codex_bin}")
        if self.dry_run:
            print("  Dry-run: enabled")
        print(f"{'=' * 60}")

    def _check_blockers(self) -> None:
        index = read_json(self.index_file)
        for step in reversed(index.get("steps", [])):
            status = step.get("status")
            if status == "error":
                raise HarnessError(f"Step {step['step']} failed: {step.get('error_message', 'unknown')}")
            if status == "blocked":
                raise HarnessError(f"Step {step['step']} blocked: {step.get('blocked_reason', 'unknown')}")
            if status != "pending":
                break

    def _ensure_created_at(self) -> None:
        index = read_json(self.index_file)
        if "created_at" not in index:
            index["created_at"] = stamp()
            write_json(self.index_file, index)

    def _execute_single_step(self, step: dict) -> bool:
        step_num = step["step"]
        step_name = step["name"]
        previous_error = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            print(f"\n  Step {step_num}/{self.total - 1}: {step_name} (attempt {attempt}/{self.MAX_RETRIES})")
            self._set_step_status(step_num, status="running", started_at=stamp())
            result = self._invoke_codex(step, attempt, previous_error)

            if result.get("status") == "blocked":
                self._set_step_status(
                    step_num,
                    status="blocked",
                    blocked_at=stamp(),
                    blocked_reason=result.get("details") or result.get("summary") or "Codex reported blocked.",
                )
                self._update_top_index("blocked")
                raise SystemExit(2)

            if result.get("status") == "completed":
                passed, ac_records, ac_message = self._run_acceptance_criteria(step_num)
                write_json(self.runs_dir / f"step{step_num}-attempt{attempt}-ac.json", {"commands": ac_records})
                if passed:
                    self._set_step_status(
                        step_num,
                        status="completed",
                        completed_at=stamp(),
                        summary=result.get("summary", ""),
                    )
                    self._commit_step(step_num, step_name)
                    print(f"  OK: Step {step_num} completed")
                    return True
                previous_error = ac_message
            else:
                previous_error = result.get("details") or result.get("summary") or "Codex did not complete the step."

            if attempt < self.MAX_RETRIES:
                self._set_step_status(step_num, status="pending", error_message=previous_error)
                print(f"  Retry: {previous_error}")
            else:
                self._set_step_status(
                    step_num,
                    status="error",
                    failed_at=stamp(),
                    error_message=f"[{self.MAX_RETRIES} attempts failed] {previous_error}",
                )
                self._commit_step(step_num, step_name)
                self._update_top_index("error")
                raise SystemExit(1)

        return False

    def _execute_all_steps(self) -> None:
        while True:
            index = read_json(self.index_file)
            pending = next((s for s in index.get("steps", []) if s.get("status") in {"pending", "running"}), None)
            if pending is None:
                print("\n  All steps completed.")
                return
            self._execute_single_step(pending)

    def _finalize(self) -> None:
        index = read_json(self.index_file)
        index["completed_at"] = stamp()
        write_json(self.index_file, index)
        self._update_top_index("completed")

        if self.git_enabled and not self.dry_run:
            self._run_git("add", "-A")
            if self._run_git("diff", "--cached", "--quiet").returncode != 0:
                msg = f"chore({self.phase_name}): mark phase completed"
                result = self._run_git("commit", "-m", msg)
                if result.returncode == 0:
                    print(f"  Commit: {msg}")
            if self.auto_push:
                branch = f"feat-{self.phase_name}"
                result = self._run_git("push", "-u", "origin", branch)
                if result.returncode != 0:
                    raise HarnessError(result.stderr.strip() or "git push failed")
                print(f"  Pushed to origin/{branch}")

        print(f"\n{'=' * 60}")
        print(f"  Phase '{self.phase_name}' completed.")
        print(f"{'=' * 60}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a Codex harness phase")
    parser.add_argument("phase_dir", help="Phase directory name, e.g. 0-mvp")
    parser.add_argument("--push", action="store_true", help="Push branch after completion")
    parser.add_argument("--codex-bin", default=None, help="Codex executable. Defaults to codex.cmd on Windows.")
    parser.add_argument("--model", default=DEFAULT_CODEX_MODEL, help="Optional Codex model override")
    parser.add_argument("--dry-run", action="store_true", help="Skip Codex calls and mark steps completed")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        CodexStepExecutor(
            args.phase_dir,
            codex_bin=args.codex_bin,
            model=args.model,
            auto_push=args.push,
            dry_run=args.dry_run,
        ).run()
        return 0
    except HarnessError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
