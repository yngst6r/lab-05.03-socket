import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"hello udp", ('localhost', 9091))
print("echo", sock.recvfrom(1024)[0].decode())
sock.close()
