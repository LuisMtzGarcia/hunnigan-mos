import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MOS = REPO / "mos.py"


class MosCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.env = {**os.environ, "MOS_ROOT": str(self.root)}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_mos(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MOS), *args],
            env=self.env,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_task_lifecycle_and_filtered_context(self) -> None:
        self.run_mos("init")
        self.run_mos(
            "add",
            "--id",
            "sample-task",
            "--title",
            "Sample task",
            "--impact",
            "high",
            "--next",
            "Open the PR",
            "--date",
            "2026-07-14",
        )
        self.run_mos(
            "update",
            "sample-task",
            "--state",
            "waiting",
            "--add-wait",
            "Reviewer approval",
            "--note",
            "PR opened and review requested",
            "--date",
            "2026-07-14",
        )

        shown = json.loads(self.run_mos("show", "sample-task").stdout)
        self.assertEqual(shown["state"], "waiting")
        self.assertEqual(shown["impact"]["level"], "high")
        self.assertEqual(shown["wait"], ["Reviewer approval"])

        context = json.loads(self.run_mos("context", "day", "--date", "2026-07-14").stdout)
        self.assertEqual(len(context["events"]), 2)
        self.assertEqual(context["pending"][0]["id"], "sample-task")

        self.run_mos(
            "complete",
            "sample-task",
            "--note",
            "PR merged",
            "--done",
            "Merged implementation",
            "--date",
            "2026-07-14",
        )
        self.assertIn("OK\t1 tasks\t3 events", self.run_mos("verify").stdout)
        self.assertIn("Sample task", (self.root / "TASKS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
