from collections import OrderedDict
from typing import NamedTuple, List, Optional, Tuple, IO, Dict, Set

import toml
from typeguard import typechecked

from lib.url_re import UrlFriendlySearch


@typechecked
class ConfigTestCase(NamedTuple):
    input: str
    expected_output: str


@typechecked
class SiteConfig(NamedTuple):
    name: str
    base_url_pattern: UrlFriendlySearch
    essential_query: Set[str]
    target_url: str
    test_cases: Optional[List[ConfigTestCase]]


@typechecked
def _get_test_cases(test_cases: Optional[List[List[str]]]) -> Optional[List[ConfigTestCase]]:
    if test_cases is None:
        return
    return [
        ConfigTestCase(i, e)
        for i, e in test_cases
    ]


def parse_sites(f: IO) -> List[SiteConfig]:
    d = toml.load(f, _dict=OrderedDict)
    return [
        SiteConfig(
            name=k,
            base_url_pattern=UrlFriendlySearch(v['base_url_pattern']),
            essential_query=set(v['essential_query']),
            target_url=v['target_url'],
            test_cases=_get_test_cases(v.get('test_cases'))
        )
        for k, v in d.items()
    ]
