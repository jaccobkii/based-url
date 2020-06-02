from typing import Iterable, List

import requests
import re

from lib.sites_config import RedirectConfig


def trace_url(url: str) -> Iterable[str]:
    res = requests.get(url, allow_redirects=False)
    while res.status_code == 302 or res.status_code == 304:
        url = res.headers['Location']
        yield url
        res = requests.get(url, allow_redirects=False)


def trace_redirect_url(redirects: List[RedirectConfig], url: str) -> str:
    redirect = None
    for r in redirects:
        if r.source.matches(url):
            redirect = r
            break
    if redirect is not None:
        for u in trace_url(url):
            if redirect.destination.matches(u):
                url = u
                break
    return url
