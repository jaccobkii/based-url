from urllib.parse import urlencode
from typing import Optional, List

import flask
from flask import Flask, Response
from werkzeug.routing import BaseConverter

from lib.short_url import trace_redirect_url
from lib.sites_config import parse_sites, SiteConfig, RedirectConfig, parse_redirects
from lib.url_transform import transform_sites

sites: Optional[List[SiteConfig]] = None
redirects: Optional[List[RedirectConfig]] = None

app = Flask(__name__)

def get_full_url(url):
    args = flask.request.args
    if args:
        qs = urlencode(args)
        url = f"{url}?{qs}"
    return url

def handle_url(url_src):
    redirect_url = trace_redirect_url(redirects, url_src)
    dst_url = transform_sites(sites, redirect_url)
    return dst_url

@app.route('/api/transform/<path:url>', methods=['GET'])
def _normal_transform_route(url):
    url = get_full_url(url)
    res = handle_url(url)
    if res is None:
        return url
    else:
        return res


@app.route('/api/strict/transform/<path:url>', methods=['GET'])
def _strict_transform_route(url):
    url = get_full_url(url)
    res = handle_url(url)
    if res is None:
        return Response(f"No site matches url: {url}", status=400)
    else:
        return res


if __name__ == '__main__':
    with open('sites.toml') as sf, open('redirects.toml') as rf:
        sites = parse_sites(sf)
        redirects = parse_redirects(rf)
    app.run('0.0.0.0', 14208)
