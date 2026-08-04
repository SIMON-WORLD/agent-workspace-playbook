import pathlib
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
        self.assertIn("README.en.md", check_repository_hygiene.REQUIRED_FILES)
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


if __name__ == "__main__":
    unittest.main()
