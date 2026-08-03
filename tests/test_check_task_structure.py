import pathlib
import tempfile
import unittest

from scripts import check_task_structure


class CheckTaskStructureTests(unittest.TestCase):
    def _make_task(self, root, name):
        task = root / "01_tasks" / name
        for folder in ("01_assets", "02_output", "03_logs", "04_tmp"):
            (task / folder).mkdir(parents=True, exist_ok=True)
        (task / "prompt.md").write_text("# Prompt\n", encoding="utf-8")
        (task / "notes.md").write_text("# Notes\n", encoding="utf-8")
        return task

    def test_clean_task_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            self._make_task(root, "2026-08-03-1200-demo-task")
            self.assertEqual(check_task_structure.check_workspace(root), [])

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            task = self._make_task(root, "2026-08-03-1200-demo-task")
            (task / "notes.md").unlink()
            issues = check_task_structure.check_workspace(root)
            self.assertTrue(any("missing notes.md" in issue for issue in issues))

    def test_forbidden_root_item_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            task = self._make_task(root, "2026-08-03-1200-demo-task")
            (task / ".venv").mkdir()
            issues = check_task_structure.check_workspace(root)
            self.assertTrue(any(".venv" in issue for issue in issues))

    def test_nested_on_demand_allowed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            task = self._make_task(root, "2026-08-03-1200-demo-task")
            (task / "01_assets" / "01_input").mkdir(parents=True, exist_ok=True)
            self.assertEqual(check_task_structure.check_workspace(root), [])


if __name__ == "__main__":
    unittest.main()