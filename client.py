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

client.sendall(encode_command("RENAME", "name", "my_first_name"))
print(client.recv(1024))

client.sendall(encode_command("GET", "my_first_name"))
print(client.recv(1024))



# client.sendall(encode_command("SET", "time", "thursday"))
# print(client.recv(1024))

# client.sendall(encode_command("SET", "money", "100mill"))
# print(client.recv(1024))

# client.sendall(encode_command("SET", "temp", "123"))
# print(client.recv(1024))

# client.sendall(encode_command("EXPIRE", "temp", "1"))
# print(client.recv(1024))

# time.sleep(2)

# client.sendall(encode_command("KEYS"))
# print(client.recv(1024))

# client.sendall(encode_command("SET", "name", "Sean"))
# print(client.recv(1024))

# client.sendall(encode_command("KEYS"))
# print(client.recv(1024))

# client.sendall(encode_command("FLUSHDB"))
# print(client.recv(1024))

# client.sendall(encode_command("KEYS"))
# print(client.recv(1024))

# client.sendall(encode_command("MSET", "name", "Sean",'age',"25","job", "none"))
# print(client.recv(1024))

# client.sendall(encode_command("MGET", "name", "age","job"))
# print(client.recv(1024))




#client.sendall(encode_command("TTL", "name"))
#print(client.recv(1024)) 


#client.sendall(encode_command("EXPIRE", "name", "10"))
#print(client.recv(1024))

#client.sendall(encode_command("TTL", "name"))
#print(client.recv(1024)) 

#time.sleep(15)

#client.sendall(encode_command("EXISTS",'name'))
#print(client.recv(1024))

client.sendall(encode_command("INCR",'counter'))
print(client.recv(1024))

#client.sendall(encode_command("DECR",'counter1'))
#print(client.recv(1024))

#client.sendall(encode_command("SET", "name", "Sean"))
#print(client.recv(1024))

#client.sendall(encode_command('SAVE'))
#print(client.recv(1024))


#client.sendall(encode_command("LOAD"))
#print(client.recv(1024))

#client.sendall(encode_command("GET","name"))
#print(client.recv(1024))


#time.sleep(10)



client.close()