from io import BytesIO
from gevent.pool import Pool
from gevent.server import StreamServer
from collections import namedtuple

Error=namedtuple('Error',('message',)) # this is like a class basically, a small class


class CommandError(Exception):
    pass
class Disconnect(Exception):
    pass

class ProtocolHandler:
    def handle_request(self,socket_file):
        first_line =socket_file.readline().strip()

        if not first_line:
            raise Disconnect()

        if not first_line.startswith(b'*'):# byte comparison
            raise CommandError("expected a RESp Array")
        
        # this will give us the number of arguemtns we can expect
        num_args=int(first_line[1:])

        args=[]
        for thing in range(num_args):
            length_line=socket_file.readline().strip()

            if not length_line:
                raise Disconnect()


            if not length_line.startswith(b'$'):# needs to be compared to bytes
                raise CommandError("Expected Bulk String")
        
            length= int(length_line[1:])

            value= socket_file.read(length)
            socket_file.read(2) # consume /r/n

            args.append(value.decode())
        return args
        





    def write_response(self,socket_file,data):

        # this here is us dealing with the response types we should send back for commands, in the required format
        if isinstance(data,Error):
            socket_file.write(f"-{data.message}\r\n".encode("utf-8"))
        elif data is None:
            socket_file.write(b"$-1\r\n")
        elif isinstance(data,int):
            socket_file.write(f":{data}\r\n".encode("utf-8"))
        else:
            data=str(data).encode('utf-8')
            socket_file.write(b"$" + str(len(data)).encode('utf-8')+b"\r\n")
            socket_file.write(data+b"\r\n")
        socket_file.flush()

class Server:
    def __init__(self,host='127.0.0.1',port=31337,max_clients=64):
        self._kv={}
        self.host=host
        self.port=port

        self._protocol=ProtocolHandler()

        self._pool=Pool(max_clients)

        self._server= StreamServer(
            (host,port),
            self.connection_handler,
            spawn=self._pool
        )
    def connection_handler(self,conn,address):
        socket_file=conn.makefile('rwb')
        # this here handles our connection, we can connect and input data, and it will be handled by handler
        while True:
            try:
                data=self._protocol.handle_request(socket_file)
            except Disconnect:
                break

            try:
                resp= self.get_response(data)

            except CommandError as exec:
                resp= Error(exec.args[1])
        return self._protocol.write_response(socket_file,resp)
    def run(self):
        # not the best to do a forever but its ok for now
        self._server.serve_forever()
    



    def get_response(self,data):
        command= data[0]
        # this is how we can return specified data that we have stored within redis based on what command has been entered
        
        if command.upper()== "SET":
            self._kv[data[1]]=data[2]
            return "OK"
        elif command.upper() == "GET":
            return self._kv.get(data[1])
        elif command.upper() == "DEL":
            if data[1] in self._kv:
                del self._kv[data[1]]
                return 1
            else:
                return 0
        elif command.upper()=="EXISTS":
            val=data[1] in self._kv
            if val == True:
                return 1
            else:
                return 0
        else:
            raise CommandError("Unknow Command encountered")
        

        




        

    


if __name__ == "__main__":

    server = Server()
    print("Mini Redis running on 127.0.0.1:31337")
    server.run()
    