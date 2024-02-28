import time
import requests
import warnings
import logging
import pathlib
from flask import Flask, request, Response
from typing import Type, TypeVar

from util import *
from model import *

app = Flask(__name__, static_url_path='/I_HAVE_TO_FIND_A_PATH_TO_BLOCK_FLASK_STATIC_PATH_BECAUSE_I_DONT_KNOW_IT_WELL')
T = TypeVar('T')


class Configs:
    host_match = HostMatch()
    setting = Setting()


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy_request(path):

    host_match_rules = Configs.host_match.list
    proxy_dict = Configs.setting.proxy

    def match_origin_host(alias) -> str | None:
        if ls := [matcher[0] for matcher in host_match_rules if matcher[1] == alias]:
            return ls[0]
        else:
            return None

    def match_alias_host(origin) -> str | None:
        if ls := [matcher[0] for matcher in host_match_rules if matcher[1] == origin]:
            return ls[0]
        else:
            return None

    def replace_all_origin_host(content: T) -> Type[T]:
        for match in host_match_rules:
            content = content.replace(match[0], match[1])
        return content

    def replace_all_alias_host(content: T) -> T:
        for match in host_match_rules:
            content = content.replace(match[1], match[0])
        return content

    headers = dict(request.headers)
    method = request.method
    url = request.url
    from_host = request.headers['Host']
    request_body = request.data
    ip = request.headers['X-Real-IP']

    logger = logging.Logger('{} {} {}'.format(ip, method, url))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s][%(name)s] %(msg)s'))
    logger.handlers.append(console_handler)
    logger.debug('Request received')

    matched_host = match_origin_host(from_host)
    if not matched_host:
        return Response(status=404)

    target_url = replace_all_alias_host(url)
    if not https:
        target_url = target_url.replace('http', 'https')
    headers['Host'] = matched_host

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        max_retry_times = 2
        logger.debug(f'Start proxy request, max {max_retry_times}')
        for retry_times in range(max_retry_times):
            try:
                logger.debug(f'{retry_times}')
                response = requests.request(method, target_url, headers=headers, allow_redirects=False, data=request_body, proxies=proxy_dict)
                logger.debug(f'{retry_times}: ok')
                break
            except Exception as e:
                response = None
                logger.debug(f'{retry_times}: {e}')
    if response == None:
        return Response(status=404)

    content = response.content
    status_code = response.status_code
    response_headers = dict(response.headers)
    mime_type = response.headers.get('Content-Type') or response.headers.get('content-type')
    logger.debug(f'{status_code}: {len(content)}')

    # 因为是代理请求，因此去除response_headers中某些控制流传输的部分
    try_pop_ignore_cap(response_headers, 'Transfer-Encoding')
    try_pop_ignore_cap(response_headers, 'Content-Encoding')

    # 重定向返回
    if status_code in [301, 302, 303, 307, 308] and 'location' in response_headers:
        redirect_url = response_headers['location']
        
        redirect_url = replace_all_origin_host(redirect_url)
        if not https:
            redirect_url = redirect_url.replace('https', 'http')
        response_headers['location'] = redirect_url

    if mimetype_is_text(mime_type):
        content = replace_all_origin_host(content.decode()).encode()

    proxy_response = Response(content, status=status_code, mimetype=mime_type, headers=response_headers)
    logger.debug(f'return')
    return proxy_response


if __name__ == '__main__':
    host, port, https = Configs.setting.running_config
    app.run(host=host, port=port, debug=True, threaded=True)
