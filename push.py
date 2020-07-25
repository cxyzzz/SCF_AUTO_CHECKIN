import os
import json
import requests

QY_WEIXING_BOT_KEY = os.environ.get('QY_WEIXING_BOT_KEY')

def push(title: str, msg: str):
    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('key', QY_WEIXING_BOT_KEY),
    )

    data = {
        "msgtype": "text",
        "text": {
            "content": f"{title}\n{msg}"
        }
    }
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send',
                             headers=headers, params=params, data=json.dumps(data))
    print(response.text)
