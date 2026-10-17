
import unittest

from backend.app.agents.researcher import normalize_source_url


class TestSourceUrlNormalization(unittest.TestCase):
    def test_accepts_https_url(self):
        result = normalize_source_url("https://example.com/article")

        self.assertEqual(
            result,
            ("https://example.com/article", "https://example.com/article"),
        )

    def test_accepts_http_url(self):
        result = normalize_source_url("http://example.com/article")

        self.assertEqual(
            result,
            ("http://example.com/article", "http://example.com/article"),
        )

    def test_removes_trailing_slash(self):
        first = normalize_source_url("https://example.com/article/")
        second = normalize_source_url("https://example.com/article")

        self.assertEqual(first, second)

    def test_normalizes_hostname_case(self):
        first = normalize_source_url("https://EXAMPLE.COM/article")
        second = normalize_source_url("https://example.com/article")

        self.assertEqual(first, second)

    def test_removes_fragment_but_preserves_query(self):
        result = normalize_source_url(
            "https://example.com/article?ref=research#section"
        )

        self.assertEqual(
            result,
            (
                "https://example.com/article?ref=research",
                "https://example.com/article?ref=research",
            ),
        )

    def test_rejects_non_http_scheme(self):
        self.assertIsNone(
            normalize_source_url("javascript:alert(1)")
        )

    def test_rejects_missing_hostname(self):
        self.assertIsNone(
            normalize_source_url("https:///article")
        )

    def test_rejects_invalid_port(self):
        self.assertIsNone(
            normalize_source_url("https://example.com:invalid/article")
        )

    def test_rejects_empty_url(self):
        self.assertIsNone(normalize_source_url(""))

    def test_rejects_missing_url(self):
        self.assertIsNone(normalize_source_url(None))


if __name__ == "__main__":
    unittest.main()
