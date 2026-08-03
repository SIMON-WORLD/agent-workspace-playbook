import unittest

from scripts import check_commit_emails


class CommitEmailTests(unittest.TestCase):
    def test_allowed_bot_and_agent_emails(self):
        self.assertTrue(check_commit_emails.is_allowed("project-test-bot@example.com"))
        self.assertTrue(check_commit_emails.is_allowed("noreply@github.com"))
        self.assertTrue(check_commit_emails.is_allowed("noreply@openai.com"))
        self.assertTrue(check_commit_emails.is_allowed("noreply@anthropic.com"))

    def test_allowed_github_noreply_emails(self):
        self.assertTrue(check_commit_emails.is_allowed("12345+agent@users.noreply.github.com"))
        self.assertTrue(check_commit_emails.is_allowed("agent@users.noreply.github.com"))

    def test_blocks_personal_email(self):
        self.assertFalse(check_commit_emails.is_allowed("person@example.org"))


if __name__ == "__main__":
    unittest.main()
