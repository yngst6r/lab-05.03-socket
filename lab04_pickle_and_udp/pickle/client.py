import socket, pickle
sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send(pickle.dumps({"name": "alice", "n": 42}))
print("echo", pickle.loads(sock.recv(4096)))
sock.close()
