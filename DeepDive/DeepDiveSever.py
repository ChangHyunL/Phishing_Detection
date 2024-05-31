import socket
import threading
from checkjs import exec as checkjs_exec
from checkhtml import exec as checkhtml_exec


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

            input_data = exec(url)
            # input_data.to_csv('x_input.csv', index=False)
            # var = input_data.values[0]
            # input_data = list(map(int, input_data.split(' ')))
            # print("input_data : ", input_data)
            # print('var = ', var)
            # input_list = var.tolist()
            # int_list = list(map(int, input_list))
            # int_list.insert(0, url)
            # print('int_list : ', int_list)
            print("input_data : ", input_data)
            sendMessage = input_data
            print("sendMessage : ", sendMessage)

            data = str(sendMessage).encode()
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
server_socket.bind(('', 9998))
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


def exec(url):
    checkjs_exec(url)
    checkhtml_exec(url)
    return "hello"
