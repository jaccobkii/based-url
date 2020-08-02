import os
import unittest
import warnings
from pathlib import Path

from lib.sites_config import parse_sites
from lib.url_transform import transform_url


class SitesTestCase(unittest.TestCase):
    def run_test(self, fp):
        with open(fp) as f:
            config = parse_sites(f)
        for site in config:
            if site.test_cases is None:
                warnings.warn(f"No test_cases in site: {site.name}", UserWarning)
                continue
            for idx, (url, expected) in enumerate(site.test_cases):
                res = transform_url(site, url)
                self.assertIsNotNone(res, f"Failed to match url '{url}' at site: {site.name}")
                self.assertEqual(expected, res, f"Failed at site '{site.name}' case {idx+1}, expected: {expected}, got: {res}")

    def test(self):
        self.run_test(Path(__file__).parent.parent / 'sites.example.toml')


if __name__ == '__main__':
    unittest.main()
