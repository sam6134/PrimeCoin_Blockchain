import socket

s = socket.socket()
port = 8888
s.connect(('localhost', port))
z = 'mine\n'
s.sendall(z.encode())    
s.close()