import os
import re

db_url = os.getenv('DATABASE_URL')

realms = {
    '0': { 'service': 'digital', 'shop': 'videoa' },
    '1': { 'service': 'mono', 'shop': 'dvd' },
}

o2m = ('maker', 'label', 'series', 'director')
m2m = ('keyword', 'actress', 'histrion')

DOMAIN = 'http://www.dmm.co.jp/'
PIC_DOMAIN = 'http://pics.dmm.co.jp/'

url_bases = {
    'video': '{service}/{shop}/-/detail/=/cid={cid}',
    'pics': '{service}/{realm}/{pid}/{_pid}{pic_i}.jpg',
    'maker': '{service}/{shop}/-/maker/=/keyword={keyword}',
    'article': '{service}/{shop}/-/list/=/article={article}/id={id}',
    'mutual': 'misc/-/mutual-link/ajax-index/=/cid={cid}/service={service}/shop={shop}'
}

_re = {
    '_pid': '(?P=pid)',
    'id': r'(?P<id>\d+)',
    'pic_i': '(?P<type>[a-z0-9-]+)',
    'keyword': '(?P<keyword>[a-z]+)',
    'realm': r'(video|movie/adult|\w+)',
}

_rew = {
    k: r'(?P<%s>\w+)'%k for k in ('service', 'shop', 'article', 'cid', 'pid')
}

url_parsers = {
    k: re.compile(v.format(**_re, **_rew)) for k, v in url_bases.items()
}

def url_for(base=None, **kwargs):
    if base == 'pics':
        return PIC_DOMAIN + url_bases['pics']
    return DOMAIN + url_bases.get(base, '').format(**kwargs)

def parse_url(base=None, url=''):
    try:
        return url_parsers[base].search(url).groupdict()
    except (KeyError, AttributeError):
        return {}
