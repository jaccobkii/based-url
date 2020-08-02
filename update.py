import toml
import requests
from typing import NamedTuple


class UConf(NamedTuple):
    redirects: str
    sites: str


def download(url: str, fp: str):
    res = requests.get(url)
    with open(fp, 'w') as f:
        f.write(res.text)


def load_config() -> UConf:
    with open('update.toml') as f:
        d = toml.load(f)
    return UConf(**d)


def main():
    conf = load_config()
    download(conf.sites, 'sites.toml')
    download(conf.redirects, 'redirects.toml')


if __name__ == '__main__':
    main()
