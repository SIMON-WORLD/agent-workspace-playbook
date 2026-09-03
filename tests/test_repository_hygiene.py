import pathlib
import subprocess
import tempfile
import unittest

from scripts import check_repository_hygiene


class RepositoryHygieneTests(unittest.TestCase):
    def test_required_files_match_workflow_contract(self):
        self.assertIn(".github/workflows/tests.yml", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("scripts/check_commit_emails.py", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("tests/test_repository_hygiene.py", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("scripts/build_index.py", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("tests/test_build_index.py", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("README.zh-CN.md", check_repository_hygiene.REQUIRED_FILES)

    def test_local_path_examples_are_allowed_only_with_context(self):
        local_path = "C:" + "\\Users\\name\\Desktop\\report.md"
        self.assertTrue(
            check_repository_hygiene.is_allowed_local_path_line(
                "Do not write outputs to " + local_path
            )
        )
        self.assertFalse(
            check_repository_hygiene.is_allowed_local_path_line(
                "Saved report at " + local_path
            )
        )

    def test_binary_suffixes_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir) / "image.png"
            path.write_bytes(b"\x89PNG\r\n")
            self.assertIsNone(check_repository_hygiene.read_text(path))

    def test_agent_rule_file_requires_at_least_one(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            missing = check_repository_hygiene.check_required_files(root)
            self.assertTrue(
                any("AGENTS.md, CLAUDE.md" in message for message in missing)
            )
            (root / "AGENTS.md").write_text("", encoding="utf-8")
            missing = check_repository_hygiene.check_required_files(root)
            self.assertFalse(
                any("AGENTS.md, CLAUDE.md" in message for message in missing)
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            (root / "CLAUDE.md").write_text("", encoding="utf-8")
            missing = check_repository_hygiene.check_required_files(root)
            self.assertFalse(
                any("AGENTS.md, CLAUDE.md" in message for message in missing)
            )



    def test_root_layout_flags_unexpected_entries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            (root / "node_modules").mkdir()
            (root / "README.md").write_text("", encoding="utf-8")
            issues = check_repository_hygiene.check_root_layout(root)
            self.assertTrue(any("node_modules" in issue for issue in issues))
            self.assertFalse(any("README.md" in issue for issue in issues))

    def _make_minimal_repo(self, root):
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        for file_name in check_repository_hygiene.REQUIRED_FILES:
            path = root / file_name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        (root / "AGENTS.md").write_text("", encoding="utf-8")

    def test_nested_git_directories_are_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            (root / ".git").mkdir()
            (root / "sub" / ".git").mkdir(parents=True)
            nested = check_repository_hygiene.find_nested_git_directories(root)
            self.assertEqual(nested, [root / "sub" / ".git"])

    def test_only_root_git_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            (root / ".git").mkdir()
            nested = check_repository_hygiene.find_nested_git_directories(root)
            self.assertEqual(nested, [])

    def test_run_rejects_nested_git_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            self._make_minimal_repo(root)
            (root / "scripts" / ".git").mkdir(parents=True)
            self.assertEqual(check_repository_hygiene.run(root), 1)

    def test_run_passes_with_only_root_git(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            self._make_minimal_repo(root)
            self.assertEqual(check_repository_hygiene.run(root), 0)

if __name__ == "__main__":
    unittest.main()
