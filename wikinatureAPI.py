
from KakaoReply import KakaoReply



class wikinatureBot(KakaoReply):
    # 메인 키보드 버튼
    def chatbot_info(self):
        self.main_butns = [ 'NameChecker 사용법', '검색하기', '예시', 'WikiNature 소개' ]


# 챗봇 입장시 기본 키보드 키
def keyboard( event_msg, context ) :
    kakao = wikinatureBot( )
    return kakao.main_keyboard()


# 질의 답변 처리
def message( event_msg, context ) :
    event = event_msg
    cmd = event[ 'body' ]
    print( event )
    pass
