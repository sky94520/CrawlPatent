import json
import requests
import logging


def get_random_proxy():
    """获取随机的IP地址"""
    url = 'http://47.107.246.172:5555/random'
    response = requests.get(url, timeout=10)
    datum = json.loads(response.text)
    if datum['status'] == 'success':
        return datum['proxy']
    else:
        print(datum['msg'])
        return None


def error(proxy):
    url = 'http://47.107.246.172:5555/error/' + proxy
    try:
        response = requests.post(url, timeout=10)
    except Exception as e:
        logging.warning('代理%s无法使用，且在反馈时失败%s' % (proxy, e))

    return True


def success(proxy):
    url = 'http://47.107.246.172:5555/success/' + proxy
    try:
        response = requests.post(url, timeout=10)
    except Exception as e:
        logging.warning('代理%s可用，但在反馈时失败 %s' % (proxy, e))

    return True
