# request: 클라이언트로부터 GTTP 요청을 받았을 때 요청 정보를 확인할 수 있는 모듈
# jsonify: 데이터 객체를 json 응답으로 변환해주는 유틸리티
from flask import Flask, request, jsonify, abort
import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)


# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    print("3333333")
    mySocket.connect((host, port))
    print("44444444")

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data


@app.route('/', methods=['GET'])
def index():
    print('hello')

# 챗봇 엔진 query 전송 API
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'TEST':
            # 챗봇 API 테스트
            print("11111")
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            print("22222")
            return jsonify(ret)

        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            pass

        elif bot_type == "NAVER":
            # 네이버톡톡 Web hook 처리
            pass
        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='127.0.0.1', port=5000)
    #app.run()
