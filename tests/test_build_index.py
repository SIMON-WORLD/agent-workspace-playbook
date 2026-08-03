import pathlib
import tempfile
import unittest

from scripts import build_index


class BuildIndexTests(unittest.TestCase):
    def _workspace(self, tasks_text: str, readme_text: str = "# My Workspace"):
        temp_dir = tempfile.TemporaryDirectory()
        root = pathlib.Path(temp_dir.name)
        (root / "README.md").write_text(readme_text, encoding="utf-8")
        (root / "TASKS.md").write_text(tasks_text, encoding="utf-8")
        return root, temp_dir

    def test_build_index_chinese(self):
        tasks = (
            "| 日期时间 | 任务名称 | 目录 | 状态 | 产出文件 | 备注 |\n"
            "|---|---|---|---|---|---|\n"
            "| 2026-08-04 02:51 | review-pr | 01_tasks/2026-08-04-review-pr/ | 进行中 | | |\n"
            "| 2026-07-01 10:00 | old-task | 01_tasks/2026-07-01-old-task/ | 完成 | | |\n"
        )
        root, temp_dir = self._workspace(tasks, "# 我的工作区")
        try:
            output = build_index.render_index(root)
            self.assertIn("我的工作区", output)
            self.assertIn("## 活动任务", output)
            self.assertIn("2026-08-04-review-pr", output)
            self.assertIn("## 最近任务", output)
            active_section = output.split("## 最近任务")[0]
            recent_section = output.split("## 最近任务")[1]
            self.assertNotIn("2026-07-01-old-task", active_section)
            self.assertIn("2026-07-01-old-task", recent_section)
        finally:
            temp_dir.cleanup()

    def test_build_index_english_headers(self):
        tasks = (
            "| Date Time | Task Name | Directory | Status | Outputs | Notes |\n"
            "|---|---|---|---|---|---|\n"
            "| 2026-08-04 02:51 | review-pr | 01_tasks/2026-08-04-review-pr/ | In progress | | |\n"
        )
        root, temp_dir = self._workspace(tasks)
        try:
            output = build_index.render_index(root)
            self.assertIn("## Active Tasks", output)
            self.assertIn("review-pr", output)
        finally:
            temp_dir.cleanup()

    def test_render_is_idempotent(self):
        tasks = (
            "| Date Time | Task Name | Directory | Status | Outputs | Notes |\n"
            "|---|---|---|---|---|---|\n"
            "| 2026-08-04 02:51 | a | 01_tasks/a/ | done | | |\n"
        )
        root, temp_dir = self._workspace(tasks)
        try:
            self.assertEqual(build_index.render_index(root), build_index.render_index(root))
        finally:
            temp_dir.cleanup()

    def test_check_mode(self):
        tasks = (
            "| Date Time | Task Name | Directory | Status | Outputs | Notes |\n"
            "|---|---|---|---|---|---|\n"
            "| 2026-08-04 02:51 | a | 01_tasks/a/ | done | | |\n"
        )
        root, temp_dir = self._workspace(tasks)
        try:
            generated = build_index.render_index(root)
            (root / "INDEX.md").write_text(generated, encoding="utf-8")
            self.assertEqual(build_index.check_index(root), 0)
            (root / "INDEX.md").write_text("stale", encoding="utf-8")
            self.assertEqual(build_index.check_index(root), 1)
        finally:
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
