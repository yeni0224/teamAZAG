from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import check_dangerous_command as hook

ROOT = Path(__file__).resolve().parent.parent


class HookPolicyTests(unittest.TestCase):
    def run_hook(self, payload: dict | None = None, env: dict[str, str] | None = None) -> tuple[int, str]:
        stdin = json.dumps(payload) if payload is not None else ""
        stderr = io.StringIO()
        env_patch = {
            "CODEX_TOOL_INPUT": "",
            "CLAUDE_TOOL_INPUT": "",
        }
        if env:
            env_patch.update(env)

        with patch.dict(os.environ, env_patch, clear=False):
            with patch("sys.stdin", io.StringIO(stdin)):
                with redirect_stderr(stderr):
                    code = hook.main()
        return code, stderr.getvalue()

    def test_allows_safe_codex_bash_command(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": 'python -m unittest discover -s scripts -p "test_*.py" -v'},
            }
        )
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")

    def test_blocks_git_reset_hard_from_stdin_payload(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "git reset --hard"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("git", stderr)

    def test_blocks_windows_recursive_force_delete(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "Remove-Item -Recurse -Force C:\\tmp"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("Remove-Item", stderr)

    def test_blocks_legacy_claude_env_payload(self):
        code, stderr = self.run_hook(
            env={
                "CLAUDE_TOOL_INPUT": json.dumps({"command": "rm -rf build"}),
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("rm", stderr)

    def test_blocks_rm_flags_in_either_order(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "rm -fr build"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("rm", stderr)

    def test_blocks_git_clean_split_flags(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "git clean -f -d"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("git", stderr)

    def test_blocks_cmd_delete_split_flags(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "del /q /s build"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("del", stderr)

    def test_blocks_drop_table_case_insensitive(self):
        code, stderr = self.run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "drop table users"},
            }
        )
        self.assertEqual(code, 2)
        self.assertIn("DROP", stderr)

    def test_hook_script_blocks_dangerous_stdin_payload(self):
        payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "git clean -fdx"},
            }
        )
        completed = subprocess.run(
            [sys.executable, "scripts/check_dangerous_command.py"],
            cwd=ROOT,
            input=payload,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("BLOCKED", completed.stderr)

    def test_hook_script_allows_safe_stdin_payload(self):
        payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "python scripts/codex_execute.py --help"},
            }
        )
        completed = subprocess.run(
            [sys.executable, "scripts/check_dangerous_command.py"],
            cwd=ROOT,
            input=payload,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stderr, "")

    def test_codex_hook_config_points_to_safety_hook(self):
        config = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
        pre_tool = config["hooks"]["PreToolUse"][0]
        self.assertEqual(pre_tool["matcher"], "^Bash$")
        hook_entry = pre_tool["hooks"][0]
        self.assertEqual(hook_entry["type"], "command")
        self.assertEqual(hook_entry["command"], "python scripts/check_dangerous_command.py")
        self.assertEqual(hook_entry["timeout"], 30)

    def test_claude_hooks_include_safety_and_stop_tests(self):
        config = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        pre_tool = config["hooks"]["PreToolUse"][0]
        self.assertEqual(pre_tool["matcher"], "Bash")
        self.assertEqual(pre_tool["hooks"][0]["command"], "python scripts/check_dangerous_command.py")

        stop = config["hooks"]["Stop"][0]
        self.assertEqual(stop["matcher"], "")
        self.assertEqual(
            stop["hooks"][0]["command"],
            'python -m unittest discover -s scripts -p "test_*.py" -v',
        )


if __name__ == "__main__":
    unittest.main()
