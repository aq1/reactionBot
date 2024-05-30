import base64
import datetime
import hashlib
import hmac
import json
import time
import urllib
import urllib.parse
import urllib.request

import requests

import settings


def get_headers(timestamp, params, method, path):
    if method.upper() == 'GET':
        params.update({'signTimestamp': timestamp})
        sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        del params['signTimestamp']
    else:
        request_body = json.dumps(params)
        encode_params = 'requestBody={}&signTimestamp={}'.format(
            request_body, timestamp
        )
    sign_params_first = [method.upper(), path, encode_params]
    sign_params_second = '\n'.join(sign_params_first)
    sign_params = sign_params_second.encode(encoding='UTF8')
    secret_key = settings.API_SECRET_KEY.encode(encoding='UTF8')
    digest = hmac.new(secret_key, sign_params, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()

    return {
        'Content-Type': 'application/json',
        'key': settings.API_KEY,
        'signTimestamp': str(timestamp),
        'signature': signature,
    }


def request(*, path, method='get', params=None):
    params = params or {}
    timestamp = int(time.time() * 1000)
    headers = get_headers(
        timestamp=timestamp,
        params=params,
        method=method,
        path=path,
    )

    url = f'{settings.API_URL}{path}'
    try:
        r = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )
        print(f'Req {datetime.datetime.now().isoformat(timespec="seconds")} {path} {r.status_code}')
        r.raise_for_status()
    except requests.RequestException as e:
        print(e)
        return {}, False
    return r.json(), True
