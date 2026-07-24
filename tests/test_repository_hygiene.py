import pathlib
import tempfile
import unittest

from scripts import check_repository_hygiene


class RepositoryHygieneTests(unittest.TestCase):
    def test_required_files_match_workflow_contract(self):
        self.assertIn(".github/workflows/tests.yml", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("scripts/check_commit_emails.py", check_repository_hygiene.REQUIRED_FILES)
        self.assertIn("tests/test_repository_hygiene.py", check_repository_hygiene.REQUIRED_FILES)

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


if __name__ == "__main__":
    unittest.main()
