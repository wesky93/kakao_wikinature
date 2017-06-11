import sys

# 경로 설정
sys.path.append( "/var/task/.venv/lib/python3.6/site-packages" )
import requests
from KakaoReply import KakaoReply


# 센트리 연결
import os
from raven import Client
from raven.transport.http import HTTPTransport

# raven 클라이언트 생성
def cli() :
    # 센트리 프로젝트 연결 주소
    # 람다 환경변수에서 SENTRU값을 dsn으로 적어준다
    dsn = os.environ.get( 'SENTRY' )

    # 람다에서 raven사용시 전송방식을 HTTP로 지정해줘 한다
    client = Client( dsn=dsn, transport=HTTPTransport )
    return client

sentry = cli()

key = 'hb8NTDfY%2FQ2fEe4MiYwodBcwcsOn6u8TYMdYV%2BfiH9KMkahhnyiRLz%2BjnDONdensgT44OwUr6iq0IX4VgBcngg%3D%3D'


# 국명 검색 API endpoint
def NameInfo(num):
    """
    학명번호로 상세정보 조회
    :param num: 학명 번호
    :return:
    """
    InfoUrl = 'http://openapi.nature.go.kr/openapi/service/rest/KpniService/btncInfo'
    parms = {"ServiceKey": key, "q1": num, "_type": "json"}
    # 학명 번호로 상세 정보 요청
    r = requests.get(InfoUrl, parms)

    # 식물 상세 정보에서 필요한 자료만 추출
    data = r.json()['ns1.BtncInfoResponse']['ns1.body']['ns1.item']
    info = {}
    info['국명'] = data['ns1.korname']
    info['학명'] = data["ns1.plantSpecsScnm"]
    info['학명id'] = data["ns1.stpltScnmId"]
    return info


def search(name, st=3):
    """
    식물이름을 검색하여 매칭되는 국명이 있을경우 해당 국명의 상세정보를 조회하여 딕셔너리 값으로 반환/없을 경우 Nnoe
    :param name:
    :param st:
    :return:
    """
    SearchUrl = 'http://openapi.nature.go.kr/openapi/service/rest/KpniService/korSearch'
    parms = {'ServiceKey': key, 'st': st, 'sw': name, '_type': 'json'}
    r = requests.get(SearchUrl, params=parms)
    item = r.json()['ns1.KorSearchResponse']['ns1.body']['ns1.item']

    # test code
    # print('item={0}, type={1}'.format(item,type(item)))

    if item != '':
        if type(item['ns1.KorSearchVO']) == type(list()):
            """
            결과값이 두개 이상 나올경우, 추천명 자료를 추출하고 이외의 자료는 학명ID목록으로 내보낸다.
            """
            unrecom_ids = []
            recomID = int()
            # 학명ID 목록 모음
            items = item['ns1.KorSearchVO']
            for info in items:
                ID = info['ns1.plantScnmId']
                if info['ns1.recom'] == '추천명':
                    # 이미 추천명이 존재할경우 비추천명에 추가
                    if recomID:
                        subinfo = (ID,NameInfo(ID)['국명'])
                        unrecom_ids.append(subinfo)
                    else:
                        recomID = ID
                else:
                    subinfo = (ID, NameInfo(ID)['국명'])
                    unrecom_ids.append(subinfo)

            # 추천명이 없을 경우, 결과를 보여주기 위해 비추천명에서 하나를 선택해 recomID로 할당한후 비추천명 목록에서 제거한다
            if not recomID:
                recomID = unrecom_ids.pop()[0]

            unrecom_list = ['{0}({1})'.format(name,id) for id,name in unrecom_ids]
            unrecom_list.insert(0,'국명(ID)')
            etc = '이외에 {0}가지의 결과가 더있습니다. \n 다른 식물을 찾으신다면 아래 학명ID를 검색해보세요\n{1}'.format(len(items) - 1, ',\n'.join(unrecom_list))
            data = {'state': True, 'multi': True, 'etc': etc}
            data.update(NameInfo(recomID))
        elif type(item['ns1.KorSearchVO']) == type(dict()):
            """ 결과값이 1개일 경우 """
            # 매칭된 국명 번호
            ID = item['ns1.KorSearchVO']['ns1.plantScnmId']
            try:
                # 국명번호 상세 조회 요청
                data = {"state": True, "multi": False,}
                data.update(NameInfo(ID))
            except EOFError as e:  # 정보 죄회중 오류 발생시 None값으로 반환
                etc = '해당 식물의 학명ID는 {0}입니다만.. 학명에 대한 조회를 실패했습니다'.format(ID)
                data = {'state': False, 'etc': etc}
    else:
        etc = '해당 이름으로 검색된 식물이 없습니다. 식물명을 다시 확인해 주세요'
        data = {"state": False, "etc": etc}
    return data

class wikinatureBot(KakaoReply):
    # 메인 키보드 버튼


    def tutorial(self):
        msg = "국명을 검색하면 식물의 정명,학명알수 있습니다. \n학명ID를 검색하면 정명,학명등을 알수 있습니다.\n현재 검색결과는 국,정,학명만 나오며 추후 종,분류등도 나올수 있도록 개발중입니다."
        return self.message(msg)

    def search(self):
        # 간단 사용법
        msg = '검색어를 입력하세요'
        # 검색을 위한 텍스트 버튼
        butn = self.keyboard('text')
        return self.message(msg,keyboard=butn)

    def example(self):
        msg = '아래 나오는 예시중 하나를 선택하세요'
        butn = self.keyboard('buttons',['무궁화','개나리'])
        return self.message(msg,keyboard=butn)

    def uboutthis(self):
        msg = '위키백과와 같은 집단지성으로 자연지리정보를 수집,공유하기 위한 플랫폼입니다.' \
              '\n현재 국명 검색 서비스를 제공하고 있으며 추후 다양한 자연조사지원서비스로 찾아뵙겠습니다.'
        label = "여러개의 이름을 한번에 변환하기"
        butn_url = "http://wikinature.everypython.com"
        return self.message(msg,butn_label=label,butn_url=butn_url)

    def extend_cmd( self, cmd ):
        try:
            data = search(cmd)

            if data['state']: # 검색 결과가 존재할경우

                kor = data['국명']
                eng = data['학명']
                engID = data['학명id']
                msg = f'국명: {kor}' \
                      f'\n학명: {eng}' \
                      f'\n학명ID: {engID}'

                if data['multi']: # 검색 결과가 여러개 일때
                    # todo 검색결과가 여러개 일때 해당 결과를 바로 검색할수 있는 버튼 생성
                    msg = msg+ f'\n{data["etc"]}'
                    return self.message(msg)
                else: # 검색 결과가 하나일때
                    return self.message(msg)

            else: # 검색결과가 없을 경우
                return self.message(data['etc'])
        except Exception as e:
            sentry.captureException()
            raise e

    def chatbot_info(self):
        self.main_butns = [ 'NameChecker 사용법', '검색하기', '예시', 'WikiNature 소개' ]
        self.cmd_index = {
            'NameChecker 사용법' : self.tutorial(),
            '검색하기': self.search(),
            '예시': self.example(),
            'WikiNature 소개': self.uboutthis(),
        }

# 챗봇 입장시 기본 키보드 키
def keyboard( event_msg, context ) :
    try:
        kakao = wikinatureBot( )
        return kakao.main_keyboard()
    except Exception:
        sentry.captureException()
        raise Exception
# 질의 답변 처리
def message( event_msg, context ) :
    try:
        kakao = wikinatureBot( event_msg)
        return kakao.reply()
    except Exception as e:
        sentry.captureException()
        raise e