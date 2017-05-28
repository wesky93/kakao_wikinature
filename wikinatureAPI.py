class KakaoReply :
    def __init__( self, event_msg: dict = None ) :
        if event_msg:
            self.request_info( event_msg )

    def request_info( self, event: dict ) :
        """
        요청받은 정보를 분류
        :param event: lambda로 입력받은 이벤트 딕셔너리
        :return: 
        """
        self.body = event[ 'body' ]
        self.user_key = self.body[ 'user_key' ]
        self.type = self.body[ 'type' ]
        self.content = self.body[ 'content' ]

    def keyboard( self, KeyboardType: str, butns: list = None ) :
        """
        카카오 키보드 버튼 생성기
        :param KeyboardType: buttons, text 택 일
        :param arg: buttons 형식일 경우 버튼 목록
        :return: 카카오 키보드 오브젝트
        """
        keyboard = { }
        if KeyboardType == "buttons" :
            keyboard[ "type" ] = "buttons"
            keyboard[ "buttons" ] = butns
        elif KeyboardType == "text" :
            keyboard[ "type" ] = "text"
        return keyboard

    def main_keyboard( self ) :
        """
        챗봇 입장시 출력되는 기본 버튼
        :return: 
        """
        # 출력할 버튼
        butns = [ 'NameChecker 사용법', '검색하기', '예시', 'WikiNature 소개' ]
        return self.keyboard( "buttons", butns )


# 챗봇 입장시 기본 키보드 키
def keyboard( event_msg, context ) :
    kakao = KakaoReply( )
    return kakao.main_keyboard()


# 질의 답변 처리
def message( event_msg, context ) :
    event = event_msg
    cmd = event[ 'body' ]
    print( event )
    pass
