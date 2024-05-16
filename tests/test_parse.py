import unittest

from addresskr import jusogokr, 도로명주소


class TestAddressParser(unittest.TestCase):
    def test_jusogokr_api(self):
        self.assertEqual('삼평동', jusogokr.search('경기도 성남시 분당구 판교역로192번길 14-2')[0]['emdNm'])

        old_key = jusogokr.settings.JUSO_GO_KR_API_KEY
        jusogokr.settings.JUSO_GO_KR_API_KEY = 'xxx'
        with self.assertRaises(ValueError, msg='승인되지 않은 KEY 입니다.'):
            jusogokr.search('경기도 성남시 분당구 판교역로192번길 14-2, 912-비54호 (삼평동, 골드타워)')

        jusogokr.settings.JUSO_GO_KR_API_KEY = old_key

    def test_parse(self):
        address = 도로명주소.parse('경기도 성남시 분당구 판교역로192번길 14-2, 912-비54호 (삼평동, 골드타워)')
        self.assertEqual('삼평동', address.읍면동명)
        self.assertEqual('4113510900', address.법정동코드)
        self.assertEqual('912-비54호', address.상세주소)