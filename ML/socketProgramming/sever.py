import socket
import threading
import numpy as np
from sklearn.externals import joblib

model = joblib.load(
    'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Models/logistic_model.pkl')


def predict(input_data):
    # 입력 데이터를 머신러닝 모델에 넣어 예측값을 얻음
    prediction = model.predict([input_data])
    return prediction.tolist()  # 예측값을 리스트로 변환

# binder함수는 서버에서 accept가 되면 생성되는 socket 인스턴스를 통해 client로 부터 데이터를 받으면 echo형태로 재송신하는 메소드이다.


def binder(client_socket, addr):
    # 커넥션이 되면 접속 주소가 나온다.
    print('Connected by', addr)
    try:
        while True:
            # socket의 recv함수는 연결된 소켓으로부터 데이터를 받을 대기하는 함수입니다. 최초 4바이트를 대기합니다.
            data = client_socket.recv(4)
            # 최초 4바이트는 전송할 데이터의 크기이다. 그 크기는 little big 엔디언으로 byte에서 int형식으로 변환한다.
            length = int.from_bytes(data, "little")
            # 다시 데이터를 수신한다.
            data = client_socket.recv(length)
            # 수신된 데이터를 str형식으로 decode한다.
            msg = data.decode()
            print('Received from', addr, msg)

            # msg를 머신러닝으로 돌려 결과 값 반환
            # 예시
            input_data = list(map(int, msg.split(',')))
            sendMessage = predict(input_data)
            data = str(sendMessage).encode()  # 바이너리(byte)형식으로 변환한다.
            # data = msg.encode()  # 바이너리(byte)형식으로 변환한다.
            length = len(data)  # 바이너리의 데이터 사이즈를 구한다.
            # 데이터 사이즈를 little 엔디언 형식으로 byte로 변환한 다음 전송한다.
            client_socket.sendall(length.to_bytes(4, byteorder='little'))
            # 데이터를 클라이언트로 전송한다.
            client_socket.sendall(data)
    except:
        # 접속이 끊기면 except가 발생한다.
        print("except : ", addr)
    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()


# 소켓을 만든다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 소켓 레벨과 데이터 형태를 설정한다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
# 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
server_socket.bind(('', 9999))
# server 설정이 완료되면 listen를 시작한다.
server_socket.listen()

try:
    # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
    while True:
        # client로 접속이 발생하면 accept가 발생한다.
        # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
        client_socket, addr = server_socket.accept()
        th = threading.Thread(target=binder, args=(client_socket, addr))
        # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
        th.start()
except:
    print("server")
finally:
    # 에러가 발생하면 서버 소켓을 닫는다.
    server_socket.close()
