import base64
import hashlib
import io
import json
import os
import sys
import urllib

import PIL.Image as Image

import yande_setu

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
WX_WEBHOOK_CONF_PATH = os.path.join(BASE_PATH, 'webhook.conf')


def get_wx_webhook():
    with open(WX_WEBHOOK_CONF_PATH, 'r') as f:
        return f.readline()


def do_notify(setu, text):
    while sys.getsizeof(setu) > 2 * 1024 * 1024:
        img = Image.open(io.BytesIO(setu))
        w, h = img.size
        img.thumbnail([w / 2, h / 2], Image.ANTIALIAS)
        stream = io.BytesIO()
        img.save(stream, 'png')
        setu = stream.getvalue()
    setu_base64 = base64.b64encode(setu).decode('UTF-8')
    setu_md5 = hashlib.md5(setu).hexdigest()

    para_dict = {
        "msgtype": "image",
        "image": {
            "base64": setu_base64,
            "md5": setu_md5
        }
    }
    para_data = json.dumps(para_dict, ensure_ascii=False).encode()
    headers = {"Content-Type": "application/json"}
    request = urllib.request.Request(url=get_wx_webhook(), headers=headers)
    urllib.request.urlopen(request, para_data)

    para_dict = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    para_data = json.dumps(para_dict, ensure_ascii=False).encode()
    headers = {"Content-Type": "application/json"}
    request = urllib.request.Request(url=get_wx_webhook(), headers=headers)
    urllib.request.urlopen(request, para_data)


def main():
    setu, text = yande_setu.get_yande_setu()
    do_notify(setu, text)


main()
