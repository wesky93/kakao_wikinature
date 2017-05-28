import sys

# 경로 설정
sys.path.append( "/var/task/.venv/lib/python3.6/site-packages" )

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