import socket, threading

BUFFER_SIZE = 20


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class ThreadedServer(threading.Thread):
    def __init__(self, host, port, fn_callback):
        super().__init__(target=self._listen_thread, daemon=True, name='Remote-command listen server')

        self.fn_callback = fn_callback
        
        self.host = host
        self.port = port

        self.listening = False

        self.start()

    def _listen_thread(self):
        while True:
            if self.listening:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
                    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    _socket.bind((self.host, self.port))
                    _socket.listen(5)
                    clientsocket, address = _socket.accept()
                    print('Connection address:', address)
                    while True:
                        data = clientsocket.recv(BUFFER_SIZE)
                        if not data:
                            break
                        print("Received data:", data)
                        clientsocket.send(data) 
                        self.fn_callback(data.decode(encoding='utf-8'))
                    clientsocket.close()     
                  

            



    


