import socket
import threading

# 두 번째 파일의 함수들을 임포트합니다.
from url_detection import prepare_input, model


def predict(input_data):
    prediction = model.predict(input_data)
    return prediction[0]  # 예측 결과의 첫 번째 값을 반환


def binder(client_socket, addr):
    print('Connected by', addr)
    try:
        while True:
            data = client_socket.recv(4)
            length = int.from_bytes(data, "little")
            data = client_socket.recv(length)
            url = data.decode()
            print('Received URL from', addr, url)

            if url == "":
                break

            input_data = prepare_input(url)
            var = input_data.values[0]
            print('var = ', var)
            input_list = var.tolist()
            int_list = list(map(int, input_list))
            print('int_list : ', int_list)

            sendMessage = predict(input_data)
            print("sendMessage : ", sendMessage)
            int_list.append(sendMessage)

            data = str(int_list).encode()
            print('data :  ', data)
            length = len(data)
            client_socket.sendall(length.to_bytes(4, byteorder='little'))
            client_socket.sendall(data)

    except Exception as e:
        print("Exception:", e)
    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 9999))
server_socket.listen()

try:
    while True:
        client_socket, addr = server_socket.accept()
        th = threading.Thread(target=binder, args=(client_socket, addr))
        th.start()
except Exception as e:
    print("Server exception:", e)
finally:
    server_socket.close()
