import gevent 
import socket
import time


def encode_command(*parts):
    # have to construct the client in the way the server expects information to come in
    result = f"*{len(parts)}\r\n".encode()

    for part in parts:
        part = str(part).encode()
        result += b"$" + str(len(part)).encode() + b"\r\n"
        result += part + b"\r\n"

    return result


client= socket.socket()

client.connect(("127.0.0.1", 31337))

client.sendall(encode_command("SET", "name", "Sean"))
print(client.recv(1024))


client.sendall(encode_command("EXPIRE", "name", "10"))
print(client.recv(1024))

time.sleep(15)

client.sendall(encode_command("EXISTS",'name'))
print(client.recv(1024))

client.close()