

# 에러
class KakaoReplyError(Exception):
    pass


class MainButnsError(KakaoReplyError):
    """
    기본 메인 키보드 정보가 없을거나 잘못된 형식일 경우
    """
    pass

class KakaoReply :
    def __init__( self, event_msg: dict = None ) :
        if event_msg :
            self.request_info( event_msg )

        # 챗봇 기본 정보 호출
        self.chatbot_info()

    def chatbot_info(self):
        """
        챗봇 기본정보를 호출하기 위한 메소드입니다
        이 메소드를 오버라이딩 하여 필요한 정보를 입력하면 됩니다
        :return: 
        """
        # [필수] 기본
        self.main_butns = None

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
        if self.main_butns == None or type(self.main_butns) != type(list()):
            raise MainButnsError()
        # 출력할 버튼
        return self.keyboard( "buttons", self.main_butns )