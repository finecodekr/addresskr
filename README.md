addresskr은 도로명주소를 juso.go.kr API를 이용해서 파싱해서 부분별로 사용할 수 있는 라이브러리다.

다음과 같이 설치할 수 있다.
```shell
pip install addresskr
```

juso.go.kr API를 이용하기 때문에 API key를 발급 받아야 한다. 다음 주소에서 발급 받을 수 있다.
https://business.juso.go.kr/addrlink/openApi/apiReqst.do

발급 받은 키는 [https://github.com/theskumar/python-dotenv](python-dotenv)를 통해서 지정할 수도 있고, 수동으로 지정할 수도 있다.

`.env` 파일 사용하기
```shell
JUSO_GO_KR_API_KEY=xxxx
```

직접 지정하기
```python
from addresskr.jusogokr import settings
settings.JUSO_GO_KR_API_KEY = 'xxxx'
```

API key를 설정하고 나면 다음과 같이 사용할 수 있다.
```python
from addresskr import 도로명주소

address = 도로명주소.parse('경기도 성남시 분당구 판교역로192번길 14-2, 912-비54호 (삼평동, 골드타워)')
print(address.시군구명, address.읍면동명, address.우편번호, address.법정동코드)
```

`도로명주소` 클래스는 juso.go.kr API의 응답 필드를 한국어로 번역한 필드들에 법정동코드, 상세주소 등의 필드가 추가로 들어가 있다.
