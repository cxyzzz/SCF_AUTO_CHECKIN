# -*- coding: utf-8 -*-
import os
import re
import time
import requests
from push import push
from C189Checkin import main as C189Checkin

UA = 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36'

V2EX_COOKIE = os.environ.get('V2EX_COOKIE')
YYETS_ACCOUNT = os.environ.get('YYETS_ACCOUNT')
YYETS_PASSWORD = os.environ.get('YYETS_PASSWORD')
C189_ACCOUNT = os.environ.get('C189_ACCOUNT')
C189_PASSWORD = os.environ.get('C189_PASSWORD')
吾爱破解_COOKIE = os.environ.get('WA_COOKIE')
NETEASE_COOKIE = os.environ.get('NETEASE_COOKIE')


session = requests.session()


def v2ex_checkin():
    V2EX_DOMAIN = r'v2ex.com'
    V2EX_URL_START = r'https://' + V2EX_DOMAIN
    V2EX_MISSION = V2EX_URL_START + r'/mission/daily'
    V2EX_BALANCE_URL = V2EX_URL_START + r'/balance'

    def get_once_url(data):
        p = r'/mission/daily/redeem\?once=\d+'
        m = re.search(p, data)
        if m:
            return m.group()
        else:
            return None

    def get_balance(data):
        day_balance = re.search(r'\d{8} 的每日登录奖励 \d+ 铜币', data)
        if (day_balance):
            day_balance = day_balance.group()
            total_balance = re.search(r'right;">(\d+)', data).group(1)
            return f"{day_balance}，余额：{total_balance}"
        else:
            print("V2EX_COOKIE ERROR!")

    def checkin():
        session.cookies.update({'A2': V2EX_COOKIE})
        session.get(V2EX_URL_START)
        data = session.get(V2EX_MISSION)
        print(data.text)
        once = get_once_url(data.text)
        if(once):
            v2ex_coin_url = V2EX_URL_START + once
            session.get(v2ex_coin_url)
        else:
            print("重复签到！")
            # return
        msg = get_balance(session.get(V2EX_BALANCE_URL).text)
        return msg

    title = 'V2ex 签到'
    msg = checkin()
    if(msg):
        push(title, msg)


def yyets_checkin():
    HEADERS = {
        'User-Agent': UA,
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    def login():
        HEADERS['Host'] = 'a.zmzapi.com'
        params = (
            ('g', 'api/public'),
            ('m', 'v2'),
            ('accesskey', '519f9cab85c8059d17544947k361a827'),
            ('client', '2'),
            ('a', 'login'),
            ('account', YYETS_ACCOUNT),
            ('password', YYETS_PASSWORD),
        )

        response = session.get(
            'http://a.zmzapi.com/index.php', headers=HEADERS, params=params)
        res = response.json()
        if(res['data']):
            return res['data']
        else:
            print(res['info'])

    def checkin():
        HEADERS['HOST'] = 'h5.rrhuodong.com'
        url = 'http://h5.rrhuodong.com/index.php'

        data = login()
        if (not data):
            return
        params = (
            ('g', 'api/mission'),
            ('m', 'index'),
            ('a', 'login'),
            ('uid', data['uid']),
            ('token', data['token']),
        )
        # 访问活动页获取 Cookie
        session.get(url, headers=HEADERS, params=params)

        # 签到
        params = (
            ('g', 'api/mission'),
            ('m', 'clock'),
            ('a', 'weeks'),
            ('id', '2'),
        )
        response = session.get(url, headers=HEADERS, params=params)
        res = response.json()
        if (res['status']):
            print(res['info'])
        else:
            pass
        params = (
            ('g', 'api/mission'),
            ('m', 'clock'),
            ('a', 'store'),
            ('id', '2'),
        )
        response = session.get(url, headers=HEADERS, params=params)
        res = response.json()
        if (res['status']):
            print(res['info'])
        else:
            pass
        params = (
            ('g', 'api/mission'),
            ('m', 'index'),
            ('a', 'user_info'),
        )
        response = session.get(url, headers=HEADERS, params=params)
        return response.json()

    res = checkin()
    if(res):
        title = "人人影视签到"
        msg = f"昵称：{res['data']['nickname']}，等级：{res['data']['main_group_name']}，人人钻：{res['data']['point']}"
        push(title, msg)


def 吾爱破解_签到():
    if (not 吾爱破解_COOKIE):
        print("吾爱破解_COOKIE NONE!")
        return
    url = 'https://www.52pojie.cn/home.php'
    cookies = dict([cookie.split('=', 1) for cookie in 吾爱破解_COOKIE.split(';')])
    headers = {
        'Host': 'www.52pojie.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.52pojie.cn',
        'Accept-Language': 'zh,zh-CN;q=0.9',
    }
    params = {
        'mod': 'task',
        'do': 'apply',
        'id': '2'
    }
    session.get(url, headers=headers, params=params, cookies=cookies)
    params['do'] = 'draw'
    res = session.get(url, headers=headers, params=params, cookies=cookies)
    if (re.search(r'home.php\?mod=space&amp;uid=\d+', res.text)):
        push(title="吾爱破解签到", msg="签到完毕！")


def netease_checkin():
    if (not NETEASE_COOKIE):
        print("NETEASE_COOKIE NONE!")
        return
    url = 'http://music.163.com/api/point/dailyTask'
    cookies = dict([cookie.split('=', 1)
                    for cookie in NETEASE_COOKIE.split(';')])
    headers = {
        'Pragma': 'no-cache',
        'DNT': '1',
        'Accept-Encoding': 'text',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'User-Agent': UA,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Referer': 'http://music.163.com/discover',
        'Connection': 'keep-alive',
    }

    params = {'type': 0}
    title = "网易云音乐签到"
    session.get(url, headers=headers, params=params, cookies=cookies)
    params['type'] = 1
    response = session.get(url, headers=headers,
                           params=params, cookies=cookies)
    res = response.json()
    if (res['code'] == -2):
        print(res['msg'])
    else:
        push(title=title, msg=res['msg'])


def main(*args):
    v2ex_checkin()
    time.sleep(1)
    # yyets_checkin()
    吾爱破解_签到()
    time.sleep(1)
    netease_checkin()
    time.sleep(1)
    C189Checkin(C189_ACCOUNT, C189_PASSWORD)
    session.close()


if __name__ == '__main__':
    main()
