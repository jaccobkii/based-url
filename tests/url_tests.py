import unittest

from lib.url_re import convert_pattern


class UrlTestCase(unittest.TestCase):
    def run_test(self, url, expected):
        pat = convert_pattern(url)
        self.assertEqual(expected, pat, f"expected: {expected}, got: {pat}")

    def test_dot(self):
        self.run_test(r"https://github.com", r"https://github\.com")
        self.run_test(r".", r"\.")
        self.run_test(r"\.+", r".+")

    def test_group_name(self):
        self.run_test(r"(?abc:abc)", r"(?P<abc>abc)")
        self.run_test(r"(\?abc:abc)", r"(\?abc:abc)")
        self.run_test(r"\(?abc:abc)", r"\(?abc:abc)")


if __name__ == '__main__':
    unittest.main()
