import socket
import remote

LOCAL_HOST = '127.0.0.1'
TCP_PORT = 8080
BUFFER_SIZE = 20

local_ip = remote.get_ip()

tcp_ip = input("> Enter an ip (press enter to use local ip: " + local_ip + "):")
if tcp_ip == '':
    tcp_ip = local_ip


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = input("> Enter a message: ")

    s.connect((tcp_ip, TCP_PORT))
    s.send(bytearray(msg, encoding='utf-8'))
    data = s.recv(BUFFER_SIZE)
    s.close()

    print("Received: ", data.decode(encoding='utf-8'))
