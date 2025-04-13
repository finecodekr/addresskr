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
    if settings.JUSO_GO_KR_API_KEY is None:
        raise ValueError('juso.go.kr의 API key가 설정되지 않았습니다. dotenv를 통해서 JUSO_GO_KR_API_KEY를 설정하거나, '
                         'addresskr.jusogokr.settings.JUSO_GO_KR_API_KEY에 직접 설정하세요.')

    res = requests.get('http://www.juso.go.kr/addrlink/addrLinkApi.do',
                       data={'confmKey': settings.JUSO_GO_KR_API_KEY,
                             'keyword': keyword,
                             'resultType': 'json'},
                       headers={'Accept-Language': 'ko'}).json()

    if res['results']['common']['errorCode'] == '0':
        return res['results']['juso']

    raise ValueError(res['results']['common']['errorMessage'])
