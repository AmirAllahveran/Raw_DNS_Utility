import socket

HOST = socket.gethostbyname('localhost')
PORT = 53

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = 'Hello, world'
    s.send(message.encode())
