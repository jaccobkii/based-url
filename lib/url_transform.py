from typing import Optional, Dict, List
from urllib.parse import urlparse, parse_qs, urlencode

from lib.sites_config import SiteConfig
from lib.url_re import UrlFriendlySearch


def transform_url(site: SiteConfig, url: str) -> Optional[str]:
    pu = urlparse(url)
    base_url = f"{pu.scheme}://{pu.netloc}{pu.path}"
    query = parse_qs(pu.query)
    new_query = urlencode({
        k: v
        for k, v in query.items()
        if k in site.essential_query
    })
    data = site.base_url_pattern.get_dict_or_none(base_url)
    if data is None:
        return None
    new_base_url = site.target_url.format(**data)
    if new_query:
        new_url = f"{new_base_url}?{new_query}"
    else:
        new_url = new_base_url
    return new_url


def transform_sites(sites: List[SiteConfig], url: str) -> Optional[str]:
    for s in sites:
        res = transform_url(s, url)
        if res is not None:
            return res
    return None
