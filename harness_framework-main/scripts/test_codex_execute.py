from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent))
import codex_execute as cx


class CodexExecuteTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self._make_harness(self.root)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _make_harness(self, root: Path) -> None:
        (root / "docs").mkdir()
        (root / "schemas").mkdir()
        (root / "phases" / "0-demo").mkdir(parents=True)

        (root / "AGENTS.md").write_text("# Rules\n- stay scoped\n", encoding="utf-8")
        (root / "CLAUDE.md").write_text("# Legacy\n- old rule\n", encoding="utf-8")
        (root / "docs" / "HARNESS.md").write_text("# Harness\nrunner owns state\n", encoding="utf-8")
        (root / "schemas" / "step_result.schema.json").write_text("{}", encoding="utf-8")

        top_index = {"phases": [{"dir": "0-demo", "status": "pending"}]}
        (root / "phases" / "index.json").write_text(json.dumps(top_index), encoding="utf-8")

        phase_index = {
            "project": "Demo",
            "phase": "demo",
            "steps": [
                {"step": 0, "name": "first", "status": "pending"},
            ],
        }
        (root / "phases" / "0-demo" / "index.json").write_text(json.dumps(phase_index), encoding="utf-8")
        (root / "phases" / "0-demo" / "step0.md").write_text(
            """# Step 0: first

## 작업
Do a tiny task.

## Acceptance Criteria

```bash
python --version
```
""",
            encoding="utf-8",
        )

    def test_extract_acceptance_commands_removes_comments(self):
        text = """# Step

## Acceptance Criteria

```bash
npm run build # compile
npm test
```

## Next
"""
        self.assertEqual(cx.extract_acceptance_commands(text), ["npm run build", "npm test"])

    def test_extract_acceptance_commands_keeps_escaped_hash_in_quotes(self):
        text = r"""# Step

## Acceptance Criteria

```bash
python -c "print(\"# not a comment\")" # comment
```
"""
        self.assertEqual(cx.extract_acceptance_commands(text), ['python -c "print(\\"# not a comment\\")"'])

    def test_build_step_context_includes_completed_summary(self):
        index = {
            "steps": [
                {"step": 0, "name": "setup", "status": "completed", "summary": "created app"},
                {"step": 1, "name": "ui", "status": "pending"},
            ]
        }
        result = cx.CodexStepExecutor._build_step_context(index)
        self.assertIn("Step 0 (setup): created app", result)
        self.assertNotIn("ui", result)

    def test_prompt_includes_guardrails_and_step(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        prompt = executor._build_prompt({"step": 0, "name": "first"})
        self.assertIn("AGENTS.md", prompt)
        self.assertIn("runner owns state", prompt)
        self.assertIn("Do a tiny task", prompt)
        self.assertIn("직접 수정하지 마라", prompt)

    def test_codex_command_uses_skip_git_when_not_repo(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, codex_bin="codex.cmd")
        command = executor._codex_command("prompt", self.root / "result.json")
        self.assertEqual(command[:2], ["codex.cmd", "exec"])
        self.assertIn("--json", command)
        self.assertIn("--model", command)
        self.assertIn("gpt-5.5", command)
        self.assertIn("--skip-git-repo-check", command)

    def test_dry_run_writes_result_and_prompt(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        result = executor._invoke_codex({"step": 0, "name": "first"}, 1, None)
        self.assertEqual(result["status"], "completed")
        self.assertTrue((self.root / "phases" / "0-demo" / "runs" / "step0-attempt1-result.json").exists())
        self.assertTrue((self.root / "phases" / "0-demo" / "runs" / "step0-attempt1-prompt.md").exists())

    def test_acceptance_criteria_runner_records_success(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        passed, records, message = executor._run_acceptance_criteria(0)
        self.assertTrue(passed)
        self.assertEqual(records[0]["status"], "passed")
        self.assertEqual(message, "Acceptance Criteria passed.")

    def test_acceptance_criteria_blocks_dangerous_command(self):
        (self.root / "phases" / "0-demo" / "step0.md").write_text(
            """# Step 0: first

## Acceptance Criteria

```bash
rm -fr build
```
""",
            encoding="utf-8",
        )
        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        passed, records, message = executor._run_acceptance_criteria(0)
        self.assertFalse(passed)
        self.assertEqual(records[0]["returncode"], 2)
        self.assertIn("dangerous command", records[0]["stderr_tail"])
        self.assertIn("Acceptance Criteria failed", message)

    def test_single_step_dry_run_updates_index(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        executor._execute_single_step({"step": 0, "name": "first", "status": "pending"})

        index = json.loads((self.root / "phases" / "0-demo" / "index.json").read_text(encoding="utf-8"))
        step = index["steps"][0]
        self.assertEqual(step["status"], "completed")
        self.assertIn("completed_at", step)
        self.assertIn("dry-run completed", step["summary"])

    def test_run_resumes_running_step(self):
        index_file = self.root / "phases" / "0-demo" / "index.json"
        index = json.loads(index_file.read_text(encoding="utf-8"))
        index["steps"][0]["status"] = "running"
        index_file.write_text(json.dumps(index), encoding="utf-8")

        executor = cx.CodexStepExecutor("0-demo", root=self.root, dry_run=True)
        executor._execute_all_steps()

        index = json.loads(index_file.read_text(encoding="utf-8"))
        self.assertEqual(index["steps"][0]["status"], "completed")

    def test_invoke_codex_nonzero_returns_error(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root, codex_bin="codex.cmd")
        completed = subprocess.CompletedProcess(args=["codex"], returncode=42, stdout="{}", stderr="bad")

        with patch("subprocess.run", return_value=completed):
            result = executor._invoke_codex({"step": 0, "name": "first"}, 1, None)

        self.assertEqual(result["status"], "error")
        self.assertIn("42", result["summary"])

    def test_checkout_branch_skips_when_not_git(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root)
        executor._checkout_branch()

    def test_checkout_branch_uses_existing_branch(self):
        executor = cx.CodexStepExecutor("0-demo", root=self.root)
        executor.git_enabled = True
        executor._run_git = MagicMock(
            side_effect=[
                MagicMock(returncode=0, stdout="main\n", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=""),
            ]
        )

        executor._checkout_branch()
        self.assertEqual(executor._run_git.call_args_list[-1].args, ("checkout", "feat-demo"))


if __name__ == "__main__":
    unittest.main()
