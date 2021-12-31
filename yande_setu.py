import json
import random

import requests
import xmltodict

PROXY = {
    'http': "http://127.0.0.1:1080",
    'https': "http://127.0.0.1:1080",
}

YANDE_API = 'https://yande.re/post.json'
YANDE_TAG_API = 'https://yande.re/tag.xml?limit=50&order=count'

TARGET_SCORE = 100


class YandePictureInfo:
    def __init__(self, yande_json):
        self._id = yande_json['id']
        self._file_url = yande_json['file_url']
        self._score = yande_json['score']

    @property
    def post_url(self):
        return f'https://yande.re/post/show/{self._id}'

    def get_file(self):
        r = requests.get(self._file_url, proxies=PROXY, timeout=100)
        return r.content

    @property
    def score(self):
        return self._score


def get_tag():
    r = requests.get(YANDE_TAG_API, proxies=PROXY, timeout=100)
    tags_json = json.loads(json.dumps(xmltodict.parse(r.text)))
    tag_list = tags_json['tags']['tag']
    return random.choice(tag_list)['@name']


def get_yande_setu():
    tag = get_tag()

    if random.randint(0, 100) > 80:
        tag = 'genshin_impact'

    params = {
        'tags': f'{tag} score:>{TARGET_SCORE} order:random',
        'limit': 1,
        'api_version': 2,
    }

    r = requests.get(YANDE_API, params=params, proxies=PROXY, timeout=100)
    y = YandePictureInfo(r.json()['posts'][0])
    return y.get_file(), f'{y.post_url}\ntag: {tag} score: {y.score}'
