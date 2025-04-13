"""
Parse Korean address text into various address fields based on juso.go.kr API
"""
__version__ = '0.1.3'

import csv
import os
import re
from dataclasses import dataclass, field, fields

from addresskr import jusogokr


"""
법정동코드표는 다음 주소에서 다운로드 받은 것이다.
https://www.code.go.kr/stdcode/regCodeL.do
"""
with open(os.path.dirname(__file__) + '/법정동코드 전체자료.txt', encoding='euckr') as f:
    법정동코드표 = [[col for col in row] for row in csv.reader(f, delimiter='\t')]


@dataclass(kw_only=True)
class 도로명주소:
    전체_도로명주소: str = field(default='', metadata={'key': 'roadAddr'})
    도로명주소_참고항목_제외: str = field(metadata={'key': 'roadAddrPart1'})
    도로명주소_참고항목: str = field(default=None, metadata={'key': 'roadAddrPart2'})
    지번주소: str = field(metadata={'key': 'jibunAddr'})
    도로명주소_영문: str = field(metadata={'key': 'engAddr'})
    우편번호: str = field(metadata={'key': 'zipNo'})
    행정구역코드: str = field(metadata={'key': 'admCd'})
    도로명코드: str = field(metadata={'key': 'rnMgtSn'})
    건물관리번호: str = field(metadata={'key': 'bdMgtSn'})
    상세건물명: str = field(default=None, metadata={'key': 'detBdNmList'})
    건물명: str = field(default=None, metadata={'key': 'bdNm'})
    공동주택여부: str = field(metadata={'key': 'bdKdcd', 'help': '0: 비공동주택, 1: 공동주택'})
    시도명: str = field(metadata={'key': 'siNm'})
    시군구명: str = field(metadata={'key': 'sggNm'})
    읍면동명: str = field(metadata={'key': 'emdNm'})
    법정리명: str = field(default=None, metadata={'key': 'liNm'})
    도로명: str = field(metadata={'key': 'rn'})
    지하여부: str = field(metadata={'key': 'udrtYn', 'help': '0: 지상, 1: 지하'})
    건물본번: int = field(metadata={'key': 'buldMnnm'})
    건물부번: int = field(metadata={'key': 'buldSlno'})
    산여부: str = field(metadata={'key': 'mtYn', 'help': '0: 대지, 1: 산'})
    지번본번_번지: int = field(metadata={'key': 'lnbrMnnm'})
    지번부번_호: int = field(metadata={'key': 'lnbrSlno'})
    읍면동일련번호: str = field(metadata={'key': 'emdNo'})
    변동이력여부: str = field(metadata={'key': 'hstryYn', 'help': '0: 현행 주소정보, 1: 요청변수의 keyword(검색어)가 변동된 주소정보에서 검색된 정보'})
    관련지번: str = field(default=None, metadata={'key': 'relJibun'})
    관할주민센터: str = field(default=None, metadata={'key': 'hemdNm'})
    상세주소: str = ''
    법정동코드: str = None
    세무서코드: str = None  # not implemented yet
    특수지코드: str = None

    def __post_init__(self):
        법정동주소 = ' '.join(filter(lambda x: x, [self.시도명, self.시군구명, self.읍면동명, self.법정리명]))
        try:
            row = next(filter(lambda row: row[1] == 법정동주소, 법정동코드표))
            self.법정동코드 = row[0]
        except:
            raise ValueError(f'법정동코드를 찾을 수 없습니다. {법정동주소}')

        if self.산여부 == '1':
            self.특수지코드 = '1'
        else:
            self.특수지코드 = '0'

    @staticmethod
    def parse(text):
        address, 법정동명_건물명 = 도로명주소.split_법정동명_공동주택건물명(text)

        # 주소가 상세주소를 포함하고 있는 경우 어디까지가 상세주소인지 알 수 없기 때문에, 전체 조각에서 뒷부분을 한 조각씩 분리해가면서 검색해보고
        # 검색 결과가 있으면 그 시점의 앞부분을 도로명주소로 보고 뒷부분을 상세주소로 본다.
        # 앞부분은 도로명주소 API의 필드를 그대로 한국어로 번역해서 넣고 뒷부분은 상세주소로 합쳐서 넣는다.
        parts = address.split(' ')
        for l in range(len(parts), 2, -1):
            data = jusogokr.search(' '.join(parts[:l]))
            if data:
                return 도로명주소.from_juso_response(data[0], ' '.join(parts[l:]))
        else:
            raise ValueError(f'주소를 찾을 수 없습니다. {text}')

    @classmethod
    def from_juso_response(cls, data, detail_address=''):
        return cls(**{field.name: data.get(field.metadata['key']) for field in fields(cls) if 'key' in field.metadata},
                   상세주소=detail_address)

    @staticmethod
    def split_법정동명_공동주택건물명(address):
        searched = re.search(r'\(.+\)', address)
        법정동명_건물명 = ''
        parts = []
        if searched:
            법정동명_건물명 = searched.group()
            parts = [p for p in re.split(r'[, ]', 법정동명_건물명[1:-1]) if p]

        도로명주소 = ' '.join([p for p in re.split(r'[ ,]', address.replace(법정동명_건물명, '')) if p])
        return 도로명주소, parts
