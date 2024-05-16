import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv


@dataclass
class Settings:
    JUSO_GO_KR_API_KEY: str


load_dotenv()
settings = Settings(JUSO_GO_KR_API_KEY=os.getenv('JUSO_GO_KR_API_KEY'))


def search(keyword: str):
    res = requests.get('http://www.juso.go.kr/addrlink/addrLinkApi.do',
                       data={'confmKey': settings.JUSO_GO_KR_API_KEY,
                             'keyword': keyword,
                             'resultType': 'json'},
                       headers={'Accept-Language': 'ko'}).json()

    if res['results']['common']['errorCode'] == '0':
        return res['results']['juso']

    raise ValueError(res['results']['common']['errorMessage'])
