# 에러
class KakaoReplyError( Exception ) :
    pass


class MainButnsError( KakaoReplyError ) :
    """
    기본 메인 키보드 정보가 없을거나 잘못된 형식일 경우
    """
    pass


class KakaoReply :
    def __init__( self, event_msg: dict = None ) :
        ## 변수 목록
        # 요청 정보
        self.body = { }
        self.user_key = ''
        self.type = ''
        self.content = ''

        # 챗봇 정보
        self.main_butns = None  # 챗봇 입장시 노출되는 버튼목록
        self.cmd_index = { }  # 기본 명령어 목록

        ## 챗봇 초기화
        # 요청정보가 존재할시 정보 추출
        if event_msg :
            self.request_info( event_msg )

        # 챗봇 기본 정보 호출
        self.chatbot_info()

    ## 기본 정보 초기화 메소드
    # 요청 정보 초기화
    def request_info( self, event: dict ) :
        """
        요청 정보 초기화
        :param event: lambda로 입력받은 이벤트 딕셔너리
        :return: 
        """
        self.body = event[ 'body' ]
        self.user_key = self.body[ 'user_key' ]
        self.type = self.body[ 'type' ]
        self.content = self.body[ 'content' ]

    # 챗봇 정보 초기화
    def chatbot_info( self ) :
        """
        챗봇 기본정보 초기화
        이 메소드를 오버라이딩 정보를 초기화하면 됩니다
        :return: 
        """
        # [필수] 기본 노출 버튼
        self.main_butns = None
        # [필수] 기본 명령어 인덱스
        # ex) self.cmd_index = { "소개": self.intro(), "사용법":self.howtouse() }
        self.cmd_index = { }

    ## 생성 메소드

    # 키보드 버튼 생성
    def keyboard( self,
                  KeyboardType: str,
                  butns: list = None
                  ) :
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

    # 메세지 생성
    def message( self,
                 text: str = None,
                 photo_url: str = None,
                 photo_width: str = 720,
                 photo_height: str = 630,
                 butn_label: str = None,
                 butn_url: str = None,
                 keyboard: dict = None
                 ) :
        """
        리스폰 메시시 생성
        :param text: 메세지에 들어갈 텍스트
        :param photo_url: 이미지 주소
        :param photo_with: 이미지 폭(defalut:720)
        :param photo_height: 이미지 높이(defalut:720)
        :param butn_label: 버튼 라벨
        :param butn_url: 버튼 클릭시 이동할 url
        :param keyboard: 다음 진행을 위한 키보드 버튼(default: 기본 메인 키보드 버튼)
        :return: 
        """

        msg = { }

        if text :
            msg[ 'text' ] = text

        if photo_url :
            msg[ 'photo' ] = { }
            msg[ 'photo' ][ 'url' ] = photo_url
            msg[ 'photo' ][ 'width' ] = photo_width
            msg[ 'photo' ][ 'height' ] = photo_height

        if butn_label :
            msg[ 'message_button' ] = { }
            msg[ 'message_button' ][ 'label' ] = butn_label
            msg[ 'message_button' ][ 'url' ] = butn_url

        result = { 'message' : msg }

        # 추가 키보드 버튼 출력
        if keyboard :
            result[ 'keyboard' ] = keyboard
        else :
            result[ 'keyboard' ] = self.main_keyboard()

        return result

    ## 요청 처리 메소드
    # 기본 명령 처리 메소드
    def reply( self ) :
        """
        챗봇 명령어 처리 메소드
        :return: 
        """
        # 요청된 명령어가 기본 명령어에 존재할경우 해당 메소드 실행
        if self.content in self.cmd_index :
            return self.cmd_index[ self.content ]
        # 기본 명령어가 아닐경우 확장 명령어 메소드 실행
        else :
            return self.extend_cmd( self.content )

    # 기본 키보드 정보 알림 메소드
    def main_keyboard( self ) :
        """
        챗봇 입장시 출력되는 기본 버튼
        :return: 
        """
        if type( self.main_butns ) != type( list() ) :
            raise MainButnsError()
        # 출력할 버튼
        return self.keyboard( "buttons", self.main_butns )

    def extend_cmd( self, cmd ) :
        """
        기본 명령어 이외에 추가적인 명령어를 입력받을려면 이 메소드를 오버라이드 하여 사용하세요
        :param cmd: 
        :return: 
        """
        return self.message("해당 요청에 대한 결과가 없습니다",keyboard=self.main_keyboard())
