from urllib.parse import urlencode
from typing import Optional, List

import flask
from flask import Flask, Response
from werkzeug.routing import BaseConverter

from lib.sites_config import parse_sites, SiteConfig
from lib.url_transform import transform_sites

sites: Optional[List[SiteConfig]] = None

app = Flask(__name__)

def get_full_url(url):
    args = flask.request.args
    if args:
        qs = urlencode(args)
        url = f"{url}?{qs}"
    return url


@app.route('/api/transform/<path:url>', methods=['GET'])
def _normal_transform_route(url):
    url = get_full_url(url)
    res = transform_sites(sites, url)
    if res is None:
        return url
    else:
        return res


@app.route('/api/strict/transform/<path:url>', methods=['GET'])
def _strict_transform_route(url):
    url = get_full_url(url)
    res = transform_sites(sites, url)
    if res is None:
        return Response(f"No site matches url: {url}", status=400)
    else:
        return res


if __name__ == '__main__':
    with open('sites.toml') as f:
        sites = parse_sites(f)
    app.run('0.0.0.0', 14208)
